from pathlib import Path
import json
import re

INDEX = Path('index.html')
HOME_MD = Path('home.md')
LLMS_FULL = Path('llms-full.txt')
LLMS = Path('llms.txt')
HOME_JSON = Path('home.json')


def sub_once(text, pattern, replacement, label, flags=re.S):
    out, n = re.subn(pattern, replacement, text, count=1, flags=flags)
    if n != 1:
        raise RuntimeError(f'{label}: expected 1 replacement, got {n}')
    return out


s = INDEX.read_text(encoding='utf-8')

# --- Metadata: horizontal credit + collections + embedded credit positioning.
s = sub_once(s, r'<title>.*?</title>', '<title>Credituz · Análise de crédito, cobrança e embedded credit com IA</title>', 'title', flags=0)
s = sub_once(
    s,
    r'<meta name="description" content="[^"]*">',
    '<meta name="description" content="Analise clientes, organize seu CRM de crédito, automatize cobranças e ofereça crédito multibanco com Credituz OS e CORBAN AI.">',
    'meta description',
    flags=0,
)

# --- Machine-readable schema embedded in the home.
m = re.search(r'<script type="application/ld\+json">(.*?)</script>', s, flags=re.S)
if not m:
    raise RuntimeError('JSON-LD not found')
schema = json.loads(m.group(1))
for node in schema.get('@graph', []):
    if node.get('@type') == 'Organization':
        node['description'] = 'Plataforma de análise de crédito, cobrança e embedded credit com IA para empresas.'
    elif node.get('@type') == 'SoftwareApplication':
        node['description'] = ('Plataforma de crédito e cobrança com IA. O Credituz OS reúne análise de crédito, política, CRM de crédito e cobrança; '
                               'o CORBAN AI permite simular, solicitar e acompanhar crédito multibanco com CRM Corban; o Enterprise combina produtos e módulos sob medida.')
        node['featureList'] = [
            'Análise de crédito e Credituz Score',
            'Política de crédito',
            'CRM de crédito no Credituz OS',
            'Régua de cobrança com IA em WhatsApp e e-mail',
            'Recebíveis, baixa e conciliação',
            'Simulação de crédito multibanco no CORBAN AI',
            'Pedido e acompanhamento de crédito no CORBAN AI',
            'CRM Corban para simulações, pedidos, pendências e status',
            'Embedded credit',
            'Enterprise componível com Credituz OS e/ou CORBAN AI',
            'Construtor de contratos com IA no Enterprise',
            'Assinatura digital e serviços de cartório digital no Enterprise',
            'API, White Label, SSO, integrações e soluções customizadas com IA no Enterprise',
        ]
        node['offers'] = [
            {
                '@type': 'Offer',
                'name': 'Credituz OS',
                'price': '297',
                'priceCurrency': 'BRL',
                'description': 'R$ 297 por mês mais R$ 16 por análise. Análise de crédito, política, CRM de crédito, cobrança com IA, recebíveis, conciliação e analytics para até 3 usuários.'
            },
            {
                '@type': 'Offer',
                'name': 'CORBAN AI',
                'priceCurrency': 'BRL',
                'description': 'Modelo comercial conforme a operação. Embedded credit com simulação multibanco, pedido de crédito, acompanhamento e CRM Corban.'
            },
            {
                '@type': 'Offer',
                'name': 'Enterprise',
                'priceCurrency': 'BRL',
                'description': 'Sob medida. Combine Credituz OS e/ou CORBAN AI com gestão operacional, contratos com IA, assinatura digital, cartório digital, SMS, API, White Label, SSO, integrações e soluções customizadas com IA.'
            }
        ]
    elif node.get('@type') == 'FAQPage':
        node['mainEntity'] = [
            {'@type':'Question','name':'Qual a diferença entre Credituz OS e CORBAN AI?','acceptedAnswer':{'@type':'Answer','text':'O Credituz OS é voltado a análise de crédito, política, CRM de crédito e cobrança. O CORBAN AI é voltado a embedded credit: simulação multibanco, pedido de crédito, acompanhamento e CRM Corban.'}},
            {'@type':'Question','name':'Preciso contratar Credituz OS e CORBAN AI juntos?','acceptedAnswer':{'@type':'Answer','text':'Não. Os produtos podem ser usados separadamente. No Enterprise, podem ser combinados e adaptados à operação da empresa.'}},
            {'@type':'Question','name':'O que é o CRM Corban?','acceptedAnswer':{'@type':'Answer','text':'É o CRM do CORBAN AI para acompanhar simulações, pedidos de crédito, documentação, pendências, banco, status e contratação.'}},
            {'@type':'Question','name':'Onde ficam contratos, assinatura digital e cartório digital?','acceptedAnswer':{'@type':'Answer','text':'Esses recursos passam a fazer parte das soluções Enterprise, que são montadas conforme a necessidade operacional da empresa.'}},
            {'@type':'Question','name':'A Credituz atende somente o mercado imobiliário?','acceptedAnswer':{'@type':'Answer','text':'Não. A Credituz atende empresas que precisam analisar clientes, cobrar recebíveis ou incorporar crédito à própria jornada. As páginas de segmentos detalham aplicações específicas.'}},
        ]
