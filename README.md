# Image OCR to Notion Skill

[中文](README.zh-CN.md) | English

An Agent Skill for acquiring local or publicly shared images, running on-device OCR with macOS Vision, cleaning the text, and optionally saving it to an authorized Notion destination.

## Contents

- `SKILL.md`: end-to-end capture workflow and safety boundaries
- `scripts/`: public-page image downloader and local Vision OCR helpers
- `references/xiaohongshu.md`: public-link limitations and troubleshooting
- `agents/openai.yaml`: UI metadata

The OCR path runs locally. The optional public-link downloader requires `curl-cffi` and does not read browser cookies or bypass access controls.

## Use

Install this repository with an Agent Skills-compatible client, or copy it into your agent's skills directory. macOS 13 or later, Python 3, and Swift are required for OCR.

## Authorship

Created by Xiangri from a self-built Hermes Agent workflow. Xiaohongshu and Notion retain their own terms and licenses.

## License

[MIT](LICENSE)
