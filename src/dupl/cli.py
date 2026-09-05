import argparse
import subprocess
import sys

CHECKS: dict[str, list[str]] = {
    "ruff format": ["uv", "run", "ruff", "format", "--check", "."],
    "ruff check": ["uv", "run", "ruff", "check", "."],
    "mypy": ["uv", "run", "mypy", "."],
}

FIX_CHECKS: dict[str, list[str]] = {
    "ruff check": ["uv", "run", "ruff", "check", "--fix", "."],
    "ruff format": ["uv", "run", "ruff", "format", "."],
    "mypy": ["uv", "run", "mypy", "."],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    checks = FIX_CHECKS if args.fix else CHECKS

    failed: list[str] = []
    for name, command in checks.items():
        print(f"\n=== {name} ===", flush=True)
        if subprocess.run(command, check=False).returncode:  # noqa: S603 -- commands are hardcoded, not untrusted input
            failed.append(name)

    print("\n=== Summary ===", flush=True)
    if failed:
        print(f"FAILED: {', '.join(failed)}")
        return 1
    print(f"passed: {', '.join(checks)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
