#!/usr/bin/env python3
"""Validate xsoar_config.json and ensure custom pack URLs are reachable (GET only)."""
import json
import sys
import urllib.request
from pathlib import Path


def load_config(path: Path):
    """Read and parse JSON config file."""
    try:
        with path.open(encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        sys.exit(f"ERROR: {path} not found")
    except PermissionError:
        sys.exit(f"ERROR: permission denied for {path}")
    except json.JSONDecodeError as err:
        sys.exit(
            f"ERROR: {path}: {err.msg} at line {err.lineno} column {err.colno}"
        )
    except OSError as err:
        sys.exit(f"ERROR: I/O error while reading {path}: {err}")


def validate_urls(custom_packs):
    """Return a list of error strings for unreachable or missing URLs."""
    errors = []
    for pack in custom_packs:
        url = pack.get("url")
        if not url:
            errors.append(
                f"ERROR: missing 'url' for custom pack {pack.get('id', '<unknown>')}"
            )
            continue
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                if resp.status != 200:
                    errors.append(f"ERROR: {url} returned status {resp.status}")
        except Exception as exc:
            errors.append(f"ERROR: cannot download {url}: {exc}")
    return errors


def main() -> None:
    cfg_path = Path("xsoar_config.json")
    config = load_config(cfg_path)
    errors = validate_urls(config.get("custom_packs", []))

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    print(
        f"OK: {cfg_path} is valid JSON and all custom pack URLs are reachable",
        file=sys.stdout,
    )


if __name__ == "__main__":
    main()
