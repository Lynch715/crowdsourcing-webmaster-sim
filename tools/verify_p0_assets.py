#!/usr/bin/env python3
"""Verify the complete art-asset contract and write checksums."""

import hashlib
from pathlib import Path

from PIL import Image

from build_p0_assets import ASSETS, ROOT


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    failures: list[str] = []
    checksum_lines: list[str] = []
    expected_paths = set(ASSETS)
    actual_paths = {
        path.relative_to(ROOT / "assets").as_posix()
        for category in ("char", "bg", "event", "ui")
        for path in (ROOT / "assets" / category).rglob("*.png")
    }
    if len(ASSETS) != 36:
        failures.append(f"MANIFEST_COUNT {len(ASSETS)} != 36")
    for relative in sorted(expected_paths - actual_paths):
        failures.append(f"MISSING_FROM_RUNTIME {relative}")
    for relative in sorted(actual_paths - expected_paths):
        failures.append(f"UNEXPECTED_RUNTIME_FILE {relative}")

    digest_paths: dict[str, list[str]] = {}

    for relative, (_, expected_size, expected_alpha) in ASSETS.items():
        path = ROOT / "assets" / relative
        if not path.exists():
            failures.append(f"MISSING {relative}")
            continue
        with Image.open(path) as image:
            if image.size != expected_size:
                failures.append(
                    f"SIZE {relative}: {image.size} != {expected_size}"
                )
            has_alpha = image.mode in {"RGBA", "LA"} or "transparency" in image.info
            if has_alpha != expected_alpha:
                failures.append(
                    f"ALPHA {relative}: {has_alpha} != {expected_alpha}"
                )
            if expected_alpha:
                alpha = image.convert("RGBA").getchannel("A")
                low, high = alpha.getextrema()
                if low == high == 255:
                    failures.append(f"OPAQUE_ALPHA {relative}")
        digest = sha256(path)
        digest_paths.setdefault(digest, []).append(relative)
        checksum_lines.append(f"{digest}  {relative}")

    for relatives in digest_paths.values():
        if len(relatives) > 1:
            failures.append(f"DUPLICATE_CONTENT {', '.join(relatives)}")

    checksum_path = ROOT / "assets/CHECKSUMS.sha256"
    checksum_path.write_text("\n".join(checksum_lines) + "\n", encoding="utf-8")

    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(ASSETS)} assets; exact dimensions and alpha contract verified")


if __name__ == "__main__":
    main()
