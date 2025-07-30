Generate the SDK Folder
=======================

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

Running the Tessell MCP Server
===============================

The Tessell MCP server can be run in two modes:

1. AWS Lambda Mode
------------------

This mode is for deploying the MCP server as an AWS Lambda function. The entry point is `app.py`, which is designed specifically for Lambda environments. Deploy this file to AWS Lambda and configure your environment variables as needed.

2. Local Mode (STDIO) for MCP Clients
--------------------------------------

You can also run the MCP server locally for use with MCP clients (such as Cursor or Visual Studio Code). Add the following configuration to your client settings:

```json
{
  "mcpServers": {
    "tessell": {
      "command": "uv",
      "args": [
        "--directory",
        "<path-to-your-tessell-ai-mcp-server>",
        "run",
        "main.py"
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

- Replace `<path-to-your-tessell-ai-mcp-server>` with the absolute path to your project directory.
- Set the environment variables to your actual Tessell API values.
- This allows MCP clients to launch and communicate with your MCP server in local (stdio) mode.