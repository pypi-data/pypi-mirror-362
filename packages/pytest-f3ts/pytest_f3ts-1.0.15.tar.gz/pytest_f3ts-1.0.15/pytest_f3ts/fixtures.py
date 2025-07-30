"""F3TS Pytest Plugin Fixtures.

Various utility fixtures for accessing test plan configuration and test runner
parameters.
"""
import logging
import time

import pytest

from pytest_f3ts import schemas
from pytest_f3ts.runner_client import F3TSASCIIAPI, F3TSBackendAPI
from pytest_f3ts.utils import (
    SerialNumber,
    StatusBanner,
    UserDialog,
    get_config_from_file,
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def backend_api(pytestconfig) -> F3TSBackendAPI:
    """F3TS Backend Webservice API.

    Object for creating and sending requests to the Test Executer (TE)
    """
    try:
        return F3TSBackendAPI(
            api_url=pytestconfig.option.backend_url,
            run_id=pytestconfig.option.run_id,
            plan_id=pytestconfig.option.plan_id,
            slot_id=pytestconfig.option.slot_id,
            frontend_client_id=pytestconfig.option.frontend_client_id,
        )

    except Exception as err:
        print(
            f"WARNING: Unable to connect to backend API at {pytestconfig.option.backend_url}: {err}"
        )


@pytest.fixture(scope="session")
def local_api(pytestconfig) -> F3TSASCIIAPI:
    """F3TS Backend Webservice API.

    Object for creating and sending requests to the Test Executer (TE)
    """
    return F3TSASCIIAPI(slot_id=pytestconfig.option.slot_id)


@pytest.fixture(scope="session")
def test_plan_config(pytestconfig, backend_api) -> schemas.PytestTestPlanConfig:
    """Fixture that provides access to the test plan configuration information.

    Returns the test plan configuration information. This is loaded from a YAML
    file that is titled either `config.yaml` within the same directory as the
    current test file, or can be defined by adding the `--f3ts_config` variable
    to the `pytest` command line call. For example:

    ```
    pytest -p f3ts --f3ts_config=path/to/config.yml
    ```

    The test plan must match the schema defined by the `TestPlanConfig` model.
    """
    if backend_api:
        config_obj = backend_api.get_config(
            slot_id=pytestconfig.option.slot_id,
        )
    else:
        config_obj = get_config_from_file(
            f3ts_config=pytestconfig.option.f3ts_config,
            slot_id=pytestconfig.option.slot_id,
        )

    logger.info(f"test_plan_config: {config_obj}")
    return config_obj


@pytest.fixture
def test_config(
    test_plan_config: schemas.PytestTestPlanConfig, request
) -> schemas.TestCase:
    """Fixture that provides test case configuration information.

    Returns the test case configuration information for the current
    test case. This requires the test case name to match the key within
    the configuration file, for example, a test named `test_5v0_voltage`
    would require the following section in the test configuration file:

    ```
    test_cases:
      test_5v0_voltage:
        test_id: 2.1
        error_code: 201
        error_msg: "Voltage out of spec"
        min_limit: 4.9
        max_limit: 5.1
        user_vars:
          user_dict_key1: user_dict_value1
          user_dict_key2: user_dict_value2
    ```
    """
    test_func_name = request.node.name.split("[")[0]

    if test_func_name in test_plan_config.test_cases.keys():
        return test_plan_config.test_cases[test_func_name]
    else:
        return None


@pytest.fixture(scope="session")
def fixture_config(
    test_plan_config: schemas.PytestTestPlanConfig, request, pytestconfig
) -> schemas.FixtureSettings:
    """Fixture that provides test fixture configuration information.

    Returns the test fixture configuration information for the current
    test fixture. This requires the test fixture id to match the fixture_id
    set the configuration file

    Required "pytest --slot_id" parameter specified on startup and
    within config.yml
    Required "pytest --fixture_id" parameter specified on startup and
    within config.yml:

    Example Use Case:

    ```yaml
    slot_1:
        slot_id: 1
        config:
            user_dict_key1: user_dict_value1
            user_dict_key2: user_dict_value2

    slot_2:
        slot_id: 2
        config:
            user_dict_key1: user_dict_value3
            user_dict_key2: user_dict_value4

    ```

    ```python
        def test_fixture_parameter(fixture_config):
            config_value = fixture_config.config['user_dict_key1']

            assert user_dict_value1==config_value, "Matches Fixture 1"
            assert user_dict_value3==config_value, "Matches Fixture 2"

    ```

    Start test program with --slot_id specified below:

        pytest --slot_id=1

    This grants the test runner access to slot_1's user defined parameters.
    This is useful for hardware serial numbers or MAC IDs that are different
    fixture to fixture but are required for the automated test software to
    function as desired.

    """
    if pytestconfig.option.slot_id is None:
        raise AssertionError(
            "ERROR: No Slot ID specified via --slot_id, "
            "no fixture_settings available"
        )

    return test_plan_config.fixture_settings


@pytest.fixture(autouse=True)
def auto_logger(test_config, record_property):
    """Log standard F3TS variables."""
    if test_config:
        record_property("test_config", dict(test_config))


@pytest.fixture
def f3ts_assert(backend_api, local_api, test_config, record_property, request):
    """Fixture to manually send assertion result to the Test Executer (TE).

    Assert statements made with f3ts_assert will show up as sub results within
    the test application GUI and stored as a result in the results database.
    """
    assert_id = 1
    start = time.time()

    def custom_assert(
        assert_value: bool = None,
        min_limit=None,
        meas=None,
        max_limit=None,
        test_id=None,
        test_name=None,
        description=None,
        error_code=None,
        error_msg=None,
    ):
        nonlocal assert_id, start
        args = locals()

        terminalreporter = request.config.pluginmanager.getplugin("terminalreporter")

        if backend_api:
            api = backend_api
        else:
            api = local_api

        assertion = schemas.ResultCreate(
            test_name=request.node.name,
            operator_id=api.operator_id,
            start=start,
            stop=time.time(),
            duration=time.time() - start,
            passed=bool(assert_value),
        )

        search_props = [
            "test_id",
            "description",
            "error_code",
            "error_msg",
            "min_limit",
            "max_limit",
            "meas",
        ]
        for key, value in args.items():
            if key in search_props:
                if args[key] is not None:
                    setattr(assertion, key, value)
                elif test_config and key in dict(test_config).keys():
                    setattr(assertion, key, dict(test_config)[key])

        assertion.test_id = str(assertion.test_id) + "." + str(assert_id)
        if assertion.meas is None:
            assertion.meas = assertion.passed

        assert_id += 1
        start = time.time()

        terminalreporter.ensure_newline()
        terminalreporter.section(f"Test ID: {assertion.test_id}", sep="-")

        terminalreporter.line(str(assertion))
        api.send_test_result(assertion)
        if not backend_api:
            request.config.api_data["results"] += [assertion]

        if not assertion.passed:
            print(" sending error notification to GUI ".center(80, "-"))

            error_message = "Subtest Failed"
            error_code = ""

            if "error_msg" in args.keys():
                error_message = args["error_msg"]
            elif "error_msg" in dict(test_config).keys():
                error_message = test_config.error_msg

            if "error_code" in args.keys():
                error_code = args["error_code"]
            elif "error_code" in dict(test_config).keys():
                error_code = test_config.error_code

            error_notif = schemas.Notif(
                title=f"ERROR {error_code}: {assertion.test_name}",
                message=error_message,
                okButtonText="OK",
            )

            terminalreporter.ensure_newline()
            terminalreporter.section(f"Error ID: {error_code}", sep="-")
            terminalreporter.line(str(error_notif))

            api.send_user_notif(error_notif)

        # Record test properties
        record_property("f3ts-assert", assertion.dict())
        assert assert_value

    yield custom_assert


@pytest.fixture(scope="session")
def user_dialog(backend_api) -> UserDialog:
    """Fixture that provides user dialog features.

    Sending dialog messages to terminal that requires
    user input require stdin enabled via:

        pytest -s

    """
    user_dialog = UserDialog(backend_api)

    yield user_dialog

    user_dialog.close()


@pytest.fixture(scope="session")
def status_banner(backend_api) -> StatusBanner:
    """Fixture that provides ability to override status banner."""
    yield StatusBanner(backend_api)


@pytest.fixture(scope="session")
def serial_number(backend_api) -> SerialNumber:
    """Fixture for accessing the serial number of the device under test (DUT)."""
    yield SerialNumber(backend_api)


@pytest.fixture(scope="session")
def logfile_storage(backend_api):
    """Fixture to manually upload log files to the Test Executor (TE)."""

    def upload(filename: str, filepath: str):
        if backend_api is not None:
            attachment = schemas.AttachmentCreate(name=filename, filepath=filepath)

            backend_api.upload_logfile(backend_api.run_id, attachment)

    yield upload
