from click import ClickException

from config.config import Config


class VersionNotInstalledError(ClickException):
    def __init__(self, version=None):
        super().__init__(
            f"Version {version} is not installed."
            if version
            else "No Wake version is activated, use WAKE USE command first."
        )
        self.version = version


class InvalidSignature(ClickException):
    def __init__(self):
        super().__init__("Invalid signature")


class VerificationHashesMismatch(ClickException):
    def __init__(self, expected, actual):
        super().__init__(
            f"Verification hashes do not match: expected {expected}, got {actual}"
        )
        self.expected = expected
        self.actual = actual


class UnsupportedWakeVersion(ClickException):
    def __init__(self, version):
        super().__init__(f"ERROR: Payload and/or signature files failed verification!")
        self.version = version


class CondaUnpackError(ClickException):
    def __init__(self, code, err):
        super().__init__(f"conda-unpack failed with code {code}: {err}")
