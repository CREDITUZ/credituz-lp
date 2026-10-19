#!/usr/bin/env python3
"""Gera o portal guia.credituz.ai (pasta guia/) a partir de guia-src/.

Uso:
  python3 scripts/build_guia.py           # valida e gera guia/
  python3 scripts/build_guia.py --check   # valida e falha se guia/ estiver desatualizada

Fonte:
  guia-src/site.yaml            configuracao (URL, AdSense, contato)
  guia-src/artigos/<slug>.md    artigos (frontmatter YAML + Markdown), regras em guia-src/ESCRITA.md
  guia-src/paginas/<slug>.md    paginas institucionais (sobre, contato, privacidade, termos)
  guia-src/ferramentas/<slug>.html  calculadoras (fragmento de corpo com script proprio)
  guia-src/static/              arquivos copiados como estao (css, logo, icones)

A pasta guia/ e a raiz publicada pela Vercel (projeto separado do GitHub Pages do credituz.ai).
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
import unicodedata
from datetime import date
from pathlib import Path

import markdown
import yaml

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "guia-src"
OUT = ROOT / "guia"

CATEGORIES = {
    "financiamento": ("Financiamento", "Como funciona, juros, entrada, renda e portabilidade."),
    "fgts": ("FGTS", "Como usar o Fundo de Garantia na compra e no financiamento."),
    "programas": ("Programas e regras", "Minha Casa Minha Vida, SFH, SFI e regras do sistema."),
    "credito": ("Crédito e score", "Score, nome sujo, análise de crédito e crédito negado."),
    "custos": ("Custos e documentos", "ITBI, cartório, seguros, avaliação e documentação."),
    "alternativas": ("Alternativas", "Consórcio, home equity e a conta de alugar ou comprar."),
    "direitos": ("Seus direitos", "Distrato, atraso na entrega e juros de obra."),
}
REQUIRED = ["title", "description", "category", "published", "updated", "key_points", "faq", "sources", "related"]
DASHES = re.compile("[—–]")
MONTHS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
          "setembro", "outubro", "novembro", "dezembro"]

errors: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def slugify(value: str, separator: str = "-") -> str:
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_-]+", separator, value)


def fmt_date(d: date) -> str:
    return f"{d.day} de {MONTHS[d.month - 1]} de {d.year}"


def as_date(v, where: str) -> date:
    if isinstance(v, date):
        return v
    try:
        return date.fromisoformat(str(v))
    except ValueError:
        err(f"{where}: data invalida {v!r}")
        return date.today()


def split_front(text: str, where: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        err(f"{where}: sem frontmatter YAML")
        return {}, text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        err(f"{where}: YAML invalido ({e})")
        meta = {}
    return meta, m.group(2)


def md_to_html(body: str) -> tuple[str, list[tuple[str, str]]]:
    md = markdown.Markdown(
        extensions=["tables", "sane_lists", "toc", "smarty"],
        extension_configs={
            "toc": {"slugify": slugify, "toc_depth": "2"},
            "smarty": {"smart_dashes": False, "smart_quotes": False},
        },
    )
    out = md.convert(body)
    out = re.sub(r"<table>", '<div class="tbl"><table>', out)
    out = re.sub(r"</table>", "</table></div>", out)
    toc = [(t["id"], t["name"]) for t in md.toc_tokens]
    return out, toc


def load_site() -> dict:
    site = yaml.safe_load((SRC / "site.yaml").read_text(encoding="utf-8"))
    site["url"] = site["url"].rstrip("/")
    return site


# ---------------------------------------------------------------- layout

def adsense_head(site: dict) -> str:
    client = (site.get("adsense_client") or "").strip()
    if not client:
        return ""
    # Anuncios nao personalizados ate a pessoa aceitar cookies (LGPD). A escolha fica em
    # localStorage guia_consent = "all" | "essential".
    return (
        "<script>window.adsbygoogle=window.adsbygoogle||[];"
        "try{if(localStorage.getItem('guia_consent')!=='all'){window.adsbygoogle.requestNonPersonalizedAds=1}}"
        "catch(e){window.adsbygoogle.requestNonPersonalizedAds=1}</script>\n"
        f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={esc(client)}" '
        'crossorigin="anonymous"></script>\n'
        f'<meta name="google-adsense-account" content="{esc(client)}">\n'
    )


def analytics_head(site: dict) -> str:
    ga = (site.get("ga4_id") or "").strip()
    if not ga:
        return ""
    return (
        f'<script async src="https://www.googletagmanager.com/gtag/js?id={esc(ga)}"></script>\n'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}"
        "var c='denied';try{if(localStorage.getItem('guia_consent')==='all')c='granted'}catch(e){}"
        "gtag('consent','default',{ad_storage:c,analytics_storage:c,ad_user_data:c,ad_personalization:c});"
        f"gtag('js',new Date());gtag('config','{esc(ga)}');</script>\n"
    )


NAV = [("/", "Início", "opt"), ("/categoria/financiamento", "Financiamento", "opt"),
       ("/categoria/fgts", "FGTS", "opt"), ("/simulador", "Simulador", ""),
       ("/artigos", "Todos os guias", "")]


def page(site: dict, *, path: str, title: str, description: str, body: str,
         jsonld: list | None = None, og_type: str = "website", active: str = "",
         noindex: bool = False) -> str:
    url = site["url"] + (path if path != "/" else "/")
    full_title = title if title.endswith(site["name"]) else f"{title} | {site['name']}"
    nav = "".join(
        f'<a href="{h}" class="{c}{" on" if h == active else ""}">{esc(t)}</a>' for h, t, c in NAV
    )
    ld = "".join(
        f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>\n'
        for x in (jsonld or [])
    )
    robots = '<meta name="robots" content="noindex">\n' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">\n'
    year = date.today().year
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description)}">
{robots}<link rel="canonical" href="{esc(url)}">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{esc(site['name'])}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{esc(url)}">
<meta property="og:locale" content="pt_BR">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/estilo.css?v={site['_css_v']}">
{adsense_head(site)}{analytics_head(site)}{ld}</head>
<body>
<a class="skip" href="#conteudo">Pular para o conteúdo</a>
<header class="top"><div class="wrap">
<a class="brand" href="/" aria-label="{esc(site['name'])}, página inicial"><img class="logo-light" src="/assets/logo-credituz.png" alt="Credituz" width="68" height="20"><img class="logo-dark" src="/assets/logo-credituz-branco.png" alt="" width="68" height="20"><span>Guia</span></a>
<nav class="nav" aria-label="Principal">{nav}</nav>
</div></header>
<main id="conteudo">
{body}
</main>
<footer class="foot"><div class="wrap">
<div class="cols">
<div><h3>Guias</h3><ul>{''.join(f'<li><a href="/categoria/{k}">{esc(v[0])}</a></li>' for k, v in CATEGORIES.items())}</ul></div>
<div><h3>Ferramentas</h3><ul><li><a href="/simulador">Simulador de financiamento</a></li><li><a href="/quanto-posso-financiar">Quanto posso financiar</a></li></ul></div>
<div><h3>Sobre</h3><ul><li><a href="/sobre">Quem somos e política editorial</a></li><li><a href="/contato">Contato</a></li><li><a href="/privacidade">Privacidade e cookies</a></li><li><a href="/termos">Termos de uso</a></li><li><a href="#" data-consent-open>Preferências de cookies</a></li></ul></div>
</div>
<p class="legal">Conteúdo informativo e educativo. Não é recomendação financeira, jurídica ou de investimento; regras, taxas e valores mudam e devem ser confirmados com o banco, o cartório ou um profissional antes de qualquer decisão. {esc(site['name'])} é mantido por {esc(site['company'])}, CNPJ {esc(site['cnpj'])}. © {year}</p>
</div></footer>
<div class="consent" role="dialog" aria-live="polite" aria-label="Cookies" id="consent">
<p>Usamos cookies essenciais e, se você permitir, cookies de anúncios e medição do Google para personalizar anúncios. Veja a <a href="/privacidade">política de privacidade</a>.</p>
<div class="row"><button type="button" data-consent="all">Aceitar todos</button><button type="button" class="alt" data-consent="essential">Só essenciais</button></div>
</div>
<script>
(function(){{var k='guia_consent',b=document.getElementById('consent');
function g(){{try{{return localStorage.getItem(k)}}catch(e){{return null}}}}
function s(v){{try{{localStorage.setItem(k,v)}}catch(e){{}}b.classList.remove('show');
if(typeof gtag==='function'){{var c=v==='all'?'granted':'denied';gtag('consent','update',{{ad_storage:c,analytics_storage:c,ad_user_data:c,ad_personalization:c}})}}
if(v==='all'&&window.adsbygoogle&&window.adsbygoogle.requestNonPersonalizedAds){{location.reload()}}}}
if(!g())b.classList.add('show');
document.addEventListener('click',function(e){{var t=e.target.closest('[data-consent]');if(t){{s(t.getAttribute('data-consent'));return}}
if(e.target.closest('[data-consent-open]')){{e.preventDefault();b.classList.add('show')}}}});
}})();
</script>
</body>
</html>
"""


