#!/usr/bin/env python3
"""Valida os contratos essenciais de SEO, GEO e arquitetura de produto."""

import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://credituz.ai/"
CORE = [
    "index.html",
    "pages/blog.html",
    "pages/credituz-os.html",
    "pages/corban-ai.html",
    "pages/enterprise.html",
    "pages/construtoras.html",
    "pages/imobiliarias.html",
    "white-label.html",
    "pages/integracoes.html",
    "pages/artigos/roi-tecnologia-imobiliarias-como-calcular-apresentar-socios.html",
    "pages/artigos/corretor-imoveis-crm-ia-follow-up.html",
]
JSON_LD_REQUIRED = {
    "index.html",
    "pages/blog.html",
    "pages/credituz-os.html",
    "pages/corban-ai.html",
    "pages/enterprise.html",
    "pages/artigos/roi-tecnologia-imobiliarias-como-calcular-apresentar-socios.html",
    "pages/artigos/corretor-imoveis-crm-ia-follow-up.html",
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.in_json = False
        self.title_parts = []
        self.json_parts = []
        self.json_documents = []
        self.description = ""
        self.canonical = ""
        self.h1 = 0
        self.images_without_alt = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "script" and values.get("type") == "application/ld+json":
            self.in_json = True
            self.json_parts = []
        if tag == "meta" and values.get("name", "").lower() == "description":
            self.description = values.get("content", "").strip()
        if tag == "link" and "canonical" in values.get("rel", "").split():
            self.canonical = values.get("href", "").strip()
        if tag == "h1":
            self.h1 += 1
        if tag == "img" and not values.get("alt", "").strip():
            self.images_without_alt.append(values.get("src", "imagem sem src"))
        if tag == "a" and values.get("href"):
            self.anchors.append(values["href"])

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json:
            self.json_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_json:
            self.json_documents.append("".join(self.json_parts))
            self.in_json = False

    @property
    def title(self):
        return "".join(self.title_parts).strip()


def expected_url(relative):
    if relative == "index.html":
        return SITE
    return SITE + relative


def main():
    errors = []

    for relative in CORE:
        path = ROOT / relative
        if not path.exists():
            errors.append(f"arquivo obrigatório ausente: {relative}")
            continue
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        if not 1 <= len(parser.title) <= 60:
            errors.append(f"title fora de 1–60 caracteres em {relative}: {len(parser.title)}")
        if not 110 <= len(parser.description) <= 160:
            errors.append(
                f"description fora de 110–160 caracteres em {relative}: "
                f"{len(parser.description)}"
            )
        if parser.canonical != expected_url(relative):
            errors.append(
                f"canonical incorreto em {relative}: {parser.canonical or 'ausente'}"
            )
        if parser.h1 != 1:
            errors.append(f"{relative} deve ter exatamente um H1; encontrou {parser.h1}")
        if parser.images_without_alt:
            errors.append(
                f"imagens sem alt em {relative}: {', '.join(parser.images_without_alt)}"
            )
        for document in parser.json_documents:
            try:
                json.loads(document)
            except ValueError as exc:
                errors.append(f"JSON-LD inválido em {relative}: {exc}")
        if relative in JSON_LD_REQUIRED and not parser.json_documents:
            errors.append(f"JSON-LD obrigatório ausente em {relative}")

    home_schema = json.loads((ROOT / "home.json").read_text(encoding="utf-8"))
    organizations = [
        item for item in home_schema.get("@graph", [])
        if item.get("@type") == "Organization"
    ]
    if not organizations or not organizations[0].get("logo"):
        errors.append("Organization em home.json precisa conter logo")

    try:
        sitemap = ET.parse(ROOT / "sitemap.xml")
        locs = [node.text for node in sitemap.findall("{*}url/{*}loc")]
    except (ET.ParseError, OSError) as exc:
        errors.append(f"sitemap.xml inválido: {exc}")
        locs = []
    if len(locs) != len(set(locs)):
        errors.append("sitemap.xml contém URLs duplicadas")
    if any(not url.startswith(SITE) or "www.credituz.ai" in url for url in locs):
        errors.append("sitemap.xml contém host ou protocolo não canônico")
    required_urls = {
        SITE,
        SITE + "pages/blog.html",
        SITE + "pages/credituz-os.html",
        SITE + "pages/corban-ai.html",
        SITE + "pages/enterprise.html",
        SITE + "pages/credituz-score.html",
    }
    missing_urls = sorted(required_urls - set(locs))
    if missing_urls:
        errors.append("URLs essenciais ausentes do sitemap: " + ", ".join(missing_urls))

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    for agent in ("OAI-SearchBot", "GPTBot", "ClaudeBot", "PerplexityBot"):
        if f"User-agent: {agent}" not in robots:
            errors.append(f"crawler ausente de robots.txt: {agent}")
    if "Sitemap: https://credituz.ai/sitemap.xml" not in robots:
        errors.append("robots.txt não referencia o sitemap canônico")

    blog = (ROOT / "pages/blog.html").read_text(encoding="utf-8")
    static_section = blog.split("STATIC_ARTICLES_START", 1)[-1].split(
        "STATIC_ARTICLES_END", 1
    )[0]
    static_cards = len(re.findall(r'<a class="card" href="artigos/', static_section))
    if static_cards != 119:
        errors.append(f"blog deve pré-renderizar 119 cards; encontrou {static_cards}")
    if "STATIC_ARTICLES_START" not in blog or "STATIC_ARTICLES_END" not in blog:
        errors.append("marcadores do índice estático do blog ausentes")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    for product in ("credituz-os", "corban-ai", "enterprise", "credituz-score"):
        if f"https://credituz.ai/pages/{product}.html" not in llms:
            errors.append(f"produto ausente de llms.txt: {product}")

    stale_domain = re.compile(r"https?://(?:www\.)?(?:credituz\.com\.br|www\.credituz\.ai)")
    for path in ROOT.rglob("*"):
        if path.suffix not in {".html", ".md", ".txt", ".xml"}:
            continue
        if stale_domain.search(path.read_text(encoding="utf-8")):
            errors.append(f"domínio antigo encontrado em {path.relative_to(ROOT)}")

    for path in ROOT.rglob("*.html"):
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        for href in parser.anchors:
            if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            parsed = urlparse(href)
            if parsed.scheme or parsed.netloc or not parsed.path or parsed.path == "/":
                continue
            link_path = unquote(parsed.path)
            target = (
                ROOT / link_path.lstrip("/")
                if link_path.startswith("/")
                else path.parent / link_path
            )
            if link_path.endswith("/"):
                target = target / "index.html"
            if not target.exists():
                errors.append(
                    f"link interno quebrado em {path.relative_to(ROOT)}: {href}"
                )

    segment_copy = "\n".join(
        (ROOT / page).read_text(encoding="utf-8")
        for page in ("pages/construtoras.html", "pages/imobiliarias.html")
    )
    for legacy_claim in (
        "50 contratos com IA",
        "20 assinaturas digitais",
        "40% da comissão",
        "75% da comissão",
        "por R$ 0,15 por envio",
    ):
        if legacy_claim in segment_copy:
            errors.append(f"oferta antiga ainda presente nas páginas de segmento: {legacy_claim}")

    if errors:
        print("Falhas de SEO/GEO:")
        for error in errors:
            print("-", error)
        return 1
    print(f"SEO/GEO validado: {len(CORE)} páginas essenciais e {len(locs)} URLs no sitemap")
    return 0


if __name__ == "__main__":
    sys.exit(main())
