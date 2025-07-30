"""
Nuuly BigQuery MCP Server
"""

import os
import httpx
import logging

# Configuration for BigQuery MCP Server
BIGQUERY_MCP_SERVER_URL = os.getenv("BIGQUERY_MCP_SERVER_URL", "https://www.example.com")
# API Key for authentication
BIGQUERY_MCP_API_KEY = os.getenv("BQ_API_KEY")

logger = logging.getLogger(__name__)

from fastmcp import FastMCP, Context

mcp = FastMCP("Nuuly BigQuery MCP")

@mcp.tool()
async def run_query(ctx: Context, database: str, sql: str) -> str:
    """Run a SQL query against the database and return results.

    Args:
        ctx: The MCP server provided context.
        database: The name of a database (BigQuery dataset)
        sql: The SQL query string to execute. Accepts SELECT, SHOW, EXPLAIN queries only
    Returns:
        A JSON string representing the query result (columns and rows).
    """
    try:
        # Prepare request payload
        payload = {
            "function_name": "run_query",
            "parameters": {
                "database": database,
                "sql": sql
            }
        }
        logger.info(f"Sending request to {BIGQUERY_MCP_SERVER_URL}")
        
        # Check if API key is available
        if not BIGQUERY_MCP_API_KEY:
            logger.error("BQ_API_KEY environment variable is not set")
            return {"error": "API key not configured. Set BQ_API_KEY environment variable."}
            
        # Include API key in headers
        headers = {"x-api-key": BIGQUERY_MCP_API_KEY}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(BIGQUERY_MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: status={e.response.status_code}, body={e.response.text}")
        return {"error": f"BigQuery MCP server error: {e.response.status_code}", "details": e.response.text}
    except Exception as e:
        logger.error(f"Exception reaching BigQuery MCP server: {e}")
        return {"error": "Failed to reach BigQuery MCP server", "details": str(e)}

@mcp.tool()
async def get_schema(ctx: Context, database: str) -> str:
    """Get the schema of all tables in the database.

    Args:
        ctx: The MCP server provided context.
        database: The name of a database (BigQuery dataset) - this can 
            be an instance name or an alias. A full list of databases is available via the
            `list_databases` tool.
    Returns:
        A JSON string describing the tables and their columns, foreign keys, primary keys,
            and constraints.
    """
    try:
        payload = {
            "function_name": "get_schema",
            "parameters": {
                "database": database
            }
        }
        logger.info(f"Sending request to {BIGQUERY_MCP_SERVER_URL}")
        
        # Check if API key is available
        if not BIGQUERY_MCP_API_KEY:
            logger.error("BQ_API_KEY environment variable is not set")
            return {"error": "API key not configured. Set BQ_API_KEY environment variable."}
            
        # Include API key in headers
        headers = {"x-api-key": BIGQUERY_MCP_API_KEY}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(BIGQUERY_MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: status={e.response.status_code}, body={e.response.text}")
        return {"error": f"BigQuery MCP server error: {e.response.status_code}", "details": e.response.text}
    except Exception as e:
        logger.error(f"Exception reaching BigQuery MCP server: {e}")
        return {"error": "Failed to reach BigQuery MCP server", "details": str(e)}

@mcp.tool()
async def list_databases(ctx: Context) -> str:
    """List all databases and their aliases accessible via BigQuery.

    Args:
        ctx: The MCP server provided context.
    Returns:
        A JSON string representing the list of databases, their aliases, and instance info.
    """
    try:
        payload = {
            "function_name": "list_databases",
            "parameters": {}
        }
        logger.info(f"Sending request to {BIGQUERY_MCP_SERVER_URL}")
        
        # Check if API key is available
        if not BIGQUERY_MCP_API_KEY:
            logger.error("BQ_API_KEY environment variable is not set")
            return {"error": "API key not configured. Set BQ_API_KEY environment variable."}
            
        # Include API key in headers
        headers = {"x-api-key": BIGQUERY_MCP_API_KEY}
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(BIGQUERY_MCP_SERVER_URL, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: status={e.response.status_code}, body={e.response.text}")
        return {"error": f"BigQuery MCP server error: {e.response.status_code}", "details": e.response.text}
    except Exception as e:
        logger.error(f"Exception reaching BigQuery MCP server: {e}")
        return {"error": "Failed to reach BigQuery MCP server", "details": str(e)}