new_jsonld = json.dumps(schema, ensure_ascii=False, separators=(',', ':'))
s = s[:m.start(1)] + new_jsonld + s[m.end(1):]

# --- Navigation. Products are distinct from solutions; segments remain vertical landing pages.
old_solutions = '''<li class="nav-has-sub">
      <a href="#produto" class="nav-sub-trigger">Soluções <span class="nav-caret">▾</span></a>
      <ul class="nav-submenu">
          <li><a href="./pages/credituz-score.html">Score de crédito</a></li>
          <li><a href="./pages/crm-de-credito.html">CRM de crédito</a></li>
          <li><a href="./pages/contratos-imobiliarios-digitais.html">Contratos e assinatura</a></li>
          <li><a href="./pages/cobranca-e-recebiveis-imobiliarios.html">Cobrança e recebíveis</a></li>
          <li><a href="./pages/portal-vendas-empreendimentos.html">Portal de vendas</a></li>
          <li><a href="./pages/gestao-de-unidades-imobiliarias.html">Gestão de unidades</a></li>
      </ul>
  </li>'''
new_products = '''<li class="nav-has-sub">
      <a href="#produtos" class="nav-sub-trigger">Produtos <span class="nav-caret">▾</span></a>
      <ul class="nav-submenu">
          <li><a href="#credituz-os">Credituz OS</a></li>
          <li><a href="#corban-ai">CORBAN AI</a></li>
          <li><a href="./pages/credituz-score.html">Credituz Score</a></li>
          <li><a href="#enterprise">Enterprise</a></li>
      </ul>
  </li>'''
if old_solutions not in s:
    raise RuntimeError('navigation solutions block not found')
s = s.replace(old_solutions, new_products, 1)
s = s.replace('            <li><a href="#corban-ai">CORBAN AI</a></li>\n            <li><a href="#financeiro">Financeiro</a></li>', '''            <li class="nav-has-sub">
                <a href="#produtos" class="nav-sub-trigger">Soluções <span class="nav-caret">▾</span></a>
                <ul class="nav-submenu">
                    <li><a href="./pages/analise-de-credito-score-incorporadoras.html">Análise de crédito</a></li>
                    <li><a href="./pages/crm-de-credito.html">CRM de crédito</a></li>
                    <li><a href="./pages/cobranca-e-recebiveis-imobiliarios.html">Cobrança com IA</a></li>
                    <li><a href="#corban-ai">Embedded credit</a></li>
                </ul>
            </li>''', 1)

# --- Hero: broader company-level promise.
s = s.replace('<p class="hero-kicker">Sistema operacional de crédito e cobrança</p>', '<p class="hero-kicker">Crédito, cobrança e embedded finance com IA</p>', 1)
s = sub_once(s, r'<h1 class="hero-title" id="heroTitle">.*?</h1>', '''<h1 class="hero-title" id="heroTitle">
        Decida para quem vender. <em>Receba melhor. Ofereça crédito.</em>
    </h1>''', 'hero h1')
s = sub_once(s, r'<p class="hero-sub" id="heroSub">.*?</p>', '''<p class="hero-sub" id="heroSub">
        Analise clientes, organize sua operação de crédito, automatize cobranças e ofereça crédito multibanco com IA usando Credituz OS e CORBAN AI.
    </p>''', 'hero sub')
s = sub_once(s, r'<div class="hero-ttv">.*?</div>', '''<div class="hero-ttv">
        <span class="hero-ttv-item"><span class="hero-ttv-num">OS</span><span class="hero-ttv-label">Análise + CRM + cobrança</span></span>
        <span class="hero-ttv-item"><span class="hero-ttv-num">AI</span><span class="hero-ttv-label">Embedded credit multibanco</span></span>
        <span class="hero-ttv-item"><span class="hero-ttv-num">ENT</span><span class="hero-ttv-label">Infraestrutura sob medida</span></span>
    </div>''', 'hero value strip')
