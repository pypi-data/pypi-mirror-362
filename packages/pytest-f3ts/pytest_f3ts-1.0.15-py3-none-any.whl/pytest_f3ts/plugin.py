"""Main Pytest Plugin Scaffolding."""
import logging
import os
import time

from pytest_f3ts import schemas
from pytest_f3ts.runner_client import F3TSASCIIAPI, F3TSBackendAPI

logger = logging.getLogger(__name__)


def safe_format(value, default=" ", width=15):
    """Return a formatted string or a default value if None."""
    if value is None:
        value = default
    value = str(value)

    if len(value) > width:
        value = value[: width - 3] + "..."

    return f"{value:<{width}}"


def pytest_addoption(parser):
    """Add F3TS Plugin related options."""
    group = parser.getgroup("f3ts", "f3ts test plugin")

    group.addoption(
        "--test_name",
        action="store",
        help="Test name, used for creating the log filename",
    )
    group.addoption(
        "--run_id",
        action="store",
        default="DEV",
        help="Database Run ID to send results to",
    )
    group.addoption(
        "--plan_id",
        action="store",
        default="DEV",
        help="Database Plan ID to grab configuration information from",
    )
    group.addoption(
        "--slot_id",
        action="store",
        default="1",
        help="Slot ID of fixture that ran the test",
    )
    group.addoption(
        "--frontend_client_id",
        action="store",
        default="backend",
        help="Runner websocket client ID to connect to",
    )
    group.addoption(
        "--serial_number",
        action="store",
        help="Serial Number of the device being tested",
    )
    group.addoption(
        "--f3ts_config",
        action="store",
        default="config.yml",
        help="F3TS Configuration File",
    )
    group.addoption(
        "--backend_url",
        action="store",
        help="Backend API",
    )
    group.addoption(
        "--fixture_url",
        action="store",
        default="http://localhost:8886",
        help="Fixture API",
    )
    group.addoption("--teardown", action="store_true")
    group.addoption(
        "--skip-summary",
        action="store_true",
        help="Skip FixturFab Test Runner Report Summary",
    )


def pytest_configure(config):
    """Add markers and other configuration information for the F3TS plugin."""
    if not config.option.teardown:
        config.api_data = {}
        p = F3TSReporter(config)
        config.pluginmanager.register(p, "f3ts_reporter")


