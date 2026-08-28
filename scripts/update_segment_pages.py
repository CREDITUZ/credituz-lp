from pathlib import Path
import re


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'missing marker: {label}')
    return text.replace(old, new, 1)

# ---------- Construtoras ----------
p = Path('pages/construtoras.html')
s = p.read_text(encoding='utf-8')
s = replace_once(s, '<title>Plataforma com IA para construtoras | Credituz</title>', '<title>Análise de crédito e financiamento para construtoras | Credituz</title>', 'construtoras title')
s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Analise o comprador antes de financiar a entrada, acompanhe o financiamento até o repasse e controle contratos, cobrança e unidades em uma única plataforma.">', s, count=1)
s = replace_once(s, '<link rel="canonical" href="https://www.credituz.ai/pages/construtoras.html">', '<link rel="canonical" href="https://credituz.ai/pages/construtoras.html">', 'construtoras canonical')

s = replace_once(s,
'''    <h1>Financie a entrada de quem <span class="hl">o banco vai aprovar</span> no repasse.</h1>
    <p class="lead">A Credituz analisa o comprador com a sua política de crédito antes de você assumir o risco — e conduz a venda até a chave: simulação multibanco, contrato com IA, cobrança e o espelho do empreendimento numa fonte única.</p>
    <div class="hero-actions">
        <a class="btn btn-dark" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=saas-credituzai" target="_blank" rel="noopener">Testar agora!</a>
        <a class="btn btn-soft" href="https://wa.me/5511936209409" target="_blank" rel="noopener">Falar com um especialista</a>
    </div>''',
'''    <h1>Venda hoje para quem o banco <span class="hl">vai financiar amanhã.</span></h1>
    <p class="lead">Analise o comprador antes de financiar a entrada, simule o crédito em múltiplos bancos e acompanhe cada operação até o repasse. Menos risco de distrato, mais previsibilidade de carteira e uma única visão da venda até a chave.</p>
    <div class="hero-actions">
        <a class="btn btn-dark" data-track="segment_construtoras_start" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=construtoras" target="_blank" rel="noopener">Começar agora</a>
        <a class="btn btn-soft" data-track="segment_construtoras_how" href="#jornada-credito">Ver como funciona</a>
    </div>''', 'construtoras hero')

s = re.sub(r'''    <div class="proof-strip">\s*<span><b>R\$ 300M</b> em crédito solicitado</span>\s*<span><b>&lt;30s</b> por simulação</span>\s*<span><b>80%</b> menos tempo de fechamento</span>\s*<span><b>\+40</b> operações na plataforma</span>\s*</div>''',
'''    <div class="proof-strip">
        <span><b>Score</b> e política de crédito própria</span>
        <span><b>Multibancos</b> em uma única jornada</span>
        <span><b>CRM de crédito</b> até o repasse</span>
        <span><b>Carteira</b> com visão por unidade</span>
    </div>''', s, count=1)

s = replace_once(s, '<h2>O prejuízo começa dois anos antes de aparecer.</h2>', '<h2>O risco nasce na venda. O problema só aparece no repasse.</h2>', 'construtoras problem h2')
s = replace_once(s, '<p class="sub">Quem financia a entrada assume o risco de crédito sozinho — e só descobre o erro quando o banco entra na conversa.</p>', '<p class="sub">Quando a construtora parcela a entrada sem uma leitura adequada de crédito, pode carregar o risco por meses até descobrir que o comprador não consegue concluir o financiamento bancário.</p>', 'construtoras problem sub')
s = replace_once(s, '<h2>Aprove hoje quem o banco vai aprovar depois.</h2>', '<h2>Aumente a chance de financiar no repasse antes de assumir o risco.</h2>', 'construtoras motor h2')
s = replace_once(s, '<p class="sub">Você escreve a política de crédito, consulta bureaus e mede capacidade de renda no ato da venda — com a mesma régua que vai decidir o repasse lá na frente. É o que transforma análise em seguro contra distrato.</p>', '<p class="sub">Use política própria, bureau, capacidade de pagamento e sinais de crédito para selecionar melhor quem entra na carteira. A decisão final de financiamento continua sendo do banco, mas sua operação chega ao repasse com muito mais contexto e controle.</p>', 'construtoras motor sub')

