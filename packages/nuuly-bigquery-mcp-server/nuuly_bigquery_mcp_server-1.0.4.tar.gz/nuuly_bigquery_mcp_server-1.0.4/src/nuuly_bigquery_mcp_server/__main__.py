"""
Entry point for the Nuuly BigQuery MCP Server
"""

import os
import sys
import logging
from .server import mcp

def main():
    """Entry point for the MCP server when run as a command-line tool."""
    # Configure logging
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("Starting Nuuly BigQuery MCP server")
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
