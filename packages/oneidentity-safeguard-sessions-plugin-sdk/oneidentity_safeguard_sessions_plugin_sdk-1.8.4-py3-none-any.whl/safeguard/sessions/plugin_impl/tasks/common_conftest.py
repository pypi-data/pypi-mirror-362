#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
from configparser import ConfigParser
import os
import pytest
from vcr.request import Request


SITE_PARAMETER_FILENAMES = ("site_parameters.ini", "site_parameters_custom.ini")


@pytest.fixture
def interactive(request):
    backend_service = request.config.getoption("backend_service")

    class InteractiveServices(object):
        def message(self, msg, *args):
            if backend_service == "replay":
                return

            self._print_msg(msg, *args)

        def askforinput(self, msg, *args):
            input_request = Request(method="GET", uri="http://keyboard/{}".format(msg), body="", headers={})

            if backend_service == "replay":
                cassette = request.getfixturevalue("vcr_cassette")
                return cassette.play_response(input_request)["body"]

            self._print_msg(msg, *args)
            self._fd_output("> ")
            user_input = self._fd_input()

            if backend_service == "record":
                cassette = request.getfixturevalue("vcr_cassette")
                response = {"body": user_input, "status": {"code": 200, "message": "OK"}}
                cassette.append(input_request, response)

            return user_input

        def _print_msg(self, msg, *args):
            self._fd_output("\n{}\n# {}\n{}\n".format(80 * "*", msg % args, 80 * "*"))

        def _fd_output(self, msg):
            with os.fdopen(os.dup(1), "w") as stdout:
                stdout.write(msg)

        def _fd_input(self):
            with os.fdopen(os.dup(0), "r") as stdin:
                return stdin.readline().rstrip()

    return InteractiveServices()


@pytest.fixture(autouse=True)
def fake_backend(request):

    backend_service = request.config.getoption("backend_service")
    if backend_service == "replay":
        request.config.option.vcr_record = "none"
        request.config.option.vcr_record_mode = "none"
        request.getfixturevalue("vcr_cassette")
    elif backend_service == "record":
        request.config.option.vcr_record = "all"
        request.config.option.vcr_record_mode = "all"
        cassette = request.getfixturevalue("vcr_cassette")
        cassette.data = []
    elif backend_service != "use":
        # recording mode default is 'once'
        raise ValueError()


def pytest_addoption(parser):
    parser.addoption(
        "--backend-service",
        action="store",
        default="replay",
        choices=["record", "replay", "use"],
        help="How to behave wrt the external service: record, replay or use",
    )


@pytest.fixture
def site_parameters(request):
    cp = ConfigParser()
    assert cp.read([os.path.join(os.path.dirname(request.fspath), filename) for filename in SITE_PARAMETER_FILENAMES])
    yield dict(cp.items("site"))
