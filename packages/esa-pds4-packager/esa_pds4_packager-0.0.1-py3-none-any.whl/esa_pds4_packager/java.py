import os
import shutil
import subprocess


def is_java_available():
    """Check if Java is executable on the current system and NO_JAVA is not set."""
    if os.environ.get("NO_JAVA") is not None:
        return False
    try:
        java_path = shutil.which("java")
        if java_path is None:
            return False
        result = subprocess.run(
            [java_path, "-version"],
            check=False,
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False
