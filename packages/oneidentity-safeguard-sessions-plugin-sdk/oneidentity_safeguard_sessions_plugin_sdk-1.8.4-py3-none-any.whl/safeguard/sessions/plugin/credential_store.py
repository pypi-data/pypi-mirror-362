#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
#
"""
.. py:module:: safeguard.sessions.plugin.credential_store
    :synopsis: Interface to read credentials from the configured local credential store.

The CredentialStore service implements retrieving and decrypting of credentials from a configured local credential
store.

Configuration example
=====================
.. code-block:: ini

    [credential_store]
    # Name of the local credential store configured in SPS for hosting sensitive
    # configuration data. For more information, read the "Store sensitive
    # plugin data securely" section in the documentation.
    ; name=<name-of-credential-store-policy-that-hosts-sensitive-data>

Acquiring a CredentialStore
---------------------------
.. code-block:: python

    from safeguard.sessions.plugin import PluginConfiguration
    from safeguard.sessions.plugin import CredentialStore

    class Plugin:
       def __init__(self, configuration):
           self.__config = PluginConfiguration(configuration)
           self.__cred_store = CredentialStore.from_config(self.__config)
"""
import json
from safeguard.sessions.plugin_impl.credential_store import credential_store_parameters_factory
from .credential_store_exceptions import *  # noqa: F401, F403
from .logging import get_logger


class CredentialStore:
    """
    The :class:`CredentialStore` class represents access to a local credential store.

    Do not instantiate a :class:`CredentialStore` with its constructor, rather use the :meth:`from_config` method.
    """

    def __init__(self, database, decryptor):
        self.__logger = get_logger(__name__)
        self.__database = database
        self.__decryptor = decryptor

    @classmethod
    def from_config(cls, plugin_configuration, section="credential_store", name=None):
        """
        The :meth:`from_config` class method creates an instance of :class:`CredentialStore` from a given plugin
        configuration.

        :param plugin_configuration: plugin configuration object
        :type plugin_configuration: :class:`PluginConfiguration \
          <safeguard.sessions.plugin.plugin_configuration.PluginConfiguration>`
        :param str section: name of the section where the credential store name is stored
        :param str name: name of the credential store policy
        :return: credential store service instance
        :rtype: :class:`CredentialStore <safeguard.sessions.plugin.credential_store.CredentialStore>`
        """
        credential_store_name = name or plugin_configuration.get(section, "name", required=True)
        return cls(*credential_store_parameters_factory(credential_store_name))

    def get_all(self):
        """
        The :meth:`get_all` method retrieves all decrypted credentials from the credential store.

        :return: list of tuples of members (user, host, credential)
        :rtype: list
        :raises: :class:`RequiredConfigurationSettingNotFound
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
        """
        self.__logger.info("Collecting all encrypted values")
        # Decryptor service always returns the decrypted credential in a list, hence the pop call on __unpack_cred
        return [(row[0], row[1], self.__unpack_cred(row[2]).pop(0)) for row in self.__database.query_all()]

    def get_credentials(self, host, user):
        """
        The :meth:`get_credentials` method retrieves all the decrypted credentials for a given host and user pair.

        :param str host: host name to retrieve credentials for
        :param str user: user name to retrieve credentials for
        :return: list of unfiltered, decrypted credentials
        :rtype: list
        :raises: :class:`RequiredConfigurationSettingNotFound
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
        """
        result = []
        for packed in self.__database.query_one(host, user):
            result.extend(self.__unpack_cred(packed[0]))
        return result

    def get_passwords(self, host, user):
        """
        The :meth:`get_passwords` method retrieves all the decrypted passwords for a given host and user pair.

        :param str host: host name retrieve passwords for
        :param str user: user name retrieve passwords for
        :return: list of unfiltered, decrypted passwords
        :rtype: list
        :raises: :class:`RequiredConfigurationSettingNotFound
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
        """
        return self.__get_filtered_creds(host, user, self._is_password)

    def get_keys(self, host, user):
        """
        The :meth:`get_keys` method retrieves all the decrypted SSH Keys for a given host and user pair.

        :param str host: host name retrieve SSH Keys for
        :param str user: user name retrieve SSH Keys for
        :return: list of unfiltered, decrypted SSH Keys
        :rtype: list
        :raises: :class:`RequiredConfigurationSettingNotFound
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
        """
        return self.__get_filtered_creds(host, user, self._is_key)

    def get_certificates(self, host, user):
        """
        The :meth:`get_certificates` method retrieves all the decrypted X509 Key for a given host and user pair.

        :param str host: host name retrieve X509 Key for
        :param str user: user name retrieve X509 Key for
        :return: list of unfiltered, decrypted X509 Key
        :rtype: list
        :raises: :class:`RequiredConfigurationSettingNotFound
          <safeguard.sessions.plugin.plugin_configuration_exceptions.RequiredConfigurationSettingNotFound>`
        """
        return self.__get_filtered_creds(host, user, self._is_cert)

    def __get_filtered_creds(self, host, user, predicate):
        return [cred for cred in self.get_credentials(host, user) if predicate(cred)]

    def __unpack_cred(self, cred):
        return json.loads(self.__decryptor.decrypt(cred))

    @staticmethod
    def _is_password(cred):
        return isinstance(cred, str)

    @staticmethod
    def _is_key(cred):
        return isinstance(cred, dict) and cred["type"] in ("ssh-rsa", "ssh-dss", "ecdsa-sha2-nistp256")

    @staticmethod
    def _is_cert(cred):
        return isinstance(cred, dict) and cred["type"] in ("x509v3-sign-rsa", "x509v3-sign-dss")
