# Tessell MCP Server

Tessell MCP Server enables natural language interaction with your Tessell environment through the Model Context Protocol (MCP). This tool allows you to manage and automate tasks in Tessell using supported MCP clients.

## Overview
The Tessell MCP Server provides a local bridge between your MCP client and the Tessell API. With this integration, you can perform operations such as managing databases, services, and other resources in your Tessell tenant using conversational commands.

## Key Capabilities
- Interact with Tessell resources using natural language
- Streamlined management of databases, services, and more
- Connects securely to your Tessell tenant via API credentials

## Requirements
- Tessell account with API key
- Tenant API base URL and tenant ID
- Compatible MCP client (e.g., Claude Desktop, Cursor)
- Python (>=3.13) and uvx

## Installation & Configuration

To set up the Tessell MCP Server, add the following configuration to your MCP client's configuration file (such as `mcp_config.json`):

```json
{
  "mcpServers": {
    "tessell": {
      "command": "uvx",
      "args": [
        "tessell-mcp@latest"
      ],
      "env": {
        "TESSELL_API_BASE": "{your-tenant-api-url}",
        "TESSELL_API_KEY": "{your-api-key}",
        "TESSELL_TENANT_ID": "{your-tenant-id}"
      }
    }
  }
}
```

Be sure to replace the placeholders with your actual Tessell tenant information.

## How to Use

After configuration, restart your MCP client. You can now issue natural language commands to manage your Tessell environment. For example:
- "Create a new database named 'analytics-db'."
- "Show all running services in my Tessell account."
- "Back up the 'prod-db' database."

## Security Notes
- Tessell MCP Server is intended for local development and IDE integrations only.
- Keep your API key and tenant credentials secure and private.
- Review and approve all actions before allowing execution via the MCP client.

---
