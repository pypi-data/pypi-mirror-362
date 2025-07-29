import binascii
import hashlib
import os
import platform
import re
import shutil
import subprocess
import tarfile
import urllib.request

import cryptography.exceptions
import packaging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.dsa import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from google.cloud import storage

from config.config import Config
from wake_versions.exceptions import (
    CondaUnpackError,
    InvalidSignature,
    UnsupportedWakeVersion,
    VerificationHashesMismatch,
    VersionNotInstalledError,
)


def get_wake_machine_info() -> str:
    curr_platform = platform.system().lower()
    arch = platform.machine().lower()

    if curr_platform not in ["windows", "darwin", "linux"]:
        raise RuntimeError(f"Invalid platform {curr_platform}")

    if curr_platform == "darwin":
        curr_platform = "macos"

    if arch == "arm64" or arch == "aarch64":
        arch = "arm64"
    elif arch.endswith("64"):
        arch = "x64"

    if curr_platform == "windows" and arch == "arm64":
        arch = "x64"

    return {"platform": curr_platform, "arch": arch}


class WakeFiles:
    def __init__(self):
        self.__VERSIONS_DIR = os.path.expanduser("~/.wake-arena/wake")

        if not os.path.exists(self.__VERSIONS_DIR):
            os.makedirs(self.__VERSIONS_DIR)

        info = get_wake_machine_info()

        self.platform = info["platform"]
        self.arch = info["arch"]

    def get_machine_postfix(self):
        return f"{self.platform}-{self.arch}"

    def get_version_name(self, version: str) -> str:
        return f"wake-{version}-{self.get_machine_postfix()}"

    def get_conda_archive(self, version: str) -> str:
        return f"{self.get_version_name(version)}.tar.gz"

    def get_archive_hash_signature(self, version: str) -> str:
        return f"{self.get_conda_archive(version)}.sha256.sig"

    def get_archive_hash(self, version: str) -> str:
        return f"{self.get_conda_archive(version)}.sha256"

    def download(self, url: str, file_name: str) -> str:
        urllib.request.urlretrieve(url, self.get_path(file_name))

    def delete(self, file_name: str) -> str:
        os.remove(self.get_path(file_name))

    def get_path(self, file_name: str) -> str:
        return os.path.join(self.__VERSIONS_DIR, file_name)

    def get_version_from_file(self, file: str) -> str:
        version = re.search(
            r"^(?:wake-)?(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$",
            file,
        )
        if not version:
            return None

        return re.sub(
            rf"-{self.get_machine_postfix()}\..*",
            "",
            version.string.replace("wake-", ""),
        )

    def list(self):
        versions = []
        for x in os.listdir(self.__VERSIONS_DIR):
            if x != self.__VERSIONS_DIR:
                versions.append(x)
        return versions