def ad_slot(site: dict) -> str:
    # Com anuncios automaticos o Google escolhe as posicoes; este bloco so existe quando ha
    # um slot manual configurado em site.yaml (adsense_slot_artigo).
    client = (site.get("adsense_client") or "").strip()
    slot = str(site.get("adsense_slot_artigo") or "").strip()
    if not client or not slot:
        return ""
    return (
        f'<div class="ad"><ins class="adsbygoogle" style="display:block" data-ad-client="{esc(client)}" '
        f'data-ad-slot="{esc(slot)}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
        "<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>"
    )


# ---------------------------------------------------------------- conteudo

def load_articles() -> dict[str, dict]:
    arts: dict[str, dict] = {}
    for f in sorted((SRC / "artigos").glob("*.md")):
        slug = f.stem
        where = f"artigos/{f.name}"
        text = f.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            if DASHES.search(line):
                err(f"{where}:{i}: travessao proibido: {line.strip()[:80]}")
        meta, body = split_front(text, where)
        for k in REQUIRED:
            if k not in meta:
                err(f"{where}: campo obrigatorio ausente: {k}")
        if meta.get("category") not in CATEGORIES:
            err(f"{where}: categoria invalida {meta.get('category')!r}")
        d = str(meta.get("description", ""))
        if not 100 <= len(d) <= 175:
            err(f"{where}: description com {len(d)} caracteres (esperado 100 a 175)")
        if len(str(meta.get("title", ""))) > 80:
            err(f"{where}: title longo demais")
        if re.search(r"^#\s", body, re.M):
            err(f"{where}: o corpo nao deve ter titulo '# '")
        words = len(re.findall(r"\w+", body))
        if words < 900:
            err(f"{where}: corpo curto ({words} palavras)")
        meta["slug"] = slug
        meta["body"] = body
        meta["words"] = words
        meta["published"] = as_date(meta.get("published"), where)
        meta["updated"] = as_date(meta.get("updated"), where)
        meta.setdefault("reading_minutes", max(1, round(words / 200)))
        arts[slug] = meta
    return arts


