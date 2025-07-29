#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#

import json
from enum import Enum
from safeguard.sessions.plugin_impl.test_utils.aa_plugin import (
    assert_verdict_is_valid_json,
    assert_verdict_outcome_is_valid,
    assert_needinfo_verdict,
)


class ScenarioStep(Enum):
    authentication = 1
    authorization = 2
    session_end = 3


class AAPluginTester:
    def __init__(self, plugin_cls, plugin_configuration, parameters):
        self.plugin_cls = plugin_cls
        self.plugin_configuration = plugin_configuration
        self.parameters = parameters

    @classmethod
    def run_scenario(cls, plugin_cls, plugin_configuration, scenario_params, server_username=None, gateway_user=None):
        tester = cls(
            plugin_cls,
            plugin_configuration,
            scenario_params(
                cookie={},
                session_cookie={},
                server_username=server_username,
                gateway_user=gateway_user,
                key_value_pairs={},
            ),
        )
        return tester.execute_steps(tester)

    @staticmethod
    def execute_steps(tester):
        auth_success = tester.execute_authenticate()
        if auth_success:
            tester.execute_authorize()
        tester.execute_session_end()

    def execute_authenticate(self):
        while True:
            verdict = self.plugin_cls(self.plugin_configuration).authenticate(
                **self._make_auth_parameters(self.parameters.make_copy()))
            final_verdict = self._assert_verdict_for("plugin authenticate", verdict)
            if final_verdict is not None:
                return final_verdict

    def execute_authorize(self):
        while True:
            verdict = self.plugin_cls(self.plugin_configuration).authorize(**self.parameters)
            final_verdict = self._assert_verdict_for("plugin authorize", verdict)
            if final_verdict is not None:
                return final_verdict

    def _handle_question(self, verdict):
        question = verdict["question"]
        answer = input(question[1])
        self.parameters["key_value_pairs"][question[0]] = answer

    def _assert_verdict_for(self, preamble, verdict):
        assert_verdict_is_valid_json(verdict, preamble)

        verdict = json.loads(json.dumps(verdict))
        self._handle_cookies(verdict)

        final_verdict = ("ACCEPT", "DENY")
        needinfo_verdict = ("NEEDINFO",)
        possible_verdicts = final_verdict + needinfo_verdict
        assert_verdict_outcome_is_valid(verdict, preamble, possible_verdicts)
        if verdict["verdict"] in final_verdict:
            print("{} finished with: {}".format(preamble, json.dumps(self.clean(verdict), sort_keys=True, indent=4)))
            return verdict["verdict"] == "ACCEPT"
        else:
            assert_needinfo_verdict(verdict, preamble)
            self._handle_question(verdict)

    def execute_session_end(self):
        preamble = "plugin session end"
        params = {k: v for k, v in self.parameters.items() if k in ["session_id", "cookie", "session_cookie"]}
        self.plugin_cls(self.plugin_configuration).session_ended(**params)
        print("{} finished".format(preamble))

    @classmethod
    def clean(cls, data):
        if isinstance(data, dict):
            return {k: cls.clean(v) for k, v in data.items() if "_" != k[0]}
        else:
            return data

    def _handle_cookies(self, verdict):
        if "cookie" in verdict:
            self.parameters["cookie"] = verdict["cookie"]
        if "session_cookie" in verdict:
            self.parameters["session_cookie"] = verdict["session_cookie"]

    @staticmethod
    def _make_auth_parameters(params):
        params.pop("gateway_groups", None)
        params.pop("server_hostname", None)
        params.pop("server_ip", None)
        params.pop("server_port", None)
        return params
