from pathlib import Path
import re

def sub1(s, pattern, repl, label, flags=0):
    out, n = re.subn(pattern, repl, s, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'{label}: expected 1 replacement, got {n}')
    return out

def add_before(s, marker, block, label):
    if block.strip() in s:
        return s
    if marker not in s:
        raise SystemExit(f'{label}: marker missing')
    return s.replace(marker, block + '\n' + marker, 1)

# Construtoras
p=Path('pages/construtoras.html'); s=p.read_text(encoding='utf-8')
s=sub1(s,r'<title>.*?</title>','<title>Análise de crédito e financiamento para construtoras | Credituz</title>','c title')
s=sub1(s,r'<meta name="description" content="[^"]*">','<meta name="description" content="Analise o comprador antes de financiar a entrada, acompanhe o financiamento até o repasse e controle contratos, cobrança e unidades em uma única plataforma.">','c meta')
s=sub1(s,r'<link rel="canonical" href="[^"]+">','<link rel="canonical" href="https://credituz.ai/pages/construtoras.html">','c canonical')
s=sub1(s,r'<h1>Financie a entrada de quem <span class="hl">o banco vai aprovar</span> no repasse\.</h1>','<h1>Venda hoje para quem o banco <span class="hl">vai financiar amanhã.</span></h1>','c h1')
s=sub1(s,r'<p class="lead">A Credituz analisa o comprador.*?</p>','<p class="lead">Analise o comprador antes de financiar a entrada, simule o crédito em múltiplos bancos e acompanhe cada operação até o repasse. Menos risco de distrato, mais previsibilidade de carteira e uma única visão da venda até a chave.</p>','c lead',re.S)
s=sub1(s,r'<div class="hero-actions">.*?</div>', '<div class="hero-actions">\n        <a class="btn btn-dark" data-track="segment_construtoras_start" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=construtoras" target="_blank" rel="noopener">Começar agora</a>\n        <a class="btn btn-soft" data-track="segment_construtoras_how" href="#jornada-credito">Ver como funciona</a>\n    </div>','c actions',re.S)
s=sub1(s,r'<div class="proof-strip">.*?</div>','<div class="proof-strip">\n        <span><b>Score</b> e política de crédito própria</span>\n        <span><b>Multibancos</b> em uma única jornada</span>\n        <span><b>CRM de crédito</b> até o repasse</span>\n        <span><b>Carteira</b> com visão por unidade</span>\n    </div>','c proof',re.S)
s=s.replace('<h2>O prejuízo começa dois anos antes de aparecer.</h2>','<h2>O risco nasce na venda. O problema só aparece no repasse.</h2>',1)
s=s.replace('<p class="sub">Quem financia a entrada assume o risco de crédito sozinho — e só descobre o erro quando o banco entra na conversa.</p>','<p class="sub">Quando a construtora parcela a entrada sem uma leitura adequada de crédito, pode carregar o risco por meses até descobrir que o comprador não consegue concluir o financiamento bancário.</p>',1)
s=s.replace('<h2>Aprove hoje quem o banco vai aprovar depois.</h2>','<h2>Aumente a chance de financiar no repasse antes de assumir o risco.</h2>',1)
s=s.replace('<p class="sub">Você escreve a política de crédito, consulta bureaus e mede capacidade de renda no ato da venda — com a mesma régua que vai decidir o repasse lá na frente. É o que transforma análise em seguro contra distrato.</p>','<p class="sub">Use política própria, bureau, capacidade de pagamento e sinais de crédito para selecionar melhor quem entra na carteira. A decisão final de financiamento continua sendo do banco, mas sua operação chega ao repasse com muito mais contexto e controle.</p>',1)
journey_c='''<section class="wrap" id="jornada-credito">
  <div class="tag">Do contrato ao repasse</div>
  <h2>Depois de pedir o financiamento, você continua enxergando a operação.</h2>
  <p class="sub">Credituz OS e CORBAN AI conectam simulação, solicitação, documentos, pendências e status bancário. Comercial, backoffice e cliente deixam de depender de planilhas e mensagens soltas para saber o próximo passo.</p>
  <div class="jornada">
    <div class="j-step hot"><span class="j-n">01</span><b>Analise antes da venda</b><span class="j-d">Score, política de crédito e capacidade de pagamento ajudam a decidir quem entra na carteira.</span></div>
    <div class="j-step"><span class="j-n">02</span><b>Simule e solicite</b><span class="j-d">Compare cenários e organize o pedido de financiamento em uma jornada única.</span></div>
    <div class="j-step"><span class="j-n">03</span><b>Acompanhe pendências</b><span class="j-d">Saiba o que falta, onde a operação está e qual é o próximo passo com o cliente.</span></div>
    <div class="j-step"><span class="j-n">04</span><b>Chegue ao repasse</b><span class="j-d">Mantenha visibilidade da contratação e da unidade até a conclusão da jornada financeira.</span></div>
  </div>
  <blockquote class="depo" style="margin-top:24px"><p>“Saímos de uma situação de baixo controle para o <strong>controle total da nossa carteira</strong>. Hoje sabemos exatamente o status de cada unidade, cada contrato e cada repasse.”</p><footer><span><b>Adson Soares</b><br>Gestor de Incorporação · NJS Engenharia</span></footer></blockquote>
</section>'''
s=add_before(s,'<section class="wrap" id="funcionalidades">',journey_c,'c journey')
if '"Credituz para construtoras e incorporadoras"' not in s:
    schema='<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"Análise de crédito e financiamento para construtoras","url":"https://credituz.ai/pages/construtoras.html"},{"@type":"Service","name":"Credituz para construtoras e incorporadoras","provider":{"@type":"Organization","name":"Credituz","url":"https://credituz.ai/"},"areaServed":"BR","serviceType":"Análise de crédito e operação de financiamento imobiliário"}]}</script>\n'
    s=s.replace('</head>',schema+'</head>',1)
