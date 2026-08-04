#!/usr/bin/env python3
"""
Traduz as paginas de marketing da LP de PT para EN preservando todo o HTML,
scripts, estilos, URLs e termos de marca. Gera os espelhos em en/.

Motor: DeepL. Requer DEEPL_API_KEY. Conta gratuita usa a URL api-free (padrao);
para Pro defina DEEPL_API_URL=https://api.deepl.com/v2/translate.

O resultado de cada trecho fica em scripts/translation-cache.json, versionado no
repo. Sem ele, toda execucao remandava as 7 paginas inteiras (~49 mil caracteres)
e a cota gratuita de 500 mil/mes rendia ~10 rodadas. Com o cache, so o texto que
mudou vai para a API. Para forcar a retraducao completa, rode com
TRANSLATION_CACHE_BUST=1.

Paginas juridicas (termos, privacidade, dpo, uso-aceitavel) ficam de fora de
proposito; links para elas no EN passam a apontar para a versao em portugues.
"""
import os
import re
import json
import time
import urllib.request
import urllib.parse

from bs4 import BeautifulSoup, NavigableString, Comment

SOURCE_LANG = "PT"
TARGET_LANG = os.environ.get("DEEPL_TARGET", "EN-US")
DEEPL_URL = os.environ.get("DEEPL_API_URL", "https://api-free.deepl.com/v2/translate")
DEEPL_KEY = os.environ.get("DEEPL_API_KEY")

# Paginas de marketing: (origem PT, destino EN). Juridicas ficam de fora.
PAGES = [
    ("index.html", "en/index.html"),
    ("white-label.html", "en/white-label.html"),
    ("pages/incorporadoras.html", "en/pages/incorporadoras.html"),
    ("pages/imobiliarias.html", "en/pages/imobiliarias.html"),
    ("pages/seja-parceiro.html", "en/pages/seja-parceiro.html"),
    ("pages/locacao-temporada.html", "en/pages/locacao-temporada.html"),
    ("pages/integracoes.html", "en/pages/integracoes.html"),
]

# Paginas que NAO sao traduzidas; links para elas no EN apontam para o PT.
LEGAL_BASENAMES = {
    "privacidade.html", "termos.html", "dpo.html", "uso-aceitavel.html",
    "glossario.html", "blog.html",
}

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

CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "translation-cache.json")
CACHE_BUST = os.environ.get("TRANSLATION_CACHE_BUST") == "1"

CACHE = {}
# Chaves usadas nesta execucao. O arquivo e reescrito so com elas, para nao
# acumular texto de secoes que ja sairam da pagina.
USED = set()


def load_cache():
    """Le o cache do disco. Idioma alvo diferente invalida tudo: a traducao
    guardada e para outro destino."""
    if CACHE_BUST or not os.path.exists(CACHE_PATH):
        return
    try:
        with open(CACHE_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (ValueError, OSError):
        return
    if data.get("target_lang") != TARGET_LANG:
        return
    CACHE.update(data.get("entries", {}))


def save_cache(podar=False):
    """Grava o cache. Durante o loop salva tudo (`podar=False`): se a API falhar
    na 5a pagina, o que ja foi pago nas quatro primeiras nao se perde. So no fim,
    com todas as paginas lidas, e seguro descartar o que ninguem usa mais."""
    entries = {k: CACHE[k] for k in sorted(USED)} if podar else dict(CACHE)
    payload = {
        "target_lang": TARGET_LANG,
        "entries": {k: entries[k] for k in sorted(entries)},
    }
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")


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
    USED.update(unique_texts)
    pending = [t for t in unique_texts if t not in CACHE]
    reaproveitados = len(unique_texts) - len(pending)
    chars = sum(len(t) for t in pending)
    print("  {} trechos: {} do cache, {} para a API ({} caracteres)".format(
        len(unique_texts), reaproveitados, len(pending), chars))
    if not pending:
        return
    if not DEEPL_KEY:
        raise SystemExit("DEEPL_API_KEY nao definido")
    BATCH = 40
    i = 0
    while i < len(pending):
        chunk = pending[i:i + BATCH]
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
            CACHE[orig] = restore_terms(tr["text"], mp)
        i += BATCH
        time.sleep(0.3)


def rewrite_legal_links(soup):
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") or href.startswith("mailto") or href.startswith("tel"):
            continue
        base = href.split("?")[0].split("#")[0].rstrip("/").split("/")[-1]
        if base in LEGAL_BASENAMES:
            a["href"] = "/pages/" + base


def translate_file(src, out):
    with open(src, encoding="utf-8") as f:
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
    deepl_translate(unique)

    def tr(s):
        return CACHE.get(s.strip(), s)

    for n in text_nodes:
        original = str(n)
        stripped = original.strip()
        translated = CACHE.get(stripped, stripped)
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
    rewrite_legal_links(soup)
    html_tag = soup.find("html")
    if html_tag:
        html_tag["lang"] = "en"
    outdir = os.path.dirname(out)
    if outdir:
        os.makedirs(outdir, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print("Gerado:", out)


def main():
    load_cache()
    print("Cache: {} trechos ja traduzidos{}".format(
        len(CACHE), " (ignorado por TRANSLATION_CACHE_BUST)" if CACHE_BUST else ""))
    for src, out in PAGES:
        if os.path.exists(src):
            translate_file(src, out)
            save_cache()
        else:
            print("Origem ausente, pulando:", src)
    save_cache(podar=True)
    print("Cache gravado com {} trechos em {}".format(len(USED & set(CACHE)), CACHE_PATH))


if __name__ == "__main__":
    main()
