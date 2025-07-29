#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
"""
.. py:module:: safeguard.sessions.plugin.box_configuration
    :synopsis: Provide access to SPS configuration model.
"""
from safeguard.sessions.plugin_impl.box_config import BoxConfig


def ensure_box_config(func):
    def wrapped_func(cls, *args, **kwargs):
        cls._ensure_box_config()
        return func(cls, *args, **kwargs)

    return wrapped_func


class BoxConfiguration:
    _box_config = None

    @classmethod
    def open(cls):
        return cls

    @classmethod
    def close(cls):
        if cls._box_config:
            cls._box_config.close()
            cls._box_config = None

    @classmethod
    @ensure_box_config
    def _query(cls, end_point):
        return cls._box_config.query(end_point)

    @classmethod
    @ensure_box_config
    def get_gateway_fqdn(cls):
        return cls._box_config.get_gateway_fqdn()

    @classmethod
    @ensure_box_config
    def get_starling_join_credential_string(cls):
        return cls._box_config.get_starling_join_credential_string()

    @classmethod
    @ensure_box_config
    def get_http_proxy(cls):
        return cls._box_config.get_http_proxy()

    @classmethod
    @ensure_box_config
    def get_trusted_ca_lists(cls):
        return cls._box_config.get_trusted_ca_lists()

    @classmethod
    def _ensure_box_config(cls):
        if not cls._box_config:
            cls._box_config = BoxConfig()

    @classmethod
    @ensure_box_config
    def _get_impl(cls):
        return cls._box_config