def check_links(arts: dict, tools: set[str], pages: set[str]) -> None:
    valid = {f"/artigos/{s}" for s in arts} | {f"/{t}" for t in tools} | {f"/{p}" for p in pages} | \
        {f"/categoria/{c}" for c in CATEGORIES} | {"/", "/artigos"}
    for s, a in arts.items():
        for r in a.get("related") or []:
            if r not in arts:
                err(f"artigos/{s}.md: related aponta para slug inexistente {r!r}")
        for href in re.findall(r"\]\((/[^)\s#]*)", a["body"]):
            if href.rstrip("/") not in valid and href not in valid:
                err(f"artigos/{s}.md: link interno quebrado {href}")
        for src in a.get("sources") or []:
            if not str(src.get("url", "")).startswith("http"):
                err(f"artigos/{s}.md: fonte sem URL valida: {src}")


def render_article(site: dict, a: dict, arts: dict) -> str:
    body_html, toc = md_to_html(a["body"])
    cat_name = CATEGORIES[a["category"]][0]
    path = f"/artigos/{a['slug']}"
    url = site["url"] + path
    # anuncio manual depois do 2o h2, quando configurado
    slot = ad_slot(site)
    if slot:
        parts = body_html.split("<h2", 3)
        if len(parts) > 3:
            body_html = parts[0] + "<h2" + parts[1] + "<h2" + parts[2] + slot + "<h2" + parts[3]
    kp = "".join(f"<li>{esc(x)}</li>" for x in a["key_points"])
    toc_html = "".join(f'<li><a href="#{i}">{esc(n)}</a></li>' for i, n in toc)
    faq = "".join(
        f"<details><summary>{esc(q['q'])}</summary><p>{esc(q['a'])}</p></details>" for q in a["faq"]
    )
    srcs = "".join(
        f'<li><a href="{esc(s["url"])}" rel="nofollow noopener" target="_blank">{esc(s["title"])}</a></li>'
        for s in a["sources"]
    )
    rel = "".join(
        f'<li><a href="/artigos/{r}">{esc(arts[r]["title"])}</a><p>{esc(arts[r]["description"])}</p></li>'
        for r in a["related"] if r in arts
    )
    upd = a["updated"]
    pub = a["published"]
    date_line = f"Atualizado em {fmt_date(upd)}" if upd != pub else f"Publicado em {fmt_date(pub)}"
    body = f"""<div class="art">
<nav class="crumbs" aria-label="Você está em"><a href="/">Início</a> / <a href="/categoria/{a['category']}">{esc(cat_name)}</a></nav>
<article>
<h1>{esc(a['title'])}</h1>
<p class="desc">{esc(a['description'])}</p>
<div class="meta"><span>{date_line}</span><span>{a['reading_minutes']} min de leitura</span><span>Por <a href="/sobre">Redação {esc(site['name'])}</a></span></div>
<section class="box" aria-labelledby="resumo"><h2 id="resumo">Resumo rápido</h2><ul>{kp}</ul></section>
<nav class="box toc" aria-labelledby="indice"><h2 id="indice">Neste guia</h2><ol>{toc_html}</ol></nav>
<div class="body">
{body_html}
</div>
<section class="after faq" aria-labelledby="faq"><h2 id="faq">Perguntas frequentes</h2>{faq}</section>
<section class="after src" aria-labelledby="fontes"><h2 id="fontes">Fontes consultadas</h2><ol>{srcs}</ol></section>
<p class="note">Conteúdo informativo, revisado em {fmt_date(upd)}. Regras, taxas e valores mudam: confirme as condições com o banco, o cartório ou um profissional antes de decidir. Encontrou um erro? <a href="/contato">Avise a gente</a>.</p>
</article>
<section class="after" aria-labelledby="leia"><h2 id="leia">Continue lendo</h2><ul class="list">{rel}</ul></section>
</div>"""
    jsonld = [
        {
            "@context": "https://schema.org", "@type": "Article", "headline": a["title"],
            "description": a["description"], "inLanguage": "pt-BR", "mainEntityOfPage": url,
            "datePublished": pub.isoformat(), "dateModified": upd.isoformat(),
            "articleSection": cat_name, "wordCount": a["words"],
            "author": {"@type": "Organization", "name": f"Redação {site['name']}", "url": site["url"] + "/sobre"},
            "publisher": {"@type": "Organization", "name": site["company"], "url": "https://credituz.ai",
                          "logo": {"@type": "ImageObject", "url": site["url"] + "/assets/logo-credituz.png"}},
            "citation": [s["url"] for s in a["sources"]],
        },
        {
            "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Início", "item": site["url"] + "/"},
                {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"{site['url']}/categoria/{a['category']}"},
                {"@type": "ListItem", "position": 3, "name": a["title"], "item": url},
            ],
        },
        {
            "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}}
                for q in a["faq"]
            ],
        },
    ]
    return page(site, path=path, title=a["title"], description=a["description"], body=body,
                jsonld=jsonld, og_type="article", active=f"/categoria/{a['category']}")


