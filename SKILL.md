---
name: image-ocr-to-notion
description: Download images from a public Xiaohongshu share link or accept local images, run private on-device OCR on macOS, clean the extracted text, and save it to Notion after explicit approval.
license: MIT
metadata:
  author: Xiangri
  version: "1.0.0"
  compatibility: macOS 13 or later with Python 3 and Swift; optional curl-cffi for public Xiaohongshu links and a configured Notion integration for saving.
  hermes:
    tags: [ocr, notion, xiaohongshu, macos, knowledge-capture]
---

# Image OCR to Notion

[中文说明](SKILL.zh-CN.md) | English

Capture text from local images or a public Xiaohongshu share link, clean it without inventing facts, and optionally save the result to Notion.

## Route the request

- Local images or a directory: start with on-device OCR.
- Public Xiaohongshu share link: download the post images, then run OCR.
- Existing OCR text: skip extraction and start with cleanup.
- A requested Notion destination: prepare the page, show a concise preview, and write only after the user authorizes the external change.

Do not retrieve cookies, tokens, or browser data from a real browser profile. Do not bypass login, anti-bot, or access controls. Stop when a public share link no longer exposes the post.

## 1. Acquire images

For local input, resolve and validate every image path. For a public Xiaohongshu link, install the optional dependency in an isolated environment, then run:

```bash
python3 scripts/download_xhs_images.py "<public-share-url>" --output "<output-directory>"
```

The downloader creates one folder containing numbered images and `metadata.json`. Review [references/xiaohongshu.md](references/xiaohongshu.md) when the link fails or the request raises access or copyright questions.

## 2. Run local OCR

```bash
python3 scripts/ocr_images.py "<image-directory>" --output "<ocr-output.txt>"
```

This calls Apple Vision locally. Images are processed in filename order. The command does not upload images to an OCR service.

## 3. Clean the text

Preserve the source meaning and structure:

- join obvious OCR line breaks;
- correct errors only when the image or context makes the correction clear;
- retain headings, lists, quotations, names, numbers, and URLs;
- mark uncertain text instead of guessing;
- remove navigation chrome and isolated recognition noise.

Keep the raw OCR file alongside the cleaned result so later corrections remain traceable.

## 4. Save to Notion

Use the Notion MCP, CLI, or API already available in the target environment. Never embed credentials or database IDs in the skill. Resolve configuration from the user's environment, such as `NOTION_API_TOKEN` and `NOTION_DATABASE_ID`, or ask the user to choose a destination.

Before writing, show the proposed title, destination, source URL, and a short content preview. After authorization:

1. Create or append the page.
2. Preserve the source URL and capture date.
3. Read the page back and verify its title and representative content.
4. Report the confirmed page URL and any omitted or uncertain text.

## Completion checks

- The raw OCR and cleaned text are both available.
- No browser profile, browser cookie, or private token was read.
- The cleaned text contains no unsupported additions.
- Any Notion mutation was authorized and read back.

See [examples/README.md](examples/README.md) for local-image and public-share-link command sequences.
