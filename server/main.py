# server/main.py

from . import calculator          
from . import os_tools            
from . import security
from mcp.server.fastmcp import run_all_servers

if __name__ == "__main__":
    run_all_servers(transport="stdio")