p.write_text(s,encoding='utf-8')

# Imobiliarias
p=Path('pages/imobiliarias.html'); s=p.read_text(encoding='utf-8')
s=sub1(s,r'<title>.*?</title>','<title>CRM de crédito e financiamento para imobiliárias | Credituz</title>','i title')
s=sub1(s,r'<meta name="description" content="[^"]*">','<meta name="description" content="Analise o comprador, simule em múltiplos bancos, solicite o financiamento e acompanhe cada etapa até a contratação com o CRM de crédito da Credituz.">','i meta')
s=sub1(s,r'<link rel="canonical" href="[^"]+">','<link rel="canonical" href="https://credituz.ai/pages/imobiliarias.html">','i canonical')
s=sub1(s,r'<h1>Analise o crédito de quem compra <span class="hl">e de quem aluga</span>\.</h1>','<h1>Simule, peça e acompanhe o financiamento <span class="hl">sem tirar o cliente da sua operação.</span></h1>','i h1')
s=sub1(s,r'<p class="lead">A Credituz aprova comprador e inquilino.*?</p>','<p class="lead">Analise o comprador, simule em múltiplos bancos, solicite o crédito e acompanhe cada etapa até a contratação. Seu corretor vende o imóvel e continua enxergando o financiamento.</p>','i lead',re.S)
s=sub1(s,r'<div class="hero-actions">.*?</div>', '<div class="hero-actions">\n        <a class="btn btn-dark" data-track="segment_imobiliarias_start" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=imobiliarias" target="_blank" rel="noopener">Simular um financiamento</a>\n        <a class="btn btn-soft" data-track="segment_imobiliarias_how" href="#jornada-credito">Ver como funciona</a>\n    </div>','i actions',re.S)
s=sub1(s,r'<div class="proof-strip">.*?</div>','<div class="proof-strip">\n        <span><b>CRM de crédito</b> do pedido à contratação</span>\n        <span><b>Multibancos</b> para comparar cenários</span>\n        <span><b>Score</b> antes de avançar a venda</span>\n        <span><b>CORBAN AI</b> conectado à jornada</span>\n    </div>','i proof',re.S)
s=s.replace('<h2>A decisão de crédito não é sua — e devia ser.</h2>','<h2>A venda não termina quando o cliente pede financiamento.</h2>',1)
s=s.replace('<p class="sub">Na venda e na locação, quem aprova hoje é o banco ou a seguradora. Você fica com o risco e sem a receita.</p>','<p class="sub">Quando a proposta sai da imobiliária e vai para banco, correspondente ou parceiro, o corretor perde visibilidade. O cliente continua perguntando — mas a informação fica espalhada.</p>',1)
s=s.replace('<h2>A régua de aprovação passa a ser sua.</h2>','<h2>Crédito deixa de ser uma caixa-preta depois da venda.</h2>',1)
s=s.replace('<p class="sub">O mesmo motor decide o comprador e o inquilino: você escreve a política, consulta bureaus e mede capacidade de pagamento no ato — sem depender da análise do banco ou da seguradora para saber se aquele contrato vai se pagar.</p>','<p class="sub">Analise o comprador antes de avançar, organize a solicitação e acompanhe documentos, pendências e status do financiamento. A decisão bancária continua sendo da instituição financeira; a visibilidade da jornada fica com a sua equipe.</p>',1)
journey_i='''<section class="wrap" id="jornada-credito">
  <div class="tag">CRM de crédito + CORBAN AI</div>
  <h2>O corretor continua acompanhando o cliente depois do pedido de crédito.</h2>
  <p class="sub">A Credituz transforma financiamento em uma jornada rastreável: da simulação à contratação, com status compartilhado entre comercial, operação e cliente.</p>
  <div class="jornada">
    <div class="j-step hot"><span class="j-n">01</span><b>Analise o comprador</b><span class="j-d">Use score e sinais de crédito antes de investir tempo em uma operação que pode não avançar.</span></div>
    <div class="j-step"><span class="j-n">02</span><b>Simule em bancos</b><span class="j-d">Compare cenários de financiamento sem pulverizar a jornada em diferentes ferramentas.</span></div>
    <div class="j-step"><span class="j-n">03</span><b>Solicite o crédito</b><span class="j-d">Centralize documentos e informações necessárias para iniciar o processo.</span></div>
    <div class="j-step"><span class="j-n">04</span><b>Acompanhe o status</b><span class="j-d">Veja pendências, movimentações e próximos passos até a contratação.</span></div>
  </div>
</section>'''
s=add_before(s,'<section class="wrap" id="funcionalidades">',journey_i,'i journey')
locacao='''<section class="wrap" id="locacao">
  <div class="tag">Também administra locação?</div>
  <h2>Use a mesma infraestrutura para analisar e cobrar sua carteira.</h2>
  <p class="sub">Para operações de locação, a Credituz também pode apoiar a análise do inquilino e organizar cobrança, recebíveis e conciliação conforme os recursos contratados e disponíveis.</p>
  <div class="grid">
    <div class="card"><div class="num">01</div><h3>Análise de crédito</h3><p>Score, política própria e sinais de risco para apoiar a decisão de locação.</p></div>
    <div class="card"><div class="num">02</div><h3>Cobrança e recebíveis</h3><p>Organize régua de cobrança, meios de pagamento e baixa/conciliação da carteira.</p></div>
  </div>
</section>'''
s=add_before(s,'<section class="wrap" id="preco">',locacao,'i locacao')
if '"Credituz para imobiliárias"' not in s:
    schema='<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"WebPage","name":"CRM de crédito e financiamento para imobiliárias","url":"https://credituz.ai/pages/imobiliarias.html"},{"@type":"Service","name":"Credituz para imobiliárias","provider":{"@type":"Organization","name":"Credituz","url":"https://credituz.ai/"},"areaServed":"BR","serviceType":"CRM de crédito e financiamento imobiliário"}]}</script>\n'
    s=s.replace('</head>',schema+'</head>',1)
p.write_text(s,encoding='utf-8')
