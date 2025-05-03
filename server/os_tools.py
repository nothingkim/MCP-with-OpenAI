from pathlib import Path
import subprocess, psutil, sys
from mcp.server.fastmcp import FastMCP
from .security import secure   
mcp = FastMCP("os")

@mcp.tool()
@secure("list_dir")
def list_dir(path: str = ".") -> list[str]:
    return [p.name for p in Path(path).iterdir()]

@mcp.tool()
@secure("open_chrome")
def open_chrome(url: str = "about:blank", incognito: bool = False) -> str:
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    args = [chrome, url] + (["--incognito"] if incognito else [])
    subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     close_fds=(sys.platform!="win32"))
    return f"Chrome launched with {url}"

@mcp.tool()
@secure("cpu_usage")
def cpu_usage() -> float:
    return psutil.cpu_percent(interval=1)

@mcp.tool()
@secure("mem_usage")
def mem_usage() -> dict:
    v = psutil.virtual_memory()
    return {"total": v.total, "used": v.used, "percent": v.percent}

# add some features if you want

if __name__ == "__main__":
    # debug: confirm this file actually launched
    print("  os_tools MCP server starting…", flush=True)
    mcp.run(transport="stdio")
