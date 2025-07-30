# MCP TMAP

The MCP connects to the TMAP API.

It currently supports the following APIs:
* [Public Transit API](https://openapi.sk.com/products/detail?svcSeq=59&menuSeq=394)
  * Transit route
* [Location API](https://openapi.sk.com/products/detail?svcSeq=4&menuSeq=10)
  * Full text geocoding

## Prerequisites

Before you begin, ensure you have the following installed:

* **Python:** Version 3.13 or higher
* **uv:** You can find installation instructions [here](https://github.com/astral-sh/uv).
* **SK Open API:** You need API credentials (app key) from the [SK open API](https://openapi.sk.com/).

## Configuration

1. **Create a `.env` file:**  Create a file in the project root.

2. **Add API Credentials:** Edit the `.env` file and add your SK open API credentials.
    ```.env
    SK_OPEN_API_APP_KEY="YOUR_APP_KEY_HERE"
    ```
    Please verify the exact environment variable names required by checking `src/mcp_tmap/tmap_client.py`.

## Running the MCP

1. **Sync Dependencies:** Navigate to the project root directory in your terminal and run the following command. This will create a virtual environment (if one doesn't exist) and install all dependencies specified in `pyproject.toml`.
    ```bash
    uv sync
    ```

2. **Run:**: You can run the MCP server using `uv`.
    ```bash
    uv run src/mcp_tmap
    ```

    For development,
    ```bash
    source .venv/bin/activate
    mcp dev src/mcp_tmap/server.py
    ```
