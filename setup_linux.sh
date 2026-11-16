#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

find_python3() {
    local candidate
    for candidate in "${PYTHON:-}" python3.12 python3 python; do
        [[ -n "$candidate" ]] || continue
        if command -v "$candidate" >/dev/null 2>&1 && \
            "$candidate" -c 'import sys; raise SystemExit(sys.version_info.major != 3 or sys.version_info.minor > 13)' >/dev/null 2>&1; then
            PYTHON="$(command -v "$candidate")"
            return 0
        fi
    done
    return 1
}

run_as_root() {
    if [[ "$EUID" -eq 0 ]]; then
        "$@"
    elif command -v sudo >/dev/null 2>&1; then
        sudo "$@"
    else
        echo "Python 3 is missing. Install it with your system package manager, then rerun this script." >&2
        exit 1
    fi
}

if ! find_python3; then
    if command -v apt-get >/dev/null 2>&1; then
        run_as_root apt-get update
        run_as_root apt-get install -y python3 python3-venv
    elif command -v dnf >/dev/null 2>&1; then
        run_as_root dnf install -y python3
    elif command -v yum >/dev/null 2>&1; then
        run_as_root yum install -y python3
    elif command -v pacman >/dev/null 2>&1; then
        run_as_root pacman -Sy --noconfirm python
    elif command -v zypper >/dev/null 2>&1; then
        run_as_root zypper --non-interactive install python3
    else
        echo "Python 3 is missing and no supported package manager was found." >&2
        exit 1
    fi

    if ! find_python3; then
        echo "Python installation completed, but Python 3 is still unavailable on PATH." >&2
        exit 1
    fi
fi

VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
if [[ -x "$VENV_PYTHON" ]] && ! "$VENV_PYTHON" -c 'import sys; raise SystemExit(sys.version_info.major != 3 or sys.version_info.minor > 13)' >/dev/null 2>&1; then
    echo "The existing .venv uses a Python version unsupported by this setup. Rename or remove .venv, then rerun this script." >&2
    exit 1
elif [[ ! -x "$VENV_PYTHON" ]]; then
    "$PYTHON" -m venv "$ROOT_DIR/.venv"
fi

"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r "$ROOT_DIR/Code/requirements.txt" pytest

export PYTHONPATH="$ROOT_DIR/Code${PYTHONPATH:+:$PYTHONPATH}"
export SDL_VIDEODRIVER=dummy
export SDL_AUDIODRIVER=dummy
"$VENV_PYTHON" -m pytest "$ROOT_DIR/Tests"

echo "Setup and tests completed. Start the game with: .venv/bin/python Code/main.py"