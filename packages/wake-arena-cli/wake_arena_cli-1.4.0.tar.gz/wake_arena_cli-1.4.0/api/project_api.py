import os
import urllib
from logging import Logger
from typing import Optional

import requests
from click import ClickException


class ProjectApiError(ClickException):
    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


class ProjectApi:
    __CLIENT_CREDENTIALS = {
        "client_id": "client-device-cli",
        "client_secret": "cApysib58~8LiWhmmREQP35r1z#17#fr!vxgD-noaJN@3T25f3JPYuclFZbiyscw",
    }

    def __init__(
        self,
        logger: Logger,
        server_url: str,
        token: str = None,
        oauth_client_id: str = None,
        oauth_client_secret: str = None,
    ):
        self.logger = logger
        self.token = token
        self.server_url = server_url
        self.oauth_client_id = (
            oauth_client_id
            if oauth_client_id
            else self.__CLIENT_CREDENTIALS["client_id"]
        )
        self.oauth_client_secret = (
            oauth_client_secret
            if oauth_client_secret
            else self.__CLIENT_CREDENTIALS["client_secret"]
        )
        self.headers = {}
        if token is not None:
            self.headers["Authorization"] = f"Bearer {token}"

    def __check_response(self, res: requests.Response):
        isJson = res.headers.get("content-type").startswith("application/json")
        body = res.json() if isJson else res.text

        if res.status_code != 200:
            code = body.get("code") if isJson else res.status_code

            self.logger.error(f"Wake Arena API error: {res.status_code}")
            if code:
                self.logger.error(f"{code}")

            raise ProjectApiError(f"Wake Arena API error: {res.status_code}", code)

        return body

    def create_project(self, project_name: str):
        body = {"name": project_name}
        res = requests.post(
            self.server_url + "/api/v0/projects", json=body, headers=self.headers
        )
        return self.__check_response(res)

    def get_project(self, project_id: str):
        res = requests.get(
            self.server_url + f"/api/v0/projects/{project_id}", headers=self.headers
        )
        return self.__check_response(res)

    def list_projects(self):
        res = requests.get(self.server_url + "/api/v0/projects", headers=self.headers)
        return self.__check_response(res)

    def get_upload_link(
        self, project_id: str, name: str | None, format: str, wake_version: str
    ):
        body = (
            {"name": name, "format": format, "wakeVersion": wake_version}
            if name
            else {"format": format, "wakeVersion": wake_version}
        )

        res = requests.post(
            self.server_url + f"/api/v0/projects/{project_id}/code-upload",
            json=body,
            headers=self.headers,
        )
        return self.__check_response(res)

    def get_vulnerability_check(self, project_id: str, check_id: str):
        return self.__check_response(
            requests.get(
                self.server_url + f"/api/v0/projects/{project_id}/checks/{check_id}",
                headers=self.headers,
            )
        )

    def get_vulnerability_check_state_logs(
        self, project_id: str, check_id: str, last_seen_time: Optional[str] = None
    ):
        url = self.server_url + f"/api/v0/projects/{project_id}/checks/{check_id}/logs"

        if last_seen_time:
            url += "?" + urllib.parse.urlencode({"lastSeenTime": last_seen_time})

        return self.__check_response(requests.get(url, headers=self.headers))

    def get_device_code(self, name: str):
        return self.__check_response(
            requests.post(
                self.server_url + "/api/v0/oauth/devices/code",
                json={
                    "clientId": self.__CLIENT_CREDENTIALS["client_id"],
                    "clientSecret": self.__CLIENT_CREDENTIALS["client_secret"],
                    "name": name,
                },
            )
        )

    def generate_api_token(
        self,
        device_code: str,
    ):
        return self.__check_response(
            requests.post(
                self.server_url + "/api/v0/oauth/devices/token",
                json={"deviceCode": device_code},
            )
        )

    def get_user_profile(self):
        return self.__check_response(
            requests.get(self.server_url + "/api/v0/profile", headers=self.headers)
        )
