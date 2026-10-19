---
title: "Consórcio ou poupar: qual junta mais para comprar imóvel"
description: "Compare consórcio e poupança com aplicação em CDB: simulação com parcela, CDI, reajuste INCC e a diferença entre ter a carta e ter o dinheiro guardado."
category: alternativas
published: 2026-10-19
updated: 2026-10-19
reading_minutes: 8
key_points:
  - "Para juntar uma carta de R$ 300 mil corrigida em 5 anos, o CDB líquido exigiria cerca de R$ 5.192 por mês. No consórcio, a parcela inicial é de R$ 1.800."
  - "A comparação honesta não é só de custo: no consórcio você pode receber a carta antes de ter o valor todo, mas continua pagando parcelas."
  - "Poupar dá liquidez e não tem taxa de administração. Consórcio dá disciplina e uma data incerta de uso."
  - "Com o mesmo valor mensal, a aplicação rende mais que o consórcio se você sair antes da contemplação, porque a devolução tem prazo e correção próprios."
  - "Em outubro de 2026, o CDI estava em 13,65% ao ano, e a poupança rende 0,5% ao mês mais TR quando a Selic está acima de 8,5%."
faq:
  - q: "Consórcio rende mais que a poupança?"
    a: "Não é uma comparação de rendimento. O consórcio não rende nada para você; ele entrega um crédito corrigido pelo INCC, com taxa de administração. A aplicação em CDB ou poupança é a alternativa para acumular dinheiro."
  - q: "Vale mais guardar o dinheiro no CDB ou entrar no consórcio?"
    a: "Se você quer o imóvel em poucos anos e pode ficar com o dinheiro aplicado, o CDB costuma ser mais flexível. Se a disciplina de parcela fixa é o que falta, o consórcio pode ajudar, desde que a taxa seja comparada."
  - q: "A poupança rende quanto em 2026?"
    a: "Pela regra da Lei 12.703/2012, quando a Selic está acima de 8,5% ao ano, a poupança rende 0,5% ao mês mais a TR. Com a Selic em 13,75%, esse é o caso em outubro de 2026."
  - q: "Consórcio é mais barato que financiamento para comprar casa?"
    a: "Depende do prazo até a contemplação e da taxa de administração. O guia de consórcio ou financiamento faz essa comparação com simulação própria."
sources:
  - title: "Banco Central: Selic e Copom (reunião de 16/09/2026), via notícias de mercado"
    url: "https://www.bcb.gov.br/"
  - title: "Lei 8.177/1991, art. 12, II (redação da Lei 12.703/2012), remuneração da poupança"
    url: "https://www.legjur.com/legislacao/art/lei_00081771991-12"
  - title: "FGV, INCC-M setembro de 2026 (press release via SindusconSP)"
    url: "https://sindusconsp.com.br/wp-content/uploads/2026/09/INCC-M_FGV_press-release_Set26.pdf"
  - title: "Lei 11.795/2008 (Lei dos Consórcios), arts. 24 e 30"
    url: "https://www.planalto.gov.br/ccivil_03/_ato2007-2010/2008/lei/l11795.htm"
  - title: "Resolução BCB 285/2023 (regras dos grupos de consórcio), arts. 19 e 21"
    url: "https://static.poder360.com.br/2023/01/resolucao-bcb-consorcios-285-19jan2023-1.pdf"
  - title: "Banco Central: Panorama do Sistema de Consórcios 2024 (taxa média de administração)"
    url: "https://www.bcb.gov.br/content/estabilidadefinanceira/panoramaconsorcio/panorama_de_consorcios_2024.pdf"
related: [consorcio-ou-financiamento, consorcio-para-investir, consorcio-desistencia, consorcio-taxa-de-administracao]
---

Consórcio e poupança servem ao mesmo objetivo, juntar dinheiro para um imóvel, mas funcionam de formas opostas. A poupança e o CDB guardam o que você deposita e pagam juros sobre esse saldo. O consórcio junta os seus pagamentos num fundo comum, desconta a taxa de administração e entrega uma carta de crédito quando você é contemplado. Por isso, a pergunta útil não é qual "rende mais", e sim quanto você precisa colocar por mês para chegar ao imóvel, quando e com que flexibilidade.