journey = '''\n<section class="wrap" id="jornada-credito">\n  <div class="tag">Do contrato ao repasse</div>\n  <h2>Depois de pedir o financiamento, você continua enxergando a operação.</h2>\n  <p class="sub">Credituz OS e CORBAN AI conectam simulação, solicitação, documentos, pendências e status bancário. Comercial, backoffice e cliente deixam de depender de planilhas e mensagens soltas para saber o próximo passo.</p>\n  <div class="jornada">\n    <div class="j-step hot"><span class="j-n">01</span><b>Analise antes da venda</b><span class="j-d">Score, política de crédito e capacidade de pagamento ajudam a decidir quem entra na carteira.</span></div>\n    <div class="j-step"><span class="j-n">02</span><b>Simule e solicite</b><span class="j-d">Compare cenários e organize o pedido de financiamento em uma jornada única.</span></div>\n    <div class="j-step"><span class="j-n">03</span><b>Acompanhe pendências</b><span class="j-d">Saiba o que falta, onde a operação está e qual é o próximo passo com o cliente.</span></div>\n    <div class="j-step"><span class="j-n">04</span><b>Chegue ao repasse</b><span class="j-d">Mantenha visibilidade da contratação e da unidade até a conclusão da jornada financeira.</span></div>\n  </div>\n  <div class="depo" style="margin-top:24px;border-radius:22px;padding:28px 26px">\n    <div class="tag" style="margin-bottom:10px">NJS Engenharia</div>\n    <p style="font-size:19px;line-height:1.5;max-width:850px">“Saímos de uma situação de baixo controle para o controle total da nossa carteira. Hoje sabemos exatamente o status de cada unidade, cada contrato e cada repasse.”</p>\n    <p style="margin-top:10px;color:var(--gray-2);font-size:14px">Adson Soares · Gestor de Incorporação</p>\n  </div>\n</section>\n'''
if 'id="jornada-credito"' not in s:
    marker = '<section class="wrap" id="modulos">'
    if marker not in s:
        raise SystemExit('missing construtoras modulos marker')
    s = s.replace(marker, journey + '\n' + marker, 1)

schema = '''\n<script type="application/ld+json">\n{\n  "@context":"https://schema.org",\n  "@graph":[\n    {"@type":"WebPage","name":"Análise de crédito e financiamento para construtoras","url":"https://credituz.ai/pages/construtoras.html","description":"Análise de crédito, acompanhamento de financiamento, contratos, cobrança e gestão de unidades para construtoras e incorporadoras."},\n    {"@type":"Service","name":"Credituz para construtoras e incorporadoras","provider":{"@type":"Organization","name":"Credituz","url":"https://credituz.ai/"},"areaServed":"BR","serviceType":"Análise de crédito e operação de financiamento imobiliário","url":"https://credituz.ai/pages/construtoras.html"}\n  ]\n}\n</script>\n'''
if '"Credituz para construtoras e incorporadoras"' not in s:
    s = s.replace('</head>', schema + '</head>', 1)
p.write_text(s, encoding='utf-8')

# ---------- Imobiliarias ----------
p = Path('pages/imobiliarias.html')
s = p.read_text(encoding='utf-8')
s = replace_once(s, '<title>Plataforma com IA para imobiliárias | Credituz</title>', '<title>CRM de crédito e financiamento para imobiliárias | Credituz</title>', 'imobiliarias title')
s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Analise o comprador, simule em múltiplos bancos, solicite o financiamento e acompanhe cada etapa até a contratação com o CRM de crédito da Credituz.">', s, count=1)
s = replace_once(s, '<link rel="canonical" href="https://www.credituz.ai/pages/imobiliarias.html">', '<link rel="canonical" href="https://credituz.ai/pages/imobiliarias.html">', 'imobiliarias canonical')

s = replace_once(s,
'''    <h1>Analise o crédito de quem compra <span class="hl">e de quem aluga</span>.</h1>
    <p class="lead">A Credituz aprova comprador e inquilino com a sua própria política — bureaus, histórico financeiro e capacidade de pagamento —, simula o financiamento nas maiores instituições do país e cobra o aluguel todo mês sozinha.</p>
    <div class="hero-actions">
        <a class="btn btn-dark" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=saas-credituzai" target="_blank" rel="noopener">Testar agora!</a>
        <a class="btn btn-soft" href="https://wa.me/5511936209409" target="_blank" rel="noopener">Falar com um especialista</a>
    </div>''',
'''    <h1>Simule, peça e acompanhe o financiamento <span class="hl">sem tirar o cliente da sua operação.</span></h1>
    <p class="lead">Analise o comprador, simule em múltiplos bancos, solicite o crédito e acompanhe cada etapa até a contratação. Seu corretor vende o imóvel e continua enxergando o financiamento.</p>
    <div class="hero-actions">
        <a class="btn btn-dark" data-track="segment_imobiliarias_start" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=imobiliarias" target="_blank" rel="noopener">Simular um financiamento</a>
        <a class="btn btn-soft" data-track="segment_imobiliarias_how" href="#jornada-credito">Ver como funciona</a>
    </div>''', 'imobiliarias hero')

s = re.sub(r'''    <div class="proof-strip">\s*<span><b>R\$ 300M</b> em crédito solicitado</span>\s*<span><b>&lt;30s</b> por simulação</span>\s*<span><b>15 min</b> até a assinatura</span>\s*<span><b>\+40</b> operações na plataforma</span>\s*</div>''',
'''    <div class="proof-strip">
        <span><b>CRM de crédito</b> do pedido à contratação</span>
        <span><b>Multibancos</b> para comparar cenários</span>
        <span><b>Score</b> antes de avançar a venda</span>
        <span><b>CORBAN AI</b> conectado à jornada</span>
    </div>''', s, count=1)

