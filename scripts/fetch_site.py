#!/usr/bin/env python3

from __future__ import annotations

import html
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


ROOT = "https://nikko-indonesia.co.id/"
SITEMAP_URL = urljoin(ROOT, "wp-sitemap-posts-page-1.xml")
OUT_DIR = Path("source-download")
PAGES_DIR = OUT_DIR / "pages"
ASSETS_DIR = OUT_DIR / "assets"


def fetch(url: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        return response.read()


def page_name(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/")
    return "home" if not path else path.replace("/", "__")


def file_name_from_url(url: str) -> str:
    parsed = urlparse(url)
    name = Path(parsed.path).name
    return name or "asset.bin"


def collect_page_urls(sitemap_xml: str) -> list[str]:
    urls = re.findall(r"<loc>(.*?)</loc>", sitemap_xml)
    return [html.unescape(url.strip()) for url in urls]


def collect_asset_urls(page_html: str, page_url: str) -> set[str]:
    candidates: set[str] = set()
    patterns = [
        r'<img[^>]+src=["\']([^"\']+)["\']',
        r'srcset=["\']([^"\']+)["\']',
        r'url\(([^)]+)\)',
    ]

    for pattern in patterns:
        for match in re.findall(pattern, page_html, flags=re.IGNORECASE):
            if pattern.endswith("srcset=[\"\\']([^\"\\']+)[\"\\']"):
                parts = [part.strip().split(" ")[0] for part in match.split(",")]
            else:
                parts = [match.strip().strip("'\"")]

            for part in parts:
                if not part or part.startswith("data:"):
                    continue
                asset_url = urljoin(page_url, part)
                if "/wp-content/" in asset_url or asset_url.endswith(
                    (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg")
                ):
                    candidates.add(asset_url)

    return candidates


def main() -> None:
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)

    sitemap_xml = fetch(SITEMAP_URL).decode("utf-8", errors="ignore")
    urls = collect_page_urls(sitemap_xml)

    all_assets: set[str] = set()

    for url in urls:
        raw_html = fetch(url).decode("utf-8", errors="ignore")
        (PAGES_DIR / f"{page_name(url)}.html").write_text(raw_html, encoding="utf-8")
        all_assets.update(collect_asset_urls(raw_html, url))

    for asset_url in sorted(all_assets):
        try:
            target = ASSETS_DIR / file_name_from_url(asset_url)
            if target.exists():
                continue
            target.write_bytes(fetch(asset_url))
        except Exception as exc:
            print(f"skip asset: {asset_url} ({exc})")

    print(f"saved {len(urls)} pages")
    print(f"saved up to {len(all_assets)} asset references")


if __name__ == "__main__":
    main()
