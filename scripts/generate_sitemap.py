#!/usr/bin/env python3
"""Gera sitemap.xml somente com páginas HTML canônicas e indexáveis."""

import argparse
import datetime
import re
import subprocess
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


LASTMOD_RE = re.compile(r"<loc>([^<]+)</loc><lastmod>(\d{4}-\d{2}-\d{2})</lastmod>")
LOC_RE = re.compile(r"<loc>([^<]+)</loc>")


def has_full_history() -> bool:
    """Checkout raso (CI de deploy) dá a todos os arquivos a data do HEAD."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "rev-parse", "--is-shallow-repository"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return False
    return out == "false"


def git_date(path: Path):
    """Data (AAAA-MM-DD) do último commit que tocou o arquivo, ou None."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "log", "-1", "--format=%cs", "--",
             path.relative_to(ROOT).as_posix()],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return out or None


def current_lastmods() -> dict:
    target = ROOT / "sitemap.xml"
    if not target.exists():
        return {}
    return dict(LASTMOD_RE.findall(target.read_text(encoding="utf-8")))


def collect():
    entries = []
    seen = set()
    for path in candidates():
        if not path.exists() or not is_canonical(path):
            continue
        url = public_url(path)
        if url not in seen:
            seen.add(url)
            entries.append((url, path))
    return entries


def render() -> str:
    """lastmod vem do git quando há histórico completo; senão mantém o valor
    já gravado no sitemap e, para URL nova, usa a data de hoje."""
    use_git = has_full_history()
    previous = current_lastmods()
    today = datetime.date.today().isoformat()
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, path in collect():
        lastmod = (git_date(path) if use_git else None) or previous.get(url) or today
        lines.append(f"  <url><loc>{url}</loc><lastmod>{lastmod}</lastmod></url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    target = ROOT / "sitemap.xml"
    if args.check:
        # Compara o conjunto de URLs e exige lastmod em todas; a data em si
        # depende do histórico git, que o checkout raso do CI não tem.
        current = target.read_text(encoding="utf-8") if target.exists() else ""
        expected = [url for url, _ in collect()]
        if LOC_RE.findall(current) != expected:
            raise SystemExit("sitemap.xml desatualizado; rode python3 scripts/generate_sitemap.py")
        if len(LASTMOD_RE.findall(current)) != len(expected):
            raise SystemExit("sitemap.xml sem lastmod em todas as URLs; rode python3 scripts/generate_sitemap.py")
        print("sitemap.xml está sincronizado")
        return
    generated = render()
    target.write_text(generated, encoding="utf-8")
    print(f"sitemap.xml gerado com {generated.count('<url>')} URLs")


if __name__ == "__main__":
    main()
