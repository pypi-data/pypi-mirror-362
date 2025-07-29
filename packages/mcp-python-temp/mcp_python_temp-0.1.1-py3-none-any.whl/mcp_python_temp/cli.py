"""
Embedded Python MCP server – macOS friendly (no setrlimit crash)
"""

import importlib
import pathlib
import re
import subprocess
import io, os, signal, traceback, sys, platform
from contextlib import redirect_stdout
from typing import Annotated, Dict, List, Optional, TypedDict
import importlib.metadata as md

from mcp.server.fastmcp import FastMCP

IS_WINDOWS = platform.system() == "Windows"
if not IS_WINDOWS:
    import resource
mcp = FastMCP("LocalPython")  # display name만이니 아무 문자열도 OK
LIB_DIR = pathlib.Path(__file__).parent / "libs"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))


def _installed_pkgs(max_len: int = 20) -> str:
    names = sorted(
        {
            d.metadata["Name"]
            for d in md.distributions()
            if str(LIB_DIR) in d.locate_file("").as_posix()
        }
    )
    head = ", ".join(names[:max_len])
    return head + (" …" if len(names) > max_len else "") or "none"


PKG_LIST = f"\n\n**Installed packages**: {_installed_pkgs()}"


class RunResult(TypedDict, total=False):
    stdout: str
    result: object
    saved_files: List[str]
    error: str


# ───────────────────── sandbox helpers ──────────────────────────
if not IS_WINDOWS:
    _ORIG_LIMITS_AS = resource.getrlimit(resource.RLIMIT_AS)
    _ORIG_LIMITS_DATA = resource.getrlimit(resource.RLIMIT_DATA)


def _try_set_limit(which: int, bytes_: int) -> bool:
    if IS_WINDOWS:
        return
    """soft 제한만 bytes_ 로 낮추고 실패면 False 반환."""
    soft, hard = resource.getrlimit(which)
    new_soft = min(bytes_, hard if hard != resource.RLIM_INFINITY else bytes_)
    try:
        resource.setrlimit(which, (new_soft, hard))
        return True
    except (ValueError, OSError):
        return False


def _sandbox_limits(timeout: int, mem_mb: int = 1024) -> None:
    """SIGALRM + 메모리 soft limit (실패해도 무시)."""
    if IS_WINDOWS:
        sys.stderr.write("[run_python] INFO: sandbox limits not applied on Windows\n")
        return
    # 1) 타임아웃
    signal.signal(
        signal.SIGALRM, lambda *_: (_ for _ in ()).throw(TimeoutError("timeout"))
    )
    signal.alarm(timeout)

    # 2) 메모리 제한 – best-effort
    want_bytes = mem_mb << 20
    ok = False
    if _try_set_limit(resource.RLIMIT_AS, want_bytes):
        ok = True
    elif platform.system() == "Darwin":  # macOS에서는 RLIMIT_DATA로 재시도
        ok = _try_set_limit(resource.RLIMIT_DATA, want_bytes)

    if not ok:
        # 제한을 걸지 못했어도 계속 진행 – 로그만 남겨 둠(선택)
        sys.stderr.write("[run_python] WARN: memory limit not applied\n")


def _clear_limits() -> None:
    if IS_WINDOWS:
        return
    """알람 + (선택) RLIMIT 원복."""
    signal.alarm(0)
    # 원복이 굳이 필요 없으면 아래 두 줄은 생략 가능
    resource.setrlimit(resource.RLIMIT_AS, _ORIG_LIMITS_AS)
    resource.setrlimit(resource.RLIMIT_DATA, _ORIG_LIMITS_DATA)


FORBIDDEN = {"subprocess", "os.system", "shutil.rmtree"}


# ───────────────────── MCP tool ────────────────────────────────


# ───── 1) 차단(블랙리스트) 패키지 ──────────────────────────────────────
DENY = {
    "tensorflow",
    "torch",
    "torchvision",  # 초대형
    "selenium",
    "subprocess32",  # 보안 위험
}

# ───── 2) 패키지명 유효성 정규식 ─────────────────────────────────────
SAFE_RE = re.compile(r"^[A-Za-z0-9._-]+(==[A-Za-z0-9._-]+)?$")