Este guia faz essa conta com números. Para entender as peças do consórcio, veja antes [como funciona o consórcio imobiliário](/artigos/consorcio-imobiliario-como-funciona).

## Os dois caminhos em uma frase

- **Poupar:** você aplica todo mês em CDB ou outra renda fixa, deixa o dinheiro render e usa o saldo quando quiser, com ou sem imóvel escolhido.
- **Consórcio:** você paga parcelas corrigidas pelo INCC, a administradora cobra taxa de administração, e em algum mês do grupo você recebe a carta para comprar o imóvel. Depois continua pagando as parcelas restantes.

Essa diferença muda tudo. Na poupança, o imóvel só é comprado quando você tem o dinheiro. No consórcio, você compra antes de juntar tudo, mas assume uma dívida com o grupo.

## Quanto rende cada opção em 2026

Em outubro de 2026, a Selic estava em 13,75% ao ano, definida na reunião do Copom de 16 de setembro, sem reunião posterior até a data. O CDI, referência para CDB, estava em 13,65%.

A poupança segue regra própria. Pela Lei 8.177/1991, com a redação da Lei 12.703/2012, quando a meta da Selic está acima de 8,5% ao ano, a poupança rende 0,5% ao mês mais a Taxa Referencial (TR). Com a TR em cerca de 2% ao ano, o rendimento efetivo fica perto de 8,3% ao ano. Um CDB de banco grande, atrelado a 100% do CDI, rende mais que isso antes do imposto de renda.

O CDB tem Imposto de Renda regressivo sobre o rendimento, de 22,5% em até 180 dias a 15% acima de 720 dias. Nos exemplos abaixo usamos 15%, que vale para aplicações de longo prazo. A poupança é isenta.

Para o consórcio, o que importa é a taxa de administração e o reajuste. Em 2024, a média dos grupos novos de imóveis foi de 20,84%, segundo o Banco Central. O INCC-M acumulava 6,61% em 12 meses em setembro de 2026, segundo a FGV.

## A simulação: juntar uma carta de R$ 300 mil

Exemplo ilustrativo, calculado em Python. O objetivo é ter, no mês 60 ou no mês 120, um valor igual à carta de R$ 300 mil corrigida pelo INCC, que seria R$ 413.153 em 5 anos e R$ 568.985 em 10 anos. As premissas:

- **Consórcio:** carta de R$ 300 mil, 200 meses, taxa de administração de 18%, fundo de reserva de 2%, parcela inicial de R$ 1.800, reajuste anual de 6,61%.
- **Poupança alternativa:** o mesmo valor mensal aplicado em CDB a 100% do CDI líquido de 15% de imposto, ou seja, cerca de 11,6% ao ano. Como a parcela do consórcio também sobe, o aporte da alternativa também é reajustado.
- Em 60 meses, o total pago no consórcio, somando as parcelas reajustadas, é de R$ 123.253.

### Resultado em 5 anos

| Item | Consórcio | Aplicação em CDB (mesmo aporte) |
|---|---|---|
| Quanto você desembolsa até o mês 60 | R$ 123.253 | R$ 123.253 |
| Valor que você tem nas mãos no mês 60 | Carta de R$ 413.153, com saldo devedor de parcelas | R$ 161.192 |
| O que dá para comprar com esse valor | Um imóvel de R$ 413 mil, financiado pelo grupo | Entrada ou imóvel menor |
| Parcelas que você ainda paga | Cerca de R$ 500 mil em valores nominais, de 140 parcelas | Nenhuma |

Repare no que a tabela mostra. No consórcio, a carta de R$ 413 mil já está com você no mês 60, mas você ainda deve cerca de R$ 500 mil em parcelas nominais. Na aplicação, você tem R$ 161 mil sem dívida nenhuma.

Para juntar R$ 413 mil em 60 meses, sem nenhuma dívida, você precisaria aplicar cerca de R$ 5.192 por mês, em valor fixo, no CDB líquido. É mais que o dobro da parcela do consórcio, e é esse o desafio real de poupar.

### Resultado em 10 anos

Em 120 meses, o consórcio entrega a carta de R$ 568.985 e a parcela já subiu para cerca de R$ 3.200. A aplicação com o mesmo aporte reajustado acumula R$ 501 mil. A diferença é menor do que a da tabela de 5 anos, mas a carta ainda está acima do saldo guardado, e a dívida do consórcio continua por mais 80 parcelas.

