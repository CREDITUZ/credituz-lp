#!/usr/bin/env python3
"""Pré-renderiza os cards do blog mantendo busca e filtros no cliente."""

import argparse
import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOG = ROOT / "pages" / "blog.html"
ARTICLES_RE = re.compile(r"const ARTICLES = (\[.*?\]);\s*\nlet activeCat", re.S)
GRID_RE = re.compile(
    r'<div class="grid" id="grid">.*?</div>\s*'
    r'<div class="empty" id="empty"',
    re.S,
)


def article_card(article):
    versus = '<span class="card-vs">Comparativo</span>' if article["versus"] else ""
    return (
        f'        <a class="card" href="artigos/{html.escape(article["slug"])}.html">\n'
        f'            <div class="card-cat">{html.escape(article["cat"])}{versus}</div>\n'
        f'            <h2>{html.escape(article["title"])}</h2>\n'
        f'            <p>{html.escape(article["sub"])}</p>\n'
        f'            <div class="card-foot"><span>{html.escape(article["date"])}</span>'
        f'<span>{html.escape(article["read"])}</span></div>\n'
        "        </a>"
    )


def plain_text(fragment):
    return html.unescape(re.sub(r"<[^>]+>", "", fragment)).strip()


def synchronize_article_copy(articles):
    """Usa H1 e subtítulo das páginas como fonte única para o índice."""
    for article in articles:
        page = ROOT / "pages" / "artigos" / f'{article["slug"]}.html'
        if not page.exists():
            continue
        source = page.read_text(encoding="utf-8")
        title = re.search(
            r'<h1[^>]*class=["\'][^"\']*\btitle\b[^"\']*["\'][^>]*>(.*?)</h1>',
            source,
            re.I | re.S,
        )
        subtitle = re.search(
            r'<p[^>]*class=["\'][^"\']*\barticle-sub\b[^"\']*["\'][^>]*>(.*?)</p>',
            source,
            re.I | re.S,
        )
        if title:
            article["title"] = plain_text(title.group(1))
        if subtitle:
            article["sub"] = plain_text(subtitle.group(1))


def render(source):
    match = ARTICLES_RE.search(source)
    if not match:
        raise SystemExit("Não foi possível localizar const ARTICLES em pages/blog.html")
    articles = json.loads(match.group(1))
    synchronize_article_copy(articles)
    serialized = json.dumps(articles, ensure_ascii=False, separators=(",", ":"))
    source = source[:match.start(1)] + serialized + source[match.end(1):]
    cards = "\n".join(article_card(article) for article in articles)
    grid = (
        '<div class="grid" id="grid">\n'
        "        <!-- STATIC_ARTICLES_START: gerado por scripts/render_blog_index.py -->\n"
        f"{cards}\n"
        "        <!-- STATIC_ARTICLES_END -->\n"
        "    </div>\n"
        '    <div class="empty" id="empty"'
    )
    rendered, count = GRID_RE.subn(grid, source, count=1)
    if count != 1:
        raise SystemExit("Não foi possível localizar #grid em pages/blog.html")
    rendered = re.sub(
        r'<div class="results-info" id="resultsInfo">.*?</div>',
        f'<div class="results-info" id="resultsInfo">{len(articles)} artigos</div>',
        rendered,
        count=1,
    )
    return rendered, len(articles)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = BLOG.read_text(encoding="utf-8")
    rendered, count = render(source)
    if args.check:
        if rendered != source:
            raise SystemExit("Índice estático do blog desatualizado; rode python3 scripts/render_blog_index.py")
        print(f"Índice estático do blog sincronizado com {count} artigos")
        return
    BLOG.write_text(rendered, encoding="utf-8")
    print(f"Índice estático do blog gerado com {count} artigos")


if __name__ == "__main__":
    main()
