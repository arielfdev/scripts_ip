"""Ping-related helpers."""

import subprocess


def ping_ip(ip: str) -> bool:
    """Return whether a Windows ping request receives a response."""
    command = ["ping", "-n", "1", "-w", "300", ip]

    try:
        # Windows ping uses -n for the echo count and -w for the timeout in ms.
        result = subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=2,
        )
    except (OSError, subprocess.TimeoutExpired):
        # Missing ping executable or an unexpected stalled process means no answer.
        return False

    # Windows returns exit code 0 when the target answers the echo request.
    return result.returncode == 0
