import os
import time
import pytest
from dotenv import load_dotenv
from mcp_core.tools.availability_machine import *

# Load environment variables from .env file if present
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "test_config.env"), override=False)

# Test configuration
TEST_SERVICE_ID = os.environ.get("TEST_SERVICE_ID")
TEST_AVAILABILITY_MACHINE_ID = os.environ.get("TEST_AVAILABILITY_MACHINE_ID")
SNAPSHOT_NAME = f"test-snapshot-pytest-{int(time.time())}"

# Required environment variables for Tessell API
REQUIRED_ENV_VARS = ["TESSELL_API_BASE", "TESSELL_API_KEY", "TESSELL_TENANT_ID"]

@pytest.fixture(autouse=True)
def check_environment():
    """Skip tests if required environment variables are missing."""
    missing_env_vars = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing_env_vars:
        pytest.skip(
            f"Missing required environment variables: {', '.join(missing_env_vars)}. "
            f"Please set them or copy tests/test_config.example to tests/test_config.env "
            f"and run: export $(cat tests/test_config.env | xargs) && python -m pytest tests/"
        )

@pytest.fixture(autouse=True)
def check_test_data():
    """Skip tests if required test data is missing."""
    if not TEST_SERVICE_ID:
        pytest.skip("TEST_SERVICE_ID not set. Please set it to run availability machine tests.")
    if not TEST_AVAILABILITY_MACHINE_ID:
        pytest.skip("TEST_AVAILABILITY_MACHINE_ID not set. Please set it to run availability machine tests.")

def test_get_availability_machine_id_by_service_id():
    """Test retrieving availability machine ID from service ID."""
    result = get_availability_machine_id(TEST_SERVICE_ID)
    assert result["status_code"] == 200
    assert "availability_machine_id" in result
    assert result["availability_machine_id"] is not None

def test_create_snapshot_tool():
    """Test creating a snapshot with description (default empty if not provided)."""
    description = "Test snapshot created by pytest"
    result = create_snapshot(
        availability_machine_id=TEST_AVAILABILITY_MACHINE_ID,
        name=SNAPSHOT_NAME,
        description=description
    )
    assert result["status_code"] == 201
    assert "snapshot" in result
    snapshot = result["snapshot"]
    # Accept either dict with 'name' or a dict with 'details' containing 'snapshot'
    if isinstance(snapshot, dict) and "details" in snapshot and "snapshot" in snapshot["details"]:
        assert snapshot["details"]["snapshot"] == SNAPSHOT_NAME
    elif isinstance(snapshot, dict) and "name" in snapshot:
        assert snapshot["name"] == SNAPSHOT_NAME
        assert snapshot.get("description", "") == description
    else:
        pytest.fail(f"Unexpected snapshot structure: {snapshot}")

def test_list_snapshots_tool():
    """Test listing snapshots."""
    result = list_snapshots(availability_machine_id=TEST_AVAILABILITY_MACHINE_ID)
    assert result["status_code"] == 200
    assert "snapshots" in result
    assert isinstance(result["snapshots"], dict)
    snapshots = result["snapshots"].get("snapshots")
    assert isinstance(snapshots, list)
    assert len(snapshots) > 0, "No snapshots found; at least one snapshot should be available."

def test_create_snapshot_invalid_am_id():
    """Test creating a snapshot with invalid availability machine ID."""
    result = create_snapshot(availability_machine_id="", name="test")
    assert result["status_code"] == 400
    assert "error" in result

def test_create_snapshot_no_name():
    """Test creating a snapshot without name."""
    result = create_snapshot(availability_machine_id=TEST_AVAILABILITY_MACHINE_ID, name="")
    assert result["status_code"] == 400
    assert "error" in result

def test_get_availability_machine_id_invalid_service():
    """Test getting availability machine ID for invalid service."""
    result = get_availability_machine_id("invalid-service-id")
    assert result["status_code"] != 200
    assert "error" in result
