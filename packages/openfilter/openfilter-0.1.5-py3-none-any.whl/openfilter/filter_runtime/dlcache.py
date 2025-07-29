"""Download cache thingy.

Environment variables:
    JFROG_API_KEY: The JFrog API key, will be deprecated by evil JFrog people at end of September 2024, use JFROG_TOKEN
        instead.

    JFROG_TOKEN: The JFrog access token to the World Bank master server.

    DLCACHE_PATH: Path to root of cache.
"""

# TODO:
# -----
# * Check checksums? May be slower, currently using update timestamp.
# * Can expand to support more sources than just artifactory.

import logging
import os
from base64 import b64encode
from datetime import datetime
from threading import Thread

import requests

from .utils import sanitize_pathname, FnmLock

__all__ = ['is_cached_file', 'DLCache', 'dlcache']

logger = logging.getLogger(__name__)

JFROG_API_KEY = os.getenv('JFROG_API_KEY') or None
JFROG_TOKEN   = os.getenv('JFROG_TOKEN') or None
DLCACHE_PATH  = os.getenv('DLCACHE_PATH') or 'cache'

is_jfrog           = lambda s: s.startswith('jfrog://')
is_cached_file     = is_jfrog


class DLCache:
    """Download and cache "jfrog://..." artifactory files transparently to local. If there is a newer version available
    then get that, otherwise use what is currently here (if present). If can't connect then just warn and use what is
    present and if nothing present then log error and indicate in return. Expects and returns local filenames prepended
    with "file://..." scheme."""

    def __init__(self, cache_path: str = './', jfrog_token: str | None = None, is_api_key: bool = False):
        self.cache_path  = cache_path
        self.jfrog_token = jfrog_token
        self.is_api_key  = is_api_key  # TODO: deprecate once JFrog deprecates API keys
        self.cache       = {}  # {'jfrog://x.jfrog.io/artifactory/repo/...': 'file://x.jfrog.io/artifactory/repo/...', ...}  # just indicates presence of downloaded valid file

    def filename(self, dlcuri):
        return sanitize_pathname(os.path.normpath(os.path.join(self.cache_path, 'jfrog', dlcuri[8:])))

    def ensure(self, dlcuri: str, fnm: str) -> bool:
        file_exists = os.path.isfile(fnm)

        try:
            fnmlock = FnmLock(fnm)

            try:
                fileurl_parts = (fileuri := dlcuri[8:]).split('/', 2)

                assert fileurl_parts[1] == 'artifactory', f'malformed JFrog Artifactory link: {dlcuri}'

                fileurl = 'https://' + fileuri
                metaurl = 'https://' + '/'.join([fileurl_parts[0], fileurl_parts[1], 'api/storage', fileurl_parts[2]])
                headers = {} if self.jfrog_token is None else \
                    {'X-JFrog-Art-Api': self.jfrog_token} if self.is_api_key else \
                    {'Authorization':   f'Bearer {self.jfrog_token}'} if len(self.jfrog_token) <= 128 else \
                    {'Authorization':   f'Basic {b64encode(f":{self.jfrog_token}".encode()).decode()}'}  # NOTE: Bearer token seen to be 64 bytes max but using 128 just in case, Basic auth is much bigger than this

                response = requests.get(metaurl, headers=headers)

                if response.status_code != 200:
                    raise RuntimeError(f'get metadata failed ({response.status_code}): {metaurl}')

                try:
                    meta = response.json()
                except Exception:
                    raise RuntimeError(f'get metadata failed: {metaurl}')

                last_update = int(datetime.fromisoformat(meta['lastUpdated'].replace("Z", "+00:00")).timestamp())

                if file_exists and last_update <= os.stat(fnm).st_mtime:
                    return True

                logger.info(f'{(action := "update" if file_exists else "download")}: {dlcuri}')

                response = requests.get(fileurl, headers=headers)

                if response.status_code != 200:
                    raise RuntimeError(f'{action} failed ({response.status_code}): {fileurl}')

                fnm_tmp = fnm + '.tmp'

                with open(fnm_tmp, 'wb') as f:
                    for chunk in response.iter_content(0x100000):
                        f.write(chunk)

                try:
                    os.rename(fnm_tmp, fnm)  # atomic on Linux

                except FileExistsError:  # Windows
                    os.unlink(fnm)  # NOT ATOMIC!
                    os.rename(fnm_tmp, fnm)

                    logger.warning(f'non-atomic move used because atomic failed for: {fnm!r}')

                os.utime(fnm, (last_update, last_update))

                return True

            finally:
                fnmlock.release()

        except Exception as exc:
            (logger.warning if file_exists else logger.error)(exc)

        return file_exists

    def files(self, uris: str | list[str]) -> str | None | list[str | None]:
        """Return "file://..." filenames for potential "jfrog://..." or other URIs, checking version and downloading
        if not currently present or nwwer versions available. If a "file://..." URIs are passed then those are returned
        unmolested. If downloaded, returns "file://..." URIs to CACHED files which may have no similarity to the
        original "jfrog://..." or other URIs. Duplicate URIs in the list are handled fine."""

        if is_single := isinstance(uris, str):
            uris = [uris]

        dlcuris   = []
        dlcurimap = {}

        for uri in uris:
            if not is_jfrog(uri):
                dlcurimap[uri] = uri

            elif uri not in dlcurimap:
                dlcurimap[uri] = len(dlcuris)

                dlcuris.append(uri)

        if dlcuris:
            def ensure_all():
                class EnsureThread(Thread):
                    def __init__(self, func, args):
                        super().__init__(daemon=True)

                        self.func = func
                        self.args = args

                    def run(self):
                        self.res = self.func(*self.args)

                for fnm in (fnms := [self.filename(dlcuri) for dlcuri in dlcuris]):
                    os.makedirs(os.path.split(fnm)[0], exist_ok=True)

                threads = [EnsureThread(self.ensure, (dlcuri, fnm)) for dlcuri, fnm in zip(dlcuris, fnms)]
                res     = []

                for thread in threads:
                    thread.start()

                for thread in threads:
                    thread.join()

                    res.append(thread.res)

                return [r and 'file://' + fnm for r, fnm in zip(res, fnms)]

            res = ensure_all()

            fileuris = [u if isinstance(u := dlcurimap[uri], str) else res[u] or None for uri in uris]

        else:
            fileuris = uris

        return fileuris[0] if is_single else fileuris


dlcache = DLCache(DLCACHE_PATH, JFROG_TOKEN or JFROG_API_KEY, JFROG_TOKEN is None)
