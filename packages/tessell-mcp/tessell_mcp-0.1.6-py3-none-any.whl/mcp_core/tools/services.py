from mcp_core.mcp_server import mcp
from mcp_core.tools.client_factory import get_tessell_api_client
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def list_services(page_size: int = 10):
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
    logger.info(f"Listing services with page_size={page_size}")
    resp = client.get_services(page_size=page_size)
    return {"status_code": resp.status_code, "content": resp.text}

@mcp.tool()
def get_service_details(service_id: str):
    """
    Retrieve the full details for a given service ID using the Tessell API client.

    Args:
        service_id (str): The ID of the service.
    Returns:
        dict: {"status_code": int, "service_details": dict} or error message.
    """
    client = get_tessell_api_client()
    resp = client.get_service_details(service_id)
    logger.info(f"Fetching full service details for service_id={service_id}, status_code={resp.status_code}")
    if resp.status_code != 200:
        logger.error(f"Failed to fetch service details: {resp.text}")
        return {"status_code": resp.status_code, "error": resp.text}
    try:
        details = resp.json()
        return {"status_code": 200, "service_details": details}
    except Exception as e:
        logger.exception("Failed to parse service details JSON.")
        return {"status_code": 500, "error": str(e)}
    
@mcp.tool()
def list_databases(service_id: str):
    """
    List databases for a given service by service_id by fetching service details and extracting the 'databases' field.
    Returns:
        dict: {"status_code": int, "databases": list}
    """
    client = get_tessell_api_client()
    logger.info(f"Listing databases for service_id={service_id} via service details")
    resp = client.get_service_details(service_id)
    if resp.status_code == 200:
        try:
            details = resp.json()
            databases = details.get("databases", [])
            return {"status_code": 200, "databases": databases}
        except Exception as e:
            logger.exception("Failed to parse service details JSON for databases.")
            return {"status_code": 500, "error": str(e)}
    else:
        logger.error(f"Failed to fetch service details for databases: {resp.text}")
        return {"status_code": resp.status_code, "error": resp.text}

@mcp.tool()
def search_services(query: str, page_size: int = 20):
    """
    Search for services by name pattern. Use a single keyword (e.g., 'sales' or 'prod' from 'sales prod').
    Prefer a distinctive word likely used in the service name.
    This tool is commonly used since users refer to services by name, but other tools require a service id.
    Agents should confirm with the user if multiple matches are found.

    Returns:
        dict: {"status_code": int, "matches": [{"id": str, "name": str}, ...]}
    """
    client = get_tessell_api_client()
    logger.info(f"Locally searching services by name: query={query}, page_size={page_size}")
    resp = client.get_services(page_size=1000)
    if resp.status_code == 200:
        import json
        services_obj = resp.json()
        # If the response is a string, try to parse it as JSON
        if isinstance(services_obj, str):
            try:
                services_obj = json.loads(services_obj)
            except Exception as e:
                logger.error(f"Failed to parse services response as JSON: {e}")
                return {"status_code": 500, "error": str(e)}
        # Extract the list of services from the 'response' key
        services_list = services_obj.get("response", [])
        results = [
            {"id": s.get("id"), "name": s.get("name")}
            for s in services_list
            if isinstance(s, dict) and query.lower() in s.get("name", "").lower()
        ]
        # Optionally, return only up to page_size results
        return {"status_code": 200, "matches": results[:page_size]}
    else:
        logger.error(f"Failed to search services: {resp.text}")
        return {"status_code": resp.status_code, "error": resp.text}

@mcp.tool()
def manage_service(service_id: str, action: str, comment: str = ""):
    """
    Start or stop a database service by service_id.
    Args:
        service_id (str): The ID of the service to act on.
        action (str): Either 'start' or 'stop'.
        comment (str, optional): Comment for the action. Used for both start and stop.
    Returns:
        dict: {"status_code": int, "result": str}
    """
    client = get_tessell_api_client()
    logger.info(f"Performing action '{action}' on service_id={service_id}")
    if action == "start":
        resp = client.start_service(service_id, comment=comment)
    elif action == "stop":
        resp = client.stop_service(service_id, comment=comment)
    else:
        logger.error(f"Invalid action: {action}")
        return {"status_code": 400, "error": "Invalid action. Use 'start' or 'stop'."}
    if resp.status_code in (200, 202):
        logger.info(f"Service {action}ed successfully for service_id={service_id}")
        return {"status_code": resp.status_code, "result": f"Service {action}ed successfully."}
    else:
        logger.error(f"Failed to {action} service: {resp.text}")
        return {"status_code": resp.status_code, "error": resp.text}

