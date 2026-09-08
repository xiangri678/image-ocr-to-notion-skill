# 图片 OCR 整理到 Notion Skill

中文 | [English](README.md)

读取本地图片或公开分享的图片，在 macOS 上使用 Vision 本地 OCR，清理识别文本，并可按用户授权保存到 Notion。

## 仓库内容

- `SKILL.md`：完整采集流程与安全边界
- `SKILL.zh-CN.md`：中文 Skill 说明
- `scripts/`：公开页面图片下载与本地 Vision OCR 脚本
- `references/xiaohongshu.md`：小红书公开链接限制和排障方法
- `examples/`：本地截图和公开分享链接的完整命令示例
- `agents/openai.yaml`：界面元数据

OCR 在本机运行。公开链接下载脚本可选依赖 `curl-cffi`，不会读取浏览器 Cookie，也不会绕过访问控制。

## 使用

通过兼容 Agent Skills 的客户端安装本仓库，或将仓库复制到 Agent 的 Skills 目录。OCR 需要 macOS 13 或更高版本、Python 3 与 Swift。

本地截图与小红书公开链接的完整示例见 [`examples/README.md`](examples/README.md)。

## 作者

由 Xiangri 根据自己构建的 Hermes Agent 工作流整理。小红书和 Notion 仍遵循各自的条款与许可证。

## 许可证

[MIT](LICENSE)