def article_list(items: list[dict]) -> str:
    return '<ul class="list">' + "".join(
        f'<li><a href="/artigos/{a["slug"]}">{esc(a["title"])}</a><p>{esc(a["description"])}</p></li>'
        for a in items
    ) + "</ul>"


def by_recent(arts: dict) -> list[dict]:
    return sorted(arts.values(), key=lambda a: (a["updated"], a["title"]), reverse=True)


def render_home(site: dict, arts: dict) -> str:
    pillar = [s for s in site.get("destaques", []) if s in arts]
    cards = "".join(
        f'<a class="card" href="/artigos/{s}"><div class="k">{esc(CATEGORIES[arts[s]["category"]][0])}</div>'
        f'<h3>{esc(arts[s]["title"])}</h3><p>{esc(arts[s]["description"])}</p></a>' for s in pillar
    )
    tools = (
        '<a class="card tool" href="/simulador"><div class="k">Ferramenta</div><h3>Simulador de financiamento</h3>'
        "<p>Compare SAC e Price, veja a primeira e a última parcela e o total de juros.</p></a>"
        '<a class="card tool" href="/quanto-posso-financiar"><div class="k">Ferramenta</div><h3>Quanto posso financiar</h3>'
        "<p>Descubra o valor de imóvel que cabe na sua renda e na sua entrada.</p></a>"
    )
    cats = ""
    for k, (name, desc) in CATEGORIES.items():
        items = [a for a in by_recent(arts) if a["category"] == k]
        if not items:
            continue
        cats += (f'<section class="sec"><div class="wrap"><h2><a href="/categoria/{k}" style="color:inherit">{esc(name)}</a></h2>'
                 f'<p class="sub">{esc(desc)}</p>{article_list(items[:4])}</div></section>')
    body = f"""<section class="hero"><div class="wrap">
<p class="eyebrow">Guia do crédito imobiliário</p>
<h1>Financiar um imóvel, explicado sem enrolação.</h1>
<p class="lede">Guias práticos sobre financiamento, FGTS, juros, custos e direitos do comprador, com dados atualizados e fontes oficiais.</p>
<div class="row"><a class="btn" href="/simulador">Simular financiamento</a><a class="btn ghost" href="/artigos/como-funciona-financiamento-imobiliario">Começar pelo básico</a></div>
</div></section>
<section class="sec"><div class="wrap"><div class="grid">{tools}{cards}</div></div></section>
<section class="sec"><div class="wrap"><h2>Assuntos</h2><p class="sub">Escolha por onde começar.</p><div class="cats">{''.join(f'<a class="chip" href="/categoria/{k}">{esc(v[0])}</a>' for k, v in CATEGORIES.items())}</div></div></section>
{cats}"""
    jsonld = [{"@context": "https://schema.org", "@type": "WebSite", "name": site["name"], "url": site["url"] + "/",
               "inLanguage": "pt-BR", "publisher": {"@type": "Organization", "name": site["company"]}}]
    return page(site, path="/", title=f"{site['name']}: financiamento imobiliário, FGTS e crédito explicados",
                description=site["description"], body=body, jsonld=jsonld, active="/")


