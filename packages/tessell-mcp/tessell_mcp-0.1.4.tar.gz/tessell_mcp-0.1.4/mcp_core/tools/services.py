from mcp_core.mcp_server import mcp
from mcp_core.tools.client_factory import get_tessell_api_client

@mcp.tool()
def get_services(page_size: int = 10):
    """
    Retrieve a detailed list of all services in the Tessell environment.

    Args:
        page_size (int, optional): The number of services to return per page. Defaults to 10.

    Returns:
        dict: A dictionary containing the HTTP status code and the raw JSON response text from the Tessell API. The response includes a list of service objects, each with fields such as ID, name, status, and availability machine ID.

    Example response:
        {
            "status_code": 200,
            "content": '[{"id": "svc-123", "name": "ServiceA", "status": "ACTIVE", "availability_machine_id": "am-456"}, ...]'
        }
    """
    client = get_tessell_api_client()
    resp = client.get_services(page_size=page_size)
    return {"status_code": resp.status_code, "content": resp.text}