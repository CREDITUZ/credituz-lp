# Credituz Landing Page - GitHub Pages

## Configuração para GitHub Pages

Este site está configurado para ser hospedado no **GitHub Pages**.

### ✅ Checklist de Configuração

- [x] Arquivo `.nojekyll` criado (desabilita Jekyll)
- [ ] **TODO**: Ativar GitHub Pages nas settings do repositório
  - Vá para: **Settings > Pages**
  - Source: selecione **Deploy from a branch**
  - Branch: selecione **main** e pasta **root** `/`
  - Clique **Save**
- [ ] **TODO**: Criar workflow em `.github/workflows/deploy.yml` com conteúdo abaixo (se não existir)

### Workflow de Deploy Automático

Crie o arquivo `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      pages: write
      id-token: write
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v4
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 🌐 URL do Site

Após ativar GitHub Pages, seu site estará disponível em:
- `https://Pedrohbrazs.github.io/credituz-lp/`

Para usar domínio customizado (`credituz.ai`), adicione:
1. Arquivo `CNAME` na raiz do repo com conteúdo: `credituz.ai`
2. Configure DNS do domínio apontando para GitHub Pages

### 📋 Headers de Segurança

Para adicionar headers de segurança no GitHub Pages, crie `_config.yml`:

```yaml
plugins:
  - jekyll-sitemap

# Headers de segurança (via GitHub Pages)
```

---

**Status**: ✅ Pronto para GitHub Pages
