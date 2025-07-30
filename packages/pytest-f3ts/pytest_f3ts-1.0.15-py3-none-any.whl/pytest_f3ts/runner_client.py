"""Test Runner API Client."""
import os

import requests
from fastapi import HTTPException
from requests import JSONDecodeError
from tenacity import retry, stop_after_attempt

from . import schemas


class F3TSBackendAPI:
    """F3TS Backend Webservice API.

    API Client for communicating with the FixturFab Test Runner Backend. This
    class is used to send test results and other information to the Backend.

    TODO: Implement API Key Authentication
    """

    def __init__(
        self,
        api_url: str = "https://backend:8888/api/v1",
        slot_id: str = "1",
        run_id: int = None,
        plan_id: int = None,
        frontend_client_id: str = "frontend",
        retries=3,
    ):
        """Initialize the F3TS Backend API.

        Store the API URL and number of request retries. A request will be
        retried for the provided number of retries. If it continues to fail,
        an exception will be raised.
        """
        self.api_url = api_url
        self.run_id = run_id
        self.plan_id = plan_id
        self.slot_id = slot_id
        self.frontend_client_id = frontend_client_id
        self.frontend_group_id = "frontend_" + self.slot_id
        self.retries = retries
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        # self.access_token = self.authenticate(username, password)
        self.operator_id = None

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        if run_id:
            self.backend_client_id = str(run_id)
            self.operator_id = self.get_operator_id()

        else:
            self.backend_client_id = "prestart"

    # def authenticate(self, username, password):
    #     data = {"username": username, "password": password}
    #     response = requests.post(
    #         f"{self.api_url}/login/access-token", headers=self.headers, data=data
    #     )
    #     if response.status_code == 200:
    #         access_token = schemas.Token.parse_obj(response.json()).access_token
    #         return access_token
    #     else:
    #         raise HTTPException(
    #             response.status_code, "Unable to authenticate login credentials."
    #         )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def get_config(self, slot_id=None):
        """Return a configuration object."""

        response = requests.get(
            f"{self.api_url}/plans/{self.plan_id}",
            headers=self.headers,
            verify=False,
        )

        if response.status_code == 200:
            plan = schemas.Plan.parse_obj(response.json())

            if slot_id:  # Parse into config for specified fixture:
                my_fixture_settings = schemas.FixtureSettings(slot_id=slot_id)
                for fixture_config in plan.fixture_settings.values():
                    if slot_id == fixture_config.slot_id:
                        my_fixture_settings = fixture_config

                f3ts_config_obj = schemas.PytestTestPlanConfig(
                    test_name=plan.name,
                    test_cases=plan.limits_settings.test_cases,
                    runner_settings=plan.runner_settings,
                    fixture_settings=my_fixture_settings,
                )

            else:
                f3ts_config_obj = schemas.TestPlanConfig(
                    test_name=plan.name,
                    test_cases=plan.limits_settings.test_cases,
                    runner_settings=plan.runner_settings,
                    fixture_settings=plan.fixture_settings,
                )

            return f3ts_config_obj

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to read test plan in backend: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def get_operator_id(self):
        """Get operator id from run information stored in database"""
        response = requests.get(
            f"{self.api_url}/runs/{self.run_id}",
            headers=self.headers,
            verify=False,
        )

        if response.status_code == 200:
            run = schemas.Run.parse_obj(response.json())
            self.operator_id = run.operator_id
            return run.operator_id

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to update test run in backend: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def update_run_data(self, run: schemas.RunUpdate):
        """Update run data with run specific information

        Add information such as log filename, serial number, etc.
        """
        response = requests.post(
            f"{self.api_url}/runs/{self.run_id}",
            data=run.json(exclude_unset=True),
            headers=self.headers,
            verify=False,
        )

        if response.status_code == 200:
            return True

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to update test run in backend: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def save_logfile(self, attachment: schemas.AttachmentCreate):
        """Save logfile from local shared directory."""
        response = requests.post(
            f"{self.api_url}/runs/{self.run_id}/attachment/",
            params={"run_id": self.run_id},
            data=attachment.json(exclude_unset=True),
            headers=self.headers,
            verify=False,
        )

        if response.status_code == 200:
            return True

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to save log file for run: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def upload_logfile(self, attachment: schemas.AttachmentCreate):
        """Upload logfile over request."""

        response = requests.post(
            f"{self.api_url}/runs/{self.run_id}/attachment/upload",
            params={
                "run_id": self.run_id,
                "outfile_dir": os.path.dirname(attachment.filepath),
            },
            files={"file": open(attachment.filepath, "rb")},
            headers={"accept": "application/json"},
            verify=False,
        )

        if response.status_code == 200:
            return True

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to upload log file to run: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def send_websocket_msg(self, message: schemas.SocketMsg):
        """Send a `pytest` test case result to the Backend."""
        response = requests.post(
            f"{self.api_url}/utils/runner_socket/send",
            data=message.json(),
            headers=self.headers,
            verify=False,
        )

        if response.status_code == 200:
            return True

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to send websocket msg to frontend: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def send_test_result(self, result: schemas.ResultCreate):
        """Send a `pytest` test case result to the Backend."""
        # Send via websocket to frontend
        message = schemas.SocketMsg(
            type="result",
            toClient=self.frontend_group_id,
            fromClient=self.backend_client_id,
            data=result,
        )

        self.send_websocket_msg(message)

        response = requests.post(
            f"{self.api_url}/runs/{self.run_id}/result/",
            data=result.json(),
            headers=self.headers,
            verify=False,
        )

        if response.status_code == 200:
            return True

        try:
            data = response.json()
        except JSONDecodeError:
            data = response.text

        raise HTTPException(
            response.status_code,
            f"Unable to send test result to backend: {data}",
        )

    @retry(reraise=True, stop=stop_after_attempt(3))
    def send_user_notif(self, notif: schemas.Notif):
        """Send one-way user dialog message to the Backend."""

        message = schemas.SocketMsg(
            type="notif",
            toClient=self.frontend_group_id,
            fromClient=self.backend_client_id,
            data=notif,
        )

        self.send_websocket_msg(message)

    @retry(reraise=True, stop=stop_after_attempt(3))
    def send_banner_update(self, banner: schemas.StatusBanner):
        """Send set banner message to the Backend."""

        message = schemas.SocketMsg(
            type="banner",
            toClient=self.frontend_group_id,
            fromClient=self.backend_client_id,
            data=banner,
        )

        self.send_websocket_msg(message)

    @retry(reraise=True, stop=stop_after_attempt(3))
    def send_serial_number(self, serial_number):
        """Send serial number to the Backend."""

        run = schemas.RunUpdate(serial_number=serial_number)
        self.update_run_data(run)

        message = schemas.SocketMsg(
            type="serial",
            toClient=self.frontend_group_id,
            fromClient=self.backend_client_id,
            data={"serial_number": serial_number},
        )

        self.send_websocket_msg(message)