def render_category(site: dict, key: str, arts: dict) -> str:
    name, desc = CATEGORIES[key]
    items = [a for a in by_recent(arts) if a["category"] == key]
    body = (f'<div class="page" style="max-width:860px"><nav class="crumbs"><a href="/">Início</a></nav>'
            f'<h1>{esc(name)}</h1><p class="lede" style="margin-bottom:24px">{esc(desc)}</p>{article_list(items)}</div>')
    return page(site, path=f"/categoria/{key}", title=f"{name}: guias de crédito imobiliário",
                description=f"{desc} Guias atualizados do {site['name']}.", body=body, active=f"/categoria/{key}")


def render_all(site: dict, arts: dict) -> str:
    blocks = ""
    for k, (name, _) in CATEGORIES.items():
        items = [a for a in by_recent(arts) if a["category"] == k]
        if items:
            blocks += f'<h2 style="margin:32px 0 10px;font-size:1.4rem;letter-spacing:-.02em">{esc(name)}</h2>{article_list(items)}'
    body = (f'<div class="page" style="max-width:860px"><nav class="crumbs"><a href="/">Início</a></nav>'
            f'<h1>Todos os guias</h1><p class="lede">{len(arts)} guias sobre financiamento, FGTS, custos e direitos do comprador.</p>{blocks}</div>')
    return page(site, path="/artigos", title="Todos os guias de crédito imobiliário",
                description=f"Lista completa dos {len(arts)} guias do {site['name']} sobre financiamento imobiliário, FGTS, custos e direitos.",
                body=body, active="/artigos")


