#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin_impl.lockfile
    :synopsis: Filesystem-based interprocess synchronization primitive implementation details.
"""

import os


def try_acquire(lockfile_path):
    try:
        with open(lockfile_path, "x") as lockfile:
            lockfile.write(str(os.getpid()))
    except FileExistsError:
        return None
    except BaseException as err:
        if os.path.exists(lockfile_path):
            os.remove(lockfile_path)
        raise err
    else:
        return lockfile_path


def release(lockfile_state):
    os.remove(lockfile_state)
