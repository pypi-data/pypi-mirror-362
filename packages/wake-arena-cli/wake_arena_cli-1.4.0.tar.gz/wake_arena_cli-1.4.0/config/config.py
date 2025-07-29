import copy
import os
from pathlib import Path
from typing import Optional as Opt

import yaml
from click import ClickException
from packaging import version
from schema import And, Optional, Schema, SchemaError, Use
from typing_extensions import Self


class ConfigError(ClickException):
    def __init__(self, message: str, errors):
        super().__init__(message)
        self.errors = errors


class Config:
    WAKE_MIN_VERSION = version.parse("4.14.0")

    def __init__(self):
        self.schema = Schema(
            Optional(
                {
                    "clients": {
                        Optional(str): {
                            "user": Optional(And(Use(str))),
                            "token": And(Use(str)),
                        }
                    },
                    "active": {
                        Optional("project"): And(Use(str)),
                        Optional("client"): And(Use(str)),
                    },
                    Optional("wake"): {
                        Optional("version"): And(Use(str)),
                    },
                }
            )
        )

        with open(self.__get_file(), "r") as file:
            config = yaml.safe_load(file)

        if not config:
            config = {"clients": {}, "active": {}}

        self.__validate(config)
        self.obj = config
        self.changes = copy.deepcopy(config)

    def __validate(self, config: dict):
        try:
            self.schema.validate(config)
        except SchemaError as err:
            raise ConfigError(
                "Invalid CLI configuration file in ~/.wake-arena/config.yaml", [err]
            )

    def __get_file(self):
        config_path = os.path.expanduser("~/.wake-arena/")
        config_file = config_path + "config.yaml"

        Path(config_path).mkdir(parents=True, exist_ok=True)
        Path(config_file).touch(exist_ok=True)

        return config_file

    def add_client(self, name: str, user: str, token: str) -> Self:
        client_config = {"user": user, "token": token}
        self.changes["clients"].update({name: client_config})
        return self

    def set_active_client(self, name: str) -> Self:
        self.changes["active"].update({"client": name})
        return self

    def set_active_project(self, slug: str) -> Self:
        self.changes["active"].update({"project": slug})
        return self

    def write(self) -> Self:
        self.__validate(self.changes)

        with open(self.__get_file(), "w") as file:
            yaml.safe_dump(self.changes, file)

        self.obj = copy.deepcopy(self.changes)
        return self

    def get_clients(self) -> dict:
        return self.obj.get("clients", {})

    def get_active(self) -> dict:
        return self.obj.get("active", {})

    def get_active_project(self) -> Opt[str]:
        return os.environ.get(
            "WAKE_ARENA_PROJECT", self.get_active().get("project", None)
        )

    def get_api_url(self) -> str:
        return os.environ.get(
            "WAKE_ARENA_API_URL",
            "https://wake-arena-project-api-jfyiuiqm6a-ey.a.run.app",
        )

    def get_web_url(self) -> str:
        return os.environ.get(
            "WAKE_ARENA_WEB_URL",
            "https://ackee.xyz/wake/arena",
        )

    def get_oauth_secret(self) -> str:
        return os.environ.get("WAKE_ARENA_OAUTH_SECRET", None)

    def get_active_client(self) -> Opt[dict]:
        api_key = os.environ.get("WAKE_ARENA_API_KEY", None)

        if api_key:
            return {"token": api_key}

        active = self.get_active()
        clients = self.get_clients()

        name = active.get("client", None)

        if not name:
            return None

        if name in clients:
            return clients.get(name)

        raise ConfigError("Invalid configuration")

    def set_wake_version(self, version: str | None) -> Self:
        self.changes.update({"wake": {"version": version}})
        return self

    def get_wake_version(self) -> Opt[str]:
        return self.obj.get("wake", {}).get("version", None)
