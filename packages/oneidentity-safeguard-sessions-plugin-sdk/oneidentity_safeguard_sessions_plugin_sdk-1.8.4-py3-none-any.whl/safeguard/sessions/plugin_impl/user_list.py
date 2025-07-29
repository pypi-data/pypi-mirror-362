#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin_impl.user_list
    :synopsis: Fake UserList implementation

To inject user defined User List policies database into the :class:`UserList \
<safeguard.sessions.plugin.user_list.UserList>` API when testing outside the SPS box.

Patch/overwrite the ``safeguard.sessions.plugin_impl.user_list.user_lists`` with your own database. The ``user_lists``
is a dictionary where the key is the name of the User List policy to define, and the value is itself a dictionary with
keys "allow" and "except" that define the default mode and exceptions for the User List - like on the Web interface.


Example usage with pytest and monkeypatch
-----------------------------------------

.. code-block:: python

    from safeguard.sessions.plugin import UserList
    from safeguard.sessions.plugin import PluginConfiguration as PluginConfig
    from safeguard.sessions.plugin_impl.user_list import user_lists

    def test_user_list(monkeypatch):
        # Data injection
        testdb = {
            "allow": "no_user", "except": ["user1"]
        }
        monkeypatch.setitem(user_lists, 'user_whitelist', testdb)

        # Test the injected data
        pc = PluginConfig('''
        [user_list]
        name=user_whitelist
        ''')

        ul = UserList.from_config(pc)

        assert ul.check_user('user1') is True
        assert ul.check_user('other_user') is False
"""
from safeguard.sessions.plugin.user_list_exceptions import LocalUserListNotFound


user_lists = {}


def user_list_parameters_factory(user_list_name):
    if user_list_name not in user_lists:
        raise LocalUserListNotFound(user_list_name)
    user_list = user_lists[user_list_name]
    return user_list["except"], user_list["allow"]
