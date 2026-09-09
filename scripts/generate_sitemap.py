#!/usr/bin/env python3
"""Gera sitemap.xml somente com páginas HTML canônicas e indexáveis."""

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://credituz.ai/"


class HeadMetadata(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.noindex = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "link" and "canonical" in values.get("rel", "").split():
            self.canonical = values.get("href")
        if tag == "meta" and values.get("name", "").lower() == "robots":
            self.noindex = "noindex" in values.get("content", "").lower()


def public_url(path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    if relative == "index.html":
        return SITE
    if relative == "en/index.html":
        return SITE + "en/"
    return SITE + relative


def candidates():
    yield ROOT / "index.html"
    yield ROOT / "white-label.html"
    yield from sorted((ROOT / "pages").rglob("*.html"))
    yield from sorted((ROOT / "en").rglob("*.html"))


def is_canonical(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    metadata = HeadMetadata()
    metadata.feed(html)
    if metadata.noindex:
        return False
    if not metadata.canonical:
        return True
    declared = urljoin(public_url(path), metadata.canonical).rstrip("/")
    expected = public_url(path).rstrip("/")
    return declared == expected


def render() -> str:
    urls = []
    seen = set()
    for path in candidates():
        if not path.exists() or not is_canonical(path):
            continue
        url = public_url(path)
        if url not in seen:
            seen.add(url)
            urls.append(url)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    lines.extend(f"  <url><loc>{url}</loc></url>" for url in urls)
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "sitemap.xml"
    generated = render()
    if args.check:
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        if current != generated:
            raise SystemExit("sitemap.xml desatualizado; rode python3 scripts/generate_sitemap.py")
        print("sitemap.xml está sincronizado")
        return
    target.write_text(generated, encoding="utf-8")
    print(f"sitemap.xml gerado com {generated.count('<url>')} URLs")


if __name__ == "__main__":
    main()
