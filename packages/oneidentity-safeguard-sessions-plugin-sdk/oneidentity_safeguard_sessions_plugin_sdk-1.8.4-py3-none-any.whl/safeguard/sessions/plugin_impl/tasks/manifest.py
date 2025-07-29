#
# Copyright 2025 One Identity LLC.
# ALL RIGHTS RESERVED.
#

"""
DISCLAMER
The files: scb/plugin-sdk/src/safeguard/sessions/plugin_fakes/tasks/manifest.py
and scb/nnx-scb/scb/plugins/manifest.py
must be identical.

Please if you modify one of them copy your changes to the other.

The unit tests of both files are located at:
scb/plugin-sdk/src/safeguard/sessions/plugin_fakes/tasks/tests/unit/test_manifest.py
"""

from time import strftime
import re
import semantic_version
import yaml
from yaml.error import YAMLError


class Manifest:
    KNOWN_PLUGIN_TYPES = ("aa", "configuration_sync", "credentialstore", "signingca")

    def __init__(self, data, filename, compatible=False):
        self.data = data
        self.parsed = {}
        self.filename = filename
        if compatible:
            self._check(fields=("name", "api", "version", "type"))
        else:
            self._check()

    @classmethod
    def from_file(cls, filename="MANIFEST"):
        try:
            with open(filename) as f:
                return cls.from_stream(f, filename)
        except FileNotFoundError:
            raise FileNotFoundError(
                "MANIFEST file not found, are we in a plugin folder?"
            )

    @classmethod
    def compatible_from_file(cls, filename="MANIFEST"):
        try:
            with open(filename) as f:
                return cls.from_stream(f, filename, compatible=True)
        except FileNotFoundError:
            raise FileNotFoundError("MANIFEST file not found in the Zip")

    @classmethod
    def from_stream(cls, stream, filename=None, compatible=False):
        try:
            return cls(yaml.safe_load(stream), filename, compatible)
        except YAMLError:
            raise FileFormatError("MANIFEST file format wrong, should be yaml")

    def _check(
        self,
        expected_type=None,
        fields=("name", "api", "version", "description", "entry_point", "type"),
    ):
        expected_type = expected_type or self.KNOWN_PLUGIN_TYPES
        for field in fields:
            if field not in self.data:
                raise RequiredFieldDoesNotExistError(
                    "MANIFEST '{}' is missing".format(field)
                )
            if self.data[field] is None:
                raise RequiredFieldIsEmptyError("MANIFEST '{}' is empty".format(field))
        if self.data["type"] not in expected_type:
            raise PluginTypeError(
                "{} not in {}".format(self.data["type"], expected_type)
            )
        if not re.fullmatch("[a-zA-Z][a-zA-Z0-9_]+", self.name):
            raise NameFormatError(
                "MANIFEST name should start with letter and continue with letter, digit or underscore"
            )
        if self.entry_point and not re.fullmatch("[A-Za-z0-9._-]+", self.entry_point):
            raise EntryPointFormatError(
                "MANIFEST entry point should only contain letters, digits, dot, dash or underscore"
            )
        if re.fullmatch("[0-9].*", str(self.version)):
            self.data["version"] = str(self.version)  # 0.9 would be float type
        else:
            raise VersionFormatError("MANIFEST version should start with a digit")

        # ignore maintenance version and make sure the format is x.y.z
        api_version = re.sub(r"^(\d+)\.(\d+)(\.\d+)?$", r"\1.\2.0", str(self.data["api"]))

        try:
            self.parsed["api"] = semantic_version.Version(api_version)

        except ValueError:
            raise ApiVersionError(
                (
                    "The value of the attribute 'api' can not be parsed as valid semantic version "
                    "The valid format should be: x.y.z where z is optional"
                )
            )

        if self.author_email:
            self._validate_author_email(self.author_email)

    def check_api_version(self, plugin_sdk_version):
        api_v = self.parsed["api"]
        sdk_v = semantic_version.Version(plugin_sdk_version)

        # maintenance version is ignored, replaced with zero
        if not api_v <= sdk_v:
            raise ApiVersionError(
                "MANIFEST api version may not be larger than Plugin SDK version"
            )
        if not api_v.major == sdk_v.major:
            raise ApiVersionError(
                "MANIFEST api major version must equal Plugin SDK major version"
            )

    @property
    def api(self):
        return self.data["api"]

    @property
    def entry_point(self):
        return self.data.get("entry_point")

    @property
    def name(self):
        return self.data["name"]

    @property
    def type(self):
        return self.data["type"]

    @property
    def version(self):
        return self.data["version"]

    @property
    def description(self):
        return self.data.get("description", "")

    @property
    def scb_min_version(self):
        return self.data.get("scb_min_version")

    @property
    def scb_max_version(self):
        return self.data.get("scb_max_version")

    @property
    def author_name(self):
        return self.data.get("author_name")

    @property
    def author_email(self):
        return self.data.get("author_email")

    def make_snapshot_version(self):
        self.data["version"] = self.data["version"] + "-" + strftime("%Y%m%dT%H%M%S")

    def add_version_suffix(self, suffix):
        self.data["version"] = self.data["version"] + "-" + suffix.lstrip("-")

    def write_file(self):
        assert self.filename is not None
        with open(self.filename, "w") as f:
            yaml.dump(self.data, f, default_flow_style=False)

    @staticmethod
    def _validate_author_email(email):
        email_pattern = r"([-+_.a-zA-Z0-9]+@[-_a-zA-Z0-9]+(\.[-_a-zA-Z0-9]+)*)?"
        if not re.fullmatch(email_pattern, email):
            raise EmailAddressFormatError("The given author email address is not valid")


class FileFormatError(AssertionError):
    pass


class RequiredFieldDoesNotExistError(AssertionError):
    pass


class RequiredFieldIsEmptyError(AssertionError):
    pass


class PluginTypeError(AssertionError):
    pass


class ApiVersionError(AssertionError):
    pass


class NameFormatError(AssertionError):
    pass


class EntryPointFormatError(AssertionError):
    pass


class VersionFormatError(AssertionError):
    pass


class EmailAddressFormatError(AssertionError):
    pass
