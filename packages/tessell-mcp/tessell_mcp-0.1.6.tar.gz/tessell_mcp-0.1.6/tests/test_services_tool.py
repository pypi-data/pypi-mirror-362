import os
import pytest
from dotenv import load_dotenv
from mcp_core.tools.services import *

# Load environment variables from .env file if present
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "test_config.env"), override=False)

# Test configuration
TEST_SERVICE_ID = os.environ.get("TEST_SERVICE_ID")

REQUIRED_ENV_VARS = ["TESSELL_API_BASE", "TESSELL_API_KEY", "TESSELL_TENANT_ID"]

@pytest.fixture(autouse=True)
def check_environment():
    missing_env_vars = [var for var in REQUIRED_ENV_VARS if not os.environ.get(var)]
    if missing_env_vars:
        pytest.skip(
            f"Missing required environment variables: {', '.join(missing_env_vars)}. "
            f"Please set them or copy tests/test_config.example to tests/test_config.env "
            f"and run: export $(cat tests/test_config.env | xargs) && python -m pytest tests/"
        )

@pytest.fixture(autouse=True)
def check_test_data():
    if not TEST_SERVICE_ID:
        pytest.skip("TEST_SERVICE_ID not set. Please set it to run service tool tests.")

def test_list_services():
    result = list_services()
    assert result["status_code"] == 200
    assert "content" in result
    assert isinstance(result["content"], str)

def test_get_service_details():
    result = get_service_details(TEST_SERVICE_ID)
    assert result["status_code"] == 200
    assert "service_details" in result
    assert isinstance(result["service_details"], dict)

def test_list_databases():
    result = list_databases(TEST_SERVICE_ID)
    assert result["status_code"] == 200
    assert "databases" in result
    logging.info(f"Databases for service {TEST_SERVICE_ID}: {result['databases']}")
    assert isinstance(result["databases"], list)


def test_search_services_by_name():
    # Use a substring of TEST_SERVICE_ID or a known service name for the query
    query = "mysql"  # Set to a valid substring or name for your environment
    result = search_services(query)
    assert result["status_code"] == 200
    logging.info(f"Search results for query '{query}': {result}")
    assert "matches" in result
    assert isinstance(result["matches"], list)

def test_service_action_invalid():
    result = manage_service(TEST_SERVICE_ID, "invalid_action")
    assert result["status_code"] == 400
    assert "error" in result

def test_service_action_start_stop():
    """Test starting and stopping a service based on its current status."""
    details_result = get_service_details(TEST_SERVICE_ID)
    assert details_result["status_code"] == 200
    details = details_result["service_details"]
    status = details.get("status")
    assert status in ("READY", "STOPPED", "STOPPING"), f"Unexpected service status: {status}"

    if status == "READY":
        stop_result = manage_service(TEST_SERVICE_ID, "stop", "Stopping for test")
        assert stop_result["status_code"] in (200, 202), f"Stop failed: {stop_result}"
    elif status == "STOPPED":
        start_result = manage_service(TEST_SERVICE_ID, "start", "Starting for test")
        assert start_result["status_code"] in (200, 202), f"Start failed: {start_result}"
    elif status == "STOPPING":
        pytest.skip("Service is stopping, not performing start/stop action.")
    else:
        pytest.fail(f"Unhandled service status: {status}")
