# 使用示例 / Examples

## 本地截图

```bash
python3 scripts/ocr_images.py ./screenshots --output /tmp/ocr-raw.txt
```

然后调用 Agent：

> 使用 `$image-ocr-to-notion` 清理 `/tmp/ocr-raw.txt`，保留不确定文字标记和来源图片顺序。先展示 Notion 页面预览，获得授权后写入并回读。

## 小红书公开分享链接

```bash
python3 -m pip install curl-cffi
python3 scripts/download_xhs_images.py 'https://www.xiaohongshu.com/...' --output /tmp/xhs-images
python3 scripts/ocr_images.py /tmp/xhs-images --output /tmp/xhs-ocr-raw.txt
```

预期产物：编号图片、`metadata.json`、原始 OCR、清理后的文本，以及在用户授权时创建并回读的 Notion 页面。公开页面需要登录或验证时立即停止。

English:

> Use `$image-ocr-to-notion` to OCR these local images, preserve uncertain text, preview the proposed Notion page, and write only after authorization.
