# Public Xiaohongshu links

Use only content exposed by a public share link that the user supplied or is authorized to archive.

The downloader opens the public page, follows an `xhslink.com` redirect when needed, reads `window.__INITIAL_STATE__`, and downloads the image URLs listed in the page state. It creates a temporary, anonymous web session; it does not read a browser profile or a logged-in account.

Stop and report the limitation when:

- the link requires login or a verification challenge;
- the page state does not contain the post;
- the post has been removed or restricted;
- the user has not established a legitimate reason to copy non-public content.

Do not add copied browser cookies, hard-coded share tokens, request signatures, or credential extraction instructions as fallbacks.
