# list_tools.py
import asyncio
import sys
import os
import traceback
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).parent

async def test(name: str, module_name: str):
    print(f"\n--- Testing {name} server ---")
    # 환경 복사 + UTF-8 강제
    env = os.environ.copy()
    env["PYTHONUTF8"] = "1"

    # stdio transport 파라미터: -m server.<module_name>
    params = StdioServerParameters(
        command=sys.executable,
        args=["-X", "utf8", "-u", "-m", f"server.{module_name}"],
        cwd=str(PROJECT_ROOT),  # 여기서는 project root
        env=env,
    )

    try:
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as session:
                await session.initialize()
                result = await session.list_tools()
                # paging 응답이면 내부 'tools' 추출
                if isinstance(result, dict) and "tools" in result:
                    entries = result["tools"]
                else:
                    entries = result

                names = []
                for t in entries:
                    if isinstance(t, dict) and "name" in t:
                        names.append(t["name"])
                    elif isinstance(t, (list, tuple)) and len(t) >= 1:
                        names.append(t[0])
                    else:
                        names.append(repr(t))

                print(f"{name} tools →", names)
    except Exception as e:
        print(f"{name} ERROR → {e!r}")
        traceback.print_exc()

async def main():
    await test("calculator", "calculator")
    await test("os_tools",  "os_tools")

if __name__=="__main__":
    asyncio.run(main())
