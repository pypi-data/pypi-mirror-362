#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import os
from collections import namedtuple


HttpProxySettings = namedtuple("HttpProxySettings", "server port username password")
_TRUSTED_CA_LISTS_LOCATION = "/etc/ssl/certs/trusted_ca_lists"


def extract_http_proxy_settings(response_body):
    proxy_enabled = response_body and response_body.get("enabled")
    authentication_enabled = proxy_enabled and response_body.get("authentication").get("selection") == "password"
    return HttpProxySettings(
        server=response_body.get("server").get("value") if proxy_enabled else None,
        port=response_body.get("port") if proxy_enabled else None,
        username=response_body.get("authentication").get("username") if authentication_enabled else None,
        password=response_body.get("authentication").get("password") if authentication_enabled else None,
    )


def extract_trusted_ca_lists(response_items):
    return {
        item.get("body").get("name"): _create_trusted_ca(item.get("body", {}), item.get("key"))
        for item in response_items
    }


def _create_trusted_ca(trusted_ca_list, reference_id):
    return dict(
        certs=[authority["certificate"]["pem"] for authority in trusted_ca_list["authorities"]],
        crls=[authority["crl"] for authority in trusted_ca_list["authorities"]],
        config=dict(
            strict_hostcheck=trusted_ca_list["strict_hostcheck"],
        ),
        name=trusted_ca_list["name"],
        type="x509v3-sign-rsa",
        location=os.path.join(_TRUSTED_CA_LISTS_LOCATION, reference_id),
    )
