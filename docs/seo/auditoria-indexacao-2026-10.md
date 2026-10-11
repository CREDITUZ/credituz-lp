# Auditoria de indexacao, out/2026 (Fase 0), versao corrigida

Branch de revisao. Nada aqui foi publicado em producao. Merge somente apos aprovacao do Pedro.

## Correcao em relacao a versao anterior

A versao anterior deste relatorio dizia que faltava <link rel="canonical"> nas paginas. Isso estava errado. Conferencia direta do HTML:

- Os 183 HTMLs do repositorio ja tem <link rel="canonical">.
- 180 apontam para https://credituz.ai/ com o caminho correto. As 3 restantes sao intencionais:
  - pages/incorporadoras.html e pages/locacao-temporada.html sao noindex e apontam para as paginas equivalentes (construtoras e imobiliarias).
  - lp/loteadoras/index.html aponta para https://loteadoras.credituz.ai/, que e o host correto dessa LP.
- Canonical nao precisa de correcao.

## Dados estruturados (JSON-LD)

- 45 paginas ja tinham JSON-LD e nao foram alteradas.
- 2 paginas noindex foram excluidas de proposito.
- 136 paginas receberam JSON-LD nesta branch:
  - 120 artigos: tipo Article, com headline (title), description (meta description), url canonica, inLanguage e publisher Organization (Credituz).
  - 16 demais paginas: tipo WebPage, com isPartOf WebSite.
- Verificacao: cada bloco foi validado como JSON antes de ser gravado. Cada arquivo alterado difere do original somente pelo bloco inserido.

## Diagnostico (Search Console, sc-domain:credituz.ai, 11/10/2026)

- Cliques mensais de abr a set/2026: 11, 65, 73, 64, 65, 57. Impressoes: 88, 402, 497, 362, 622, 623.
- A maior parte dos cliques vem da consulta de marca "credituz" (38 cliques, posicao media 2).
- Consultas nao-marca quase nao geram clique. Exemplos com impressao: "como usar ia dentro de um crm imobiliario" (32 impressoes, posicao 3), "analise de credito imobiliario" (4, posicao 27.5). "crediluz" (25) e consulta de outra marca.
- Trafego com cara de conversa com IA: 0% a 9% das impressoes, sem clique.

## Sitemap

- https://credituz.ai/sitemap.xml: 178 URLs, todas no host correto. GSC: 178 enviadas, 0 indexadas, 0 erros, 0 avisos.
- https://www.credituz.ai/sitemap.xml: 178 enviadas, 0 indexadas, 4 avisos. Acao: remover este sitemap da GSC depois de confirmar o redirecionamento 301 de www para o dominio sem www.
- Nao foi possivel verificar o 301 a partir da sandbox (acesso ao site bloqueado pela politica de rede). Verificacao manual necessaria.
- O contador de indexadas pode estar atrasado. Reavaliar em 14 dias antes de concluir.

## Causas provaveis do baixo rastreamento

1. Paginas orfas: 7 paginas sem nenhum link interno de entrada: pages/imprensa.html, pages/artigos/assinatura-digital-vs-cartorio-contrato-imobiliario.html, pages/artigos/como-cobrar-parcelas-entrada-imovel-reduzir-inadimplencia.html, pages/artigos/como-controlar-disponibilidade-unidades-lancamento-imobiliario.html, pages/artigos/credituz-vs-bureau-analise-credito-incorporadoras.html, en/pages/locacao-temporada.html e lp/loteadoras/index.html.
2. Artigos fora do pipeline do blog: 4 artigos existem so em HTML, sem arquivo .md de origem. Por isso nao aparecem na listagem gerada pelo blog (127 artigos listados de 131 existentes). Acao: criar o .md de origem ou incluir na listagem, conforme decisao do Pedro.
3. Links internos fracos nas prioritarias: pages/portal-vendas-incorporadora.html, gestao-de-unidades-imobiliarias.html, espelho-de-empreendimento.html e contratos-imobiliarios-com-ia.html tem 1 link de entrada cada. pages/regua-de-cobranca-imobiliaria.html tem 9, bom sinal.
4. Autoridade de dominio em crescimento: o site tem poucos backlinks e pouco trafego nao-marca. JSON-LD ajuda compreensao, mas nao substitui isso.

## Checklist

