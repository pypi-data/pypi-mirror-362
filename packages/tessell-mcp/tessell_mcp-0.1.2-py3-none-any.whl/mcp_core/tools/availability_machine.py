from mcp_core.mcp_server import mcp
from mcp_core.tools.client_factory import get_tessell_api_client

@mcp.tool()
def get_availability_machines(page_size: int = 10):
    """
    Retrieve a detailed list of all availability machines in the Tessell environment.

    This tool fetches all availability machines, including their unique IDs, names, statuses, and related metadata. It is useful for monitoring, auditing, and managing the lifecycle of availability machines within the environment. The tool supports pagination via the `page_size` parameter to control the number of results returned in a single call.

    Args:
        page_size (int, optional): The number of availability machines to return per page. Defaults to 10.
    Returns:
        dict: A dictionary containing the HTTP status code and the raw JSON response text from the Tessell API. The response includes a list of availability machine objects, each with fields such as ID, name, status, and other relevant metadata.

    Example response:
        {
            "status_code": 200,
            "content": '[{"id": "am-123", "name": "AMachineA", "status": "ACTIVE", ...}, ...]'
        }
    """
    client = get_tessell_api_client()
    resp = client.get_availability_machines(page_size=page_size, load_acls=True)
    return {"status_code": resp.status_code, "content": resp.text}