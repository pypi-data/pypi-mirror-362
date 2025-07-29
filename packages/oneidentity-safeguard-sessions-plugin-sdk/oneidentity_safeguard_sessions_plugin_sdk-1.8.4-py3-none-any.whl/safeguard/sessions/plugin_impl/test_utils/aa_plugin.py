#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#

import json


def assert_verdict_is_valid_json(verdict, preamble):
    assert verdict is not None, "{} should return a value".format(preamble)
    assert isinstance(verdict, dict), "{} should return a dict".format(preamble)
    assert json.dumps(verdict) is not None, "{} result must be possible to encode into JSON".format(preamble)


def assert_verdict_outcome_is_valid(verdict, preamble, possible_verdicts):
    assert "verdict" in verdict, "{} result must contain the 'verdict' key".format(preamble)
    assert verdict["verdict"] in possible_verdicts, "{} result must be one of {}".format(preamble, possible_verdicts)


def assert_needinfo_verdict(verdict, preamble):
    assert verdict["verdict"] == "NEEDINFO"
    assert "question" in verdict, "{} needinfo verdict must contain the 'question' key".format(preamble)
    question = verdict["question"]
    assert isinstance(question, list), "{} needinfo question should be a list".format(preamble)
    assert len(question) == 3, "{} needinfo question should have 3 items".format(preamble)
    assert isinstance(question[0], str), "{} needinfo question 1st item should be key string".format(preamble)
    assert isinstance(question[1], str), "{} needinfo question 2nd item should be prompt string".format(preamble)
    assert isinstance(question[2], bool), "{} needinfo question 3rd item should be disble_echo boolean".format(preamble)
