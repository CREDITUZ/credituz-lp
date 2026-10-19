---
title: "Juros de obra: o que é a taxa de evolução e como pagar menos"
description: "Entenda os juros de obra (taxa de evolução de obra) no financiamento na planta: como são calculados, por que a parcela sobe, quando param e o que diz o STJ."
category: direitos
published: 2026-10-19
updated: 2026-10-19
reading_minutes: 7
key_points:
  - "Juros de obra são os encargos que você paga ao banco enquanto o prédio é construído, sem amortizar a dívida."
  - "Eles incidem só sobre o dinheiro que o banco já liberou à construtora, por isso sobem conforme a obra avança."
  - "A amortização só começa depois da conclusão e da averbação da obra na matrícula; atrasos nessa etapa prolongam a cobrança."
  - "No Minha Casa, Minha Vida, o STJ considera ilícito cobrar juros de obra depois do prazo de entrega com a tolerância."
faq:
  - q: "O que são juros de obra?"
    a: "São os encargos mensais cobrados pelo banco durante a construção, no financiamento de imóvel na planta: juros, atualização monetária, seguros e, se houver, taxa de administração. Eles não reduzem o saldo devedor."
  - q: "Por que os juros de obra aumentam todo mês?"
    a: "Porque o banco libera o dinheiro à construtora conforme a obra avança. Quanto mais liberado, maior o saldo sobre o qual os juros incidem."
  - q: "Quando param os juros de obra?"
    a: "Quando a obra é concluída e averbada na matrícula, e o contrato passa para a fase de amortização. Até lá, a cobrança pode continuar mesmo com as chaves na mão."
  - q: "Juros de obra são ilegais?"
    a: "Não, quando previstos no contrato e cobrados dentro do prazo. O STJ considera ilícita a cobrança após o prazo de entrega com tolerância, no Minha Casa, Minha Vida (Tema 996)."
  - q: "Juros de obra e juros no pé são a mesma coisa?"
    a: "Não. Juros de obra são cobrados pelo banco no financiamento. Juros no pé são cobrados pela incorporadora nas parcelas pagas direto a ela antes das chaves."
sources:
  - title: "Caixa: cartilha de financiamento para construção, conclusão, reforma e ampliação (PF)"
    url: "https://www.caixa.gov.br/Downloads/habitacao-documentos-gerais/cartilha-habitacao-PF-construcao-conclusao-reforma-ampliacao-de-unidades-habitacionais.pdf"
  - title: "STJ, Tema 996 (REsp 1.729.593/SP): juros de obra após o prazo de entrega"
    url: "https://processo.stj.jus.br/repetitivos/temas_repetitivos/pesquisa.jsp?novaConsulta=true&tipo_pesquisa=T&cod_tema_inicial=996&cod_tema_final=996"
  - title: "Dizer o Direito: juros no pé e o EREsp 670.117/PB (STJ, 2012)"
    url: "https://www.dizerodireito.com.br/2012/07/o-que-sao-juros-no-pe-eles-sao.html"
  - title: "Migalhas: legalidade dos encargos no período de obras no MCMV (IRDR do TJSP)"
    url: "https://www.migalhas.com.br/depeso/281265/da-legalidade-da-cobranca-de-encargos-no-periodo-de-obras-em-empreendimentos-populares-financiados-pelo-programa-do-governo-federal-minha-casa-minha-vida"
  - title: "Lei 13.786/2018 (prazo de tolerância de 180 dias)"
    url: "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13786.htm"
related: [imovel-na-planta-ou-pronto, atraso-na-entrega-do-imovel, minha-casa-minha-vida, seguros-mip-e-dfi]
---

Juros de obra, também chamados de taxa de evolução de obra, são os encargos que você paga ao banco todo mês enquanto o imóvel comprado na planta está sendo construído. Eles não abatem a dívida: servem para remunerar o dinheiro que o banco já repassou à construtora. Como o repasse acompanha o andamento da obra, a cobrança começa pequena e cresce até a conclusão. Só depois que a obra é concluída e averbada na matrícula começam as parcelas normais, com amortização.

Esse modelo é comum no crédito associativo da Caixa e de outros bancos, inclusive no Minha Casa, Minha Vida, em que você assina o financiamento ainda durante a obra.

