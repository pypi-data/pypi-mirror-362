#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.user_list
    :synopsis: Interface to User List policies configured in SPS.

The UserList implements checking whether a user name matches the given
User List policy. Note that the match is case sensitive.

Configuration example
=====================
.. code-block:: ini

    [user_list]
    # Name of the User List policy configured in SPS (Policies -> User Lists)
    ; name = <user-list-policy-name>

Checking whether a user name matches a User List
------------------------------------------------

In this example we'll use the following configuration to check User List membership of user 'administrator'

.. code-block:: ini

    [user_list]
    # Name of the User List policy configured in SPS (Policies -> User Lists)
    name = my_user_list_policy

.. code-block:: python

    from safeguard.sessions.plugin import PluginConfiguration
    from safeguard.sessions.plugin import UserList

    class Plugin:
       def __init__(self, configuration):
           self.__config = PluginConfiguration(configuration)
           self.__user_list = UserList.from_config(self.__config)
           is_matched = self.__user_list.check_user('administrator')
"""

from safeguard.sessions.plugin.exceptions import PluginSDKValueError
from safeguard.sessions.plugin_impl.user_list import user_list_parameters_factory


class UserList:
    """
    The :class:`UserList` represents access to the User List policy in SPS.

    Do not instantiate UserList service with its constructor, rather use the :meth:`from_config` method.

    :param list users: a list of user names, corresponding to the except list in the policy
    :param default: 'all_users' or 'no_user', corresponding to the allow setting in the policy
    """

    ALLOW = ("all_users", "no_user")

    def __init__(self, users, default):
        if default not in self.ALLOW:
            raise PluginSDKValueError("'allow' must be one of: {}".format(self.ALLOW), {"allow": default})
        self._users = users
        self._default = default

    @classmethod
    def from_config(cls, plugin_configuration, section="user_list", name=None):
        """
        The :meth:`from_config` method creates a :class:`UserList` instance from the given plugin configuration.

        :param plugin_configuration: plugin configuration object
        :type plugin_configuration: :class:`PluginConfiguration \
          <safeguard.sessions.plugin.plugin_configuration.PluginConfiguration>`
        :param str section: name of the configuration section where the User List policy name is found
        :param str name: name of the User List policy
        :return: :class:`UserList`
        :raises: :class:`RequiredConfigurationSettingNotFound \
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>` if there
          is no such section or \"name\" option in the section defined in the configuration.
        :raises: :class:`LocalUserListNotFound \
          <safeguard.sessions.plugin.user_list_exceptions.LocalUserListNotFound>` if the given User List policy is not
          found.
        """
        user_list_name = name or plugin_configuration.get(section, "name", required=True)
        return cls(*user_list_parameters_factory(user_list_name))

    def check_user(self, username):
        """
        The :meth:`check_user` will match the user name against a User List policy that contains an "allow" and
        "except" configuration option. The returned value is True in two cases:

        1. the "allow" option equals ``no_user`` and the user name is in the "except" list (whitelist case)
        2. the "allow" option equals ``all_users`` and the user name is not in the "except" list (blacklist case)

        otherwise the return value is False.

        *Note*: the check in the "except" list is case sensitive.

        :param str username: the user name to check
        :return: bool
        """
        return (username in self._users) == (self._default == "no_user")

    def __contains__(self, username):
        """
        The 'in' operator on a UserList equals :meth:`check_user` method, thus the following is true:

        .. code-block:: python

            assert user_list.check_user('administrator') == ('administrator' in user_list)


        :param str username:
        :return: bool
        """
        return self.check_user(username)