@mcp.tool(
    name="pip_install",
    description="Install one or more PyPI packages into the embedded runtime "
    "(already-installed packages are skipped).",
)
def pip_install(
    packages: Annotated[
        str | List[str], "One or more package specs, e.g. 'PyPDF2 pandas==2.2.2'"
    ],
) -> Dict[str, object]:
    """
    Parameters
    ----------
    packages : str | list[str]
        • 'PyPDF2 pandas'          ← 공백/쉼표 구분
        • ['PyPDF2', 'pandas==2.2.2']

    Returns
    -------
    { ok: bool, installed: list[str], skipped: list[str], error?: str }
    """

    # ── ① 입력 파싱 ────────────────────────────────────────────────
    if isinstance(packages, str):
        pkgs = re.split(r"[,\s]+", packages.strip())
    else:
        pkgs = list(packages)
    pkgs = [p for p in pkgs if p]  # 빈 문자열 제거

    # ── ② 유효성 · 블랙리스트 검사 ─────────────────────────────────
    bad_format = [p for p in pkgs if not SAFE_RE.fullmatch(p)]
    denied = [p for p in pkgs if p.split("==")[0].lower() in DENY]
    if bad_format:
        return {"ok": False, "error": f"invalid name: {', '.join(bad_format)}"}
    if denied:
        return {"ok": False, "error": f"denied: {', '.join(denied)}"}

    # ── ③ 이미 설치돼 있는지 확인 ─────────────────────────────────
    missing, skipped = [], []
    for spec in pkgs:
        base, *ver = spec.split("==")
        try:
            cur_ver = md.version(base)
            if ver and cur_ver != ver[0]:
                # 버전이 다른 경우는 업그레이드 대상으로 분류
                missing.append(spec)
            else:
                skipped.append(spec)
        except md.PackageNotFoundError:
            missing.append(spec)

    # ── ④ 실제 pip install (필요할 때만) ────────────────────────────
    if missing:
        try:
            subprocess.check_call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    *missing,
                    "-t",
                    str(LIB_DIR),
                    "--upgrade",
                    "--quiet",
                ]
            )
            importlib.invalidate_caches()
            if str(LIB_DIR) not in sys.path:  # ← 추가
                sys.path.insert(0, str(LIB_DIR))
        except subprocess.CalledProcessError as e:
            return {"ok": False, "error": str(e), "installed": [], "skipped": skipped}

    return {"ok": True, "installed": missing, "skipped": skipped}


@mcp.tool(
    name="run_python",
    description=(
        "A tool that runs the Python code you write and receives the results."
        "When writing in function form, you need to write the code up to the function call part to get results."
        "Don't write code based on assumptions (columns that don't exist, functions that don't exist, etc.)."
        "Use run_python whenever the user’s goal can be met by Python code execution e.g. data analysis, visualization, file processing, etc."
        "You can see the results of the run via print or the result variable."
        "When writing an exception, make sure you can pinpoint the error."
        f"{PKG_LIST}. However, you will need to import the packages you want to use in your code."
    ),
)
def run_python(
    code: str, timeout_sec: int = 30, files: Optional[list[str]] = None
) -> RunResult:
    _sandbox_limits(timeout_sec)
    buf, g = io.StringIO(), {"FILES": files or []}

    try:
        if any(bad in code for bad in FORBIDDEN):
            # ① 금칙어 감지는 예외로 변경
            raise ValueError(f"Use of forbidden module in code: {FORBIDDEN}")

        # ② 실제 실행
        with redirect_stdout(buf):
            exec(compile(code, "<user_code>", "exec", optimize=2), g)

        return {
            "stdout": buf.getvalue(),
            "result": g.get("result", {}),
        }

    except Exception as e:
        # ③ stdout + traceback 을 합쳐서 RuntimeError 로 재발생
        err_msg = traceback.format_exc()
        raise RuntimeError(
            f"{err_msg}\n\n--- Captured stdout ---\n{buf.getvalue()}"
        ) from e  # ← FastMCP 가 isError=true 로 래핑

    finally:
        _clear_limits()

def main() -> None:
    """uvx mcp-python … 으로 실행되는 진입점."""
    mcp.run(transport="stdio")

if __name__ == "__main__":   # pip install 후 직접 호출도 가능
    main()