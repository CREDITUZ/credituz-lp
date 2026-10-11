# Auditoria de indexação, out/2026 (Fase 0)

Branch de revisão. Nada aqui foi publicado em produção. Merge somente após aprovação do Pedro.

## 1. Diagnóstico (Search Console, sc-domain:credituz.ai, 11/10/2026)

- Cliques mensais de abr a set/2026: 11, 65, 73, 64, 65, 57. Impressões: 88, 402, 497, 362, 622, 623.
- A maior parte dos cliques vem da consulta de marca "credituz" (38 cliques, posição média 2).
- Consultas não-marca quase não geram clique. Exemplos com impressão: "como usar ia dentro de um crm imobiliario" (32 impressões, posição 3), "crediluz" (25, posição 8.8, consulta de outra marca), "analise de credito imobiliario" (4, posição 27.5).
- Parcela de tráfego com cara de conversa com IA (AI-shaped): 0% a 9% das impressões, sem clique.

## 2. Sitemap

- https://credituz.ai/sitemap.xml: 178 URLs, todas no host canônico. Status da GSC: 178 enviadas, 0 indexadas. Erros: 0. Avisos: 0.
- https://www.credituz.ai/sitemap.xml: 178 enviadas, 0 indexadas. Avisos: 4. Ação: remover o sitemap www da GSC após confirmar o redirecionamento 301 de www para o domínio sem www.
- Observação: o contador de "indexadas" da GSC pode atrasar. Reavaliar em 14 dias antes de concluir.

## 3. URLs rastreadas sem indexação (15)

Prioritárias para a estratégia de crédito e cobrança:
- /pages/regua-de-cobranca-imobiliaria.html (Discovered, not indexed)
- /pages/politica-de-credito-para-incorporadoras.html (URL unknown to Google)
- /pages/portal-vendas-incorporadora.html (URL unknown to Google)
- /pages/gestao-de-unidades-imobiliarias.html (Discovered, not indexed)
- /pages/espelho-de-empreendimento.html (Discovered, not indexed)
- /pages/contratos-imobiliarios-digitais.html (Discovered, not indexed)
- /pages/contratos-imobiliarios-com-ia.html (URL unknown to Google)
- /pages/assinatura-digital-imobiliaria.html (URL unknown to Google)
- /pages/cartorio-digital-imobiliario.html (URL unknown to Google)
- /pages/imprensa.html (URL unknown to Google)
- /pages/baixa-conciliacao-recebiveis-imobiliarios.html (URL unknown to Google)
- /pages/artigos/como-controlar-disponibilidade-unidades-lancamento-imobiliario.html (URL unknown to Google)
- /pages/artigos/como-cobrar-parcelas-entrada-imovel-reduzir-inadimplencia.html (URL unknown to Google)
- /pages/artigos/assinatura-digital-vs-cartorio-contrato-imobiliario.html (Discovered, not indexed)
- /pages/artigos/credituz-vs-bureau-analise-credito-incorporadoras.html (URL unknown to Google)

Padrão: "URL is unknown to Google" indica que o Google não descobriu a página por links. "Discovered, not indexed" indica que descobriu mas não considerou digna de indexação ainda.

## 4. Problemas técnicos encontrados

1. **Canonical ausente no HTML.** A página de régua de cobrança não tem <link rel="canonical">. A informação de canonical aparece só no front matter do .md. Sem canonical explícito, o Google escolhe a URL. Correção: adicionar canonical em todas as páginas e artigos.
2. **Sem JSON-LD.** Não há bloco de dados estruturados (Article, FAQPage, Organization, BreadcrumbList, SoftwareApplication). Isso prejudica a compreensão por buscadores e por LLMs. Correção: adicionar por template.
3. **Links internos.** As páginas novas recebem pouco link de páginas com autoridade (home, blog). Correção: linkar cada página prioritária a partir da home, da página de blog e de pelo menos 3 artigos relacionados.
4. **Sitemap www.** Ainda enviado na GSC com avisos. Correção: remover após validar o 301.
5. **Títulos com "2025".** Dezenas de artigos com o ano no título e na URL. Correção: atualizar para 2026 onde houver dado atualizado, sem alterar URL já indexada (usar 301 se for trocar slug).
6. **Canibalização.** Vários artigos disputam a mesma intenção (análise de crédito, cobrança, inadimplência). Correção: consolidar ou diferenciar, conforme lista na fase 1 do plano.

## 5. Plano de correção desta branch (proposta, sem aplicar ainda)

- [ ] Validar redirecionamento 301 de www para o domínio sem www.
- [ ] Remover o sitemap www da GSC.
- [ ] Adicionar <link rel="canonical"> via template em todas as páginas.
- [ ] Adicionar JSON-LD por tipo de página (Article/FAQPage para artigos, Organization e SoftwareApplication para home e produto).
- [ ] Revisar as 15 URLs prioritárias e linkar a partir da home e do blog.
- [ ] Atualizar os títulos com "2025" conforme dado disponível.
- [ ] Revisar páginas que mencionem a grade antiga de planos (Essencial, Start, Growth, Service). A LP adota plano único de R$ 297/mês desde out/2026.
- [ ] Revisar a página credituz-vs-gyra: tom neutro, sem menção negativa aos investidores GYRA+.
- [ ] Após merge, solicitar reindexação das 15 URLs na GSC e reenviar o sitemap.
- [ ] Reavaliar em 14 dias: impressões não-marca, URLs indexadas e posição das consultas-alvo.

## 6. Consultas-alvo para medir

- análise de crédito imobiliário
- score de crédito financiamento
- régua de cobrança imobiliária
- cobrança com IA imobiliária
- análise financeira incorporadora

Somente após as correções acima faz sentido publicar os 20 artigos novos (fase 1).
