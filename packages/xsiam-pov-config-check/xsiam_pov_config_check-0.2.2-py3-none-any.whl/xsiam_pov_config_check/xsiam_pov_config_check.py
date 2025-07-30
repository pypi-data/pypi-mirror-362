#!/usr/bin/env python3

from __future__ import annotations

import json
import shutil
import sys
import tarfile
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import List

_CHUNK = 1 << 20  # 1 MiB


def load_config(path: Path) -> dict:
    try:
        with path.open(encoding="utf-8") as fp:
            return json.load(fp)
    except FileNotFoundError:
        sys.exit(f"ERROR: {path} not found")
    except PermissionError:
        sys.exit(f"ERROR: permission denied for {path}")
    except json.JSONDecodeError as err:
        sys.exit(f"ERROR: {path}: {err.msg} at line {err.lineno} column {err.colno}")
    except OSError as err:
        sys.exit(f"ERROR: I/O error while reading {path}: {err}")


def _save_to_temp(rsp: urllib.request.addinfourl) -> Path:
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        shutil.copyfileobj(rsp, tmp, length=_CHUNK)
    finally:
        tmp.close()
    return Path(tmp.name)


def _url_required(obj: dict, obj_type: str, errors: List[str]) -> str | None:
    url = obj.get("url")
    if url:
        return url

    identifier = obj.get("id") or obj.get("name") or "<unknown>"
    errors.append(f"ERROR: missing 'url' for {obj_type} {identifier}")
    return None


def _check_reachable(url: str, errors: List[str]) -> None:
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            if resp.status != 200:
                errors.append(f"ERROR: {url} returned status {resp.status}")
                return


            path_part = Path(urllib.parse.urlparse(url).path.lower())
            suffixes = path_part.suffixes
            is_zip = path_part.suffix == ".zip"
            is_targz = suffixes[-2:] == [".tar", ".gz"] or path_part.suffix == ".tgz"
            if not (is_zip or is_targz):
                return

            temp_path = _save_to_temp(resp)

        try:
            ok = verify_zip(temp_path) if is_zip else verify_tar(temp_path)
            if not ok:
                errors.append(f"ERROR: corrupt archive at {url}")
        finally:
            temp_path.unlink(missing_ok=True)

    except Exception as exc:
        errors.append(f"ERROR: cannot download {url}: {exc}")


def verify_zip(path: Path) -> bool:
    try:
        if not zipfile.is_zipfile(path):
            return False
        with zipfile.ZipFile(path) as zf:
            return zf.testzip() is None  # None ⇒ every member OK
    except (zipfile.BadZipFile, OSError):
        return False


def verify_tar(path: Path) -> bool:
    if not tarfile.is_tarfile(path):
        return False

    try:
        with tarfile.open(path, "r:*") as tf:  # auto‑detect compression
            for member in tf.getmembers():
                if not member.isreg():  # skip dirs, links, etc.
                    continue
                fh = tf.extractfile(member)
                if fh is None:
                    continue
                while fh.read(_CHUNK):  # drain payload
                    pass
        return True
    except (tarfile.TarError, OSError):
        return False


def validate_urls(cfg: dict) -> List[str]:
    errors: List[str] = []

    # custom_packs
    for pack in cfg.get("custom_packs", []):
        url = _url_required(pack, "custom_packs", errors)
        if url:
            _check_reachable(url, errors)

    # pre_config_docs
    for pack in cfg.get("pre_config_docs", []):
        url = _url_required(pack, "pre_config_docs", errors)
        if url:
            _check_reachable(url, errors)

    # post_config_docs
    for pack in cfg.get("post_config_docs", []):
        url = _url_required(pack, "post_config_docs", errors)
        if url:
            _check_reachable(url, errors)

    # lookup_datasets
    for ds in cfg.get("lookup_datasets", []):
        url = ds.get("url")
        if url:
            _check_reachable(url, errors)

    return errors


def main() -> None:
    cfg_path = Path("xsoar_config.json")
    config = load_config(cfg_path)

    errors = validate_urls(config)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        sys.exit(1)

    print(
        f"OK: {cfg_path} is valid JSON, all required URLs are reachable, "
        f"and any ZIP/tar.gz archives passed integrity checks",
        file=sys.stdout,
    )


if __name__ == "__main__":
    main()
