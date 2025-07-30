# Nuuly BigQuery MCP Server

This MCP server provides AI code editors with access to Google BigQuery data through the Model Context Protocol (MCP). It allows AI assistants to understand BigQuery datasets and tables, and to run queries against them. This implementation acts as a client that forwards requests to a remote BigQuery MCP server running on Google Cloud Run.

## Features

- List available BigQuery datasets
- Get detailed schema information for tables in a dataset
- Run SQL queries against BigQuery datasets
- Remote execution via Cloud Run service

## Prerequisites

- Python 3.8+

## Installation

### From PyPI (Recommended)

Install the package directly from PyPI:

```bash
pip install nuuly-bigquery-mcp-server
```

### From Source (Not Recommended)

1. Clone the repository:
   ```bash
   git clone https://github.com/urbn/r15-mcp.git
   cd r15-mcp/mcp_servers/bigquery-mcp
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

## Environment Variables

The server requires the following environment variables:

- `BQ_API_KEY` (required): API key for authentication with the BigQuery MCP server (see Confluence)
- `BIGQUERY_MCP_SERVER_URL` (optional): URL of the remote BigQuery MCP server (use: `https://bigquery-mcp-toolbox-oe7jbzhmjq-uk.a.run.app/mcp/invoke`)

### Configure your MCP Server

You must add this MCP server to the MCP configuration file for your LLM. After installing the package, the configuration becomes much simpler:

**Example MCP Configuration for Claude Desktop:**
```json
{
  "nuuly-bigquery-mcp": {
    "command": "nuuly-bigquery-mcp",
    "env": {
      "BQ_API_KEY": "your-api-key-here",
      "BIGQUERY_MCP_SERVER_URL": "https://bigquery-mcp-toolbox-oe7jbzhmjq-uk.a.run.app/mcp/invoke"
    }
  }
}
```

**Note:** Replace `your-api-key-here` with your actual BigQuery MCP API key.

### Available Tools

The server provides the following tools, which are forwarded to the remote BigQuery MCP server:

#### 1. list_databases

Lists all available BigQuery datasets.

```python
list_databases()
```

#### 2. get_schema

Gets the schema of all tables in a specified dataset.

```python
get_schema(database="your_dataset_name")
```

#### 3. run_query

Runs a SQL query against a BigQuery dataset.

```python
run_query(database="your_dataset_name", sql="SELECT * FROM your_table LIMIT 10")
```

## Example Usage

Here's an example of how to use the BigQuery MCP server with Claude:

```
I need to analyze data in BigQuery. Can you help me understand what datasets are available?
```

Claude will use the `list_databases` tool to show available datasets.

```
Now I want to see the schema of the 'analytics' dataset.
```

Claude will use the `get_schema` tool to show the tables and their schemas in the 'analytics' dataset.

```
Run a query to get the top 5 products by sales from the sales_data table.
```

Claude will use the `run_query` tool to execute the SQL query and display the results.

## License

Copyright © 2025 URBN Inc.
