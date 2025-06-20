#!/usr/bin/env python
import warnings
import os
import subprocess
import sys
import ensurepip
from code_monkeys.flows.engineering_flow import kickoff as flow_kickoff

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

os.environ.setdefault("CHROMA_TELEMETRY_ENABLED", "false")

# Load product requirements from a dedicated text file so that they can be
# edited without touching the Python code. The file lives at project root.
try:
    with open("project_requirements.txt", "r", encoding="utf-8") as _req_file:
        requirements = _req_file.read().strip()
except FileNotFoundError as exc:
    raise FileNotFoundError(
        "project_requirements.txt not found. Please create the file with your product description."
    ) from exc


def _bootstrap_pip() -> None:
    """Ensure `pip` is available in the current Python environment.

    Some minimal venvs are created with --without-pip, which breaks the
    agent-generated code that expects to install dependencies at runtime.
    We attempt to restore pip using the standard library's *ensurepip*; if
    that fails (very rare), we fall back to the get-pip.py bootstrap script.
    """
    try:
        import pip  # type: ignore  # noqa: F401 – just a presence check
        return  # pip already present
    except ModuleNotFoundError:
        pass  # proceed with bootstrap

    try:
        # Try the standard library helper first
        ensurepip.bootstrap()
    except Exception:  # pragma: no cover – ensurepip missing or failed
        import urllib.request, tempfile, os
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        with urllib.request.urlopen(get_pip_url) as resp, tempfile.NamedTemporaryFile(delete=False, suffix="_getpip.py") as tmp:
            tmp.write(resp.read())
            tmp_path = tmp.name
        subprocess.check_call([sys.executable, tmp_path])
        os.unlink(tmp_path)

    # Finally, upgrade pip to the latest stable version
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])


def run():
    """
    Run the code monkeys crew.
    """
    # Bootstrap packaging tools first (suggestion 5)
    _bootstrap_pip()

    # Inputs now require only the requirements; naming is handled by the architect.
    inputs = {
        'requirements': requirements,
    }

    # Run the high-level flow (handles naming + crew orchestration)
    flow_kickoff(**inputs)


if __name__ == "__main__":
    run()
