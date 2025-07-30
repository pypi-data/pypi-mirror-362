from mcp_core.mcp_server import mcp
from mcp_core.tools.client_factory import get_tessell_api_client
import logging

logger = logging.getLogger(__name__)

@mcp.tool()
def get_availability_machine_id(service_id: str):
    """
    Retrieve the availability machine ID for a given service ID.

    Args:
        service_id (str): The ID of the service.
    Returns:
        dict: {"status_code": int, "availability_machine_id": str} or error message.
    """
    client = get_tessell_api_client()
    service_resp = client.get_service_details(service_id)
    logger.info(f"Fetching service details for service_id={service_id}, status_code={service_resp.status_code}")
    if service_resp.status_code != 200:
        logger.error(f"Failed to fetch service details: {service_resp.text}")
        return {"status_code": service_resp.status_code, "error": service_resp.text}
    service_data = service_resp.json()
    availability_machine_id = service_data.get("availabilityMachineId")
    if not availability_machine_id:
        logger.warning(f"Availability machine ID not found for service_id={service_id}")
        return {"status_code": 404, "error": "Availability machine ID not found for the given service."}
    logger.info(f"Found availability_machine_id={availability_machine_id} for service_id={service_id}")
    return {"status_code": 200, "availability_machine_id": availability_machine_id}

@mcp.tool()
def create_snapshot(availability_machine_id: str, name: str = None, description: str = ""):
    """
    Create a snapshot for a given availability machine.

    Args:
        availability_machine_id (str): The ID of the availability machine.
        name (str): The name of the snapshot.
        description (str, optional): The description of the snapshot.

    Returns:
        dict: The details of the created snapshot or an error message.
    """
    client = get_tessell_api_client()
    if not availability_machine_id:
        logger.error("Availability machine ID must be provided.")
        return {"status_code": 400, "error": "Availability machine ID must be provided."}
    if not name:
        logger.error("Snapshot name must be provided.")
        return {"status_code": 400, "error": "Snapshot name must be provided."}
    try:
        logger.info(f"Creating snapshot for availability_machine_id={availability_machine_id}, name={name}")
        snapshot = client.create_snapshot(availability_machine_id, name, description)
        logger.info(f"Snapshot Requested: {snapshot}")
        return {"status_code": 201, "snapshot": snapshot}
    except Exception as e:
        logger.exception("Exception occurred while creating snapshot.")
        return {"status_code": 500, "error": str(e)}

@mcp.tool()
def list_snapshots(availability_machine_id: str):
    """
    List all snapshots for a given availability machine.
    Args:
        availability_machine_id (str): The ID of the availability machine.
    Returns:
        dict: {"status_code": int, "snapshots": list}
    """
    client = get_tessell_api_client()
    logger.info(f"Listing snapshots for availability_machine_id={availability_machine_id}")
    resp = client.get_availability_machine_snapshots(availability_machine_id)
    if resp.status_code == 200:
        data = resp.json()
        return {"status_code": 200, "snapshots": data}
    else:
        logger.error(f"Failed to list snapshots: {resp.text}")
        return {"status_code": resp.status_code, "error": resp.text}