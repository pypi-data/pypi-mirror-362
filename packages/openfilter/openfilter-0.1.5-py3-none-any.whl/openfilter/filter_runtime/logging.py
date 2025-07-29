"""Persistent and telemetric logging.

Environment variables:
    LOG_PATH: Path to logs and metrics, set to 'false' to disable.

    LOGS_FILE_SIZE:
    LOGS_TOTAL_SIZE:
    METRICS_FILE_SIZE:
    METRICS_TOTAL_SIZE:

    METRICS_INTERVAL: Number of seconds between metrics samples.
"""

import logging
import os
from datetime import datetime
from time import time
from typing import Literal

from .rolllog import RollLog
from .utils import JSONType, sanitize_filename

__all__ = ['Logger']

logger = logging.getLogger(__name__)

LOG_PATH           = False if (_ := os.getenv('LOG_PATH')) == 'false' else _ or 'logs'
LOGS_FILE_SIZE     = int(os.getenv('LOGS_FILE_SIZE') or 5_000_000)
LOGS_TOTAL_SIZE    = int(os.getenv('LOGS_TOTAL_SIZE') or 100_000_000)
METRICS_FILE_SIZE  = int(os.getenv('METRICS_FILE_SIZE') or 5_000_000)
METRICS_TOTAL_SIZE = int(os.getenv('METRICS_TOTAL_SIZE') or 100_000_000)
METRICS_INTERVAL   = float(os.getenv('METRICS_INTERVAL') or 60)

LOG_CATEGORIES     = ('logs', 'metrics')

LOG_LEVELNAME_MAP  = {
    'CRITICAL': 'CRITICAL',
    'FATAL':    'CRITICAL',
    'ERROR':    'ERROR',
    'WARN':     'WARNING',
    'WARNING':  'WARNING',
    'INFO':     'INFO',
    'DEBUG':    'DEBUG',
    'NOTSET':   'DEBUG',
}

LogCategory = Literal['logs'] | Literal['metrics']


class LogHandler(logging.Handler):
    def __init__(self, rlog: RollLog):
        logging.Handler.__init__(self)

        self.rlog = rlog

    def emit(self, record):
        self.rlog.write({
            'ts':   datetime.fromtimestamp(ts := record.created, self.rlog.tz).isoformat(),
            'pid':  record.process,
            'thid': record.thread,
            'lvl':  LOG_LEVELNAME_MAP.get(record.levelname, 'INFO'),  # we want 5 fixed level names
            'msg':  record.message,
        }, ts)

    def flush(self):
        self.rlog.flush()

    def close(self):
        logging.Handler.close(self)


class Logger:
    def __init__(self,
        id:               str,
        utc:              bool = False,
        *,
        log_path:         str | Literal[False] | None = None,
        metrics_interval: float | None = None,
    ):
        self.fixed_metrics = {}
        self.aggregate     = {}  # {'metric': (metric sum, metric count), 'metric_count': metric value}  - first is for averaging, seconcd is last value

        if log_path is None:
            log_path = LOG_PATH

        self.log_path = log_path

        if log_path is False:
            self.logs_rlog    = None
            self.metrics_rlog = None

        else:
            self.logs_rlog    = RollLog(mode='json',
                file_size=LOGS_FILE_SIZE, total_size=LOGS_TOTAL_SIZE, utc=utc,
                **Logger.path_prefix_and_suffix(log_path, id, 'logs'))
            self.logs_handler = LogHandler(self.logs_rlog)
            root_logger       = logging.getLogger()

            root_logger.addHandler(self.logs_handler)

            self.metrics_interval = METRICS_INTERVAL if metrics_interval is None else metrics_interval
            self.metrics_t        = time() + self.metrics_interval
            self.metrics_rlog     = RollLog(mode='json',
                file_size=METRICS_FILE_SIZE, total_size=METRICS_TOTAL_SIZE, utc=utc,
                **Logger.path_prefix_and_suffix(log_path, id, 'metrics'))

    @property
    def enabled(self):
        return self.log_path is not False

    def close(self):
        if self.metrics_rlog is not None:
            self.metrics_rlog.close()

        if self.logs_rlog is not None:
            logging.getLogger().removeHandler(self.logs_handler)

            self.logs_handler.close()
            self.logs_rlog.close()

    def write_metrics(self, metrics: dict[str, JSONType]):
        td = time() - self.metrics_t

        aggregate = self.aggregate

        for metric, value in metrics.items():  # yes we do 'ts' as well unnecessarily, but it is not used
            if metric.endswith('_count') or not isinstance(value, (int, float)):
                aggregate[metric] = value
            elif (v := aggregate.get(metric)) is None:
                aggregate[metric] = (value, 1)

            else:
                sum, num          = v
                aggregate[metric] = (sum + value, num + 1)

        if td < 0:
            return

        ts = metrics['ts']

        for metric, value in aggregate.items():
            if value.__class__ is tuple:
                sum, num          = value
                aggregate[metric] = sum / num

        self.aggregate  = {}
        self.metrics_t += (td // (mi := METRICS_INTERVAL) + 1) * mi
        metrics_rlog    = self.metrics_rlog

        metrics_rlog.write({**aggregate, **self.fixed_metrics,
            'ts': datetime.fromtimestamp(ts, metrics_rlog.tz).isoformat()}, ts)

    def set_fixed_metrics(self, **kwargs):
        """Passing None for a metric will remove that metric. Safe to change existing or remove nonexistent metrics."""

        fixed_metrics = self.fixed_metrics

        for metric, value in kwargs.items():
            if value is not None:
                fixed_metrics[metric] = value
            elif metric in fixed_metrics:
                del fixed_metrics[metric]

    @staticmethod
    def path_prefix_and_suffix(path: str, id: str, category: LogCategory):
        return dict(path=os.path.join(path, sanitize_filename(id), category), prefix=category, suffix=None)
