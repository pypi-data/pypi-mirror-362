#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#
import re


def plugin_sdk_installed(pip_requirements):
    pattern = r"^oneidentity[_-]safeguard[_-]sessions[_-]plugin[_-]sdk"
    return re.search(pattern, pip_requirements, re.MULTILINE) is not None