class F3TSReporter:
    """F3TS Test Runner Reporter Plugin.

    This plugin implements all backend communication with the
    F3TS Test Runner application.
    """

    start_time = None

    def __init__(self, config):
        self.config = config
        self.api = None
        self.run_id = self.config.option.run_id
        self.slot_id = self.config.option.slot_id
        self.frontend_client_id = self.config.option.frontend_client_id

        try:
            self.api = F3TSBackendAPI(
                api_url=self.config.option.backend_url,
                run_id=self.run_id,
                slot_id=self.slot_id,
                frontend_client_id=self.frontend_client_id,
            )
            self.operator_id = self.api.operator_id

        except Exception as e:
            logger.warning(
                "WARNING: Unable to connect to backend API, "
                f"not sending results to backend!\n{e}"
            )
            self.run_id = 0
            self.operator_id = 0
            self.api = F3TSASCIIAPI(config.api_data, slot_id=self.slot_id)

    def pytest_collection_modifyitems(self, items):
        """Pre-processing after collection has been called."""
        self.start_time = time.time()
        terminalreporter = self.config.pluginmanager.getplugin("terminalreporter")

        tests = [i.originalname for i in items]
        terminalreporter.ensure_newline()
        terminalreporter.line(f"tests collected: {tests}")

    def pytest_runtest_logreport(self, report):
        """Send the unit test report to the Backend.

        Create a TestReport model from the `pytest` `report` object
        and send the results to the backend webserver. Send error
        notification after failed test.
        """
        terminalreporter = self.config.pluginmanager.getplugin("terminalreporter")

        # Only send results for "call" actions
        if report.when == "call":
            # Create base TestResult
            result = schemas.ResultCreate(
                test_name=report.head_line,
                operator_id=self.operator_id,
                start=report.start,
                stop=report.stop,
                duration=report.duration,
                passed=report.passed,
            )

            # Add user keys
            user_properties_dict = dict()
            for user_property in report.user_properties:
                user_properties_dict[user_property[0]] = user_property[1]

            search_props = [
                "test_id",
                "description",
                "error_code",
                "error_msg",
                "min_limit",
                "max_limit",
                "meas",
            ]
            if "test_config" in user_properties_dict.keys():
                config_dict = dict(user_properties_dict["test_config"])
                for k, v in config_dict.items():
                    if k in search_props:
                        setattr(result, k, v)

            for k, v in user_properties_dict.items():
                if k in search_props:
                    setattr(result, k, v)

            terminalreporter.ensure_newline()
            terminalreporter.section(f"Test ID: {result.test_id}", sep="-")

            terminalreporter.line(str(result))
            self.api.send_test_result(result)

            # Send error message notification is test failed:
            if not result.passed:
                error_message = "Unknown Error Occured"
                error_code = ""

                if result.error_msg:
                    error_message = result.error_msg

                if result.error_code:
                    error_code = result.error_code

                error_notif = schemas.Notif(
                    title=f"ERROR {error_code}: {result.test_name}",
                    message=error_message,
                    okButtonText="OK",
                )
                terminalreporter.ensure_newline()
                terminalreporter.section(
                    f"ERROR {error_code}: {result.test_name}", sep="="
                )

                terminalreporter.line(str(error_notif))
                self.api.send_user_notif(error_notif)

    def pytest_sessionfinish(self, session):
        """Send the test finished message to the Backend."""

    def pytest_terminal_summary(self, terminalreporter, exitstatus, config):
        """Send collected run information to database.

        Updates information such as duration, serial number, fixture id, etc.
        """

        duration = time.time() - self.start_time
        run = schemas.RunUpdate(
            slot_id=config.option.slot_id,
            operator_id=self.operator_id,
            duration=duration,
            passed=(exitstatus == 0),
            num_failed=(len(terminalreporter.stats.get("failed", []))),
            num_passed=(len(terminalreporter.stats.get("passed", []))),
            num_skipped=(len(terminalreporter.stats.get("skipped", []))),
        )

        terminalreporter.ensure_newline()
        terminalreporter.section("Fixturfab Test Runner (Updating Run...)", sep="-")
        terminalreporter.line(str(run))
        self.api.update_run_data(run)

        # Generate Test Report Summary if no backend API is connected:
        if self.api.api_url is None and not config.option.skip_summary:
            terminalreporter.ensure_newline()
            terminalreporter.section(" FixturFab Test Runner Summary ", bold=True)
            terminalreporter.ensure_newline()
            width = os.get_terminal_size().columns - 71
            if width < 60:
                name_width = 25
                desc_width = 35
            else:
                name_width = int((width * 3) / 8)
                desc_width = width - name_width

            # Header
            header = f"{'Test ID ':<9} {'Test Name':<{name_width}} {'Description':<{desc_width}} {'Min Limit':<11} {'Measurement':<13} {'Max Limit':<11} {'Passed':<8} {'Duration (s)':<10}"
            terminalreporter.write("-" * len(header) + "\n")
            terminalreporter.write(header + "\n")
            terminalreporter.write("-" * len(header) + "\n")

            # Iterate over all collected test reports
            for result in config.api_data["results"]:
                terminalreporter.write(
                    f"{safe_format(result.test_id, width=9)} "
                    f"{safe_format(result.test_name, width=name_width)} "
                    f"{safe_format(result.description, width=desc_width)} "
                    f"{safe_format(result.min_limit, width=11)} "
                    f"{safe_format(result.meas, width=13)} "
                    f"{safe_format(result.max_limit, width=11)} "
                    f"{safe_format(str(result.passed), default='N/A', width=8)} "
                    f"{safe_format(round(result.duration, 5), default='N/A', width=10)}\n"
                )

            terminalreporter.write("-" * len(header) + "\n")