s = replace_once(s, '<h2>A decisão de crédito não é sua — e devia ser.</h2>', '<h2>A venda não termina quando o cliente pede financiamento.</h2>', 'imobiliarias problem h2')
s = replace_once(s, '<p class="sub">Na venda e na locação, quem aprova hoje é o banco ou a seguradora. Você fica com o risco e sem a receita.</p>', '<p class="sub">Quando a proposta sai da imobiliária e vai para banco, correspondente ou parceiro, o corretor perde visibilidade. O cliente continua perguntando — mas a informação fica espalhada.</p>', 'imobiliarias problem sub')
s = replace_once(s, '<h2>A régua de aprovação passa a ser sua.</h2>', '<h2>Crédito deixa de ser uma caixa-preta depois da venda.</h2>', 'imobiliarias motor h2')
s = replace_once(s, '<p class="sub">O mesmo motor decide o comprador e o inquilino: você escreve a política, consulta bureaus e mede capacidade de pagamento no ato — sem depender da análise do banco ou da seguradora para saber se aquele contrato vai se pagar.</p>', '<p class="sub">Analise o comprador antes de avançar, organize a solicitação e acompanhe documentos, pendências e status do financiamento. A decisão bancária continua sendo da instituição financeira; a visibilidade da jornada fica com a sua equipe.</p>', 'imobiliarias motor sub')

journey = '''\n<section class="wrap" id="jornada-credito">\n  <div class="tag">CRM de crédito + CORBAN AI</div>\n  <h2>O corretor continua acompanhando o cliente depois do pedido de crédito.</h2>\n  <p class="sub">A Credituz transforma financiamento em uma jornada rastreável: da simulação à contratação, com status compartilhado entre comercial, operação e cliente.</p>\n  <div class="jornada">\n    <div class="j-step hot"><span class="j-n">01</span><b>Analise o comprador</b><span class="j-d">Use score e sinais de crédito antes de investir tempo em uma operação que pode não avançar.</span></div>\n    <div class="j-step"><span class="j-n">02</span><b>Simule em bancos</b><span class="j-d">Compare cenários de financiamento sem pulverizar a jornada em diferentes ferramentas.</span></div>\n    <div class="j-step"><span class="j-n">03</span><b>Solicite o crédito</b><span class="j-d">Centralize documentos e informações necessárias para iniciar o processo.</span></div>\n    <div class="j-step"><span class="j-n">04</span><b>Acompanhe o status</b><span class="j-d">Veja pendências, movimentações e próximos passos até a contratação.</span></div>\n  </div>\n</section>\n'''
if 'id="jornada-credito"' not in s:
    marker = '<section class="wrap" id="modulos">'
    if marker not in s:
        raise SystemExit('missing imobiliarias modulos marker')
    s = s.replace(marker, journey + '\n' + marker, 1)

locacao = '''\n<section class="wrap" id="locacao">\n  <div class="tag">Também administra locação?</div>\n  <h2>Use a mesma infraestrutura para analisar e cobrar sua carteira.</h2>\n  <p class="sub">Para operações de locação, a Credituz também pode apoiar a análise do inquilino e organizar cobrança, recebíveis e conciliação conforme os recursos contratados e disponíveis.</p>\n  <div class="grid">\n    <div class="card"><div class="num">01</div><h3>Análise de crédito</h3><p>Score, política própria e sinais de risco para apoiar a decisão de locação.</p></div>\n    <div class="card"><div class="num">02</div><h3>Cobrança e recebíveis</h3><p>Organize régua de cobrança, meios de pagamento e baixa/conciliação da carteira.</p></div>\n  </div>\n</section>\n'''
if 'id="locacao"' not in s:
    marker = '<section class="wrap" id="preco">'
    if marker in s:
        s = s.replace(marker, locacao + '\n' + marker, 1)
    else:
        # fallback before FAQ when pricing id differs
        marker = '<section class="wrap" id="faq">'
        if marker not in s:
            raise SystemExit('missing imobiliarias pricing/faq marker')
        s = s.replace(marker, locacao + '\n' + marker, 1)

schema = '''\n<script type="application/ld+json">\n{\n  "@context":"https://schema.org",\n  "@graph":[\n    {"@type":"WebPage","name":"CRM de crédito e financiamento para imobiliárias","url":"https://credituz.ai/pages/imobiliarias.html","description":"CRM de crédito para analisar compradores, simular, solicitar e acompanhar financiamentos imobiliários."},\n    {"@type":"Service","name":"Credituz para imobiliárias","provider":{"@type":"Organization","name":"Credituz","url":"https://credituz.ai/"},"areaServed":"BR","serviceType":"CRM de crédito e financiamento imobiliário","url":"https://credituz.ai/pages/imobiliarias.html"}\n  ]\n}\n</script>\n'''
if '"Credituz para imobiliárias"' not in s:
    s = s.replace('</head>', schema + '</head>', 1)
p.write_text(s, encoding='utf-8')