## Como funciona

1. **Você assina o financiamento com a obra em andamento.** O contrato define o valor total financiado, mas o banco não entrega tudo de uma vez à construtora.
2. **O banco libera o dinheiro aos poucos.** A cada medição, o banco confere o percentual da obra concluído e repassa a parte correspondente.
3. **Você paga encargos sobre o que foi liberado.** Segundo a cartilha da Caixa, durante a obra cabe ao cliente pagar juros de obra, atualização monetária, seguros e taxa de administração, quando houver. Os juros incidem sobre o percentual do financiamento já liberado, não sobre o total contratado.
4. **A obra termina e é averbada.** A Caixa informa que a amortização começa depois da conclusão da obra e da averbação na matrícula. A partir daí, vêm as parcelas da tabela SAC ou Price.

### O que entra no boleto da fase de obra

| Componente | O que é |
|---|---|
| Juros | taxa do contrato aplicada sobre o saldo já liberado |
| Atualização monetária | correção do saldo pela TR (Taxa Referencial), nos contratos que a usam |
| Seguros MIP e DFI | seguro de morte e invalidez e seguro de danos ao imóvel, obrigatórios (veja [seguros MIP e DFI](/artigos/seguros-mip-e-dfi)) |
| Taxa de administração | quando prevista no contrato |

## Exemplo: como a cobrança cresce

Exemplo ilustrativo, calculado em Python. Premissas: financiamento de R$ 300 mil, taxa nominal de 10,5% ao ano (0,875% ao mês), obra de 24 meses, banco liberando 10% no primeiro mês e chegando a 100% no último, em ritmo linear. Sem TR, seguros e taxa de administração.

| Momento | Liberado | Juros de obra no mês |
|---|---|---|
| Mês 1 | 10% (R$ 30 mil) | R$ 262 |
| Mês 12 | cerca de 53% | R$ 1.392 |
| Mês 24 | 100% (R$ 300 mil) | R$ 2.625 |
| Total em 24 meses | | R$ 34.650 |

Repare: R$ 34.650 pagos ao banco sem reduzir um real da dívida. E se a averbação atrasar 6 meses depois de 100% liberado, são mais 6 x R$ 2.625, ou R$ 15.750, de juros puros.

Por isso o prazo de obra e a burocracia depois dela pesam no seu bolso. Na vida real, a liberação não é linear: depende do cronograma, e o valor muda com a TR e os seguros. Confira no extrato do banco o saldo liberado de cada mês.

## Quando os juros de obra param

A cobrança termina quando o contrato passa para a fase de amortização, o que exige:

- obra concluída e habite-se emitido pela prefeitura;
- averbação da construção na matrícula do imóvel, no Cartório de Registro de Imóveis;
- em muitos casos, individualização das matrículas das unidades.

Ou seja, receber as chaves não encerra automaticamente os juros de obra. Se a construtora demora a averbar, você pode continuar pagando encargos por meses já morando no imóvel.

## O que diz a Justiça

**Cobrança dentro do prazo é permitida.** Os tribunais costumam aceitar os juros de obra quando estão previstos no contrato e a obra está dentro do prazo.

**Cobrança após o prazo de entrega, no MCMV, é ilícita.** No Tema 996, julgado em setembro de 2019, o STJ fixou que, nos contratos do Minha Casa, Minha Vida, é ilícito cobrar do comprador juros de obra ou encargo equivalente depois do prazo contratual de entrega das chaves, incluída a tolerância. O caso chegou ao STJ a partir de um incidente de resolução de demandas repetitivas (IRDR) do Tribunal de Justiça de São Paulo, que já considerava ilícito esse repasse após o prazo contratual.

O prazo de tolerância, em contratos de incorporação firmados após a Lei 13.786/2018, é de no máximo 180 dias. Para entender os direitos quando a obra atrasa, veja [atraso na entrega do imóvel](/artigos/atraso-na-entrega-do-imovel).

Em contratos fora do MCMV, a resposta depende das cláusulas e do caso. Alguns contratos já preveem que a construtora assume os encargos após certo atraso. Leia o seu e, havendo dúvida, procure o Procon, a Defensoria ou um advogado.

