# Guia Credituz: regras de escrita dos artigos

Portal: https://guia.credituz.ai, conteúdo de crédito imobiliário para a PESSOA FÍSICA
(quem quer comprar, financiar ou já financiou um imóvel). Monetizado com Google AdSense,
então cada artigo precisa ser útil, original, preciso e atual (tema YMYL: dinheiro).

## Formato do arquivo

Um arquivo por artigo: `guia-src/artigos/<slug>.md`. O slug é curto, sem ano, sem acento,
em minúsculas com hífen (ex.: `sac-ou-price`). Frontmatter YAML obrigatório:

```yaml
---
title: "SAC ou Price: qual tabela escolher no financiamento do imóvel"   # até ~65 caracteres
description: "Frase de 140 a 160 caracteres que resume o que o leitor aprende."
category: financiamento        # um de: financiamento, fgts, programas, credito, custos, alternativas, direitos
published: 2026-10-19
updated: 2026-10-19
reading_minutes: 9             # palavras / 200, arredondado
key_points:                    # 3 a 5 frases curtas, o "resumo em 30 segundos"
  - "..."
faq:                           # 3 a 5 perguntas reais que as pessoas buscam
  - q: "Pergunta?"
    a: "Resposta direta em 1 a 3 frases."
sources:                       # 3 a 8 fontes, de preferência oficiais
  - title: "Nome da página ou documento"
    url: "https://..."
related: [outro-slug, mais-um-slug]   # 2 a 4 slugs da lista de pautas
---
```

Depois do frontmatter vem o corpo em Markdown. NÃO repita o título como `#`. Use `##` para
seções e `###` para subseções. Tabelas em Markdown são bem-vindas. Sem HTML no corpo.

## Público e tom

- Leitor: pessoa comum, 25 a 50 anos, primeira compra ou já com financiamento. Não é corretor,
  não é incorporadora, não é correspondente bancário. Nada de "dicas para corretores venderem".
- Português do Brasil, "você", direto, frases curtas, sem jargão sem explicação. Explique a
  sigla na primeira vez (ex.: "CET (Custo Efetivo Total)").
- Comece respondendo a pergunta do título no primeiro parágrafo. Nada de introdução genérica
  ("O sonho da casa própria..."), nada de "neste artigo vamos explorar".
- Sem clichês de texto de IA: proibido "desvende", "mergulhe", "navegar pelas complexidades",
  "crucial", "jornada", "em suma", "vale ressaltar", "no cenário atual", "é fundamental".
- PROIBIDO travessão: nunca use "—" nem "–" em lugar nenhum (nem em título). Use vírgula,
  dois-pontos, parênteses ou ponto. O build reprova o arquivo se encontrar.
- Sem emoji. Sem exclamação.

## Precisão (o mais importante)

- Data de referência: outubro de 2026. Pesquise na web (WebSearch/WebFetch) toda regra, limite,
  taxa ou valor que possa ter mudado: Selic, tetos do SFH, regras do FGTS, faixas do MCMV,
  limites da Caixa, alíquota de ITBI etc. Não confie na memória para números.
- Todo número concreto precisa ter fonte no frontmatter e, quando relevante, a data no texto
  ("em outubro de 2026, a Selic está em X%, segundo o Copom"). Se não achar fonte confiável
  e atual, NÃO invente: escreva de forma qualitativa ou diga que o valor muda e onde consultar.
- Prefira fontes oficiais: gov.br, Caixa, Banco Central (bcb.gov.br), Planalto (leis), CMN,
  prefeituras, Receita, STJ, Serasa/Boa Vista para score, Abecip. Mídia séria (Valor, Folha,
  Estadão, InfoMoney, g1) serve para notícia recente.
- Taxas de banco mudam toda semana: se citar, diga a data e a fonte, e mostre como comparar
  (CET), em vez de cravar "o banco X é o mais barato".
- Exemplos numéricos (simulação de SAC/Price, ITBI etc.) devem ser calculados de verdade
  (rode um cálculo em Python se precisar) e marcados como exemplo ilustrativo.