s = s.replace('CRM de crédito · CORBAN AI · Credituz Score · Contratos · Cobrança · Sem fidelidade', 'Análise de crédito · CRM de crédito · Cobrança com IA · Embedded credit multibanco', 1)

# --- Problem section + product architecture.
problem_and_products = '''<!-- DOR -->
<section class="dor">
  <div class="dor-inner">
    <div class="section-tag">O problema</div>
    <h2>A venda acontece.<br><em>O risco e o trabalho começam depois.</em></h2>
    <p class="dor-lead">Empresas ainda analisam crédito manualmente, acompanham clientes em planilhas, cobram de forma reativa e mandam o cliente para terceiros quando ele precisa de financiamento.</p>
    <div class="dor-grid">
      <div class="dor-card"><div class="dor-number">01</div><h3>Você vende antes de entender o risco.</h3><p>Sem uma análise consistente, score, capacidade de pagamento e política de crédito ficam espalhados ou dependem de processos manuais.</p><span class="dor-solution">Credituz OS</span></div>
      <div class="dor-card"><div class="dor-number">02</div><h3>A cobrança depende da sua equipe.</h3><p>Vencimentos, atrasos e follow-ups exigem ações manuais. Quanto maior a carteira, mais difícil manter uma régua consistente.</p><span class="dor-solution">Credituz OS</span></div>
      <div class="dor-card"><div class="dor-number">03</div><h3>Seu cliente precisa de crédito e você o manda embora.</h3><p>A jornada sai da sua empresa justamente quando ele precisa financiar. Você perde visibilidade do pedido e do relacionamento.</p><span class="dor-solution">CORBAN AI</span></div>
      <div class="dor-card"><div class="dor-number">04</div><h3>Sua operação financeira está espalhada.</h3><p>Crédito, CRM, cobrança, bancos e processos internos funcionam separados e criam controles paralelos conforme a empresa cresce.</p><span class="dor-solution">Enterprise</span></div>
    </div>
  </div>
</section>

<style id="product-architecture-styles">
.product-architecture{padding:96px 24px;background:#fff}.product-architecture-inner{max-width:1120px;margin:0 auto}.product-architecture-head{max-width:820px;margin-bottom:36px}.product-architecture-head h2{font-size:clamp(34px,5vw,54px);margin:8px 0 14px}.product-architecture-head p{font-size:18px;color:var(--gray-2);line-height:1.55}.product-architecture-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}.product-arch-card{border:1px solid var(--gray-soft);border-radius:24px;padding:32px;background:var(--paper-warm)}.product-arch-card h3{font-size:30px;margin:6px 0 10px}.product-arch-card p{color:var(--gray-2)}.product-flow{margin:22px 0;display:flex;align-items:center;gap:7px;flex-wrap:wrap;font-size:13px;font-weight:650}.product-flow i{font-style:normal;color:var(--gray-3)}.product-arch-list{list-style:none;padding:0;margin:0 0 24px}.product-arch-list li{padding:7px 0;font-size:14px}.product-arch-list li:before{content:'✓';color:var(--good);font-weight:700;margin-right:8px}.product-arch-link{display:inline-flex;padding:12px 18px;border-radius:999px;background:var(--ink);color:#fff;text-decoration:none;font-weight:700}.product-architecture-note{margin-top:18px;padding:22px;border-radius:20px;background:#f4f9ff;color:var(--gray-1)}.product-architecture-note strong{color:var(--lime-deep)}@media(max-width:760px){.product-architecture-grid{grid-template-columns:1fr}.product-architecture{padding:72px 20px}}
</style>
<section class="product-architecture" id="produtos">
  <div class="product-architecture-inner">
    <div class="product-architecture-head"><div class="section-tag">Produtos</div><h2>Dois produtos. Uma infraestrutura financeira.</h2><p>Use Credituz OS para analisar risco e receber melhor. Use CORBAN AI para incorporar crédito à jornada do seu cliente. No Enterprise, combine os dois e adicione gestão operacional e módulos específicos.</p></div>
    <div class="product-architecture-grid">
      <article class="product-arch-card" id="credituz-os"><div class="section-tag">Credituz OS</div><h3>Analise. Acompanhe. Cobre.</h3><p>O sistema operacional para empresas que precisam decidir melhor para quem vender e automatizar o relacionamento financeiro depois da venda.</p><div class="product-flow"><span>Cliente</span><i>→</i><span>Análise</span><i>→</i><span>Política</span><i>→</i><span>CRM de crédito</span><i>→</i><span>Cobrança</span><i>→</i><span>Recebimento</span></div><ul class="product-arch-list"><li>Credituz Score integrado e política de crédito</li><li>CRM de crédito</li><li>Régua de cobrança com IA em WhatsApp e e-mail</li><li>Recebíveis, baixa, conciliação e analytics</li><li>Até 3 usuários</li></ul><a class="product-arch-link" href="#pricing">Conhecer Credituz OS</a></article>
      <article class="product-arch-card"><div class="section-tag">CORBAN AI</div><h3>Simule. Solicite. Financie.</h3><p>Embedded credit para empresas que querem oferecer crédito aos próprios clientes sem construir uma operação financeira do zero.</p><div class="product-flow"><span>Cliente</span><i>→</i><span>Simulação</span><i>→</i><span>Bancos</span><i>→</i><span>Pedido</span><i>→</i><span>CRM Corban</span><i>→</i><span>Contratação</span></div><ul class="product-arch-list"><li>Simulação de crédito multibanco</li><li>Pedido de crédito</li><li>CRM Corban para propostas, pendências e status</li><li>Jornada embedded credit</li><li>Acompanhamento da operação até a contratação</li></ul><a class="product-arch-link" href="#corban-ai">Conhecer CORBAN AI</a></article>
    </div>
    <div class="product-architecture-note"><strong>Use separadamente ou conecte os dois.</strong> Credituz OS organiza risco e recebimento. CORBAN AI organiza a originação de crédito.</div>
  </div>
</section>'''
s = sub_once(s, r'<!-- DOR -->\s*<section class="dor">.*?</section>', problem_and_products, 'problem section')

