import sys
import subprocess


def main():
    cmd = [sys.executable, "-m", "poetry", "clovers"] + sys.argv[1:]
    try:
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode})", file=sys.stderr)
        return e.returncode
    except FileNotFoundError:
        return 127
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
