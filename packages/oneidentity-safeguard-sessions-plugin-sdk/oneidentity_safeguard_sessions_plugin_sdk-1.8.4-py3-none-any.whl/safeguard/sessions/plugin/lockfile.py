#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.lockfile
    :synopsis: Filesystem-based interprocess synchronization primitive.
"""

from contextlib import contextmanager
import os
from safeguard.sessions.plugin import logging
from safeguard.sessions.plugin_impl.lockfile import try_acquire, release
from time import sleep


class Lockfile:
    """
    The :class:`Lockfile` represents an interprocess synchronization primitive.
    """

    def __init__(self, path):
        """
        The :meth:`__init__` method initializes a new, unacquired lockfile.

        :param str path: path of the lockfile
        """

        self.__path = os.path.realpath(path)
        self.__state = None
        self.__logger = logging.get_logger(__name__)

    @property
    def path(self):
        """
        Path of the lockfile.
        """
        return self.__path

    @property
    def is_acquired(self):
        """
        True, if this Lockfile instance is acquired; otherwise, False.
        """
        return self.__state is not None

    def try_acquire(self):
        """
        The :meth:`try_acquire` method tries to acquire the lock.

        Calling this method on an already acquired lock issues a warning.

        :return: Whether the acquisition was successful.
        """
        if self.is_acquired:
            self.__logger.warning("Trying to acquire an already acquired lockfile: %s", self.path)
            return True

        self.__state = try_acquire(self.path)

        if self.is_acquired:
            self.__logger.debug("Lockfile successfully acquired: %s", self.path)
        else:
            self.__logger.debug("Lockfile is already taken: %s", self.path)

        return self.is_acquired

    def acquire(self, *, timeout=0, retries=0):
        """
        The :meth:`acquire` method acquires the lock.

        The acquisition is attempted at least once, waiting :paramref:`timeout`
        seconds before trying again, doing this :paramref:`retries` times.
        If none of the attempts were successful, :class:`TimeoutError` is raised.

        :param float timeout: number of seconds to wait between retries; default: 0
        :param int retries: number of times to retry acquiring the lock before failing; default: 0
        :raises: :class:`TimeoutError`
        """

        while not self.try_acquire():
            if retries > 0:
                self.__logger.debug("Waiting %s seconds before trying to acquire lockfile: %s", timeout, self.path)
                sleep(timeout)
                retries -= 1
            else:
                self.__logger.debug("Failed to acquire lockfile: %s", self.path)
                raise TimeoutError()

    def release(self):
        """
        The :meth:`release` method releases an acquired lock.

        Calling this method on an unacquired lock issues a warning.
        """
        if not self.is_acquired:
            self.__logger.warning("Release called on unacquired lockfile: %s", self.path)
            return

        self.__state = release(self.__state)  # pylint: disable=assignment-from-no-return, assignment-from-none
        self.__logger.debug("Lockfile released: %s", self.path)


@contextmanager
def lockfile(path, *, timeout=0, retries=0):
    """
    Context manager for executing code inside an interprocess mutex.

    :param str path: path of the lockfile
    :param float timeout: number of seconds to wait between retries; default: 0
    :param int retries: number of times to retry acquiring the lock before failing; default: 0

    .. code-block:: python
        from safeguard.sessions.plugin_impl.lockfile import lockfile

        with lockfile('/tmp/resource.lock', timeout):
            # use resource here
    """
    lf = Lockfile(path)
    lf.acquire(timeout=timeout, retries=retries)
    try:
        yield lf
    finally:
        lf.release()


def lockfile_for(file_path, *, timeout=0, retries=0):
    """
    Context manager for executing code inside an interprocess mutex for the specified file.

    This helper method suffixes the provided file path with '.lock', as it is customary for lockfiles.

    :param str file_path: path of a file to create the lockfile for
    :param float timeout: number of seconds to wait between retries; default: 0
    :param int retries: number of times to retry acquiring the lock before failing; default: 0
    """
    return lockfile(file_path + ".lock", timeout=timeout, retries=retries)
