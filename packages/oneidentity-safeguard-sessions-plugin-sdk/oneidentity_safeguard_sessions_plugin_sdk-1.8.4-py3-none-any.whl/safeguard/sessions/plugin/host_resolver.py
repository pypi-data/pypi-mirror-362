#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.host_resolver
    :synopsis: DNS utilities
"""
from .logging import get_logger
import socket


class HostResolver:
    """
    The :class:`HostResolver` class represents a utility class to access DNS services.

    Do not instantiate :class:`HostResolver` with its constructor, rather use the :meth:`from_config` method.
    """

    def __init__(self):
        self.logger = get_logger(__name__)

    @classmethod
    def from_config(cls, plugin_configuration):
        """
        The :meth:`from_config` method creates an instance of HostResolver service.

        :param plugin_configuration: plugin configuration object
        :type plugin_configuration: :class:`PluginConfiguration \
          <safeguard.sessions.plugin.plugin_configuration.PluginConfiguration>`
        :return: HostResolver instance
        :rtype: :class:`HostResolver <safeguard.sessions.plugin.host_resolver.HostResolver>`
        """
        del plugin_configuration  # currently it doesn't have options
        return cls()

    def resolve_hosts_by_ip(self, ip_address):
        """
        The :meth:`resolve_hosts_by_ip` method uses the DNS service to resolve a given IP address into a list of the
        primary fully qualified domain name and possible alias names.

        :param str ip_address: the IP address to resolve
        :return: list of host names
        :raises: socket.error
        """
        hosts = []

        try:
            socket.inet_aton(ip_address)  # Is it really an IP?
        except socket.error:
            return [ip_address]

        try:
            hostname, aliases, _ = socket.gethostbyaddr(ip_address)
            hosts.append(hostname)
            hosts.extend(aliases)
        except socket.herror:
            self.logger.warning("Failed to look up system name based on address: %s", ip_address)
        return hosts
