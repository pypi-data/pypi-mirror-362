#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin_impl.database
    :synopsis: Fake implementation of the credential store back-end database

This can be used for testing purposes.
If you rather like to use your own database you can pass it as a constructor parameter

Acquiring a database object
---------------------------
.. code-block:: python

    from safeguard.sessions.plugin_impl.database import FakeDatabase

    myFake = FakeDatabase(database = {})

Example database
----------------
.. code-block:: python

    {
        "user": {"host": [("password")]},
        "user1": {"host1": [({"type": "ssh-rsa", "key": "theKey"})]}
    }
"""

SQLITE_DB = {
    "user1": {"host1": [("secret",), ("mistery",)]},
    "user2": {"host1": [("dev_secret2",)]},
    "user3": {"host1": [({"type": "ssh-rsa", "key": "myKey"},)]},
    "user4": {"host1": [({"type": "x509v3-sign-rsa", "key": "myKey", "cert": "myCert"},)]},
    "user5": {
        "host1": [
            ("secret",),
            ({"type": "x509v3-sign-rsa", "key": "myKey", "cert": "myCert"},),
            ({"type": "ssh-rsa", "key": "myKey"},),
        ]
    },
}


class FakeDatabase:
    """
    This class implements the fake back-end database for credential stores
    """

    def __init__(self, database=SQLITE_DB):
        """
        Contructor.

        :param dict database: Holding the data can represent database rows
        """
        self.__database = database

    def query_one(self, host, username):
        """
        Retrieve one credential belongs to a host, user pair

        :param str host: Host name
        :param str username: User name
        :return: List of tuples with a string or a dict depending on the credential site
        :rtype: list
        """
        return self.__database.get(username, {}).get(host, [])

    def query_all(self):
        """
        Retrieve all credentials from the database

        :return: list of tuples with (user, host, credential)
        :rtype: list
        """
        result = []
        for user in self.__database:
            host = [k for k in self.__database[user].keys()][0]
            for credential in self.__database[user][host]:
                cred = credential[0]
                result.append((user, host, cred))
        return result
