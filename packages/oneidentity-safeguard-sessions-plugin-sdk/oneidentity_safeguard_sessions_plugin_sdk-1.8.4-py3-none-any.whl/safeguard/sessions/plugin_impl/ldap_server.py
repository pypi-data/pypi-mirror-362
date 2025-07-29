#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
#
"""
.. py:module:: safeguard.sessions.plugin_impl.ldap_server
    :synopsis: Fake LdapServer implementation

To inject user defined LDAP database into the :class:`LDAPServer \
<safeguard.sessions.plugin.ldap_server.LDAPServer>` API when testing outside the SPS box.

Patch/overwrite the ``safeguard.sessions.plugin_impl.ldap_server.ldap_servers`` with your own LDAP like database.

The ``ldap_servers`` is a dictionary where the key is the name of the LDAP Server policy to define, and the value
itself is a dictionary where "users", "groups" keys define users and groups respectively. See the example
for more detail.


Example usage with pytest and monkeypatch
-----------------------------------------

.. code-block:: python

    from safeguard.sessions.plugin import LDAPServer
    from safeguard.sessions.plugin import PluginConfiguration as PluginConfig
    from safeguard.sessions.plugin_impl.ldap_server import ldap_servers

    def test_user_list(monkeypatch):
        # Data injection
        testdb = {
            'users': {
                'root': {
                    'description': 'adminuser',
                    'cn': 'root',
                    'multivalue': ['a', 'b'],
                    'numeric': 1000,
                },
                'wsmith': {
                    'description': 'user',
                    'cn': 'wsmith',
                    'multivalue': ['x', 'y'],
                },
            },
            'groups': {
                'admins': ['root'],
                'dbuser': ['wsmith']
            }
        }
        monkeypatch.setitem(ldap_servers, 'adserver', testdb)

        # Test the injected data
        pc = PluginConfig('''
        [ldap_server]
        name=adserver
        ''')

        ls = LDAPServer.from_config(pc)

        assert ls.get_user_string_attribute('numeric') == ['1000']
        assert ls.filter_user_groups('root', ['admins']) == ['admins']
"""

from safeguard.sessions.plugin.ldap_server_exceptions import LDAPOperationError, LDAPUserNotFound

ldap_servers = {}


class LdapService:
    def __init__(self, ldap_policy="adserver", database=ldap_servers):
        self.__database = database
        self.__ldap_policy = ldap_policy

    def get_user_string_attribute(self, username, attribute):
        if not self._user_exists(username):
            raise LDAPUserNotFound({"policy": self.__ldap_policy, "username": username})

        user_data = {
            (key.lower() if hasattr(key, "lower") else key): value
            for key, value in self.__database[self.__ldap_policy]["users"][username].items()
        }

        result = user_data.get(attribute.lower(), [])

        result = result if isinstance(result, list) else [result]
        try:
            return [item.decode("utf-8") if isinstance(item, bytes) else str(item) for item in result]
        except UnicodeDecodeError as e:
            raise LDAPOperationError(
                "LDAP attribute is not UTF-8 string",
                {"reason": str(e), "policy": self.__ldap_policy, "username": username, "attribute": attribute},
            )

    def get_user_string_attributes(self, username, attributes):
        return {attribute: self.get_user_string_attribute(username, attribute) for attribute in attributes}

    def filter_user_groups(self, username, groups):
        if not self._user_exists(username):
            raise LDAPUserNotFound({"policy": self.__ldap_policy, "username": username})

        profile = self.__database[self.__ldap_policy]
        if "groups" not in profile:
            return []

        return [group for group in groups if username in profile["groups"].get(group, ())]

    def _user_exists(self, username):
        try:
            profile = self.__database[self.__ldap_policy]
        except KeyError:
            raise LDAPOperationError("No such profile in the database", {"policy": self.__ldap_policy})

        if "users" not in profile:
            raise LDAPOperationError("get_user failed; No such object")

        return username in profile["users"]
