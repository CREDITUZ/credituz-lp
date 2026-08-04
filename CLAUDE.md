# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## O que é

Site estático da Credituz (`credituz.ai`): landing page, páginas de segmento, blog com 119 artigos e um pacote GEO (Generative Engine Optimization) voltado a crawlers de IA. **Não há build step, bundler, `package.json`, testes ou lint.** Cada HTML é autocontido: CSS e JS inline, fontes via Google Fonts, ícones em `assets/`.

## Comandos

```bash
# Servir localmente (qualquer servidor estático serve; os links usam caminhos absolutos "/...")
# O http.server manda .md sem charset e o navegador assume latin-1 (acento vira mojibake);
# a producao serve "text/markdown; charset=utf-8" corretamente.
python3 -c "import http.server,socketserver as s;h=http.server.SimpleHTTPRequestHandler;h.extensions_map['.md']='text/markdown; charset=utf-8';s.TCPServer(('',8000),h).serve_forever()"

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

O resultado de cada trecho fica em `scripts/translation-cache.json`, **versionado e commitado pelo próprio Action** junto com `en/`. Sem ele toda execução remandava as 7 páginas inteiras (~49 mil caracteres) e a cota gratuita da DeepL — 500 mil/mês — rendia só ~10 rodadas; com ele, uma frase alterada custa algumas dezenas de caracteres. O cache é gravado a cada página, então uma falha de API no meio não descarta o que já foi pago, e é podado ao final (texto que saiu da página sai do arquivo). Trocar `DEEPL_TARGET` invalida tudo, porque a tradução guardada é para outro destino; para forçar a retradução completa, rode com `TRANSLATION_CACHE_BUST=1`.

A chave vive no secret `DEEPL_API_KEY` (plano API Free, chave terminada em `:fx`, endpoint `api-free.deepl.com` — que já é o padrão do script).

### Páginas

- `index.html` (~223 KB) — LP principal, seções identificadas por `<section id="...">`: `roi`, `credituz-os`, `corban-ai`, `produto-por-dentro`, `produto`, `como-funciona`, `comparar`, `integracoes`, `pricing`, `indicacao`, `faq`, `metodologia`.
- `white-label.html` — oferta white label.
- `pages/` — segmento (`incorporadoras`, `imobiliarias`, `seja-parceiro`, `locacao-temporada`), `integracoes`, `blog`, `glossario` e jurídicas (`termos`, `privacidade`, `dpo`, `uso-aceitavel`).
- `pages/artigos/` — artigos com layout de leitura próprio (fonte serif Newsreader, barra de progresso, `max-width:720px`), distinto do layout da LP.

`pages/blog.html` tem busca e filtros por categoria em JS inline, com contadores hardcoded nos botões `data-cat`.

### Design system (replicado por arquivo, não compartilhado)

Não há CSS externo — cada página redeclara suas variáveis em `:root`. Ao criar uma página nova, copie o bloco `:root` + reset de uma página existente do mesmo tipo (LP ou artigo).

**Todo o site em PT já roda o DNA de `correspondente.credituz.ai`** (documentado em `docs/DESIGN.md`): superfícies quase brancas, um único acento azul, cenas pretas de contraste e tipografia do sistema — **nenhuma página carrega Google Fonts**. Os nomes de token `--lime`/`--lime-deep`/`--rust` foram mantidos para não reescrever as ~4.000 linhas que os consomem, mas **os valores são azuis** (`#0071e3` / `#0066cc`). Sobre cena escura o acento é `--accent-bright #6bb2ff`, porque `#0071e3` não lê no preto; `--warn`/`--bad` cobrem o que era semanticamente negativo. O wordmark é `assets/logo-credituz.png` (`-branco.png` sobre fundo escuro), não mais texto.

Os 132 arquivos compartilham **6 blocos de CSS distintos**, cada um replicado byte a byte dentro do seu grupo. Ao editar o estilo de um grupo, replique nos demais arquivos dele:

| Bloco | Arquivos |
|---|---|
| LP | `index.html` |
| segmento | `pages/{incorporadoras,imobiliarias,seja-parceiro,locacao-temporada}.html` |
| interna | `pages/{integracoes,termos,privacidade,dpo,uso-aceitavel}.html` |
| artigo | os 119 `pages/artigos/*.html` (idêntico nos 119) |
| blog | `pages/blog.html` |
| glossário | `pages/glossario.html` |
| white label | `white-label.html` |

`en/**` é gerado e herda o estilo do PT no próximo push (ver Internacionalização).

**Navbar adaptativa.** Toda página tem, antes de `</body>`, um script que inverte a nav (`.on-dark`) quando a faixa dela cobre uma seção escura. A detecção lê a **luminância do fundo computado** de cada `section`/`footer`/`header`, então seção escura nova funciona sozinha; para forçar, use `data-nav-dark` no elemento. Cada bloco de CSS traz as regras `nav.on-dark` correspondentes (fundo `rgba(29,29,31,.72)`, logo invertida por `filter: brightness(0) invert(1)`, CTA em branco).

### Tracking

`index.html` carrega **dois** containers GTM (`GTM-KN3GQNDJ` e `GTM-T2M9N4CR`) e o Meta Pixel `3261631577333056`. CTAs apontam para `https://dashboard.usecredituz.com/auth/login?screen_hint=signup` e para o WhatsApp `https://wa.me/5511936201544`.

## Convenções

- Commits em português, Conventional Commits, **sem acentuação** no assunto, indicando o escopo bilíngue quando aplicável: `chore(layout): move a Calculadora de ROI para logo apos a secao Problema, PT e EN`.
- Links internos são absolutos a partir da raiz (`/pages/...`), então o site precisa ser servido pela raiz — abrir o HTML via `file://` quebra navegação e assets.
- `docs/` guarda a documentação interna (design system, deploy). Fica fora da raiz de propósito: o GitHub Pages publica o repositório inteiro, e o `robots.txt` bloqueia `/docs/` e `/scripts/` para não misturar documentação com a landing page nos buscadores e nos crawlers de IA.