- [x] JSON-LD nas paginas sem dados estruturados (esta branch).
- [ ] Verificar redirecionamento 301 de www para o dominio sem www (manual, no provedor de hospedagem).
- [ ] Remover o sitemap www da GSC apos a verificacao acima.
- [ ] Decidir sobre os 7 links orfaos (aprovacao do Pedro).
- [ ] Decidir sobre os 4 artigos fora do blog: criar .md ou incluir na listagem (aprovacao do Pedro).
- [ ] Linkar as 4 prioritarias com 1 link de entrada a partir do blog e de artigos relacionados (aprovacao do Pedro).
- [ ] Atualizar titulos com "2025" conforme dado disponivel.
- [ ] Revisar paginas com a grade antiga de planos (Essencial, Start, Growth, Service). A LP adota plano unico de R$ 297/mes desde out/2026.
- [ ] Revisar credituz-vs-gyra: tom neutro, sem mencao negativa aos investidores GYRA+.
- [ ] Apos merge: solicitar reindexacao das URLs prioritarias na GSC e reenviar o sitemap.
- [ ] Reavaliar em 14 dias: impressoes nao-marca, URLs indexadas e posicao das consultas-alvo.

## Consultas-alvo para medir

- analise de credito imobiliario
- score de credito financiamento
- regua de cobranca imobiliaria
- cobranca com IA imobiliaria
- analise financeira incorporadora


## Atualização: medições e ações (2026-10-11)

### Medições no GSC (via GSC Wizard)
- Sitemap principal: 178 URLs enviadas, **130 com impressões** (campo `indexedInGscCount`). O campo agregado `contents.indexed = 0` **não** deve ser usado como base: a correção anterior deste relatório que afirmava "0 indexadas" está superada.
- 48 URLs sem impressão, classificadas pela inspeção:
  - 16 indexadas, mas sem exposição (indexadas sem demanda nas consultas atuais);
  - 23 desconhecidas pelo Google (sem registro de rastreamento);
  - 9 descobertas ou rastreadas, mas não indexadas.
- Diagnóstico corrigido: o problema não é falta de conteúdo. É majoritariamente falta de sinais internos (descoberta e exposição) e demanda limitada em parte dos temas.
- Páginas órfãs (sem link de entrada): 7, incluindo os 4 rascunhos, `pages/imprensa.html`, `en/pages/locacao-temporada.html` e `lp/loteadoras/index.html`.

### Divergência entre endpoints (não resolvida)
- `GET_PAGE_PERFORMANCE` / sitemap somam ~2.599 impressões e 71 cliques em 28 dias.
- A tendência mensal mostra ~600 impressões/mês.
- Ação: conferir o número na interface do Search Console antes de usar como KPI.

### Bing
- Sem chave configurada (`notConfigured`). Ação pendente do responsável pelo domínio.

### Ações aplicadas (commit 8c7e14e)
- B: bloco "Leia também" com 3 links internos em 6 artigos do cluster imobiliário.
- C: `noindex, follow` nos 4 rascunhos (`assinatura-digital-vs-cartorio-contrato-imobiliario`, `como-cobrar-parcelas-entrada-imovel-reduzir-inadimplencia`, `como-controlar-disponibilidade-unidades-lancamento-imobiliario`, `credituz-vs-bureau-analise-credito-incorporadoras`).
- `sitemap.xml` regenerado: 178 -> 174 URLs (sem os 4 rascunhos).

### Pendências
- Verificar manualmente o 301 de `www.credituz.ai` para `credituz.ai` (não verificável a partir do ambiente).
- Remover o sitemap com `www` da GSC, se existir.
- Configurar a chave do Bing.
- Decidir sobre títulos com "2025" e CTR baixo.
- Decidir sobre as órfãs restantes.
- Reavaliar em 14 dias; só então iniciar a fase 1 (20 novos artigos).


## Atualização: itens A, B e C (2026-10-11)
- www.credituz.ai NÃO redireciona para credituz.ai (curl confirmou página normal em www). Correção pendente: 301 de www para o domínio principal na camada de hospedagem (Vercel ou GitHub Pages). Enquanto não corrigido, há conteúdo duplicado.
- Search Console: continua registrado https://www.credituz.ai/sitemap.xml (4 avisos). Remover pela interface do GSC após corrigir o 301.
- Bing: pendente de chave do responsável pelo domínio.
- Órfãs: imprensa linkada no rodapé da home; en/pages/locacao-temporada linkada no rodapé da versão en; lp/loteadoras linkada a partir de 2 artigos de loteadoras.
- Títulos com 2025: lista e proposta em docs/seo/titulos-2025-proposta.md. Nenhum título alterado até aprovação.