# Remove real-estate-only examples from the generic credit-engine section.
s = s.replace('<div class="motor-seg-card"><span class="tagx">Construtora</span><h4>Não financie a entrada de quem vai reprovar no repasse.</h4><p>A análise acontece antes de você assumir o risco. Quem entra na carteira é quem chega ao financiamento bancário aprovado — menos distrato, menos unidade voltando ao estoque depois de dois anos.</p></div>', '<div class="motor-seg-card"><span class="tagx">Venda a prazo</span><h4>Aprove clientes com uma política de crédito consistente.</h4><p>Score, capacidade de pagamento e sinais de risco ajudam sua equipe a padronizar decisões antes de assumir exposição financeira.</p></div>', 1)
s = s.replace('<div class="motor-seg-card"><span class="tagx">Imobiliária</span><h4>Aprove o inquilino com dado, não com fiador no escuro.</h4><p>O mesmo motor analisa histórico financeiro e capacidade de pagamento para locação. A régua de aprovação passa a ser sua, e não a da seguradora.</p></div>', '<div class="motor-seg-card"><span class="tagx">Cobrança recorrente</span><h4>Use o mesmo dado de crédito para acompanhar sua carteira.</h4><p>A análise deixa de ser um evento isolado e passa a alimentar CRM, política e decisões de cobrança ao longo do relacionamento.</p></div>', 1)