class WakeVersionManager:
    def __init__(self, config: Config) -> None:
        self.__BUCKET_NAME = "wake-conda"

        public_key_path = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "resources",
            "conda_public_key.pem",
        )

        with open(public_key_path, "rb") as f:
            self.public_key = load_pem_public_key(f.read(), default_backend())

        self.storage = storage.Client.create_anonymous_client()
        self.files = WakeFiles()
        self.config = config

        pass

    def get_storage_url(self, file: str) -> str:
        return (
            self.storage.bucket(self.__BUCKET_NAME)
            .blob(file)
            ._get_download_url(client=self.storage)
        )

    def get_activation_command(self, version: str):
        if self.files.platform == "windows":
            activate_command = (
                'set "PYTHONPATH=" && set "PYTHONHOME=" && set "PYTHONSTARTUP=" && set PYTHONNOUSERSITE=1 && "'
                + os.path.join(self.files.get_path(version), "Scripts", "activate.bat")
                + '"'
            )
            shell = "cmd.exe"
        else:
            activate_command = (
                'unset PYTHONPATH && unset PYTHONHOME && unset PYTHONSTARTUP && export PYTHONNOUSERSITE=1 && . "'
                + os.path.join(self.files.get_path(version), "bin", "activate")
                + '"'
            )
            shell = "/bin/bash"
        return activate_command, shell

    def install(self, version: str):
        file_name = self.files.get_conda_archive(version)
        self.files.download(self.get_storage_url(file_name), file_name)
        self.verify_archive(version, self.files.get_path(file_name))
        self.extract_archive(version, self.files.get_path(file_name))
        self.files.delete(file_name)
        self.conda_unpack(version)
        self.config.set_wake_version(version)
        self.config.write()

    def get_active(self) -> str | None:
        return self.config.get_wake_version()

    def deactivate(self):
        self.config.set_wake_version(None)
        self.config.write()

    def activate(self, version: str) -> str:
        if version not in self.list_local():
            raise VersionNotInstalledError(version)

        if packaging.version.parse(version) < Config.WAKE_MIN_VERSION:
            raise UnsupportedWakeVersion(version)

        self.config.set_wake_version(version)
        self.config.write()

    def shell(self, version) -> str:
        version = self.get_active() if not version else version
        if not version:
            raise VersionNotInstalledError()

        if version not in self.list_local():
            raise VersionNotInstalledError(version)

        activate_command, shell = self.get_activation_command(version)
        os.execl(
            shell,
            "bash",
            "-c",
            f'{activate_command} && conda-unpack && export PS1="wake-{version}: " && exec {shell}',
        )

    def uninstall(self, version: str) -> str:
        version_path = self.files.get_path(version)
        if os.path.exists(version_path):
            shutil.rmtree(version_path)
            if self.config.get_wake_version() == version:
                self.config.set_wake_version(None)
                self.config.write()
            return version
        else:
            return None

    def verify_archive(self, version: str, arch_file_name: str):
        hash_file_name = self.files.get_archive_hash(version)
        sig_file_name = self.files.get_archive_hash_signature(version)

        self.files.download(self.get_storage_url(hash_file_name), hash_file_name)
        self.files.download(self.get_storage_url(sig_file_name), sig_file_name)

        with (
            open(arch_file_name, "rb") as arch_file,
            open(self.files.get_path(hash_file_name), "rb") as hash_file,
            open(self.files.get_path(sig_file_name), "rb") as sig_file,
        ):
            archive = arch_file.read()
            sha_hash = hash_file.read()
            signature = sig_file.read()

        try:
            self.public_key.verify(
                signature,
                sha_hash,
                ec.ECDSA(hashes.SHA256()),
            )
        except cryptography.exceptions.InvalidSignature as e:
            raise InvalidSignature()

        expected_hash = binascii.unhexlify(sha_hash.decode("utf-8").split()[0])
        actual_hash = hashlib.sha256(archive).digest()

        if expected_hash != actual_hash:
            raise VerificationHashesMismatch(expected_hash, actual_hash)

        self.files.delete(hash_file_name)
        self.files.delete(sig_file_name)

    def extract_archive(self, version: str, arch_file_name: str):
        if os.path.exists(self.files.get_path(version)):
            shutil.rmtree(self.files.get_path(version))
        with tarfile.open(arch_file_name, "r:gz") as tar:
            tar.extractall(path=self.files.get_path(version))

    def conda_unpack(self, version: str):
        activate_command, shell = self.get_activation_command(version)
        process = subprocess.run(
            [shell, "-c", f"{activate_command} && conda-unpack"],
            capture_output=True,
            text=True,
        )

        if process.returncode != 0:
            raise CondaUnpackError(process.returncode, process.stderr)

    def uniq_versions(self, versions) -> list[str]:
        uniq_versions = list(filter(lambda x: x != None, list(set(versions))))
        uniq_versions.sort(reverse=True)
        return uniq_versions

    def list_local(self) -> list[str]:
        file_versions = [self.files.get_version_from_file(x) for x in self.files.list()]
        return self.uniq_versions(file_versions)

    def list_remote(self, version_prefix=""):
        search = self.files.get_conda_archive(f"{version_prefix}*")
        conda_files = self.storage.list_blobs(self.__BUCKET_NAME, match_glob=search)
        file_versions = [self.files.get_version_from_file(x.name) for x in conda_files]
        return self.uniq_versions(file_versions)

    def get_shell_version(self):
        try:
            result = subprocess.run(
                ["wake", "--version"], capture_output=True, text=True, check=True
            )
            wake_version = result.stdout.strip()
        except:
            wake_version = None
        return wake_version
