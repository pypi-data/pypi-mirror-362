"""
Entry point for running the Nuuly Postgres MCP Server as a module.
"""

import logging
import sys
from . import run

def main():
    """Entry point for running the package as a module."""
    # Setup logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        stream=sys.stderr
    )
    
    # Run the MCP server
    try:
        run()
    except Exception as e:
        logging.error(f"Error running MCP server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