# --- CORBAN AI: make it a standalone embedded-credit product with its own CRM.
new_corban = '''<section class="corban" id="corban-ai"><div class="corban-inner"><span class="corban-eyebrow">CORBAN AI · Embedded credit</span><h2 class="corban-h2">Transforme sua empresa em um <span class="corban-hl">canal de crédito.</span></h2><p class="corban-intro">Incorpore simulação, solicitação e acompanhamento de crédito multibanco à experiência do seu cliente. O CORBAN AI organiza a originação em uma jornada própria, com CRM Corban para acompanhar cada pedido até a contratação.</p><div class="corban-steps"><div class="corban-step"><span class="corban-num">01</span><h3>Simule em múltiplas instituições</h3><p>Compare possibilidades de crédito para o perfil do cliente sem tirá-lo da sua jornada.</p></div><div class="corban-step"><span class="corban-num">02</span><h3>Envie o pedido de crédito</h3><p>Organize a solicitação e os documentos necessários para a instituição escolhida.</p></div><div class="corban-step"><span class="corban-num">03</span><h3>Acompanhe no CRM Corban</h3><p>Centralize simulações, propostas, banco, documentação, pendências e status da operação até a contratação.</p></div></div><div class="corban-why"><div class="corban-why-item"><span><strong>Embedded credit:</strong> mantenha a oferta de crédito dentro da experiência da sua empresa.</span></div><div class="corban-why-item"><span><strong>Visibilidade:</strong> acompanhe o pedido sem depender de mensagens soltas para descobrir o próximo passo.</span></div><div class="corban-why-item"><span><strong>Originação:</strong> transforme crédito em uma nova capacidade comercial para o seu negócio, conforme o modelo da operação.</span></div></div><div class="corban-cta"><a class="corban-btn" href="https://wa.me/5511936209409" data-track="corban_sales">Conhecer o CORBAN AI</a><a class="corban-wa" href="#pricing">ver produtos e preços</a></div></div></section>'''
s = sub_once(s, r'<section class="corban" id="corban-ai">.*?</section>', new_corban, 'corban section')

# Correct old architecture copy that described CORBAN AI as part of the OS.
s = s.replace('No centro da plataforma: CORBAN AI', 'Produto integrado quando você precisar: CORBAN AI')
s = s.replace('O correspondente bancário digital que simula em vários bancos, aprova e contrata o financiamento dentro do mesmo fluxo.', 'Embedded credit para simular, solicitar e acompanhar crédito multibanco com CRM Corban.')
s = s.replace('ERP não fecha financiamento. CRM não origina crédito. <strong>O CORBAN AI da Credituz faz as duas coisas, no mesmo fluxo.</strong>', 'Use <strong>Credituz OS para risco e recebimento</strong> e <strong>CORBAN AI para originação de crédito</strong>. No Enterprise, conecte os dois à sua operação.')

# Generalize steps and product showcase language.
s = s.replace('Da <em>simulação</em> à entrega das chaves.', 'Da <em>análise</em> ao recebimento. Do pedido à contratação.', 1)
s = s.replace('Não é um chatbot. É a <em>plataforma inteira</em> da sua operação.', 'Uma operação financeira que sua equipe <em>consegue enxergar.</em>', 1)
s = s.replace('Toda a operação em uma plataforma. Veja as telas reais que sua equipe usa todos os dias.', 'Clientes, crédito, cobranças e indicadores conectados em uma experiência operacional única.', 1)

# Score becomes a self-service entry product, not one of the three main commercial plans.
score_entry = '''<section class="entry-choice" id="credituz-score"><div class="entry-choice-inner"><div class="entry-head"><div class="section-tag">Credituz Score</div><h2>Só precisa analisar um cliente?</h2><p>Comece pela consulta avulsa. Sem assinatura e sem mensalidade.</p></div><div class="entry-grid" style="grid-template-columns:1fr;max-width:680px;margin:0 auto"><article class="entry-card"><div class="entry-tag">Uso ocasional</div><h3>Credituz Score</h3><div class="entry-price">R$ 27,70 <small>/ análise</small></div><p>Uma análise completa de crédito para usar quando precisar.</p><ul class="entry-list"><li>Score e sinais de risco</li><li>Renda estimada e parcela máxima</li><li>Restrições, protestos e processos conforme dados disponíveis</li><li>Sem assinatura</li></ul><a class="entry-btn" href="./pages/credituz-score.html" data-track="home_score_entry">Fazer uma análise</a></article></div><div class="entry-note">Faz análises todos os meses? No Credituz OS, cada análise custa R$ 16 e passa a fazer parte do seu CRM de crédito.</div></div></section>'''
s = sub_once(s, r'<section class="entry-choice" id="comece">.*?</section>', score_entry, 'score entry')

