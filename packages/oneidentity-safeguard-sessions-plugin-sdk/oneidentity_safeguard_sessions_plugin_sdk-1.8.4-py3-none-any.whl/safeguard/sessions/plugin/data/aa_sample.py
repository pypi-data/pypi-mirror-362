#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from copy import deepcopy


class GatewayAndTargetUserDiffer(RuntimeError):
    pass


scenarios = {}


def scenario(cls):
    scenarios[cls.__name__] = cls
    return cls


class Parameters(dict):
    description = ""

    def __init__(
        self,
        cookie=None,
        session_cookie=None,
        protocol=None,
        gateway_user=None,
        gateway_groups=None,
        gateway_domain=None,
        server_username=None,
        server_hostname=None,
        server_ip=None,
        server_port=None,
        server_domain=None,
        key_value_pairs=None,
    ):
        super().__init__(
            cookie=cookie if isinstance(cookie, dict) else {},
            session_cookie=session_cookie if isinstance(session_cookie, dict) else {},
            session_id="{}-example-1".format(protocol) if protocol else "example-1",
            connection_name="example",
            protocol=protocol,
            client_ip="1.2.3.4",
            client_port=12341,
            client_hostname="theclient.foo.bar",
            gateway_user=gateway_user,
            gateway_groups=gateway_groups,
            gateway_domain=gateway_domain,
            server_username=server_username,
            server_hostname=server_hostname,
            server_port=server_port,
            server_ip=server_ip,
            server_domain=server_domain,
            key_value_pairs=key_value_pairs if isinstance(key_value_pairs, dict) else {},
        )

    def __setitem__(self, key, value):
        if key in self:
            return super().__setitem__(key, value)
        else:
            raise KeyError("May not create new keys.")

    def __delitem__(self, key):
        raise NotImplementedError()

    @property
    def mfa_password(self):
        return self["key_value_pairs"].get("otp")

    @mfa_password.setter
    def mfa_password(self, value):
        self["key_value_pairs"]["otp"] = value

    @property
    def otp(self):
        return self.mfa_password

    @otp.setter
    def otp(self, value):
        self.mfa_password = value

    def answer_question(self, key, value):
        self["key_value_pairs"][key] = value

    def make_copy(self):
        return deepcopy(dict(self))


@scenario
class SshWithoutGatewayAuth(Parameters):
    description = "SSH session without priory gateway authentication"

    def __init__(self, server_username, gateway_user, **kwargs):
        if server_username != gateway_user:
            raise GatewayAndTargetUserDiffer()
        super().__init__(
            server_username=server_username if server_username else "gatewayuser",
            protocol="ssh",
            server_port=22,
            server_ip="5.6.7.8",
            **kwargs,
        )


@scenario
class SshWithGatewayAuth(Parameters):
    description = "SSH session with gateway authentication"

    def __init__(self, server_username, gateway_user, **kwargs):
        super().__init__(
            server_username=server_username if server_username else "targetuser",
            gateway_user=gateway_user if gateway_user else "gatewayuser",
            protocol="ssh",
            server_port=22,
            server_ip="5.6.7.8",
            **kwargs,
        )


@scenario
class RdpWithoutGatewayAuth(Parameters):
    description = "RDP session without gateway authentication"

    def __init__(self, gateway_user, **kwargs):
        super().__init__(protocol="rdp", **kwargs)
        self["key_value_pairs"]["username"] = gateway_user if gateway_user else "gatewayuser"


@scenario
class RdpWithGatewayAuth(Parameters):
    description = "RDP session with gateway authentication"

    def __init__(self, gateway_user, **kwargs):
        super().__init__(protocol="rdp", gateway_user=gateway_user if gateway_user else "gatewayuser", **kwargs)
