#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import hashlib
import os
import shutil
from OpenSSL import crypto

from safeguard.sessions.plugin.box_configuration_settings import extract_http_proxy_settings


stable_box_configuration = {
    "gateway_fqdn": None,
    "starling_join_credential_string": None,
    "http_proxy": None,
    "trusted_ca_lists": None,
    "trusted_ca_lists_location": "/tmp/trusted_ca_lists",
}
unstable_box_configuration = {}


class BoxConfig:
    @classmethod
    def query(cls, end_point):
        keys = [item for item in end_point.split("/") if item]
        return cls._get_value(unstable_box_configuration, keys)

    @classmethod
    def _get_value(cls, model, keys):
        try:
            return cls._get_value(model[keys[0]], keys[1:]) if keys else model
        except KeyError:
            return {
                "error": {
                    "details": {"mount_point": "/", "resource": keys[0]},
                    "message": "Resource was not found",
                    "type": "ResourceNotFound",
                }
            }

    @classmethod
    def get_gateway_fqdn(cls):
        return stable_box_configuration["gateway_fqdn"]

    @classmethod
    def get_starling_join_credential_string(cls):
        return stable_box_configuration["starling_join_credential_string"]

    @classmethod
    def get_http_proxy(cls):
        response_body = stable_box_configuration["http_proxy"]
        return extract_http_proxy_settings(response_body)

    @classmethod
    def get_trusted_ca_lists(cls):
        _update_with_location()
        return stable_box_configuration["trusted_ca_lists"]

    @classmethod
    def close(cls):
        pass


def _update_with_location():
    base_dir = stable_box_configuration["trusted_ca_lists_location"]
    shutil.rmtree(base_dir, ignore_errors=True)
    os.mkdir(base_dir)

    for ca_list_name, ca_list in stable_box_configuration["trusted_ca_lists"].items():
        ca_folder = os.path.join(base_dir, hashlib.sha256(ca_list_name.encode()).hexdigest())
        os.mkdir(ca_folder)

        for ca in ca_list["certs"]:
            file_name = _calculate_file_name(ca)
            with open(os.path.join(ca_folder, file_name), "w") as _file:
                _file.write(ca)
        ca_list["location"] = os.path.join(base_dir, ca_folder)


def _calculate_file_name(ca_pem):
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, ca_pem)
    return "{:08x}.0".format(x509.subject_name_hash())
