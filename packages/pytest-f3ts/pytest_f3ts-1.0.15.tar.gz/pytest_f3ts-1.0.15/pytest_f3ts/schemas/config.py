"""Models for messaging between the Test Executor and `pytest` processes."""

from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class GUISettings(BaseModel):
    """Test Runner GUI Settings.

    Contains settings for configuring the Test Runner, including displaying
    serial number input dialogs, enabling a test interlock check, etc.
    """

    display_name: str = None
    stop_at_first_failure: bool = True
    autorun: bool = False
    dut_count: int = 1
    dut_grid: List[int] = [1, 1]
    pytest_args: str = None


class FixtureSettings(BaseModel):
    """Test Fixture Settings.

    Contains global settings specific to a given Fixture or Fixture Slot.

    - slot_id: Fixture Slot ID
    - api_url: Fixture Slot API URL (if applicable)
    - user_vars: User defined variables available for configuration via Test Runner
    """

    slot_id: str
    api_url: str = None
    user_vars: dict = {}


class TestCase(BaseModel):
    """Test Case configuration model.

    Contains information for the given test case. This is used to configure
    pass/fail limits and provide information that is displayed within the
    Test Runner GUI.

    The following information should be specified:

    - test_id: Test ID number used to identify the test case on the GUI
    - error_code: Error code to use within debugging guide
    - error_msg: Message to display in the GUI when a failure occurs for the
        given test case
    - description: Message displayed in the GUI for the test description
    - min_limit: Minimum limit, if applicable
    - max_limit: Maximum limit, if applicable
    - user_vars: User defined variables available for configuration via Test Runner
    """

    test_id: Optional[str] = None
    error_code: Optional[str] = None
    error_msg: Optional[str] = None
    description: Optional[str] = None
    min_limit: Optional[Union[str, int, float, bool]] = None
    max_limit: Optional[Union[str, int, float, bool]] = None
    user_vars: dict = {}


class TestPlanConfig(BaseModel):
    """Test Plan Configuration file model.

    Contains the complete test plan configuration information. This includes
    the test name, GUI configuration information, and any test case
    configuration information.
    """

    test_name: str
    test_cases: Dict[str, TestCase]
    runner_settings: GUISettings
    fixture_settings: Dict[str, FixtureSettings] = {"DEV": FixtureSettings(slot_id="1")}


class PytestTestPlanConfig(BaseModel):
    """Test Plan Configuration file model.

    Contains the complete test plan configuration information. This includes
    the test name, GUI configuration information, and any test case
    configuration information.
    """

    test_name: str
    test_cases: Dict[str, TestCase]
    runner_settings: GUISettings
    fixture_settings: FixtureSettings


class BalenaRelease(BaseModel):
    id: int
    commit: str
    created_at: str
    revision: int


class ConfigInfo(BaseModel):
    """Configuration Information Message

    Message structure for sending the current test plan revision information
    to the backend.
    """

    test_plan_version: str
    test_plan_path: str
    balena_uuid: Optional[str] = None
    balena_release: Optional[BalenaRelease] = None
    test_plan_config: TestPlanConfig
