import time, json, pathlib, os, re
from functools import wraps

ACL = {
    "guest": {"list_dir", "cpu_usage", "open_chrome"},
    "nothingKim": {"list_dir", "cpu_usage", "open_chrome"},   # your login
    "power": {"*"},
    "admin": {"*"},
}
ALLOW_URL  = re.compile(r".*")
ALLOW_CMD = {"ipconfig", "dir", "netstat"}
AUDIT_PATH = pathlib.Path("audit.log")

def _user() -> str:
    return os.getlogin()

def _audit(rec: dict):
    rec["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
    AUDIT_PATH.write_text(json.dumps(rec, ensure_ascii=False) + "\n", encoding="utf-8", append=True)

def secure(tool_name: str, *, url=False, shell=False):
    def deco(fn):
        @wraps(fn)
        def wrapper(*args, **kw):
            user = _user()
            allow = ACL.get(user, set())
            if "*" not in allow and tool_name not in allow:
                _audit({"user": user, "tool": tool_name, "result": "DENY"})
                raise PermissionError(f"{user} cannot run {tool_name}")
            if url and not ALLOW_URL.match(kw.get("url", "")):
                _audit({"user": user, "tool": tool_name, "result": "BLOCK_URL"})
                raise ValueError("URL not allowed")
            if shell and kw.get("cmd", "").split()[0] not in ALLOW_CMD:
                _audit({"user": user, "tool": tool_name, "result": "BLOCK_CMD"})
                raise ValueError("Command not allowed")
            res = fn(*args, **kw)
            _audit({"user": user, "tool": tool_name, "args": kw, "result": "OK"})
            return res
        return wrapper
    return deco
