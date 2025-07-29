#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
#
"""
.. py:module:: safeguard.sessions.plugin.ldap_server
    :synopsis: Interface to LDAP Server policies configured in SPS.

The LDAPServer service implements retrieving a user attribute from preconfigured AD or unix LDAP servers.

Configuration example
=====================
.. code-block:: ini

    [ldap_server]
    # Name of the LDAP Server policy configured in SPS
    ; name = <ldap-server-policy-name>

    # The LDAP attribute name which should be used.
    # Note that this may be different from the displayed name of the
    # attribute, especially in Microsoft Windows, for example
    # "Office" attribute is encoded in "physicalDeliveryOfficeName".
    user_attribute = description

Acquiring a user attribute
==========================

In this example we'll use the following configuration to fetch the description attribute of the user administrator.

.. code-block:: ini

    [ldap_server]
    # Name of the LDAP Server policy configured in SPS
    name = my_ad_policy

    # The LDAP attribute name which should be used.
    # Note that this may be different from the displayed name of the
    # attribute, especially in Microsoft Windows, where for example
    # "Office" attribute is encoded in "physicalDeliveryOfficeName".
    user_attribute = description

.. code-block:: python

    from safeguard.sessions.plugin import PluginConfiguration
    from safeguard.sessions.plugin import LDAPServer

    class Plugin:
       def __init__(self, configuration):
           self.__config = PluginConfiguration(configuration)
           self.__ldap = LDAPServer.from_config(self.__config)
           attribute = self.__ldap.get_user_attribute('administrator')
"""

from safeguard.sessions.plugin.ldap_server_exceptions import *  # noqa: F401, F403
from safeguard.sessions.plugin_impl.ldap_server import LdapService


class LDAPServer:
    """
    The :class:`LDAPServer` represent access to the LDAP Server configured in SPS.

    Do not instantiate LDAPServer service with its constructor, rather use the :meth:`from_config` method.

    :param plugin_configuration: configuration to use
    :param str section: the section to get configuration options from
    :param ldap_service: reference to internal implementation
    """

    def __init__(self, ldap_service, user_attribute_factory, user_groups_factory):
        self.__ldap_service = ldap_service
        self.__user_attribute_factory = user_attribute_factory
        self.__user_groups_factory = user_groups_factory

    @classmethod
    def from_config(cls, plugin_configuration, section="ldap_server", name=None):
        """
        The :meth:`from_config` class method creates an :class:`LDAPServer` instance from a given plugin configuration.

        :param plugin_configuration: plugin configuration object
        :type plugin_configuration: :class:`PluginConfiguration \
          <safeguard.sessions.plugin.plugin_configuration.PluginConfiguration>`
        :param str section: name of the section where the LDAP parameters are stored
        :param str name: name of the LDAP server policy
        :return: LDAPServer instance
        :rtype: :class:`LDAPServer`
        :raises: :class:`RequiredConfigurationSettingNotFound \
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>` if there
          is no such section or \"name\" option in the section defined in the configuration.
        """
        ldap_policy = name or plugin_configuration.get(section, "name", required=True)

        def user_attribute_factory():
            return plugin_configuration.get(section, "user_attribute", required=True)

        def user_groups_factory():
            return plugin_configuration.get(section, "user_groups", required=True).split(",")

        return cls(LdapService(ldap_policy), user_attribute_factory, user_groups_factory)

    def get_user_string_attribute(self, username, attribute=None):
        """
        The :meth:`get_user_string_attribute` method can retrieve a user's string attribute from LDAP. Any string or
        numeric value that can be converted to a UTF-8 string  will be returned. On the other hand binary data will
        trigger an error, for example a JPEG photo cannot be fetched this way.

        :param str username:
        :param str attribute:
        :return: list of values in the attribute
        :raises: :class:`RequiredConfigurationSettingNotFound \
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
          if the attribute parameter is None but there is no \"user_attribute\" defined in the configuration.
        :raises: :class:`LDAPUserNotFound <safeguard.sessions.plugin.ldap_server_exceptions.LDAPUserNotFound>` if the
          user is not found in LDAP database.
        :raises: :class:`LDAPOperationError <safeguard.sessions.plugin.ldap_server_exceptions.LDAPOperationError>` on
          other LDAP related errors.
        """
        if attribute is None:
            attribute = self.__user_attribute_factory()
        return self.__ldap_service.get_user_string_attribute(username, attribute)

    def get_user_string_attributes(self, username, attributes):
        """
        The :meth:`get_user_string_attributes` method can retrieve multiple string attributes of a user from LDAP.
        Any string or numeric value that can be converted to a UTF-8 string  will be returned. On the other hand binary
        data will trigger an error, for example a JPEG photo cannot be fetched this way. The result contains a
        dictionary of attribute to list of value mapping, where missing attributes, empty attributes get the empty list
        as a value.

        *New in version 1.4.0.*

        :param str username:
        :param list attributes:
        :return: dictionary of attribute to value list
        :raises: :class:`LDAPUserNotFound <safeguard.sessions.plugin.ldap_server_exceptions.LDAPUserNotFound>` if the
          user is not found in LDAP database.
        :raises: :class:`LDAPOperationError <safeguard.sessions.plugin.ldap_server_exceptions.LDAPOperationError>` on
          other LDAP related errors.
        """
        if not attributes:
            return {}
        return self.__ldap_service.get_user_string_attributes(username, attributes)

    def filter_user_groups(self, username, groups=None):
        """
        The :meth:`filter_user_groups` method can check whether a user is member of a list of predefined groups.

        :param str username:
        :param list groups:
        :return: the input groups reduced to those groups that the user is actually a member of
        :rtype: list
        :raises: :class:`RequiredConfigurationSettingNotFound \
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
          if the groups parameter is None but there is no \"user_groups\" defined in the configuration.
        :raises: :class:`LDAPUserNotFound <safeguard.sessions.plugin.ldap_server_exceptions.LDAPUserNotFound>` if the
          user is not found in LDAP database.
        :raises: :class:`LDAPOperationError <safeguard.sessions.plugin.ldap_server_exceptions.LDAPOperationError>` on
          other LDAP related errors.
        """
        if groups is None:
            groups = self.__user_groups_factory()
        return self.__ldap_service.filter_user_groups(username, groups)
