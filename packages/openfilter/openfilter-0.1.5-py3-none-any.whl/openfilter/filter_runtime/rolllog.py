"""Rolling logger. Only one should write to a specific log (path + prefix/suffix) but many can read. Also safe for
external deletion of logs."""

import logging
import os
import re
from datetime import datetime, timezone
from json import dumps as json_dumps, loads as json_loads
from threading import RLock
from time import time
from typing import Any, NamedTuple

__all__ = ['RollLogPos', 'RollLogFile', 'RollLog']

logger = logging.getLogger(__name__)

tzstr_from_tz = lambda tz: f'{"-+"[(s := int(tz.utcoffset(None).total_seconds())) >= 0]}{(s := abs(s)) // 3600:02}{s % 3600 // 60:02}'
prefix_fixup  = lambda p: '' if p is None else p if p[-1:] in ('.', '_', '-') else f'{p}_'
suffix_fixup  = lambda s: '' if s is None else s if s[:1] in ('', '.', '_', '-') else f'_{s}'
fnm_from_dats = lambda dt, ts, tzs, pfx, sfx: \
    f'{pfx}{int(ts * 1_000_000):016}_{dt.year}-{dt.month:02}-{dt.day:02}_{dt.hour:02}-{dt.minute:02}-{dt.second:02}{tzs}{sfx}'  # specifically int(ts) to truncate so it is smaller or equal than whatever is in the log


RollLogPos = tuple[str, int]


class RollLogFile(NamedTuple):
    timestamp: float  # this MUST be first for sorting!!!
    path:      str
    size:      int


