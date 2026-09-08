#!/usr/bin/env python3
"""Run the bundled Apple Vision OCR script on every image in a directory."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


SUPPORTED_SUFFIXES = {".webp", ".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff"}
VISION_SCRIPT = Path(__file__).with_name("macos_vision_ocr.swift")


def collect_images(image_dir: Path) -> list[Path]:
    return sorted(
        path for path in image_dir.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def run_vision(images: list[Path], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["swift", str(VISION_SCRIPT), *map(str, images)],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def convert_to_png(images: list[Path], target_dir: Path) -> list[Path]:
    converted: list[Path] = []
    for index, source in enumerate(images, 1):
        target = target_dir / f"{index:04d}-{source.stem}.png"
        result = subprocess.run(
            ["sips", "-s", "format", "png", str(source), "--out", str(target)],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
        if result.returncode == 0 and target.is_file():
            converted.append(target)
    return converted


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("--output", "-o", type=Path)
    parser.add_argument("--timeout", type=int, default=300)
    args = parser.parse_args()

    if sys.platform != "darwin":
        parser.error("Apple Vision OCR requires macOS")

    image_dir = args.image_dir.expanduser().resolve()
    if not image_dir.is_dir():
        parser.error(f"not a directory: {image_dir}")
    if not VISION_SCRIPT.is_file():
        parser.error(f"missing bundled script: {VISION_SCRIPT}")

    images = collect_images(image_dir)
    if not images:
        parser.error(f"no supported images in {image_dir}")

    try:
        result = run_vision(images, args.timeout)
    except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
        print(f"OCR failed: {exc}", file=sys.stderr)
        return 1

    if result.returncode != 0:
        with tempfile.TemporaryDirectory(prefix="image-ocr-") as temp:
            converted = convert_to_png(images, Path(temp))
            if not converted:
                print(result.stderr, file=sys.stderr)
                return result.returncode or 1
            result = run_vision(converted, args.timeout)

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        return result.returncode

    if args.output:
        output = args.output.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(result.stdout, encoding="utf-8")
        print(output)
    else:
        sys.stdout.write(result.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
