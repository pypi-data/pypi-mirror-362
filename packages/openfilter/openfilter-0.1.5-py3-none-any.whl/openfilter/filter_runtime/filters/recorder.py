import logging
import os
from copy import deepcopy
from json import dumps as json_dumps
from typing import Any, NamedTuple

from openfilter.filter_runtime.filter import Filter, FilterConfig
from openfilter.filter_runtime.utils import json_getval, dict_without, split_commas_maybe

__all__ = ['RecorderConfig', 'Recorder']

logger = logging.getLogger(__name__)

DEBUG_RECORDER = bool(json_getval((os.getenv('DEBUG_RECORDER') or 'false').lower()))

is_file = lambda name: name.startswith('file://')


class RecorderConfig(FilterConfig):
    outputs: str | list[str] | list[tuple[str, dict[str, Any]]]

    rules:   list[str]
    empty:   int | None
    flush:   bool | None


class Recorder(Filter):
    """Record frame data to files as JSON or CSV. If the output filename ends with '.csv' the output will be CSV,
    otherwise JSON.

    config:
        outputs:
            Must be a single "file://..." to write to.

            `outputs` individual options:
                '!append':
                    Append to output file if present instead of deleting all data in it.

        rules:
            "+topic"         - Include entire "topic".
            "-/meta"         - Exclude "meta" section from all topics.
            "+other/meta/id" - Include item "meta.id" in topic "other".
            "+"              - Include EVERYTHING.
            "-"              - Exclude EVERYTHING.

            "+topic, -/meta, +other/meta/id, +, -" - All the above applied in order.

        flush:
            Flush output file after each write (useful for stuff in docker), default on but can turn off with False.

        empty:
            What level of empty to put, 0 = only if there is actual data, 1 = if there are at least fields even if they
            are empty (default), 2 = put everything

    Environment variables:
        DEBUG_RECORDER:
            If 'true'ish and LOG_LEVEL is set to 'debug' then will log each rule applied at each process().

    Notes:
        * The "+" is optional for including ('+/meta' is same as '/meta'), the "-" is not.

        * Only data is recorded, not images.
    """

    FILTER_TYPE = 'Output'

    @classmethod
    def normalize_config(cls, config):
        outputs = split_commas_maybe(config.get('outputs'))  # we do not assume how Filter will normalize sources/outputs in the future
        config  = RecorderConfig(super().normalize_config(dict_without(config, 'outputs')))

        if outputs is not None:
            config.outputs = outputs

        if not config.sources:
            raise ValueError('must specify at least one source')
        if not outputs or len(outputs) != 1:
            raise ValueError('must specify exactly one output')

        if isinstance(output := outputs[0], str):
            config.outputs[0] = Filter.parse_options(output)

        if not is_file(outputs[0][0]):
            raise ValueError('output must be file://')

        config.rules  = split_commas_maybe(config.rules) or ['+', '-/meta/ts']
        config._rules = _rules = []  # [(bool add, topic or '', [key, ...])]

        for rule in config.rules:
            if rule.startswith('-'):
                top_n_path, add = rule[1:], False
            elif rule.startswith('+'):
                top_n_path, add = rule[1:], True
            else:
                top_n_path, add = rule, True

            topic, *path = top_n_path.split('/')

            if path and any(not p for p in path):
                raise ValueError(f'invalid rule: {rule!r}')

            _rules.append((add, topic or None, path or None))

        if (empty := config.empty) is not None and empty not in (0, 1, 2):
            raise ValueError(f'empty must be 0 (put least), 1 or 2, not: {empty!r}')

        return config

    def init(self, config):
        super().init(FilterConfig(config, outputs=None))

    def setup(self, config):
        if DEBUG_RECORDER:
            logger.debug(f'rules: {config._rules}')

        fnm, options   = config.outputs[0]
        self.is_csv    = fnm.lower().endswith('.csv')
        self.csv_paths = None
        self.csv_order = None
        self.file      = None
        self.file      = open(fnm[7:], 'a' if options.get('append') else 'w')
        self.rules     = config._rules
        self.empty     = 1 if config.empty is None else int(config.empty)
        self.flush     = True if config.flush is None else bool(config.flush)

    def shutdown(self):
        if self.file:
            self.file.close()

    def process(self, frames):
        frames = {t: f.data for t, f in frames.items()}
        out    = {}

        def delpath(path):
            stack = []
            child = out

            for attr in path:
                parent = child

                if (child := parent.get(attr, ...)) is ...:
                    break

                stack.append((parent, attr))

            else:
                del parent[attr]

                stack.pop()

                while stack:
                    parent, attr = stack.pop()

                    if parent[attr]:
                        break

                    del parent[attr]

        def addpath(path):
            stack = []
            child = frames

            for attr in path:
                parent = child

                if (child := parent.get(attr, ...)) is ...:
                    break

                stack.append(attr)

            else:
                parent = out

                for attr in stack[:-1]:
                    parent = parent.setdefault(attr, {})

                parent[stack[-1]] = child

        for add, topic, path in self.rules:
            if DEBUG_RECORDER:
                topic_n_path = 'all' if not topic and not path else topic if not path else f'{topic or ""}/{"/".join(path or [])}'

                logger.debug(f'apply rule: {"add" if add else "remove"} {topic_n_path}')

            if add:
                if topic:
                    if path:
                        addpath([topic, *path])
                    else:
                        if (f := frames.get(topic)) is not None: out[topic] = deepcopy(f)

                else:
                    if path:
                        for t in frames: addpath([t, *path])
                    else:
                        out = {t: deepcopy(f) for t, f in frames.items()}

            else:
                if topic:
                    if path:
                        delpath([topic, *path])
                    else:
                        if topic in out: del out[topic]

                else:
                    if path:
                        for t in out: delpath([t, *path])
                    else:
                        out = {}

            if DEBUG_RECORDER:
                logger.debug(f'result: {out}')

        if (empty := self.empty) == 2 or (empty == 1 and out) or (empty == 0 and (out := Recorder.prune_empties(out))):
            if not self.is_csv:
                self.file.write(f"{json_dumps(out, separators=(',', ':'))}\n")

            else:
                entries       = Recorder.to_csv(out)
                entries_paths = set(e.path for e in entries)

                if (csv_paths := self.csv_paths) != entries_paths:
                    if csv_paths is None:
                        self.csv_paths = entries_paths
                        self.csv_order = [e.path for e in entries]

                        self.file.write(','.join(e.name for e in entries) + '\n')

                    elif diff := entries_paths - csv_paths:
                        raise ValueError(f"encountered fields which doesn't fit header: {diff} not in {csv_paths}")

                entries = {e.path: e.value for e in entries}

                self.file.write(','.join(str(entries.get(path, '')) for path in self.csv_order) + '\n')

            if self.flush:
                self.file.flush()

    @staticmethod
    def prune_empties(d: dict) -> dict:
        for k, v in list(d.items()):
            if isinstance(v, dict):
                Recorder.prune_empties(v)
            elif not isinstance(v, list):
                continue

            if not v:
                del d[k]

        return d

    class CSVEntry(NamedTuple):
        value: Any
        name:  str  # 'name'
        path:  str  # 'top/sub/.../name'

    @staticmethod
    def to_csv(d: dict) -> list[CSVEntry]:
        entries = []

        for k, v in list(d.items()):
            if isinstance(v, dict):
                entries.extend(Recorder.CSVEntry(e.value, e.name, f'{k}/{e.path}') for e in Recorder.to_csv(v))
            else:
                entries.append(Recorder.CSVEntry(v, k, k))

        return entries

    @staticmethod
    def csv_str(s: Any) -> str:
        if not isinstance(s, str):
            s = str(s)

        if '"' in s:
            s = f'''"{s.replace('"', '""')}"'''
        elif ',' in s or '\n' in s:
            s = f'''"s"'''

        return s


if __name__ == '__main__':
    Recorder.run()
