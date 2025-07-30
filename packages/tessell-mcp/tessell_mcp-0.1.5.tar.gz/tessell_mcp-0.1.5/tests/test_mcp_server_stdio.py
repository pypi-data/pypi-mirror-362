import os
import subprocess
import json
import pytest
import time

# NOTE: This test file is not yet fully tested or verified.

# Set these to valid test values for your environment
TEST_SERVICE_ID = os.environ.get("TEST_SERVICE_ID", "replace-with-test-service-id")
SNAPSHOT_NAME = "test-snapshot-stdio"

@pytest.fixture(scope="module")
def mcp_server_proc():
    os.environ["TESSELL_API_KEY"] = os.environ.get("TESSELL_API_KEY", "replace-with-test-key")
    os.environ["TESSELL_API_URL"] = os.environ.get("TESSELL_API_URL", "https://your-test-endpoint")
    proc = subprocess.Popen([
        "python", "-m", "tessell_mcp.main", "--stdio"
    ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Print initial stderr output for debugging
    for _ in range(10):
        err_line = proc.stderr.readline()
        if err_line:
            print(f"[server stderr] {err_line.rstrip()}")
        else:
            break
    print(f"[fixture] MCP server process started, pid={proc.pid}, alive={proc.poll() is None}")
    try:
        yield proc
    finally:
        proc.terminate()
        proc.wait()

def test_list_tools_stdio(mcp_server_proc):
    request = {
        "type": "list_tools",
        "request_id": "1"
    }
    mcp_server_proc.stdin.write(json.dumps(request) + "\n")
    mcp_server_proc.stdin.flush()
    for _ in range(30):
        line = mcp_server_proc.stdout.readline()
        print(f"[list_tools] Read line: {line!r}")
        if not line:
            time.sleep(0.5)
            continue
        try:
            resp = json.loads(line)
            print(f"[list_tools] Decoded JSON: {resp}")
            if resp.get("type") == "list_tools_response":
                assert any("create_snapshot" in t for t in resp.get("tools", []))
                break
        except Exception as e:
            print(f"[list_tools] Exception: {e}")
            continue
    else:
        raise AssertionError("Did not receive list_tools_response with create_snapshot tool")

def test_invoke_tool_stdio(mcp_server_proc):
    invoke_req = {
        "type": "invoke_tool",
        "request_id": "2",
        "tool_name": "get_availability_machine_id_by_service_id",
        "parameters": {"service_id": TEST_SERVICE_ID}
    }
    mcp_server_proc.stdin.write(json.dumps(invoke_req) + "\n")
    mcp_server_proc.stdin.flush()
    for _ in range(30):
        line = mcp_server_proc.stdout.readline()
        print(f"[invoke_tool] Read line: {line!r}")
        if not line:
            time.sleep(0.5)
            continue
        try:
            resp = json.loads(line)
            print(f"[invoke_tool] Decoded JSON: {resp}")
            if resp.get("type") == "tool_response" and resp.get("request_id") == "2":
                assert resp["result"]["status_code"] == 200
                assert "availability_machine_id" in resp["result"]
                break
        except Exception as e:
            print(f"[invoke_tool] Exception: {e}")
            continue
    else:
        raise AssertionError("Did not receive valid tool_response for get_availability_machine_id_by_service_id")
