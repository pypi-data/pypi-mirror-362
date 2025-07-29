import subprocess


def get_default_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "config", "--get", "init.defaultBranch"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass
    return "master"
