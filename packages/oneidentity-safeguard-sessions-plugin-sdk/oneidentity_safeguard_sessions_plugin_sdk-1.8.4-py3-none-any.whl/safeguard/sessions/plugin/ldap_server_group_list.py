#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#


from .ldap_server import LDAPServer
from .ldap_server_exceptions import LDAPOperationError, LDAPUserNotFound
from safeguard.sessions.plugin import logging


class LDAPServerGroupList:
    """
    The :class:`LDAPServerGroupList` class implements LDAP group based whitelist functionality.
    """

    def __init__(self, allow, except_list, ldap_server):
        self._allow = allow
        self._except = except_list
        self._ldap_server = ldap_server

    @classmethod
    def from_config(cls, plugin_configuration, section="ldap_server_group"):
        allow = plugin_configuration.getienum(section, "allow", ("no_user", "all_users"), required=True)
        except_list = [group.strip() for group in plugin_configuration.get(section, "except", required=True).split(",")]
        ldap_server = LDAPServer.from_config(plugin_configuration)
        return cls(allow, except_list, ldap_server)

    def check_group(self, username):
        try:
            return (self._allow == "no_user") == bool(self._ldap_server.filter_user_groups(username, self._except))
        except LDAPUserNotFound as e:
            logging.get_logger(__name__).warning(
                "Could not check LDAP group whitelist due to user not found in LDAP: {}".format(e)
            )
            return False
        except LDAPOperationError as e:
            logging.get_logger(__name__).warning("Could not check LDAP group whitelist due to LDAP error: {}".format(e))
            return False

    def __contains__(self, username):
        return self.check_group(username)