# --- Main pricing: exactly three B2B products.
pricing = '''<!-- PRICING -->
<section id="pricing" class="pricing-choice">
  <div class="pricing-choice-inner">
    <div class="pricing-choice-head">
      <div class="pricing-choice-kicker">Produtos e preços</div>
      <h2>Escolha a infraestrutura que sua operação precisa.</h2>
      <p>Credituz OS para análise, CRM e cobrança. CORBAN AI para embedded credit e originação multibanco. Enterprise para combinar produtos, gestão operacional e módulos sob medida.</p>
    </div>
    <div class="pricing-choice-grid">
      <article class="pricing-choice-card featured">
        <div class="pricing-choice-type">Análise + CRM + cobrança</div>
        <h3 class="pricing-choice-name">Credituz OS</h3>
        <div class="pricing-choice-price"><strong>R$ 297</strong><span>/mês + R$ 16 por análise</span></div>
        <p class="pricing-choice-desc">Para empresas que precisam decidir melhor para quem vender, organizar o CRM de crédito e automatizar cobrança.</p>
        <ul class="pricing-choice-list">
          <li><strong>CRM de crédito</strong></li>
          <li>Credituz Score integrado · <strong>R$ 16 por análise</strong></li>
          <li>Política de crédito</li>
          <li>Régua de cobrança com IA em WhatsApp e e-mail · <strong>R$ 0,15 por envio</strong></li>
          <li>Recebíveis, baixa e conciliação</li>
          <li>Analytics de crédito e carteira</li>
          <li><strong>Até 3 usuários</strong></li>
        </ul>
        <a class="pricing-choice-cta" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=home-pricing-os" data-track="cta_pricing_os">Começar com Credituz OS</a>
      </article>
      <article class="pricing-choice-card">
        <div class="pricing-choice-type">Embedded credit</div>
        <h3 class="pricing-choice-name">CORBAN AI</h3>
        <div class="pricing-choice-price"><strong>Comercial</strong><span>conforme a operação</span></div>
        <p class="pricing-choice-desc">Para empresas que querem oferecer crédito aos próprios clientes e acompanhar a originação de ponta a ponta.</p>
        <ul class="pricing-choice-list">
          <li>Simulação de crédito multibanco</li>
          <li>Pedido de crédito</li>
          <li><strong>CRM Corban</strong></li>
          <li>Propostas, documentos e pendências</li>
          <li>Acompanhamento de banco e status</li>
          <li>Jornada de embedded credit</li>
          <li>Originação financeira conforme o modelo comercial</li>
        </ul>
        <a class="pricing-choice-cta" href="https://wa.me/5511936209409" target="_blank" rel="noopener" data-track="cta_pricing_corban">Falar sobre CORBAN AI</a>
      </article>
      <article class="pricing-choice-card pricing-choice-enterprise" id="enterprise">
        <div class="pricing-choice-type">Infraestrutura customizada</div>
        <h3 class="pricing-choice-name">Enterprise</h3>
        <div class="pricing-choice-price"><strong>Sob medida</strong></div>
        <p class="pricing-choice-desc">Monte a infraestrutura financeira e a gestão operacional que sua empresa precisa.</p>
        <ul class="pricing-choice-list">
          <li><strong>Credituz OS e/ou CORBAN AI</strong></li>
          <li>Usuários, volumes e estrutura customizados</li>
          <li>Construtor de contratos com IA</li>
          <li>Assinatura digital</li>
          <li>Serviços de cartório digital</li>
          <li>SMS e canais adicionais</li>
          <li>Políticas e fluxos customizados</li>
          <li>API · White Label · SSO · multiempresa · integrações</li>
          <li><strong>Soluções customizadas com IA</strong></li>
          <li>SLA e atendimento dedicado</li>
        </ul>
        <a class="pricing-choice-cta" href="https://wa.me/5511936209409" target="_blank" rel="noopener" data-track="cta_pricing_enterprise">Desenhar solução Enterprise</a>
      </article>
    </div>
    <p class="pricing-choice-footnote">Precisa apenas de uma consulta? <strong>Credituz Score continua disponível por R$ 27,70 por análise, sem assinatura.</strong></p>
  </div>
</section>'''
s = sub_once(s, r'<!-- PRICING -->\s*<section id="pricing" class="pricing-choice">.*?</section>', pricing, 'pricing')

