#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import json


def assert_plugin_hook_result(actual, expected):
    check_that_data_is_serializable(actual)
    for k, v in expected.items():
        if isinstance(v, dict):
            assert v.items() <= actual[k].items()
        else:
            assert v == actual[k]


def check_that_data_is_serializable(data):
    # it may happen that we try to return byte string or data containing circular reference
    json_dump = json.dumps(data)
    del json_dump


def update_cookies(params, verdict):
    params["cookie"] = json.loads(json.dumps(verdict["cookie"]))
    params["session_cookie"] = json.loads(json.dumps(verdict["session_cookie"]))


def minimal_parameters(params):
    return dict(cookie=params["cookie"], session_cookie=params["session_cookie"], session_id=params["session_id"])