def render_simple(site: dict, slug: str, f: Path) -> str:
    text = f.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        if DASHES.search(line):
            err(f"paginas/{f.name}:{i}: travessao proibido")
    meta, body = split_front(text, f"paginas/{f.name}")
    body = body.replace("{{SITE}}", site["name"]).replace("{{EMPRESA}}", site["company"]) \
        .replace("{{CNPJ}}", site["cnpj"]).replace("{{EMAIL}}", site["email"]) \
        .replace("{{ENDERECO}}", site["address"]).replace("{{TELEFONE}}", site["phone"])
    h, _ = md_to_html(body)
    upd = as_date(meta.get("updated", date.today()), f.name)
    html_body = (f'<div class="page"><h1>{esc(meta["title"])}</h1>'
                 f'<p class="meta">Atualizado em {fmt_date(upd)}</p><div class="body">{h}</div></div>')
    return page(site, path=f"/{slug}", title=meta["title"], description=meta["description"], body=html_body,
                active=f"/{slug}")


def render_tool(site: dict, slug: str, f: Path) -> str:
    text = f.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        if DASHES.search(line):
            err(f"ferramentas/{f.name}:{i}: travessao proibido")
    meta, body = split_front(text, f"ferramentas/{f.name}")
    jsonld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": meta["title"],
               "applicationCategory": "FinanceApplication", "operatingSystem": "Web", "inLanguage": "pt-BR",
               "offers": {"@type": "Offer", "price": "0", "priceCurrency": "BRL"}, "url": f"{site['url']}/{slug}"}]
    return page(site, path=f"/{slug}", title=meta["title"], description=meta["description"],
                body=f'<div class="tool-wrap">{body}</div>', jsonld=jsonld, active=f"/{slug}")


def sitemap(site: dict, arts: dict, extra: list[str]) -> str:
    rows = [(site["url"] + "/", max((a["updated"] for a in arts.values()), default=date.today()))]
    rows += [(f"{site['url']}/artigos/{a['slug']}", a["updated"]) for a in by_recent(arts)]
    rows += [(f"{site['url']}/categoria/{k}", None) for k in CATEGORIES]
    rows += [(f"{site['url']}/{p}", None) for p in extra]
    items = "".join(
        f"<url><loc>{esc(u)}</loc>" + (f"<lastmod>{d.isoformat()}</lastmod>" if d else "") + "</url>\n"
        for u, d in rows
    )
    return f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{items}</urlset>\n'


