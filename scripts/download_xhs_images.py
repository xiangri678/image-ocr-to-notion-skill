#!/usr/bin/env python3
"""Download images exposed by a public Xiaohongshu share page."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
from pathlib import Path

HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131 Safari/537.36",
}


def initial_state(html: str) -> dict | None:
    match = re.search(r"window\.__INITIAL_STATE__\s*=\s*", html)
    if not match:
        return None
    start = html.find("{", match.end())
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(html)):
        character = html[index]
        if escaped:
            escaped = False
        elif quoted and character == "\\":
            escaped = True
        elif character == '"':
            quoted = not quoted
        elif not quoted and character == "{":
            depth += 1
        elif not quoted and character == "}":
            depth -= 1
            if depth == 0:
                return json.loads(re.sub(r"\bundefined\b", "null", html[start:index + 1]))
    return None


async def run(url: str, output_root: Path) -> Path:
    try:
        from curl_cffi.requests import AsyncSession
    except ImportError as exc:
        raise SystemExit(
            "Install the optional dependency with: python3 -m pip install curl-cffi"
        ) from exc

    async with AsyncSession(impersonate="chrome131") as session:
        await session.get("https://www.xiaohongshu.com/", headers=HEADERS, timeout=20)
        response = await session.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
        if response.status_code != 200:
            raise RuntimeError(f"public page returned HTTP {response.status_code}")
        state = initial_state(response.text)
        note_map = (state or {}).get("note", {}).get("noteDetailMap", {})
        if not note_map:
            raise RuntimeError("post data was not exposed by the public share page")

        note = next(iter(note_map.values())).get("note", {})
        title = note.get("title") or "xiaohongshu-post"
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", title).strip()[:80] or "xiaohongshu-post"
        target = output_root / safe_title
        target.mkdir(parents=True, exist_ok=True)

        downloaded = []
        for index, item in enumerate(note.get("imageList", []), 1):
            image_url = item.get("urlDefault") or item.get("url")
            if not image_url:
                image_url = next((info.get("url") for info in item.get("infoList", []) if info.get("url")), None)
            if not image_url:
                continue
            image_response = await session.get(image_url, headers={**HEADERS, "referer": "https://www.xiaohongshu.com/"}, timeout=30)
            image_response.raise_for_status()
            content_type = image_response.headers.get("content-type", "")
            suffix = ".webp" if "webp" in content_type else ".png" if "png" in content_type else ".jpg"
            destination = target / f"{index:02d}{suffix}"
            destination.write_bytes(image_response.content)
            downloaded.append(destination.name)

        metadata = {
            "title": title,
            "author": note.get("user", {}).get("nickname", ""),
            "description": note.get("desc", ""),
            "source_url": str(response.url),
            "downloaded_images": downloaded,
        }
        (target / "metadata.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
        if not downloaded:
            raise RuntimeError("the public page contained no downloadable images")
        return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="A public xhslink.com or xiaohongshu.com URL")
    parser.add_argument("--output", "-o", type=Path, default=Path.cwd() / "xhs-images")
    args = parser.parse_args()
    if not re.match(r"^https?://([^/]+\.)?(xhslink|xiaohongshu)\.com/", args.url):
        parser.error("provide a public xhslink.com or xiaohongshu.com URL")
    target = asyncio.run(run(args.url, args.output.expanduser().resolve()))
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
