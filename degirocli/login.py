import tempfile
import getpass
import functools
import multiprocessing
import stat
import asyncio
import json
import time
import pickle
import sys
import os
from pathlib import Path
from typing import Union
from typing import Optional

import degiroasync.api as dapi
import degiroasync.webapi as wapi
import degiroasync.core as dcore

from .helpers import ERROR_CODES
from .helpers import LOGGER



def get_credentials() -> dapi.Credentials:
    """
    Helper to get credentials for degiroasync provider.
    """
    DEGIRO_USERNAME = 'DEGIRO_USERNAME'
    DEGIRO_PASSWORD = 'DEGIRO_PASSWORD'
    DEGIRO_TOTP_SECRET = 'DEGIRO_TOTP_SECRET'
    if (username := os.environ.get(DEGIRO_USERNAME)) is None:
        username = input('Username: ')
        if len(username.strip()) == 0:
            raise AssertionError(
                    "{} not set and not provided".format(DEGIRO_USERNAME))
    if (password := os.environ.get(DEGIRO_PASSWORD)) is None:
        password = getpass.getpass('Password: ')
        if len(password.strip()) == 0:
            raise AssertionError("{} not set and not provided".format(DEGIRO_PASSWORD))
    totp_secret: Optional[str] = os.environ.get(DEGIRO_TOTP_SECRET) or None  # could be ''
    totp = None
    if totp_secret is None:
        # Ask user for TOTP
        totp: Optional[str] = input("One Time Password (Enter to ignore): ")
        if len(totp.strip()) == 0:
            totp = None

    return dapi.Credentials(
        username=username,
        password=password,
        totp_secret=totp_secret,
        one_time_password=totp
        )


def get_tmp_path():
    tmpdir = Path(tempfile.gettempdir())
    return tmpdir / 'degirocli' 

def _get_hash(path: Union[Path, str]) -> str:
    with open(path, 'rb') as fh:
        fhash = hash(fh)
    return fhash


def expire_path(
        path: Union[Path, str],
        lifetime_seconds: Union[int, float]=60*60*2,
        start_time_seconds: Optional[Union[int, float]] = None,
        force: bool = False,
        ):
    """
    Will remove file at path after 'lifetime_seconds'.

    Parameters
    ----------

    path
        Path to remove when expired. By default, `path` will only be removed
        if it hasn't changed since watcher started. 

    lifetime_seconds
        File at path will be expired at start_time_seconds + lifetime_seconds.

    start_time_seconds
        File at path will be expired at start_time_seconds + lifetime_seconds.
        Defaults to time.time().

    force
        If true, file at `path` will be removed even if it has changed since
        this function has been called.
    """
    # Let's detach this process.
    if os.fork() != 0:  # If os.fork == 0 this is the detached process.
        return
    if not isinstance(path, Path):
        assert isinstance(path, str)
        path = Path(path)
    fhash = _get_hash(path)
    start_time_seconds = start_time_seconds or time.time()

    while time.time() - start_time_seconds < lifetime_seconds:
        time.sleep(time.time() - start_time_seconds)

    tmp_path = get_tmp_path()
    if tmp_path.exists():
        if tmp_path.is_file():
            fhash_new = _get_hash(path)
            if fhash_new == fhash or force:
                Path.unlink(tmp_path)
            else:
                print(f'{path} has changed since it has been set to expire. '
                      f'Abort deletion.', file=sys.stderr)
                return 1
    return 0


#@functools.wraps(_expire_path)
#def expire_path(*args):
#    # Start event loop to 
#    proc = multiprocessing.Process(
#            target=_expire_path,
#            args=args,
#            daemon=False)
#    proc.start()


async def login():
    tmp_path = get_tmp_path()

    if tmp_path.exists():
        ans = input("Existing session found, delete? (y/N)").strip().lower()
        if ans in ('y', 'yes'):
            tmp_path.unlink()
        else:
            print('Abort.')
            return ERROR_CODES.SESSION_EXISTS

    # Get sessionID and write it
    credentials = get_credentials()
    session = await wapi.login(credentials)
    tmp_path.touch()
    tmp_path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    with open(tmp_path, 'w') as fh:
        json.dump({
            'version': 1,
            'format': 'degirocli',
            'session': dict(
                cookies=session.cookies,
                ),
            }, fh)
    # Delete file in 3 hour
    expire_path(tmp_path, 3*60*60)

async def _get_session_from_cache() -> dapi.Session:
    cache_path = get_tmp_path()
    if not cache_path.exists():
        raise AssertionError(
                f"{cache_path} not found. Abort. Have you tried degiro-login?")
    with open(cache_path, 'r') as fh:
        session_d = json.load(fh)
    session = dcore.SessionCore()
    session._cookies = session_d['session']['cookies']
    await wapi.get_config(session)
    await wapi.get_client_info(session)
    exc_dict = await dapi.get_dictionary(session)
    return dapi.Session(session, exc_dict)

def get_session_from_cache() -> dapi.Session:
    """
    Helper to get Session when already logged in.
    """
    return asyncio.get_event_loop().run_until_complete(_get_session_from_cache())

def  run_cli():
    asyncio.get_event_loop().run_until_complete(login())