### Juros de obra x juros no pé

| | Juros de obra | Juros no pé |
|---|---|---|
| Quem cobra | o banco | a incorporadora |
| Sobre o quê | o valor já liberado pelo banco à construtora | as parcelas que você paga direto à incorporadora antes das chaves |
| Posição do STJ | lícitos no prazo; ilícitos no MCMV após o prazo com tolerância (Tema 996) | cláusula não abusiva, desde que clara no contrato (EREsp 670.117, 2012) |

## Como reduzir o quanto você paga

- **Pergunte o estágio da obra antes de assinar.** Assinar o financiamento com a obra mais adiantada significa menos meses de juros de obra. Se a obra já está em 50%, o banco libera essa parte logo, mas você paga por menos tempo.
- **Exija o cronograma e a previsão de averbação por escrito.** Atrasos na averbação são juros que você paga sem necessidade.
- **Confira a memória de cálculo.** Saldo liberado x taxa nominal ÷ 12, mais TR, seguros e tarifa. Se o boleto não bater, peça a explicação ao banco.
- **Use amortização extra na fase certa.** Em geral, amortizar durante a obra tem pouco efeito ou não é aceito; confirme com o banco. A [amortização extra](/artigos/amortizar-financiamento-prazo-ou-parcela) costuma render mais depois que as parcelas normais começam.
- **Monitore o prazo final.** Passado o prazo de entrega com tolerância, no MCMV, a cobrança de juros de obra contra você é ilícita segundo o STJ. Guarde os boletos pagos depois dessa data.

## Como conferir o seu boleto

Você não precisa ser especialista para checar se a cobrança faz sentido. Peça ao banco, pelo aplicativo ou na agência, o extrato da fase de obra com o saldo liberado em cada mês. Depois faça a conta:

1. **Juros do mês:** saldo liberado x taxa nominal anual do contrato ÷ 12. Exemplo: R$ 150.000 x 10,5% ÷ 12 = R$ 1.312,50.
2. **Atualização:** saldo liberado x TR do mês, se o contrato usar TR. Com TR baixa, esse valor é pequeno.
3. **Seguros:** MIP e DFI aparecem no contrato ou no extrato; mudam com a idade e o valor do imóvel.
4. **Taxa de administração:** valor fixo mensal, se o contrato prever.

Se a diferença entre o boleto e a sua conta for maior do que seguros e tarifa explicam, peça a memória de cálculo por escrito. Use a taxa nominal do contrato, não a efetiva; em geral é a nominal que o banco divide por 12 nessa conta. Se o contrato trouxer outra regra, siga o contrato.

### Planejamento do orçamento na fase de obra

No financiamento na planta, muita gente paga três coisas ao mesmo tempo: as parcelas da entrada à incorporadora, os juros de obra ao banco e o aluguel de onde mora. Monte uma planilha mês a mês com as três, usando o valor máximo dos juros de obra (o do fim da obra), e veja se o orçamento aguenta o pico. Depois, some a primeira parcela da fase de amortização, que costuma ser maior do que o último boleto de juros de obra, porque passa a incluir a devolução do principal.

## Erros comuns

- **Achar que já está pagando o imóvel.** Na fase de obra, o saldo devedor não cai.
- **Planejar o orçamento pela primeira cobrança.** No exemplo, ela vai de R$ 262 a R$ 2.625. Reserve espaço para a parcela máxima, e depois para a primeira parcela de amortização, que é maior.
- **Somar juros de obra com as parcelas da incorporadora sem fazer conta.** Em muitos contratos você paga as duas coisas ao mesmo tempo.
- **Achar que receber as chaves encerra a cobrança.** Ela só acaba com a averbação.

## Resumo

- Juros de obra remuneram o dinheiro já liberado pelo banco durante a construção e não amortizam a dívida.
- Crescem com o avanço da obra e só param com a conclusão e a averbação na matrícula.
- No MCMV, cobrar juros de obra do comprador após o prazo de entrega com tolerância é ilícito (STJ, Tema 996).
- Se ainda está decidindo, compare os custos e riscos no guia [imóvel na planta ou pronto](/artigos/imovel-na-planta-ou-pronto) e simule a fase de amortização no [simulador de financiamento](/simulador).
