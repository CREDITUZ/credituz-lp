# Credituz — Landing Page + Blog + GEO

Site estático da Credituz: landing page, blog com 119 artigos e pacote GEO (Generative Engine Optimization) para visibilidade em IAs.

## Estrutura

```
index.html              → Landing page principal
home.md                 → Versão markdown da LP (para IAs/agentes)
llms.txt                → Índice do site para LLMs
llms-full.txt           → Conteúdo consolidado para LLMs
robots.txt              → Libera crawlers de IA (GPTBot, ClaudeBot, etc.)
sitemap.xml             → Mapa do site (243 URLs)
pages/
  blog.html             → Índice do blog com busca e filtros
  artigos/
    *.html              → 119 páginas de artigo (layout de leitura)
    *.md                → 119 versões markdown (para IAs)
```

## Deploy via GitHub Pages

1. Crie um repositório no GitHub e suba estes arquivos (veja comandos abaixo)
2. Em **Settings → Pages**, selecione **GitHub Actions** como source
3. O workflow `.github/workflows/deploy.yml` publica automaticamente a cada push na branch `main`

### Comandos para subir

```bash
git init
git add .
git commit -m "Deploy: LP + blog (119 artigos) + pacote GEO"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPO.git
git push -u origin main
```

## Domínio customizado (www.credituz.ai)

Para servir em `www.credituz.ai`, adicione um arquivo `CNAME` na raiz com:
```
www.credituz.ai
```
E configure o DNS conforme a documentação do GitHub Pages.

## Importante: Content-Type dos arquivos .md

O GitHub Pages serve `.md` como `text/html` por padrão. Para GEO funcionar idealmente,
os arquivos `.md` devem ser servidos como `text/plain` ou `text/markdown`. Se isso for
crítico, considere Netlify ou Vercel (que permitem configurar headers via `_headers` ou
`vercel.json`). O arquivo `.nojekyll` já garante que o GitHub Pages não processe os `.md`.