# --- Visible FAQ aligned to the new architecture.
faq = '''<!-- FAQ -->
<section id="faq">
    <div class="section-tag">Perguntas frequentes</div>
    <h2>Entenda qual produto usar.</h2>
    <div class="faq">
      <div class="faq-item"><div class="faq-q"><h4>Qual a diferença entre Credituz OS e CORBAN AI?</h4><span>+</span></div><div class="faq-a"><p>Credituz OS é para análise de crédito, política, CRM de crédito e cobrança. CORBAN AI é para embedded credit: simulação multibanco, pedido de crédito, acompanhamento e CRM Corban.</p></div></div>
      <div class="faq-item"><div class="faq-q"><h4>Preciso contratar os dois?</h4><span>+</span></div><div class="faq-a"><p>Não. Credituz OS e CORBAN AI podem ser usados separadamente. No Enterprise, eles podem ser combinados e adaptados à sua operação.</p></div></div>
      <div class="faq-item"><div class="faq-q"><h4>O que é CRM de crédito?</h4><span>+</span></div><div class="faq-a"><p>É o CRM do Credituz OS para organizar clientes, análises, política e decisões de crédito ao longo do relacionamento.</p></div></div>
      <div class="faq-item"><div class="faq-q"><h4>O que é CRM Corban?</h4><span>+</span></div><div class="faq-a"><p>É o CRM do CORBAN AI para acompanhar simulações, pedidos de crédito, documentos, pendências, banco, status e contratação.</p></div></div>
      <div class="faq-item"><div class="faq-q"><h4>Onde ficam contratos, assinatura digital e cartório digital?</h4><span>+</span></div><div class="faq-a"><p>Esses módulos passam a ser oferecidos no Enterprise, que permite desenhar uma infraestrutura financeira e de gestão operacional sob medida.</p></div></div>
      <div class="faq-item"><div class="faq-q"><h4>A Credituz atende somente o mercado imobiliário?</h4><span>+</span></div><div class="faq-a"><p>Não. A plataforma pode atender empresas que precisam analisar clientes, cobrar recebíveis ou incorporar crédito à própria jornada. As páginas de segmentos detalham aplicações específicas.</p></div></div>
    </div>
</section>'''
s = sub_once(s, r'<!-- FAQ -->\s*<section id="faq">.*?</section>\s*(?=<!-- CTA FINAL -->)', faq + '\n\n', 'faq')

# --- Final CTA broad enough for all products.
s = s.replace('<h2>Comece em <em>5 minutos</em>, sem implantação.</h2>', '<h2>Sua operação financeira pode <em>trabalhar melhor.</em></h2>', 1)
s = s.replace('Sem demo agendada. Sem ligação de vendedor. Sem implantação de 60 dias. Só você e a IA mais avançada de crédito e cobrança do Brasil. Cancele quando quiser, dentro da própria plataforma.', 'Analise melhor, cobre automaticamente e incorpore crédito à experiência dos seus clientes com a infraestrutura da Credituz.', 1)
s = s.replace('Criar minha conta agora', 'Conhecer Credituz OS', 1)

INDEX.write_text(s, encoding='utf-8')

# --- Text sources for LLMs/search: same product hierarchy.
positioning = '''## Posicionamento

A Credituz é uma plataforma de crédito, cobrança e embedded finance com IA para empresas.

Mensagem principal da home: **"Decida para quem vender. Receba melhor. Ofereça crédito."**

- **Credituz OS** organiza análise de crédito, política, CRM de crédito, cobrança e recebimento.
- **CORBAN AI** organiza embedded credit, simulação multibanco, pedido de crédito, acompanhamento e CRM Corban.
- **Enterprise** combina Credituz OS e/ou CORBAN AI com gestão operacional, integrações, módulos específicos e soluções customizadas com IA.
- **Credituz Score** permanece como porta de entrada self-service para consulta avulsa de crédito por R$ 27,70 por análise.
'''
products = '''## Produtos e preços

### Credituz OS — R$ 297/mês + R$ 16 por análise
Para empresas que precisam analisar clientes, organizar decisões no CRM de crédito e automatizar cobrança. Inclui análise de crédito, política, CRM de crédito, régua de cobrança com IA em WhatsApp e e-mail por R$ 0,15 por envio, recebíveis, baixa, conciliação, analytics e até 3 usuários.

### CORBAN AI — modelo comercial conforme a operação
Produto de embedded credit para empresas que querem oferecer crédito aos próprios clientes. Inclui simulação multibanco, pedido de crédito, CRM Corban, propostas, documentos, pendências e acompanhamento de banco/status até a contratação.

### Enterprise — sob medida
Monte a infraestrutura financeira e a gestão operacional que sua empresa precisa. Pode combinar Credituz OS e/ou CORBAN AI e incluir usuários e volumes customizados, construtor de contratos com IA, assinatura digital, serviços de cartório digital, SMS, políticas e fluxos específicos, API, White Label, SSO, multiempresa, integrações, soluções customizadas com IA, SLA e atendimento dedicado.

### Credituz Score — R$ 27,70 por análise
Consulta avulsa de crédito, sem assinatura. Para uso recorrente, as análises dentro do Credituz OS custam R$ 16 cada.
'''
problem = '''## O problema que a Credituz resolve

Empresas ainda analisam crédito manualmente, acompanham clientes em planilhas, cobram de forma reativa e enviam o cliente para terceiros quando ele precisa de financiamento.

- **Risco**: Credituz OS ajuda a estruturar análise, score, política e CRM de crédito.
- **Cobrança**: Credituz OS automatiza a régua e conecta recebíveis, baixa, conciliação e analytics.
- **Originação**: CORBAN AI mantém simulação, pedido e acompanhamento de crédito dentro da jornada da empresa, com CRM Corban.
- **Operações complexas**: Enterprise combina produtos e adiciona gestão operacional, integrações e soluções específicas com IA.
'''