class RollLog:
    """Log which enforces size limits on individual logs and totality of logs as well as allow to pull data from them
    incrementally. When total allowed size is exceeded it starts deleting older logs."""

    MODES     = ('bin', 'binl', 'txt', 'json')
    MODE_EXTS = ('.bin', '.binl','.txt', '.jsonl')

    def __init__(self,
        path:        str | None = None,
        mode:        str = 'txt',
        *,
        prefix:      str | None = None,
        suffix:      str | None = None,
        head:        str | None = None,
        file_size:   int = 5_000_000,
        total_size:  int = 100_000_000,
        flush:       bool = True,
        utc:         bool = False,
        path_create: bool = True,
        rdonly:      bool = False,
        autorefresh: bool = True,
    ):
        """Set up rolling logger. Do not run more than one of the same prefix/suffix loggers in the same `path`.

        Args:
            path: Relative or absolute path to log directory, default is current dir. Does not have to be dedicated
                to logs, they will be filtered from the files present by prefix, suffix and timestamp regex.

            mode: One of 'bin', 'binl', 'txt' or 'json'. Determines how data is serialized and deserialized.

            prefix: If provided is prepended to each log timestamp filename, e.g. 'myprefix' ->
                'myprefix_0123456789012345_2024-08-12_13-47-13.ext'. Default is no prefix.

            suffix: Explicit file suffix, may be extension ".ext" or an actual suffix followed by an extension
                "_suffix.ext". If not provided a default for the mode is used.

            head: A filename that will store position data to be tracked on what has been read from the log already.
                This will persist across multiple runs of the application. If path elements are present that that path
                is used, otherwise it is placed one directory level above where the actual logs are stored.

            file_size: Approximate size in bytes for individual log files to allow. Writes must exceed this before log
                files are rolled over.

            total_size: Sum total approximate size in bytes of all log files to allow. Once exceeded this then older
                logs will be deleted.

            flush: Default flush on .write().

            utc: Log filenames in UTC instead of local.

            path_create: If `path` doesn't exist then it will be created.

            rdonly: Set to True to make sure you don't accidentally log or prune anything.

            autorefresh: In `rdonly` True mode, upon reaching the end of the available log files list do .refresh()
                automatically in order to be able to continue in case there are new files.
        """

        if mode not in RollLog.MODES:
            raise ValueError(f"unknown mode {mode!r}, must be one 'bin', 'binl', 'txt' or 'json'")

        if head is not None and not rdonly:
            raise ValueError(f"persistent read 'head' only meant to be used in readonly mode")

        self.path        = path = os.path.abspath(path or '.')
        self.mode        = mode
        self.prefix      = prefix = prefix_fixup(prefix)
        self.suffix      = suffix = RollLog.MODE_EXTS[RollLog.MODES.index(mode)] if suffix is None else suffix_fixup(suffix)
        self.head        = head
        self.file_size   = file_size
        self.total_size  = total_size
        self.flush_      = flush
        self.utc         = utc
        self.rdonly      = rdonly
        self.autorefresh = autorefresh and rdonly  # autorefresh only valid for `rdonly` logs

        self.tz          = tz = timezone.utc if utc else datetime.now().astimezone().tzinfo
        self.tzstr       = tzstr_from_tz(tz)
        self.lock        = RLock()
        self.re_logpath  = re.compile(f'^(?:.*/)?{re.escape(prefix)}'
            r'(\d+)_\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}[-+]\d{4}' f'{re.escape(suffix)}$')  # we accept all logs from all timezones since we go by true time, the timezone is just for the humans
        self.write_file  = False if rdonly else None  # None for not created/open, False for definitevly closed for writing, is not created until something needs to be written
        self.read_file   = None  # None for not open, False for definitevly closed for reading
        self.read_idx    = 0     # in self.logfiles, value of len(self.logfiles) means at end

        if not os.path.exists(path):
            if rdonly or not path_create:
                raise ValueError(f'path {path!r} does not exist')

            os.makedirs(path, exist_ok=True)

        elif not os.path.isdir(path):
            raise ValueError(f'path {path!r} exists but is not a directory')

        self.scan_logfiles()

        if not rdonly:
            self.prune_logfiles()

        if self.logfiles and self.logfiles[-1].timestamp >= time():
            raise ValueError(f'newer log file(s) than now already exist, either something is very wrong or you are a time traveller')

        self.read_idx = len(self.logfiles)

        if head is not None:
            if not os.path.exists(head):  # exists() and not isfile() because we want to error on a directory
                pos = ('start', 0)

            else:
                with self.lock:
                    with open(head) as f:
                        pos = json_loads(f.read().strip())

                if not (isinstance(pos, list) and len(pos) == 2 and isinstance(pos[0], str) and isinstance(pos[1], int)):
                    raise RuntimeError(f'invalid log head position file {head!r}')

            self.seek(pos)

    def write_head(self, pos: RollLogPos | None = None):
        if (head := self.head) is not None:
            with self.lock:
                if pos is None:
                    pos = self.tell()

                with open((head_tmp := head + '.tmp'), 'w') as f:
                    f.write(json_dumps(pos) + '\n')

                os.rename(head_tmp, head)

    def close(self):
        with self.lock:
            self.write_head()

            if self.write_file:
                self.write_file.close()

            if self.read_file:
                self.read_file.close()

            self.write_file = False
            self.read_file  = False

    def flush(self):
        with self.lock:
            if self.write_file:
                self.write_file.flush()

    def write(self, data: Any, timestamp: float | None = None, flush: bool | None = None) -> int:
        """Write data to log, rolling file over if needed AFTER the write and pruning excess logs in this case.

        For 'bin' mode logs `data` must have a buffer interface.

        For 'txt', 'data' can be a string or iterable of strings which will all have newlines appended. Strings with
        newlines already in them will work fine but when read back they will be given line by line. Newline is appended
        to entire string passed.

        'binl' works like 'txt' except that the strings are already bytes encoded. It still counts on a newline
        delimiter, so isn't really suitable for any binary data but is meant for utf-8 encoded strings.

        For 'json' the object will be serialized and written to one single line with minimal spaces.

        The `timestamp` parameter allows you to set a timestamp for newly created log files from the timestamp of the
        entry you are logging in order to match precisely. Otherwise the timestamp of the file might wind up slightly in
        the future of the first timestamp being logged.

        Returns the number of bytes written.

        This function is threadsafe.
        """

        if (mode := self.mode) == 'txt':
            if isinstance(data, str):
                size = len(data := data.encode() + b'\n')
            else:
                size = len(data := '\n'.join(data).encode() + b'\n')

        elif mode == 'json':
            size = len(data := json_dumps(data, allow_nan=False, separators=(',', ':')).encode() + b'\n')

        elif mode == 'binl':
            if isinstance(data, (bytes, bytearray)):
                size = len(data := data + b'\n')
            else:
                size = len(data := b'\n'.join(data) + b'\n')

        else:  # mode == 'bin'
            if isinstance(data, (bytes, bytearray)):
                size = len(data)
            else:
                size = (data := memoryview(data)).nbytes

        with self.lock:
            if (write_file := self.write_file) is False:
                raise RuntimeError('can not write to a closed log')

            if write_file is not None:
                logfile = self.logfiles[-1]

            else:
                try:
                    write_file = self.write_file = open((logfile := self.new_logfile(timestamp)).path, 'wb')

                except Exception as exc:
                    logger.error(exc)

                    return 0

                self.logfiles.append(logfile)

            ret = write_file.write(data)

            self.logfiles[-1]  = RollLogFile(logfile.timestamp, logfile.path, logfile_size := logfile.size + size)
            self.logfiles_size = logfiles_size = self.logfiles_size + size

            if logfiles_size > self.total_size:
                self.prune_logfiles()

            if logfile_size >= self.file_size:
                write_file.close()

                self.write_file = None

            elif self.flush_ if flush is None else flush:
                self.write_file.flush()

            return ret

    def read_block(self, mode: str | None = None) -> bytes | list[str] | list[Any] | None:
        return self.read(mode, block=True)

    def read(self, mode: str | None = None, block: bool = False) -> bytes | str | list[str] | Any | list[Any] | None:
        """Read data from log. With `block` True read the data in a block, usually an entire log file or until the end
        of the log file currently being written. With `block` False will read the data in units of a line at a time
        for 'txt' mode and object at a time for 'json'. For 'bin' mode the `block` setting doesn't matter, it always
        returns data as if `block` were True (since there is no defined delimiter).

        If `mode` is specified then it overrides the log default mode. It is up to you to ensure the mdoe is compatible
        with the write mode. This is meant for reading data back as binary to send it over directly to some other file
        or socket without the overhead of decoding/deserializing and serializing/reencoding again.

        The return value is None if no data left to be read, bytes for 'bin' mode, a list of lines for 'txt' (with
        newlines stripped), a list of encoded lines for 'binl' with newline stripped and a list of objects for 'json'.

        This function is threadsafe.
        """

        if mode is None:
            mode = self.mode

        if mode == 'bin':
            block = True  # since there are no sestablished delimiters in pure binary mode

        autorefresh = self.autorefresh  # will only allow this to be done once in this loop

        with self.lock:
            if (read_file := self.read_file) is False:
                raise RuntimeError('can not read from a closed log')

            if (read_idx := self.read_idx) >= (nlogfiles := len(logfiles := self.logfiles)):
                if not autorefresh:
                    return None

                autorefresh = False

                self.refresh_logfiles()

                if (read_idx := self.read_idx) >= (nlogfiles := len(logfiles := self.logfiles)):
                    return None

            while True:  # while to handle file deletions zero length files (which shouldn't exist anyway, but whatever)
                if read_file is None:
                    try:
                        self.read_file = read_file = open(logfiles[read_idx].path, 'rb')

                    except FileNotFoundError:  # maybe the file was deleted? safest thing to do is skip it but leave in list of files for delete attempt l8r
                        self.read_idx = read_idx = read_idx + 1

                        if read_idx >= nlogfiles:
                            if not autorefresh:
                                return None

                            autorefresh = False

                            self.refresh_logfiles()

                            if (read_idx := self.read_idx) >= (nlogfiles := len(logfiles := self.logfiles)):
                                return None

                            continue

                if read_file is not None:
                    if data := read_file.read() if block else read_file.readline():
                        break

                    if (read_idx := read_idx + 1) >= nlogfiles:  # if on last file then it is probably still being written so don't close
                        if not autorefresh:
                            return None

                        autorefresh = False

                        self.refresh_logfiles()

                        if (read_idx := self.read_idx + 1) >= (nlogfiles := len(logfiles := self.logfiles)):
                            return None

                    read_file.close()

                    self.read_file = read_file = None
                    self.read_idx  = read_idx

        if mode == 'bin':
            return data
        if mode == 'binl':
            return data.split(b'\n')[:-1] if block else data[:-1]

        if block:
            data = data.decode().split('\n')[:-1]  # last entry will be empty string due to trailing '\n'

            return data if mode == 'txt' else [json_loads(obj) for obj in data]

        else:
            data = data[:-1].decode()  # last char will always be trailing '\n'

            return data if mode == 'txt' else json_loads(data)

    def seek_block(self, timestamp: float = 0):
        """Seek read position to a block where requested timestamp probably exists. Since we don't store our own
        timestamps and know nothing about the format of the data being stored we can only seek to a file which starts
        with the highest timestamp before the one provided. It is then up to the calling process to read from the block
        until its desired time is reached. Seeking to 0 will go to beginning of all logs."""

        with self.lock:
            if (read_file := self.read_file) is False:
                raise RuntimeError('can not seek in a closed log')

            if read_file is not None:
                read_file.close()

                self.read_file = None

            for read_idx, logfile in enumerate(self.logfiles):
                if logfile.timestamp > timestamp:
                    break

            else:
                read_idx = len(self.logfiles)

            self.read_idx = max(0, read_idx - 1)

    def seek(self, pos: RollLogPos | tuple[str, str]):
        """Seek to exact read position. If doesn't exist, seek to anything directly past it.

        Special values for `pos`:
            ('start', ?)  - seek to start of all logs
            ('end', ?)    - seek to end of all logs
            (fnm, 'end')  - seek to end of this specific log (opened, so if is written more that will be read)
        """

        with self.lock:
            if (read_file := self.read_file) is False:
                raise RuntimeError('can not seek in a closed log')

            if read_file is not None:
                read_file.close()

                self.read_file = None

            seek_fnm, seek_pos = pos

            if seek_fnm == 'start':
                self.read_idx = 0

                return

            if seek_fnm == 'end':
                self.read_idx = len(self.logfiles)

                return

            if seek_fnm != os.path.basename(seek_fnm) or not (m := self.re_logpath.match(seek_fnm)):
                raise ValueError(f'invalid seek filename {seek_fnm!r}')

            seek_timestamp = int(m.group(1)) / 1_000_000

            for read_idx, logfile in enumerate(self.logfiles):
                if logfile.timestamp > seek_timestamp:
                    break

                if os.path.basename(logfile.path) == seek_fnm:
                    try:
                        self.read_file = read_file = open(logfile.path, 'rb')
                    except FileNotFoundError:
                        read_idx += 1

                    else:
                        if seek_pos == 'end':
                            read_file.seek(0, 2)  # logfile.size MAY be out of date if something else is writing to the log file
                        else:
                            read_file.seek(seek_pos)

                    break

            else:
                read_idx = len(self.logfiles)

            self.read_idx = read_idx

    def tell(self, file_pos: bool = True) -> RollLogPos | tuple[str, None]:
        """Give exact current read position (filename and location within file (if not explicitly excluded))."""

        with self.lock:
            if (read_file := self.read_file) is False:
                raise RuntimeError('can not tell from a closed log')

            if (read_idx := self.read_idx) >= (nlogfiles := len(logfiles := self.logfiles)):
                return (os.path.basename((lf := logfiles[-1]).path), lf.size) if nlogfiles else ('start', 0)

            return (os.path.basename(logfiles[read_idx].path), 0 if read_file is None else
                read_file.tell() if file_pos else None)

    def refresh(self):
        """Refresh list of logfiles. Will close current read file if not in new list of logfiles."""

        if not self.rdonly:
            raise RuntimeError('can not refresh a writable log')
        if self.read_file is False:
            raise RuntimeError('can not refresh a closed log')

        with self.lock:
            self.refresh_logfiles()

    @staticmethod
    def filename(dt: datetime, prefix: str | None = None, suffix: str | None = None) -> str:
        """Return a filename formatted in the same way as the log files for a given datetime."""

        return fnm_from_dats(dt, dt.timestamp(), tzstr_from_tz(dt.tzinfo), prefix_fixup(prefix), suffix_fixup(suffix))


    # PRIVATE, most methods assume self.lock is held if they are doing file operations

    def new_logfile(self, ts: float | None = None) -> RollLogFile:
        if ts is not None:
            dt = datetime.fromtimestamp(ts, self.tz)
        else:
            dt = datetime.now(self.tz)
            ts = dt.timestamp()

        return RollLogFile(ts, os.path.join(self.path, fnm_from_dats(dt, ts, self.tzstr, self.prefix, self.suffix)), 0)

    def scan_logfiles(self):
        re_logpath    = self.re_logpath
        logfiles      = []
        logfiles_size = 0

        for name in os.listdir(log_path := self.path):
            if os.path.isfile(path := os.path.join(log_path, name)) and (m := re_logpath.match(path)):
                logfiles.append(RollLogFile(int(m.group(1)) / 1_000_000, path, size := os.stat(path).st_size))

                logfiles_size += size

        logfiles.sort()

        self.logfiles      = logfiles  # [LogFile, ...] in ascending order by path (really log filename which is time)
        self.logfiles_size = logfiles_size

    def prune_logfiles(self):
        total_size    = self.total_size
        itr_logfiles  = enumerate(reversed(logfiles := self.logfiles))
        logfiles_size = 0

        if logfiles:  # don't prune last file, we could be writing to it but if not then we still want to keep at least one log
            logfiles_size += next(itr_logfiles)[1].size

        for ridx, logfile in itr_logfiles:
            if (new_logfiles_size := logfiles_size + logfile.size) > total_size:
                try:
                    os.unlink(logfile.path)
                except FileNotFoundError:
                    pass
                except Exception as exc:
                    logger.error(exc)

                for _, logfile2 in itr_logfiles:
                    try:
                        os.unlink(logfile2.path)
                    except FileNotFoundError:
                        pass
                    except Exception as exc:
                        logger.error(exc)

                break

            logfiles_size = new_logfiles_size

        else:
            ridx = -1

        self.logfiles_size = logfiles_size

        if ridx != -1:  # we deleted some files, need to remove from logfiles and update the read stuff
            idx = len(logfiles) - ridx  # true index in logfiles of oldest SURVIVING file

            del logfiles[:idx]

            if (read_idx := self.read_idx - idx) >= 0:
                self.read_idx = read_idx

            else:
                self.read_idx = 0

                if read_file := self.read_file:
                    read_file.close()

                    self.read_file = None

    def refresh_logfiles(self) -> int:
        """Returns: 0 = no growth (maybe shrinkage), 1 = last logfile grew but no new logfiles, 2 = new logfiles. Will
        close read file if is not present in new list of logfiles. Should not be called with read_file is False.

        WARNING! This function currently assumes it is being called when all data has been exhausted and so will not
        correctly handle if you are within a file and there is still data to be read.
        """

        if (read_idx := self.read_idx) < (old_nlogfiles := len(old_logfiles := self.logfiles)):
            old_timestamp, old_path, old_size = old_logfiles[read_idx]
        elif not old_nlogfiles:
            old_timestamp = old_path = old_size = 0
        else:
            old_timestamp, old_path = old_logfiles[-1].timestamp, None

        self.scan_logfiles()

        close    = True
        read_idx = 0

        for read_idx, logfile in enumerate(logfiles := self.logfiles):
            if logfile.path == old_path:
                ret   = 2 if len(logfiles) > (read_idx + 1) else 1 if logfile.size > (old_size or 0) else 0
                close = False

                break

            if logfile.timestamp > old_timestamp:
                ret = 2

                break

        else:
            ret      = 0
            read_idx = len(logfiles)

        self.read_idx = read_idx

        if close and (read_file := self.read_file) is not None:
            read_file.close()

            self.read_file = None

        return ret