def llms(site: dict, arts: dict) -> str:
    out = [f"# {site['name']}", "", f"> {site['description']}", ""]
    for k, (name, _) in CATEGORIES.items():
        items = [a for a in by_recent(arts) if a["category"] == k]
        if items:
            out.append(f"## {name}")
            out += [f"- [{a['title']}]({site['url']}/artigos/{a['slug']}): {a['description']}" for a in items]
            out.append("")
    out += ["## Ferramentas", f"- [Simulador de financiamento]({site['url']}/simulador)",
            f"- [Quanto posso financiar]({site['url']}/quanto-posso-financiar)", ""]
    return "\n".join(out)


def build() -> dict[str, bytes]:
    site = load_site()
    css = (SRC / "static" / "estilo.css").read_bytes()
    import hashlib
    site["_css_v"] = hashlib.sha256(css).hexdigest()[:8]
    arts = load_articles()
    pages = {f.stem: f for f in sorted((SRC / "paginas").glob("*.md"))}
    tools = {f.stem: f for f in sorted((SRC / "ferramentas").glob("*.html"))}
    check_links(arts, set(tools), set(pages))
    files: dict[str, bytes] = {}

    def put(rel: str, text: str) -> None:
        files[rel] = text.encode("utf-8")

    put("index.html", render_home(site, arts))
    put("artigos/index.html", render_all(site, arts))
    for s, a in arts.items():
        put(f"artigos/{s}.html", render_article(site, a, arts))
    for k in CATEGORIES:
        put(f"categoria/{k}.html", render_category(site, k, arts))
    for s, f in pages.items():
        put(f"{s}.html", render_simple(site, s, f))
    for s, f in tools.items():
        put(f"{s}.html", render_tool(site, s, f))
    put("404.html", page(site, path="/404", title="Página não encontrada", description="Página não encontrada.",
                         body='<div class="page"><h1>Página não encontrada</h1><p>O endereço pode ter mudado. '
                              'Veja <a href="/artigos">todos os guias</a> ou volte para o <a href="/">início</a>.</p></div>',
                         noindex=True))
    put("sitemap.xml", sitemap(site, arts, list(tools) + list(pages)))
    put("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {site['url']}/sitemap.xml\n")
    put("llms.txt", llms(site, arts))
    client = (site.get("adsense_client") or "").strip()
    if client:
        pub = client.replace("ca-", "")
        put("ads.txt", f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n")
    put("vercel.json", json.dumps({
        "cleanUrls": True, "trailingSlash": False,
        "headers": [
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"}]},
            {"source": "/(estilo.css|assets/(.*))", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
        ],
    }, indent=2) + "\n")
    for f in (SRC / "static").rglob("*"):
        if f.is_file():
            files[str(f.relative_to(SRC / "static"))] = f.read_bytes()
    # links internos do resultado, resolvidos como a Vercel faz com cleanUrls
    for rel, data in files.items():
        if not rel.endswith(".html"):
            continue
        for href in re.findall(r'(?:href|src)="(/[^"#?]*)', data.decode("utf-8")):
            t = href.strip("/")
            if not t or t in files or f"{t}.html" in files or f"{t}/index.html" in files:
                continue
            err(f"{rel}: link interno quebrado {href}")
    return files


def main() -> int:
    check = "--check" in sys.argv
    files = build()
    if errors:
        print("Erros no guia:", file=sys.stderr)
        for e in errors:
            print("  - " + e, file=sys.stderr)
        return 1
    existing = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()} if OUT.exists() else set()
    if check:
        stale = [k for k, v in files.items() if not (OUT / k).exists() or (OUT / k).read_bytes() != v]
        extra = sorted(existing - set(files))
        if stale or extra:
            print("guia/ desatualizada; rode python3 scripts/build_guia.py", file=sys.stderr)
            for k in stale[:20]:
                print("  diferente: " + k, file=sys.stderr)
            for k in extra[:20]:
                print("  sobrando: " + k, file=sys.stderr)
            return 1
        print(f"guia/ em dia ({len(files)} arquivos)")
        return 0
    if OUT.exists():
        shutil.rmtree(OUT)
    for k, v in files.items():
        p = OUT / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(v)
    print(f"guia/ gerada: {len(files)} arquivos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
