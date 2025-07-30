"""
Nuuly Postgres MCP Server
"""

import os
import httpx
import logging
import sys
import json
from typing import Any, Dict, Optional

# Configure logging
logger = logging.getLogger(__name__)

# Configuration for Cloud Run DB Proxy
POSTGRES_MCP_SERVER_URL = os.getenv("POSTGRES_MCP_SERVER_URL", "https://www.example.com")
db_proxy_api_key = os.getenv("DB_PROXY_API_KEY")

# Import FastMCP
from fastmcp import FastMCP, Context

# Create MCP server with proper initialization
mcp = FastMCP("Nuuly Postgres MCP")

@mcp.tool()
async def run_query(ctx: Context, database: str, sql: str) -> str:
    """Run a SQL query against the database and return results.

    Args:
        ctx: The MCP server provided context.
        database: The name of a database (like orders, waving, box, product, etc)
        sql: The SQL query string to execute. Accepts SELECT, SHOW, EXPLAIN queries only
    Returns:
        A JSON string representing the query result (columns and rows).
    """
    try:
        # Validate API key is available
        if not db_proxy_api_key:
            logger.error("DB_PROXY_API_KEY environment variable not set")
            return json.dumps({"error": "DB_PROXY_API_KEY environment variable not set"})
            
        # Prepare request payload
        payload = {
            "database": database,
            "sql": sql
        }
        headers = {"X-API-KEY": db_proxy_api_key}
        url = f"{POSTGRES_MCP_SERVER_URL}/query"
        
        logger.info(f"Executing query on database: {database}")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: status={e.response.status_code}, body={e.response.text}")
        return json.dumps({"error": f"Cloud Run proxy error: {e.response.status_code}", "details": e.response.text})
    except Exception as e:
        logger.error(f"Exception reaching Cloud Run DB proxy: {e}")
        return json.dumps({"error": "Failed to reach Cloud Run DB proxy", "details": str(e)})

@mcp.tool()
async def get_schema(ctx: Context, database: str) -> str:
    """Get the schema of all tables in the database.

    Args:
        ctx: The MCP server provided context.
        database: The name of a database (like orders, waving, box, product, etc) - this can 
            be an instance name or an alias. A full list of databases is available via the
            `list_databases` tool.
    Returns:
        A JSON string describing the tables and their columns, foreign keys, primary keys,
            and constraints.
    """
    try:
        # Validate API key is available
        if not db_proxy_api_key:
            logger.error("DB_PROXY_API_KEY environment variable not set")
            return json.dumps({"error": "DB_PROXY_API_KEY environment variable not set"})
            
        payload = {"database": database}
        headers = {"X-API-KEY": db_proxy_api_key}
        url = f"{POSTGRES_MCP_SERVER_URL}/schema"
        
        logger.info(f"Fetching schema for database: {database}")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: status={e.response.status_code}, body={e.response.text}")
        return json.dumps({"error": f"Cloud Run proxy error: {e.response.status_code}", "details": e.response.text})
    except Exception as e:
        logger.error(f"Exception reaching Cloud Run DB proxy: {e}")
        return json.dumps({"error": "Failed to reach Cloud Run DB proxy", "details": str(e)})

@mcp.tool()
async def list_databases(ctx: Context) -> str:
    """List all databases and their aliases accessible via the Cloud Run DB Proxy.

    Args:
        ctx: The MCP server provided context.
    Returns:
        A JSON string representing the list of databases, their aliases, and instance info.
    """
    try:
        # Validate API key is available
        if not db_proxy_api_key:
            logger.error("DB_PROXY_API_KEY environment variable not set")
            return json.dumps({"error": "DB_PROXY_API_KEY environment variable not set"})
            
        headers = {"X-API-KEY": db_proxy_api_key}
        url = f"{POSTGRES_MCP_SERVER_URL}/databases"
        
        logger.info("Listing available databases")
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTPStatusError: status={e.response.status_code}, body={e.response.text}")
        return json.dumps({"error": f"Cloud Run proxy error: {e.response.status_code}", "details": e.response.text})
    except Exception as e:
        logger.error(f"Exception reaching Cloud Run DB proxy: {e}")
        return json.dumps({"error": "Failed to reach Cloud Run DB proxy", "details": str(e)})

def run():
    """Entry point for the MCP server."""
    # Setup logging configuration if not already configured
    if not logging.getLogger().handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            stream=sys.stderr
        )
    
    # Add global exception handler
    try:
        logger.info("Starting Nuuly Postgres MCP Server")
        mcp.run()
    except Exception as e:
        logger.error(f"Unhandled exception in MCP server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    run()
