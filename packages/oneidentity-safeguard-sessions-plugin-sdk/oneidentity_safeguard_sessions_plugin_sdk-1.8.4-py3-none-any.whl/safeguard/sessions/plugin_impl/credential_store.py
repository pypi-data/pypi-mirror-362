#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin_impl.credential_store
    :synopsis: Fake CredentialStore implementation

To inject a user defined CredentialStore database into the :class:`CredentialStore \
<safeguard.sessions.plugin.credential_store.CredentialStore>` API when testing outside the SPS box.

Patch/overwrite the ``safeguard.sessions.plugin_impl.credential_store.credential_stores`` with your own dictionary.

Note that for x509 certificates, the fake credential_store does not decrypt password protected private keys.

The ``credential_stores`` is a dictionary where the key is the name of the local Credential Store policy to define.
Inside a policy the data is keyed with user name first, then host name and then as value a list of passwords, private
keys or X509 credentials. Passwords are encoded as a simple sequence of strings. Private keys and X509 credentials are
encoded as maps where "type" indicates the kind of data present in the map.

See the examples bellow for more information.


Example usage with pytest and monkeypatch
-----------------------------------------

.. code-block:: python

    from safeguard.sessions.plugin.credential_store import CredentialStore as CredStore
    from safeguard.sessions.plugin.plugin_configuration import PluginConfiguration as PluginConfig
    from safeguard.sessions.plugin_impl.credential_store import credential_stores

    def test_credential_store(monkeypatch):
        # Data injection
        testdb = {
            # This user has a password and a private key as well
            "user": {"host": [("password",), ({"type": "ssh-rsa", "key": "theKey"},)]},
        }
        monkeypatch.setitem(credential_stores, 'local', testdb)

        # Test the injected data
        pc = PluginConfig('''
        [credential_store]
        name=local
        ''')

        cs = CredStore.from_config(pc)

        assert cs.get_passwords('host', 'user') == ['password']

"""
from safeguard.sessions.plugin.credential_store_exceptions import LocalCredentialStoreNotFound
from .database import FakeDatabase
from .decryptor import FakeDecryptor


credential_stores = {}


def credential_store_parameters_factory(credential_store_name):
    if credential_store_name not in credential_stores:
        raise LocalCredentialStoreNotFound(credential_store_name)
    return FakeDatabase(credential_stores[credential_store_name]), FakeDecryptor()
