# Developer Guide

This README is intended for developers and contributors. For end-user documentation and local MCP server usage, see `docs/tessell_mcp.md`.

For package build instructions, see [`docs/building_tessell_mcp.md`](docs/building_tessell_mcp.md).

## Code Structure

- `mcp_core/` — Common core logic and utilities for both local MCP and AWS Lambda deployments
- `api_client/` — Common API client code used by both local MCP and AWS Lambda
- `tessell_mcp/` — Root package for the local MCP server (entrypoint: `tessell_mcp/main.py`)
- `app.py` — AWS Lambda entrypoint for serverless deployment
- `docs/` — Documentation, including user-facing instructions in `tessell_mcp.md`

## Running the Tessell MCP Server

For full details on running and configuring the Tessell MCP Server in local mode, see the package documentation in `docs/tessell_mcp.md`.

### Quick Start (Local Mode)

You can test the Tessell MCP server in two ways using your MCP client config:

#### 1. Using a Direct File Path (Local Source Directory) (this is not working, using local wheel for now)

```json
{
  "mcpServers": {
    "tessell": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/your/tessell-ai-mcp-server",
        "run",
        "tessell_mcp/main.py"
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
- This runs the MCP server directly from your local source directory (no build needed).

#### 2. Using a Local Package (Wheel File)

```json
{
  "mcpServers": {
    "tessell": {
      "command": "uvx",
      "args": [
        "/absolute/path/to/your/dist/tessell_mcp-1.0.0-py3-none-any.whl"
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
- This installs and runs the MCP server from your locally built wheel file (no need to publish to PyPI).

Replace the environment variables and paths with your actual values.

For more usage instructions, features, and security notes, see `docs/tessell_mcp.md`.

If you are an end user, you will typically configure your MCP client to use the published PyPI package (e.g., `tessell-mcp@latest`), as described in the user guide (`docs/tessell_mcp.md`).

---

**Note:**
- The above instructions are for local development and testing.

## AWS Lambda Entrypoint

The file `app.py` serves as the entry point for deploying the Tessell MCP Server as an AWS Lambda function. Use this file when you want to run the MCP server in a serverless environment. Configure your Lambda environment variables as needed for your Tessell tenant.

For local development and integration with MCP clients, use the local mode instructions above.

---

## [ARCHIVED] Generate the SDK Folder

> **Note:** This section is archived and not used in the current workflow.

To generate a Python SDK from your OpenAPI specification and use it in this project:

1. **Choose a name for your SDK output folder.**
   - Example: `sdk/tessell_sdk`
2. **Place your OpenAPI YAML file** (e.g., `api_spec.yaml`) in the project root (same level as `pyproject.toml`).
3. **Generate the SDK using OpenAPI Generator:**
   ```sh
   mkdir -p sdk
   openapi-generator generate \
     -i api_spec.yaml \
     -g python \
     -o sdk/tessell_sdk
   ```
   - `-i api_spec.yaml` — Path to your OpenAPI spec file.
   - `-g python` — Generate a Python client.
   - `-o sdk/tessell_sdk` — Output directory for the generated SDK.

4. **Verify the output:**
   You should see a structure like:
   ```
   sdk/tessell_sdk/
   ├── README.md
   ├── setup.py
   ├── tessell_sdk/
   │   ├── __init__.py
   │   ├── configuration.py
   │   ├── api_client.py
   │   ├── api/
   │   │   ├── default_api.py
   │   │   └── ...
   │   ├── model/
   │   │   └── ...
   │   └── rest.py
   └── tests/
       └── ...
   ```

5. **(Optional) Install the SDK locally for development:**
   ```sh
   cd sdk/tessell_sdk
   pip install -e .
   ```
   This allows you to import the SDK in your project or Python REPL:
   ```python
   import tessell_sdk
   # Use the SDK as needed
   ```

6. **Regenerate the SDK whenever your OpenAPI spec changes** to keep your client up to date.

> **Tip:** You can add the SDK folder (e.g., `sdk/tessell_sdk`) to your `.gitignore` if you want to avoid committing generated code, or commit it for reproducibility.