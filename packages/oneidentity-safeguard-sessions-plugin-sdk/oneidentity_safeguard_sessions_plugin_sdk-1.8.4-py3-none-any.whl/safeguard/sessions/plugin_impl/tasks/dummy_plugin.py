#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#

from safeguard.sessions.plugin import AAPlugin


class Plugin(AAPlugin):
    def __init__(self, configuration):
        super().__init__(configuration)

    def do_authenticate(self):
        return {"verdict": "ACCEPT"}

    def do_authorize(self):
        if not self.connection.key_value_pairs.get("response_key"):
            return {"verdict": "NEEDINFO", "question": ["response_key", "Do you authorize this connection? ", False]}
        return {"verdict": "ACCEPT"}