- Direitos (distrato, atraso de obra): cite a lei pelo número (ex.: Lei 13.786/2018) e
  não dê conselho jurídico individual; recomende procurar advogado ou Procon quando couber.
- Não recomende produto, banco ou investimento específico. Explique, compare e mostre
  como a pessoa decide.

## Direitos autorais

Escreva tudo com as suas palavras. Nunca copie trechos das fontes; no máximo uma citação
curta (menos de 15 palavras) por fonte, entre aspas, só se a redação exata importar.
Não reproduza a estrutura de um artigo de terceiro.

## Tamanho e estrutura

- 1.400 a 2.200 palavras de corpo.
- 5 a 9 seções `##`, com pelo menos: a resposta direta, o passo a passo ou o "como funciona",
  um exemplo prático com números, erros comuns ou cuidados, e um "Resumo" ou "Próximos passos".
- Pelo menos uma tabela quando o tema comparar coisas.
- Links internos: cite 2 a 4 outros artigos do guia no texto como `[texto](/artigos/<slug>)`,
  só para slugs da lista de pautas abaixo. Calculadoras: `[simulador de financiamento](/simulador)`
  e `[calculadora de quanto posso financiar](/quanto-posso-financiar)`.
- Não mencione a Credituz no corpo. Não faça chamada comercial.

## Lista de pautas (slug: tema)

financiamento
- como-funciona-financiamento-imobiliario: guia completo de como funciona o financiamento (pilar)
- taxa-de-juros-financiamento-imobiliario: taxas em 2026, Selic, TR, CET e como comparar bancos
- sac-ou-price: diferença entre SAC e Price, com simulação
- entrada-para-financiar-imovel: quanto de entrada é preciso, cota de financiamento por banco/modalidade
- renda-para-financiar-imovel: quanto preciso ganhar, regra dos 30%, como os bancos calculam
- renda-composta: financiar com renda somada (cônjuge, parentes, amigos)
- financiamento-autonomo-mei: como autônomo e MEI comprovam renda para financiar
- portabilidade-financiamento-imobiliario: quando vale a pena e como fazer
- amortizar-financiamento-prazo-ou-parcela: amortização extra, reduzir prazo ou parcela
- imovel-na-planta-ou-pronto: financiar na planta ou pronto, diferenças de crédito e risco
fgts
- fgts-na-compra-do-imovel: regras para usar o FGTS na entrada/compra
- fgts-para-amortizar-financiamento: usar FGTS para amortizar, quitar ou pagar parcelas
- saque-aniversario-e-financiamento: como o saque-aniversário afeta o uso do FGTS na casa própria
programas
- minha-casa-minha-vida: faixas, renda, subsídio, juros e como se inscrever em 2026
- sfh-e-sfi: diferenças entre SFH e SFI, limites de valor e regras em 2026
credito
- score-para-financiamento-imobiliario: score, o que o banco avalia e como melhorar
- nome-sujo-financiamento-imobiliario: dá para financiar com restrição no CPF
- financiamento-negado: por que o banco nega e o que fazer
- cadastro-positivo-e-open-finance: como ajudam na análise de crédito
custos
- custos-para-comprar-imovel: todos os custos além da entrada (ITBI, escritura, registro, avaliação)
- itbi: o que é, quem paga, como calcular, desconto no financiamento
- documentos-para-financiamento: checklist de documentos do comprador e do imóvel
- seguros-mip-e-dfi: seguros obrigatórios do financiamento
- avaliacao-do-imovel-pelo-banco: como funciona a avaliação e o que fazer se vier abaixo
alternativas
- consorcio-ou-financiamento: comparação com simulação
- home-equity: crédito com garantia de imóvel, quando faz sentido e riscos
- alugar-ou-comprar: como fazer a conta
direitos
- distrato-imovel-na-planta: Lei do Distrato, quanto se recebe de volta
- atraso-na-entrega-do-imovel: prazo de tolerância, multas e direitos
- juros-de-obra: taxa de evolução de obra, como funciona e como reduzir
