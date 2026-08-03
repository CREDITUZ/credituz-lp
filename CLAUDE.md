# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é

Site estático da Credituz (`credituz.ai`): landing page, páginas de segmento, blog com 119 artigos e um pacote GEO (Generative Engine Optimization) voltado a crawlers de IA. **Não há build step, bundler, `package.json`, testes ou lint.** Cada HTML é autocontido: CSS e JS inline, fontes via Google Fonts, ícones em `assets/`.

## Comandos

```bash
# Servir localmente (qualquer servidor estático serve; os links usam caminhos absolutos "/...")
python3 -m http.server 8000        # → http://localhost:8000

# Rodar a tradução PT→EN localmente (requer chave DeepL)
pip install beautifulsoup4
DEEPL_API_KEY=... python scripts/translate_en.py
```

Deploy: push na `main` → GitHub Pages publica a raiz do repo. `.nojekyll` impede o Jekyll de processar os `.md`. `CNAME` fixa o domínio `credituz.ai`.

## Arquitetura

### Camada humana (HTML) e camada de máquina (MD/JSON/TXT)

Todo conteúdo relevante existe em duas formas, e **as duas precisam ser atualizadas juntas**:

| Humano | Máquina (GEO/LLM) |
|---|---|
| `index.html` | `home.md`, `home.en.md`, `home.json` (JSON-LD) |
| `pages/glossario.html` | `pages/glossario.md` |
| `pages/artigos/<slug>.html` | `pages/artigos/<slug>.md` (119 pares 1:1) |
| — | `llms.txt` (índice), `llms-full.txt` (conteúdo consolidado), `sitemap.xml`, `robots.txt` |

`robots.txt` libera explicitamente GPTBot, ClaudeBot, PerplexityBot, Google-Extended e CCBot. `llms.txt` lista cada artigo por categoria com título + descrição; ao adicionar um artigo, atualize `llms.txt`, `llms-full.txt`, `sitemap.xml` e os contadores por categoria em `pages/blog.html`.

O JSON-LD da home vive **duplicado**: inline no `<head>` do `index.html` e em `home.json`. Mudanças de preço, plano, FAQ ou feature list precisam ser refletidas nos dois, mais em `home.md`/`home.en.md`.

### Internacionalização (PT → EN, automatizada)

`en/` é **gerado**, não editado à mão. O workflow `.github/workflows/translate-en.yml` dispara em push na `main` que toque `index.html`, `white-label.html` ou as páginas de marketing em `pages/`, roda `scripts/translate_en.py` (DeepL via `DEEPL_API_KEY`) e commita `en/` com `[skip ci]`. O gatilho ignora `en/**` para não entrar em loop.

O script preserva HTML, scripts, estilos e URLs; traduz apenas nós de texto, `title`, metas OG/Twitter e atributos `alt`/`aria-label`/`placeholder`/`title`. Detalhes que importam ao editar:

- `PROTECT` — termos de marca que nunca podem ser traduzidos (Credituz OS, WhatsApp, Sienge, Open Finance, ICP-Brasil, Pix, FGTS...). **Adicione novos nomes de produto/parceiro a essa lista** antes que apareçam na LP.
- `LEGAL_BASENAMES` — páginas jurídicas (`termos`, `privacidade`, `dpo`, `uso-aceitavel`, `glossario`, `blog`) que **não** são traduzidas; links para elas no EN são reescritos para `/pages/<arquivo>`.
- `PAGES` — a lista de páginas espelhadas. Uma nova página de marketing só ganha versão EN se for adicionada aqui.
- Editar `en/index.html` manualmente é desperdício: o próximo push em `index.html` sobrescreve.

### Páginas

- `index.html` (~223 KB) — LP principal, seções identificadas por `<section id="...">`: `roi`, `credituz-os`, `corban-ai`, `produto-por-dentro`, `produto`, `como-funciona`, `comparar`, `integracoes`, `pricing`, `indicacao`, `faq`, `metodologia`.
- `white-label.html` — oferta white label.
- `pages/` — segmento (`incorporadoras`, `imobiliarias`, `seja-parceiro`, `locacao-temporada`), `integracoes`, `blog`, `glossario` e jurídicas (`termos`, `privacidade`, `dpo`, `uso-aceitavel`).
- `pages/artigos/` — artigos com layout de leitura próprio (fonte serif Newsreader, barra de progresso, `max-width:720px`), distinto do layout da LP.

`pages/blog.html` tem busca e filtros por categoria em JS inline, com contadores hardcoded nos botões `data-cat`.

### Design system (replicado por arquivo, não compartilhado)

Não há CSS externo — cada página redeclara suas variáveis em `:root`. A paleta é consistente: `--ink #0a0a0a`, `--paper #fafaf7`, `--lime #c4f352`, `--lime-deep #9bd11a`, `--rust`, escala `--gray-1..3`. Fontes: Fraunces (títulos), Geist (LP), Newsreader (artigos), JetBrains Mono (eyebrows/meta). Ao criar uma página nova, copie o bloco `:root` + reset de uma página existente do mesmo tipo (LP ou artigo).

### Tracking

`index.html` carrega **dois** containers GTM (`GTM-KN3GQNDJ` e `GTM-T2M9N4CR`) e o Meta Pixel `3261631577333056`. CTAs apontam para `https://dashboard.usecredituz.com/auth/login?screen_hint=signup` e para o WhatsApp `https://wa.me/5511936201544`.

## Convenções

- Commits em português, Conventional Commits, **sem acentuação** no assunto, indicando o escopo bilíngue quando aplicável: `chore(layout): move a Calculadora de ROI para logo apos a secao Problema, PT e EN`.
- Links internos são absolutos a partir da raiz (`/pages/...`), então o site precisa ser servido pela raiz — abrir o HTML via `file://` quebra navegação e assets.
- `credituz-site-completo.zip` na raiz é um snapshot antigo do site; não é fonte de verdade.