## Quando o consórcio perde

O consórcio costuma perder na comparação direta de patrimônio por três razões:

- **A taxa de administração é um custo que a poupança não tem.** Em 18% sobre a carta, ela equivale a R$ 54 mil em valores de hoje, pagos ao longo de 200 meses.
- **O crédito fica preso à contemplação.** Se o sorteio atrasar, você continua pagando sem ter o imóvel. Lance ajuda, mas exige dinheiro guardado, que poderia estar rendendo no CDB.
- **Se você desistir, a devolução tem prazo.** A Lei 11.795/2008 devolve o que você pagou ao fundo comum, corrigido, mas a devolução sai por sorteio ou no encerramento do grupo. Veja as regras em [desistência do consórcio](/artigos/consorcio-desistencia). Na poupança, o dinheiro está disponível no dia seguinte.

Ou seja: se você tem disciplina para poupar e sabe que pode precisar do dinheiro antes do imóvel, a aplicação oferece liquidez que o consórcio não tem.

## Quando o consórcio pode ganhar

O consórcio tem vantagens reais que a planilha de rendimentos não captura:

- **Obriga a poupar.** Parcela automática e fixa funciona para quem não consegue juntar por conta própria.
- **Não exige entrada grande nem análise de crédito antes da contemplação.** A análise acontece depois, na hora de usar a carta.
- **Trava o preço do crédito.** A carta é corrigida pelo INCC, que mede custo de construção. Se o preço dos imóveis subir mais que o INCC, a carta fica defasada no mercado, mas se subir menos, ela protege você.
- **Pode ser usado com o FGTS**, para lance ou para completar a carta, seguindo as regras da Caixa, o que não existe numa aplicação comum.

Esses pontos fazem diferença para quem não tem reserva e precisa de um empurrão. Para quem já consegue poupar, o CDB tende a ser mais eficiente.

## Como decidir na prática

Faça as três contas abaixo com a sua realidade, não só com a simulação:

1. **Quanto consegue poupar por mês, de forma constante?** Se o valor for menor que a parcela do consórcio, a aplicação não vai chegar ao imóvel no prazo que você imagina.
2. **Quanto tempo você aguenta esperar?** Com contemplação incerta, o consórcio pode levar anos. Se você paga aluguel, cada ano de espera tem custo. O guia de [alugar ou comprar](/artigos/alugar-ou-comprar) ajuda nessa conta.
3. **Você precisa de liquidez?** Se pode ter que usar o dinheiro antes do imóvel, a aplicação tem vantagem clara.

Se a sua resposta for "consigo poupar pouco, preciso de prazo e não tenho outra alternativa", o consórcio pode ajudar. Antes de assinar, compare a taxa de administração com a média de 20,84% e leia o regulamento do grupo.

## Erros comuns

- **Comparar a parcela com o rendimento.** Parcela de consórcio não é aplicação; ela é pagamento de crédito futuro.
- **Esquecer o reajuste da parcela.** No exemplo, ela passa de R$ 1.800 para cerca de R$ 2.479 em 5 anos.
- **Ignorar a poupança como base.** Ela é isenta de imposto de renda, mas rende menos que o CDB atrelado ao CDI nas condições de 2026.
- **Usar a carta contemplada para investir.** Pelas regras, receber a carta em dinheiro exige quitar o saldo devedor, e não gera ganho. Veja [consórcio para investir](/artigos/consorcio-para-investir).

## Resumo

- Para juntar R$ 413 mil em 5 anos com CDB líquido, seria preciso poupar cerca de R$ 5.192 por mês, mais que o dobro da parcela inicial do consórcio.
- No consórcio, você recebe a carta no mês 60, mas ainda deve cerca de R$ 500 mil em parcelas nominais.
- A aplicação dá liquidez e não tem taxa de administração; o consórcio dá disciplina e carta antecipada, com dívida.
- Com a Selic em 13,75% em outubro de 2026, a poupança rende 0,5% ao mês mais TR, e o CDB atrelado ao CDI rende mais.
- Compare o seu valor mensal, o prazo que aguenta esperar e a necessidade de liquidez antes de escolher. Para comparar com um financiamento, use [consórcio ou financiamento](/artigos/consorcio-ou-financiamento).
