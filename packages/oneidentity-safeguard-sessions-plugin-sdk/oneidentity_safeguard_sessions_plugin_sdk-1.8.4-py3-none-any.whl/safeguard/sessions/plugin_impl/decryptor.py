#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin_impl.decryptor
    :synopsis: Fake implemantion of the credential store credential decryptor

This service can be used for testing purposes.
"""
import json


class FakeDecryptor:
    """
    This class implements credential decryption
    """

    def decrypt(self, credential):
        """
        Decrypts the given credential

        :param str credential: the credential need to be decrypted
        :return: decoded string as json string
        :rtype: str
        """
        return "[{}]".format(json.dumps(credential))