for fp in (HOME_MD, LLMS_FULL):
    t = fp.read_text(encoding='utf-8')
    t = sub_once(t, r'## Posicionamento\n.*?(?=\n## )', positioning.rstrip(), f'{fp} positioning')
    t = sub_once(t, r'## O problema que a Credituz resolve\n.*?(?=\n## )', problem.rstrip(), f'{fp} problem')
    t = sub_once(t, r'## Planos e preços\n.*?(?=\n## )', products.rstrip(), f'{fp} plans') if '## Planos e preços' in t else sub_once(t, r'## Produtos e preços\n.*?(?=\n## )', products.rstrip(), f'{fp} products')
    t = t.replace('Sistema operacional AI-First de crédito e cobrança (CRM + crédito + contratos + cobrança + gestão financeira)', 'Plataforma de crédito, cobrança e embedded finance com IA')
    t = t.replace('A plataforma é organizada em quatro agentes de IA, cada um responsável por uma etapa da operação:', 'A plataforma é organizada em produtos com papéis diferentes na operação:')
    fp.write_text(t, encoding='utf-8')

# llms.txt top summary only; article index remains intact.
lt = LLMS.read_text(encoding='utf-8')
lt = re.sub(r'^# Credituz.*?\n\n> .*?\n', '# Credituz — Crédito, cobrança e embedded finance com IA\n\n> A Credituz é uma plataforma para empresas analisarem clientes, organizarem o CRM de crédito, automatizarem cobrança e incorporarem crédito multibanco com Credituz OS e CORBAN AI. O Enterprise combina produtos e módulos sob medida.\n', lt, count=1, flags=re.S)
LLMS.write_text(lt, encoding='utf-8')

# home.json machine-readable source.
data = json.loads(HOME_JSON.read_text(encoding='utf-8'))
for node in data.get('@graph', []):
    if node.get('@type') == 'Organization':
        node['description'] = 'Plataforma de análise de crédito, cobrança e embedded credit com IA para empresas.'
    if node.get('@type') == 'SoftwareApplication':
        node['description'] = 'Credituz OS para análise, CRM de crédito e cobrança; CORBAN AI para embedded credit, simulação multibanco, pedido e CRM Corban; Enterprise para infraestrutura financeira e gestão operacional sob medida.'
        node['featureList'] = [
            'Análise de crédito e política', 'CRM de crédito', 'Cobrança com IA em WhatsApp e e-mail', 'Recebíveis e conciliação',
            'Simulação multibanco', 'Pedido de crédito', 'CRM Corban', 'Embedded credit', 'Enterprise componível e customizado'
        ]
        node['offers'] = [
            {'@type':'Offer','name':'Credituz OS','price':'297','priceCurrency':'BRL','description':'R$ 297/mês + R$ 16 por análise. Análise de crédito, CRM de crédito, cobrança com IA e até 3 usuários.'},
            {'@type':'Offer','name':'CORBAN AI','priceCurrency':'BRL','description':'Modelo comercial conforme a operação. Embedded credit, simulação multibanco, pedido de crédito e CRM Corban.'},
            {'@type':'Offer','name':'Enterprise','priceCurrency':'BRL','description':'Sob medida. Credituz OS e/ou CORBAN AI, gestão operacional, contratos com IA, assinatura digital, cartório digital, integrações e soluções customizadas com IA.'},
        ]
    if node.get('@type') == 'FAQPage':
        node['mainEntity'] = schema['@graph'][-1]['mainEntity'] if schema.get('@graph') and schema['@graph'][-1].get('@type') == 'FAQPage' else node.get('mainEntity', [])
HOME_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print('Horizontal product architecture applied successfully.')
