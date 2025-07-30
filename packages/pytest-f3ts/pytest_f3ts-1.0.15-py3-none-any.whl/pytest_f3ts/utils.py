"""F3TS Plugin Utilities."""
import datetime
import logging
import pathlib
import ssl
import sys
from typing import Tuple, Union

import yaml
from websocket import WebSocketConnectionClosedException, create_connection

from . import schemas

logger = logging.getLogger(__name__)


def get_config_from_file(f3ts_config=None, slot_id=None):
    """Return a configuration object."""
    if f3ts_config:
        config_path = f3ts_config
    else:
        config_path = "config.yml"

    logger.info(f"config_path: {config_path}")
    with open(config_path) as f:
        config_dict = yaml.safe_load(f)
        config_obj = schemas.TestPlanConfig.parse_obj(config_dict)

    if slot_id:  # Parse into config for specified fixture:
        my_fixture_settings = schemas.FixtureSettings(slot_id=slot_id)
        for fixture_config in config_obj.fixture_settings.values():
            if slot_id == fixture_config.slot_id:
                my_fixture_settings = fixture_config

        f3ts_config_obj = schemas.PytestTestPlanConfig(
            test_name=config_obj.test_name,
            test_cases=config_obj.test_cases,
            runner_settings=config_obj.runner_settings,
            fixture_settings=my_fixture_settings,
        )
        logger.info(f"my test_plan_config: {f3ts_config_obj}")
        return f3ts_config_obj

    logger.info(f"my test_plan_config: {config_obj}")
    return config_obj


def get_settings_from_file(
    version: str, f3ts_config=None
) -> Tuple[schemas.LimitsCreate, schemas.GUISettings]:
    """Return particular settings for logging to database."""
    if f3ts_config:
        config_path = f3ts_config
    else:
        config_path = "config.yml"

    logger.info(f"config_path: {config_path}")
    with open(config_path) as f:
        config_dict = yaml.safe_load(f)
        runner_config_dict = config_dict.pop("runner_settings")
        config_dict["version"] = version
        limits_obj = schemas.LimitsCreate.parse_obj(config_dict)
        runner_config_obj = schemas.GUISettings.parse_obj(runner_config_dict)

    return limits_obj, runner_config_obj


def get_log_filename(
    test_name: str, sn: str, dirname: str, extension: str = "xml"
) -> str:
    """Return a log filename."""
    return str(
        pathlib.Path(dirname).joinpath(
            f"{test_name}"
            f"_{sn}"
            f"_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.{extension}"
        )
    )


def log_vars(record_property, recurse=1):
    """Log standard F3TS variables.

    Add the standard variables and expected configuration information to the
    JUnit-based XML test log. The following properties are recorded:

    - `test_id`: Test ID number
    - `error_code`: Error code for the test case
    - `error_msg`: Message to display when the test case fails
    - `min_limit`: Optional minimum limit
    - `max_limit`: Optional maximum limit
    - `description`: Optional test case description
    - `meas`: Value that is being measured and tested
    - `test_config`: F3TS fixture that provides test information from
       configuration files
        - The same values as listed above are logged.
    """
    caller = sys._getframe(recurse)
    if "test_config" in caller.f_locals.keys():
        for _k, _v in caller.f_locals["test_config"].dict().items():
            logger.info(f"PROPERTY: {_k} = {_v}")
            record_property(_k, _v)

    for k, v in caller.f_locals.items():
        if k in [
            "test_id",
            "error_code",
            "error_msg",
            "min_limit",
            "max_limit",
            "description",
            "meas",
        ]:
            logger.info(f"PROPERTY: {k} = {v}")
            record_property(k, v)


