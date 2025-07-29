#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from . import logging
from .ldap_server import LDAPServer
from .ldap_server_exceptions import LDAPOperationError, LDAPUserNotFound


class UserMappingExplicit:
    """
    The :class:`UserMappingExplicit`
    """

    @classmethod
    def map_username(cls, username, plugin_configuration, section="user_mapping"):
        return plugin_configuration.get(section, username.lower())


class UserMappingLdapServer:
    """
    The :class:`UserMappingLdapServer`
    """

    def __init__(self):
        self._logger = logging.get_logger(__name__)

    @classmethod
    def from_config(cls, plugin_configuration, section="user_mapping"):
        cls._ldap_server = LDAPServer.from_config(plugin_configuration)
        cls._user_attribute = plugin_configuration.get(section, "user_attribute", required=True)
        logging.configure(plugin_configuration)
        return cls()

    def map_username(self, username):
        try:
            attribute_values = self._ldap_server.get_user_string_attribute(username, self._user_attribute)
        except LDAPUserNotFound as e:
            self._logger.warning("User mapping is not possible, user not in LDAP: {}".format(e))
            return None
        except LDAPOperationError as e:
            self._logger.warning("User mapping is not possible, LDAP error occurred: {}".format(e))
            return None
        else:
            if attribute_values:
                return attribute_values[0]
        return None
