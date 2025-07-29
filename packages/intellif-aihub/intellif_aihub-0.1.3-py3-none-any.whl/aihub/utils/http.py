from __future__ import annotations

import httpx
import os


def http_download_file(url: str, dst_path: str, chunk: int = 1 << 16) -> None:
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with httpx.stream("GET", url, follow_redirects=True, timeout=None) as r:
        r.raise_for_status()
        with open(dst_path, "wb") as f:
            for block in r.iter_bytes(chunk):
                f.write(block)