class UserDialog:
    """User Dialog Interface

    Object for sending user input prompts or popup messages either
    to the GUI or the serial terminal for pytest only configuration
    """

    def __init__(self, api):
        self.api = api
        self.websocket = None

        if self.api is None:
            print(
                "WARNING: Not connected to backend API, "
                "sending all user dialog prompts to terminal. "
                "Make sure pytest stdin is enabled using -s"
            )
        else:
            self.default_timeout = 2
            self.retries = self.api.retries
            self.api_url = self.api.api_url
            self.frontend_client_id = self.api.frontend_client_id
            self.backend_client_id = self.api.backend_client_id

            self.websocket_connect()

    def websocket_connect(self):
        """Setup websocket connection to frontend."""
        attempt = 0
        while True:
            try:
                websocket_url_head = self.api_url.replace("http://", "ws://").replace(
                    "https://", "wss://"
                )
                self.websocket_url = (
                    f"{websocket_url_head}/utils/runner_socket/"
                    f"{self.backend_client_id}"
                )

                # Define SSL options for the WebSocket connection
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
                sslopt = {
                    "cert_reqs": ssl.CERT_NONE,
                    "check_hostname": False,
                    "ssl_context": ssl_context,
                }

                self.websocket = create_connection(
                    self.websocket_url, timeout=self.default_timeout, sslopt=sslopt
                )

                message = schemas.SocketMsg(
                    type="connect",
                    toClient=self.frontend_client_id,
                    fromClient=self.backend_client_id,
                )

                self.websocket.send(message.json())

                waiting = True
                while waiting:
                    response = self.websocket.recv()
                    response = schemas.SocketMsg.parse_raw(response)
                    if response.fromClient == self.frontend_client_id:
                        waiting = False

                return True

            except Exception:
                if attempt >= self.retries:
                    raise
                else:
                    attempt += 1

    def send_user_dialog(self, dialog: schemas.Dialog, timeout: int = 3600):
        """Send two-way user dialog message to the Backend."""

        self.websocket.close()
        self.websocket_connect()
        self.websocket.settimeout(timeout)

        message = schemas.SocketMsg(
            type="dialog",
            toClient=self.frontend_client_id,
            fromClient=self.backend_client_id,
            data=dialog,
        )

        # Generic error handling for any connection issues
        tries = 0
        while tries <= 1:
            try:
                self.websocket.send(message.json())

                # Wait until dialog response from connected frontent client
                while True:
                    response = self.websocket.recv()

                    response = schemas.SocketMsg.parse_raw(response)
                    if response.fromClient == self.frontend_client_id:
                        break

                    if not self.websocket.connected:
                        raise WebSocketConnectionClosedException()

                break
            except:
                self.close()
                self.websocket_connect()
                self.websocket.settimeout(timeout)

                tries += 1

        self.websocket.settimeout(self.default_timeout)
        if response:
            return schemas.DialogResponse.parse_obj(response.data)

    def send(
        self, message: schemas.Dialog, blocking: bool = True
    ) -> Union[schemas.DialogResponse, bool]:
        """Send Custom User Dialog to the GUI or terminal"""

        if self.api is None:
            response = self.send_terminal(message, blocking=blocking)

        else:
            if blocking:
                response = self.send_user_dialog(message)
            else:
                self.api.send_user_notif(message)
                return True

        return response

    def send_terminal(
        self, message: schemas.Dialog, blocking: bool = True
    ) -> schemas.DialogResponse:
        """Send Custom User Dialog to the pytest terminal

        Requires -s option to be enabled to allow stdin
        """

        response = schemas.DialogResponse()

        default_text = ""
        if message.defaultText:
            default_text = f"(ex/ {message.defaultText}\n"

        if message.inputType == "text":
            response.inputText = input(
                f"\n\n{message.title}\n{message.message}\n{default_text}--> "
            )
            response.okClicked = True
            response.cancelClicked = False

        elif blocking:
            print(f"\n\n{message.title}\n{message.message}\n{default_text}")

            ok = input(
                f"{message.okButtonText}? (y) " f"{message.cancelButtonText}? (n)\n--> "
            )
            if ok == "y":
                response.okClicked = True
                response.cancelClicked = False
            elif ok == "n":
                response.okClicked = False
                response.cancelClicked = True
            else:
                raise ValueError(f"{ok} is not a valid input.")

        else:
            print(f"\n\n{message.title}\n{message.message}\n{default_text}")

        return response

    def close(self):
        if self.websocket:
            self.websocket.close()


class StatusBanner:
    """Application Custom Status Interface

    Object for overriding the status banner in the application frontend
    """

    def __init__(self, api):
        self.api = api
        if self.api is None:
            print(
                "WARNING: Not connected to backend API, " "not updating status banner"
            )

    def override(self, override, status=None, color=None):
        if self.api is not None:
            if override:
                banner = schemas.StatusBanner(status=status, color=color)
            else:
                banner = None

            return self.api.send_banner_update(banner)

        elif override:
            print("STATUS: ", status)

        return False


class SerialNumber:
    """
    Object for setting and updating the status number in the
    application frontend
    """

    def __init__(self, api):
        self.api = api
        self.serial_number = ""
        if self.api is None:
            print(
                "WARNING: Not connected to backend API, " "not updating status banner"
            )

    def set(self, serial):
        self.serial_number = serial

        if self.api is not None:
            return self.api.send_serial_number(self.serial_number)

        return False