class F3TSASCIIAPI:
    """F3TS Backend Webservice API.

    API Client for communicating with the FixturFab Test Runner Backend. This
    class is used to send test results and other information to the Backend.

    TODO: Implement API Key Authentication
    """

    def __init__(
        self,
        config_data: dict = {},
        slot_id: str = "1",
    ):
        """Initialize the F3TS ASCII API.

        Store the API URL and number of request retries. A request will be
        retried for the provided number of retries. If it continues to fail,
        an exception will be raised.
        """
        self.api_url = None
        self.slot_id = slot_id
        self.operator_id = 0
        self.run_id = 0
        self.config_data = config_data
        self.config_data["attachments"] = []
        self.config_data["results"] = []
        self.config_data["notifs"] = []

    # def authenticate(self, username, password):
    #     data = {"username": username, "password": password}
    #     response = requests.post(
    #         f"{self.api_url}/login/access-token", headers=self.headers, data=data
    #     )
    #     if response.status_code == 200:
    #         access_token = schemas.Token.parse_obj(response.json()).access_token
    #         return access_token
    #     else:
    #         raise HTTPException(
    #             response.status_code, "Unable to authenticate login credentials."
    #         )

    def get_config(self, slot_id=None):
        """Return a configuration object."""
        self.slot_id = slot_id

    def update_run_data(self, run: schemas.RunUpdate):
        """Update run data with run specific information

        Add information such as log filename, serial number, etc.
        """
        self.config_data["run"] = run

    def upload_logfile(self, attachment: schemas.AttachmentCreate):
        """Upload logfile."""
        self.config_data["attachments"] += [attachment]

    def send_test_result(self, result: schemas.ResultCreate):
        """Send a `pytest` test case result to the Backend."""
        self.config_data["results"] += [result]

    def send_user_notif(self, notif: schemas.Notif):
        """Send one-way user dialog message to the Backend."""
        self.config_data["notifs"] += [notif]

    def send_banner_update(self, banner: schemas.StatusBanner):
        """Send set banner message to the Backend."""
        self.config_data["banner"] = banner

    def send_serial_number(self, serial_number):
        """Send serial number to the Backend."""
        self.config_data["serial_number"] = serial_number
