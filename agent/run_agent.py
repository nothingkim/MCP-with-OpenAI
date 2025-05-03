import asyncio, sys, os
from pathlib import Path
from agents import Agent, Runner
from agents.mcp import MCPServerStdio

os.environ["OPENAI_API_KEY"] = "sk-"

root   = Path(__file__).parent.parent
# srvdir no longer needed for module mode

calc_srv = MCPServerStdio(
    params={
        "command": sys.executable,
        "args": ["-X", "utf8", "-u", "-m", "server.calculator"],
        "cwd": str(root),
    },
    client_session_timeout_seconds=20,
    name="calculator",
)


os_srv = MCPServerStdio(
    params={
        "command": sys.executable,
        "args": ["-X", "utf8", "-u", "-m", "server.os_tools"],
        "cwd": str(root),
    },
    client_session_timeout_seconds=20,
    name="os",
)

agent = Agent(
    name="Local Buddy",
    model="gpt-4.1-nano",
    instructions="계산은 calculator, OS 동작은 os 툴을 사용해라.",
)

async def main():
    async with calc_srv, os_srv:
        agent.mcp_servers = [calc_srv, os_srv]
        while True:
            query = input("🧑 ")                 # My questions
            if query.lower() in ("exit", "quit"):
                break
            res = await Runner.run(agent, query)
            print("🤖", res.final_output)       # AI's answer

if __name__=="__main__":
    asyncio.run(main())
