#!/usr/bin/env python3
"""
Traduz a landing page de PT para EN preservando todo o HTML, scripts, estilos,
URLs e termos de marca. Gera en/index.html a partir de index.html.

Motor: DeepL. Requer a variavel de ambiente DEEPL_API_KEY. Para conta gratuita
use a URL api-free (padrao); para Pro defina
DEEPL_API_URL=https://api.deepl.com/v2/translate.

Estrategia: extrai apenas os textos visiveis e atributos relevantes (title, meta
description, og, twitter, alt, aria-label, placeholder, title), protege termos de
marca, traduz em lotes e reinsere. A estrutura, classes, scripts e links ficam
intactos.
"""
import os
import re
import json
import time
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup, NavigableString, Comment

SRC = os.environ.get("LP_SRC", "index.html")
OUT = os.environ.get("LP_OUT", "en/index.html")
SOURCE_LANG = "PT"
TARGET_LANG = os.environ.get("DEEPL_TARGET", "EN-US")
DEEPL_URL = os.environ.get("DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")
DEEPL_KEY = os.environ.get("DEEPL_API_KEY")

PROTECT = [
    "Credituz OS", "Credituz", "WhatsApp", "Sienge", "UAU", "Open Finance",
    "ICP-Brasil", "BACEN", "NFe", "Open Banking", "Microsoft for Startups",
    "Google for Startups", "Salesforce", "HubSpot", "Meta", "Google",
    "LinkedIn", "Instagram", "Facebook", "Pix", "FGTS", "Kenlo", "CV CRM",
]
SKIP_PARENTS = {"script", "style", "code", "pre", "noscript", "template"}
ATTRS_TEXT = ("alt", "aria-label", "placeholder", "title")
META_SPECS = [
    ("meta", {"name": "description"}, "content"),
    ("meta", {"property": "og:title"}, "content"),
    ("meta", {"property": "og:description"}, "content"),
    ("meta", {"name": "twitter:title"}, "content"),
    ("meta", {"name": "twitter:description"}, "content"),
]
URLISH = re.compile(r"^\s*(https?://|mailto:|tel:|wa\.me|/|#|\+?\d[\d\s().-]*$)")
ONLY_SYMBOLS = re.compile(r"^[\W\d_]+$")


def is_translatable_text(s):
    if isinstance(s, Comment):
        return False
    txt = s.strip()
    if not txt:
        return False
    parent = s.parent.name if s.parent else ""
    if parent in SKIP_PARENTS:
        return False
    if ONLY_SYMBOLS.match(txt):
        return False
    if URLISH.match(txt):
        return False
    return True


def protect_terms(text):
    mapping = {}
    out = text
    for i, term in enumerate(PROTECT):
        token = "\u2063X{}\u2063".format(i)
        if term in out:
            out = out.replace(term, token)
            mapping[token] = term
    return out, mapping


def restore_terms(text, mapping):
    for token, term in mapping.items():
        text = text.replace(token, term)
    return text


def deepl_translate(unique_texts):
    if not DEEPL_KEY:
        raise SystemExit("DEEPL_API_KEY nao definido")
    result = {}
    items = list(unique_texts)
    BATCH = 40
    i = 0
    while i < len(items):
        chunk = items[i:i + BATCH]
        protected, maps = [], []
        for t in chunk:
            p, m = protect_terms(t)
            protected.append(p)
            maps.append(m)
        data = [("target_lang", TARGET_LANG), ("source_lang", SOURCE_LANG),
                ("preserve_formatting", "1")]
        for p in protected:
            data.append(("text", p))
        body = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(DEEPL_URL, data=body, headers={
            "Authorization": "DeepL-Auth-Key {}".format(DEEPL_KEY),
            "Content-Type": "application/x-www-form-urlencoded",
        })
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                break
            except Exception:
                if attempt == 3:
                    raise
                time.sleep(2 * (attempt + 1))
        for orig, mp, tr in zip(chunk, maps, payload.get("translations", [])):
            result[orig] = restore_terms(tr["text"], mp)
        i += BATCH
        time.sleep(0.3)
    return result


def main():
    with open(SRC, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    text_nodes = [s for s in soup.find_all(string=True) if is_translatable_text(s)]
    meta_setters = []
    if soup.title and soup.title.string and soup.title.string.strip():
        meta_setters.append((soup.title, "_title_"))
    for name, sel, attr in META_SPECS:
        for el in soup.find_all(name, attrs=sel):
            if el.get(attr, "").strip() and not ONLY_SYMBOLS.match(el.get(attr).strip()):
                meta_setters.append((el, attr))
    attr_setters = []
    for el in soup.find_all(True):
        for a in ATTRS_TEXT:
            if el.has_attr(a) and isinstance(el.get(a), str):
                val = el.get(a).strip()
                if val and not ONLY_SYMBOLS.match(val) and not URLISH.match(val):
                    attr_setters.append((el, a))
    unique = set()
    for n in text_nodes:
        unique.add(str(n).strip())
    for el, attr in meta_setters:
        unique.add((el.string if attr == "_title_" else el.get(attr)).strip())
    for el, attr in attr_setters:
        unique.add(el.get(attr).strip())
    print("Strings unicas:", len(unique))
    table = deepl_translate(unique)

    def tr(s):
        return table.get(s.strip(), s)

    for n in text_nodes:
        original = str(n)
        stripped = original.strip()
        translated = table.get(stripped, stripped)
        prefix = original[:len(original) - len(original.lstrip())]
        suffix = original[len(original.rstrip()):]
        n.replace_with(NavigableString(prefix + translated + suffix))
    for el, attr in meta_setters:
        if attr == "_title_":
            el.string = tr(el.string)
        else:
            el[attr] = tr(el.get(attr))
    for el, attr in attr_setters:
        el[attr] = tr(el.get(attr))
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = "en"
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Gerado:", OUT)


if __name__ == "__main__":
    main()
