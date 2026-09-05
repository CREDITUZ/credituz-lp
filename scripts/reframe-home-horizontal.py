from pathlib import Path
import json
import re

ROOT = Path('.')
INDEX = ROOT / 'index.html'
HOME_MD = ROOT / 'home.md'
LLMS_FULL = ROOT / 'llms-full.txt'
LLMS = ROOT / 'llms.txt'
HOME_JSON = ROOT / 'home.json'


def sub1(text, pattern, repl, label, flags=re.S):
    out, n = re.subn(pattern, repl, text, count=1, flags=flags)
    if n != 1:
        raise SystemExit(f'expected 1 replacement for {label}, got {n}')
    return out

schema = {
    '@context': 'https://schema.org',
    '@graph': [
        {
            '@type': 'Organization',
            '@id': 'https://www.credituz.ai/#organization',
            'name': 'Credituz',
            'url': 'https://www.credituz.ai',
            'description': 'Plataforma de análise de crédito, cobrança e embedded finance com IA para empresas.',
            'foundingDate': '2024',
            'areaServed': {'@type': 'Country', 'name': 'Brasil'},
            'knowsLanguage': ['pt-BR'],
            'contactPoint': {
                '@type': 'ContactPoint',
                'contactType': 'sales',
                'telephone': '+55-11-93620-9409',
                'availableLanguage': ['Portuguese']
            }
        },
        {
            '@type': 'SoftwareApplication',
            '@id': 'https://www.credituz.ai/#software',
            'name': 'Credituz',
            'applicationCategory': 'BusinessApplication',
            'operatingSystem': 'Web',
            'description': 'A Credituz reúne análise de crédito, CRM de crédito e cobrança com IA no Credituz OS; simulação, pedido de crédito multibanco e CRM Corban no CORBAN AI; e infraestrutura financeira e gestão operacional customizadas no Enterprise.',
            'publisher': {'@id': 'https://www.credituz.ai/#organization'},
            'featureList': [
                'Análise de crédito e política de crédito',
                'CRM de crédito no Credituz OS',
                'Régua de cobrança com IA em WhatsApp e e-mail',
                'Simulação de crédito multibanco no CORBAN AI',
                'Pedido de crédito e acompanhamento da originação',
                'CRM Corban para simulações, pedidos, pendências e status',
                'Embedded credit para empresas',
                'Enterprise com construtor de contratos com IA, assinatura digital, cartório digital e soluções customizadas com IA'
            ],
            'offers': [
                {
                    '@type': 'Offer',
                    'name': 'Credituz Score',
                    'price': '27.70',
                    'priceCurrency': 'BRL',
                    'description': 'Análise de crédito avulsa, sem assinatura ou mensalidade.'
                },
                {
                    '@type': 'Offer',
                    'name': 'Credituz OS',
                    'price': '297',
                    'priceCurrency': 'BRL',
                    'description': 'R$ 297 por mês mais R$ 16 por análise, para até 3 usuários. Inclui análise de crédito, CRM de crédito e régua de cobrança com IA em WhatsApp e e-mail por R$ 0,15 por envio.'
                },
                {
                    '@type': 'Offer',
                    'name': 'CORBAN AI',
                    'priceCurrency': 'BRL',
                    'description': 'Embedded credit com simulação multibanco, pedido de crédito e CRM Corban. Modelo comercial conforme a operação.'
                },
                {
                    '@type': 'Offer',
                    'name': 'Enterprise',
                    'priceCurrency': 'BRL',
                    'description': 'Infraestrutura financeira e gestão operacional sob medida, podendo combinar Credituz OS, CORBAN AI, construtor de contratos com IA, assinatura digital, cartório digital, integrações e soluções customizadas com IA.'
                }
            ]
        },
        {
            '@type': 'WebSite',
            '@id': 'https://www.credituz.ai/#website',
            'url': 'https://www.credituz.ai',
            'name': 'Credituz',
            'publisher': {'@id': 'https://www.credituz.ai/#organization'},
            'inLanguage': 'pt-BR'
        },
        {
            '@type': 'FAQPage',
            '@id': 'https://www.credituz.ai/#faq',
            'mainEntity': [
                {
                    '@type': 'Question',
                    'name': 'Qual a diferença entre Credituz OS e CORBAN AI?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'O Credituz OS reúne análise de crédito, CRM de crédito e cobrança com IA. O CORBAN AI é a solução de embedded credit para simular, solicitar e acompanhar crédito multibanco, com CRM Corban próprio.'}
                },
                {
                    '@type': 'Question',
                    'name': 'Preciso contratar Credituz OS e CORBAN AI juntos?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'Não. Os produtos podem ser usados separadamente. Em projetos Enterprise, eles também podem ser combinados de acordo com a operação.'}
                },
                {
                    '@type': 'Question',
                    'name': 'Qual a diferença entre CRM de crédito e CRM Corban?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'O CRM de crédito pertence ao Credituz OS e organiza clientes, análises e decisões de crédito. O CRM Corban pertence ao CORBAN AI e acompanha simulações, pedidos de crédito, documentos, pendências, bancos, status e contratação.'}
                },
                {
                    '@type': 'Question',
                    'name': 'Onde ficam contratos com IA, assinatura digital e cartório digital?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'Essas funcionalidades fazem parte de soluções Enterprise e podem ser combinadas com Credituz OS, CORBAN AI e outras integrações conforme a necessidade da empresa.'}
                },
                {
                    '@type': 'Question',
                    'name': 'A Credituz atende somente o mercado imobiliário?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'Não. A Credituz atende empresas que precisam analisar clientes, automatizar cobrança ou incorporar crédito à própria jornada. As páginas de segmento detalham aplicações específicas para alguns mercados.'}
                },
                {
                    '@type': 'Question',
                    'name': 'Quanto custa o Credituz OS?',
                    'acceptedAnswer': {'@type': 'Answer', 'text': 'O Credituz OS custa R$ 297 por mês, mais R$ 16 por análise de crédito, para até 3 usuários. A régua de cobrança em WhatsApp e e-mail custa R$ 0,15 por envio.'}
                }
            ]
        }
    ]
}

new_nav = '''<nav id="nav">
    <div class="inner">
        <a href="#top" class="logo-link" aria-label="Credituz · ir para o início" onclick="event.preventDefault(); window.scrollTo({top: 0, behavior: 'smooth'});">
            <img class="logo-mark" src="/assets/logo-credituz.png" alt="Credituz" width="112" height="26">
        </a>
        <button type="button" class="nav-toggle" id="navToggle" aria-label="Abrir menu" aria-expanded="false" aria-controls="navMenu" onclick="toggleNavMenu()"><span></span><span></span><span></span></button>
        <ul id="navMenu">
            <li><a href="#top">Home</a></li>
            <li class="nav-has-sub">
                <a href="#produtos" class="nav-sub-trigger">Produtos <span class="nav-caret">▾</span></a>
                <ul class="nav-submenu">
                    <li><a href="#credituz-os">Credituz OS</a></li>
                    <li><a href="#corban-ai">CORBAN AI</a></li>
                    <li><a href="./pages/credituz-score.html">Credituz Score</a></li>
                    <li><a href="#enterprise">Enterprise</a></li>
                </ul>
            </li>
            <li class="nav-has-sub">
                <a href="#credituz-os" class="nav-sub-trigger">Soluções <span class="nav-caret">▾</span></a>
                <ul class="nav-submenu">
                    <li><a href="#credituz-os">Análise de crédito</a></li>
                    <li><a href="./pages/crm-de-credito.html">CRM de crédito</a></li>
                    <li><a href="#cobranca-ai">Cobrança com IA</a></li>
                    <li><a href="#corban-ai">Embedded credit</a></li>
                </ul>
            </li>
            <li class="nav-has-sub">
                <a href="#segmentos" class="nav-sub-trigger">Segmentos <span class="nav-caret">▾</span></a>
                <ul class="nav-submenu">
                    <li><a href="./pages/construtoras.html">Construtoras e incorporadoras</a></li>
                    <li><a href="./pages/imobiliarias.html">Imobiliárias</a></li>
                    <li><a href="#corban-ai">Correspondentes e originadores</a></li>
                    <li><a href="#segmentos">Outras empresas</a></li>
                </ul>
            </li>
            <li><a href="#pricing">Preços</a></li>
            <li><a href="./pages/blog.html">Conteúdo</a></li>
            <li class="nav-lang"><a href="https://credituz.ai/en/" data-track="lang_en" aria-label="View in English">🇺🇸 EN</a></li>
            <li><a href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=saas-credituzai" class="nav-cta" target="_blank" rel="noopener" data-track="cta_nav">Começar agora</a></li>
        </ul>
    </div>
</nav>'''

body_architecture = '''<!-- DOR -->
<section class="arch-section arch-problem" id="problema">
  <div class="arch-inner">
    <div class="section-tag">O problema</div>
    <h2>A venda acontece. <em>O risco e o trabalho começam depois.</em></h2>
    <p class="arch-lead">Empresas ainda analisam crédito de forma fragmentada, acompanham clientes em controles paralelos, cobram de forma reativa e perdem a jornada quando o cliente precisa de financiamento.</p>
    <div class="arch-grid arch-grid-4">
      <article class="arch-card"><span class="arch-num">01</span><h3>Você vende antes de entender o risco.</h3><p>Sem uma análise consistente, a inadimplência pode começar na aprovação errada. Score, renda, capacidade de pagamento e política de crédito precisam estar no fluxo da decisão.</p><span class="arch-pill">Credituz OS</span></article>
      <article class="arch-card"><span class="arch-num">02</span><h3>A cobrança depende da sua equipe.</h3><p>Vencimentos, atrasos e follow-ups não deveriam depender de alguém lembrar de cobrar. Quanto maior a carteira, maior o custo operacional de fazer isso manualmente.</p><span class="arch-pill">Credituz OS</span></article>
      <article class="arch-card"><span class="arch-num">03</span><h3>Seu cliente precisa de crédito e você o manda embora.</h3><p>Quando a jornada vai para um banco ou correspondente externo, sua empresa perde visibilidade do pedido e deixa a experiência nas mãos de terceiros.</p><span class="arch-pill">CORBAN AI</span></article>
      <article class="arch-card"><span class="arch-num">04</span><h3>Sua operação financeira está espalhada.</h3><p>Crédito, CRM, cobrança, bancos e processos internos acabam funcionando em sistemas diferentes. Operações maiores precisam de uma infraestrutura que se adapte ao negócio.</p><span class="arch-pill">Enterprise</span></article>
    </div>
    <div class="arch-statement"><strong>Credituz OS analisa e cobra. CORBAN AI financia. Enterprise customiza e conecta.</strong></div>
  </div>
</section>

<!-- PRODUTOS -->
<section class="arch-section arch-products" id="produtos">
  <div class="arch-inner">
    <div class="section-tag">Produtos</div>
    <h2>Dois produtos. <em>Uma infraestrutura financeira.</em></h2>
    <p class="arch-lead">Use o Credituz OS para analisar risco e receber melhor. Use o CORBAN AI para incorporar crédito à jornada do seu cliente. Combine os dois no Enterprise quando sua operação exigir mais.</p>
    <div class="arch-grid arch-grid-2 arch-product-grid">
      <article class="arch-product arch-product-os" id="credituz-os">
        <div class="arch-product-top"><span class="arch-product-label">Credituz OS</span><span class="arch-product-price">R$ 297/mês</span></div>
        <h3>Analise. Acompanhe. Cobre.</h3>
        <p>O sistema operacional para empresas que precisam decidir melhor para quem vender e automatizar o relacionamento financeiro depois da venda.</p>
        <div class="arch-flow"><span>Cliente</span><i>→</i><span>Análise</span><i>→</i><span>Política</span><i>→</i><span>CRM de crédito</span><i>→</i><span>Cobrança</span><i>→</i><span>Recebimento</span></div>
        <ul class="arch-list">
          <li>Análise de crédito e política de crédito</li>
          <li><strong>CRM de crédito</strong></li>
          <li>Credituz Score por <strong>R$ 16 por análise</strong></li>
          <li>Régua de cobrança com IA em WhatsApp e e-mail</li>
          <li><strong>R$ 0,15 por envio</strong></li>
          <li>Recebíveis, baixa e conciliação</li>
          <li>Analytics</li>
          <li><strong>Até 3 usuários</strong></li>
        </ul>
        <a class="arch-btn arch-btn-primary" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=home-product-os" target="_blank" rel="noopener" data-track="cta_product_os">Começar com Credituz OS</a>
      </article>
      <article class="arch-product arch-product-corban" id="corban-ai">
        <div class="arch-product-top"><span class="arch-product-label">CORBAN AI</span><span class="arch-product-price arch-product-price-small">Modelo conforme a operação</span></div>
        <h3>Simule. Solicite. Financie.</h3>
        <p>Embedded credit para empresas que querem oferecer crédito aos próprios clientes sem construir uma operação financeira do zero.</p>
        <div class="arch-flow"><span>Cliente</span><i>→</i><span>Simulação</span><i>→</i><span>Bancos</span><i>→</i><span>Pedido</span><i>→</i><span>CRM Corban</span><i>→</i><span>Contratação</span></div>
        <ul class="arch-list">
          <li>Simulação de crédito multibanco</li>
          <li>Pedido e acompanhamento de crédito</li>
          <li><strong>CRM Corban</strong> para simulações, pedidos, documentos, pendências e status</li>
          <li>Jornada de embedded credit</li>
          <li>Originação de crédito dentro da experiência da sua empresa</li>
        </ul>
        <a class="arch-btn" href="https://wa.me/5511936209409" target="_blank" rel="noopener" data-track="cta_product_corban">Conhecer CORBAN AI</a>
      </article>
    </div>
    <div class="arch-split-note"><strong>Credituz OS cuida do risco e do recebimento.</strong><span>CORBAN AI cuida da originação do crédito.</span></div>
  </div>
</section>

<!-- SCORE -->
<section class="arch-section arch-score" id="score">
  <div class="arch-inner arch-score-grid">
    <div>
      <div class="section-tag">Credituz Score</div>
      <h2>Só precisa <em>analisar um cliente?</em></h2>
      <p class="arch-lead">Faça uma análise avulsa sem assinatura e sem mensalidade. Consulte quando precisar e evolua para o Credituz OS quando a análise virar rotina.</p>
      <div class="arch-score-price"><strong>R$ 27,70</strong><span>/ análise</span></div>
      <p class="arch-muted">Score, sinais de risco, renda estimada, capacidade de pagamento, restrições, protestos, processos e demais dados disponíveis no relatório.</p>
      <a class="arch-btn arch-btn-primary" href="./pages/credituz-score.html" data-track="home_score_entry">Fazer uma análise</a>
    </div>
    <div class="arch-calc" id="calculadora-score">
      <span class="arch-mini">Quando o OS passa a compensar?</span>
      <label for="scoreVolume">Análises por mês</label>
      <input id="scoreVolume" type="range" min="1" max="150" value="30" step="1" aria-label="Quantidade de análises por mês">
      <div class="arch-calc-volume"><strong id="scoreVolumeNumber">30</strong><span>análises/mês</span></div>
      <div class="arch-calc-results"><div><span>Score avulso</span><strong id="scoreAvulso">R$ 831,00</strong></div><div><span>Credituz OS</span><strong id="scorePlano">R$ 777,00</strong></div><div><span>Diferença</span><strong id="scoreEconomia">R$ 54,00</strong></div></div>
      <p id="scoreMessage">Com 30 análises, o plano já economiza <span>R$ 54,00/mês</span> e ainda inclui os outros módulos da Credituz.</p>
      <small>A partir de 26 análises/mês, considerando mensalidade + consultas, o Credituz OS já fica mais barato que comprar todas as análises avulsas.</small>
    </div>
  </div>
</section>

<!-- COBRANCA -->
<section class="arch-section arch-collection" id="cobranca-ai">
  <div class="arch-inner">
    <div class="section-tag">Cobrança com IA</div>
    <h2>Cobrar não deveria depender de <em>alguém lembrar.</em></h2>
    <p class="arch-lead">Configure a jornada e deixe a Credituz executar os contatos automaticamente por WhatsApp e e-mail. A operação ganha consistência sem aumentar o trabalho manual.</p>
    <div class="arch-collection-flow"><span>D-3</span><i>→</i><span>D0</span><i>→</i><span>D+3</span><i>→</i><span>Novos follow-ups</span></div>
    <div class="arch-badges"><span>WhatsApp</span><span>E-mail</span><span>R$ 0,15 por envio</span><span>SMS no Enterprise sob medida</span></div>
    <a class="arch-btn arch-btn-primary" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=home-collection-os" target="_blank" rel="noopener" data-track="cta_collection_os">Automatizar cobrança</a>
  </div>
</section>

<!-- ENTERPRISE -->
<section class="arch-section arch-enterprise" id="enterprise">
  <div class="arch-inner">
    <div class="section-tag">Enterprise</div>
    <h2>Monte a infraestrutura financeira e a <em>gestão operacional</em> que sua empresa precisa.</h2>
    <p class="arch-lead">Combine Credituz OS, CORBAN AI e funcionalidades específicas em uma solução desenhada para sua operação, com integrações, automações e soluções personalizadas com IA.</p>
    <div class="arch-grid arch-grid-3">
      <article class="arch-card arch-card-dark"><span class="arch-mini">Produtos base</span><h3>Comece pela infraestrutura certa.</h3><ul class="arch-list"><li>Credituz OS</li><li>CORBAN AI</li><li>Credituz OS + CORBAN AI</li><li>Usuários e volumes customizados</li></ul></article>
      <article class="arch-card arch-card-dark"><span class="arch-mini">Módulos específicos</span><h3>Adicione o que a operação exige.</h3><ul class="arch-list"><li><strong>Construtor de contratos com IA</strong></li><li>Assinatura digital</li><li>Serviços de cartório digital</li><li>SMS e canais adicionais</li><li>Políticas e fluxos customizados</li></ul></article>
      <article class="arch-card arch-card-dark"><span class="arch-mini">Customização</span><h3>Integre e automatize o seu modelo.</h3><ul class="arch-list"><li>API e integrações específicas</li><li>White Label e SSO</li><li>Multiempresa</li><li><strong>Soluções customizadas com IA</strong></li><li>SLA e atendimento dedicado</li></ul></article>
    </div>
    <div class="arch-enterprise-close"><strong>Quando o processo da sua empresa não cabe em um software padrão, adaptamos a infraestrutura Credituz à operação.</strong><a class="arch-btn arch-btn-light" href="https://wa.me/5511936209409" target="_blank" rel="noopener" data-track="cta_enterprise">Desenhar uma solução Enterprise</a></div>
  </div>
</section>

<!-- SEGMENTOS -->
<section class="arch-section arch-segments" id="segmentos">
  <div class="arch-inner">
    <div class="section-tag">Segmentos</div>
    <h2>Uma infraestrutura. <em>Diferentes modelos de negócio.</em></h2>
    <p class="arch-lead">A home apresenta os produtos de forma horizontal. As páginas de segmento aprofundam jornadas e necessidades específicas de cada mercado.</p>
    <div class="arch-grid arch-grid-4">
      <a class="arch-card arch-link-card" href="./pages/construtoras.html"><span class="arch-mini">Mercado imobiliário</span><h3>Construtoras e incorporadoras</h3><p>Análise de comprador, cobrança, crédito e jornadas específicas da operação imobiliária.</p><b>Ver solução →</b></a>
      <a class="arch-card arch-link-card" href="./pages/imobiliarias.html"><span class="arch-mini">Mercado imobiliário</span><h3>Imobiliárias</h3><p>Análise de compradores e inquilinos, CRM, cobrança e financiamento.</p><b>Ver solução →</b></a>
      <a class="arch-card arch-link-card" href="#corban-ai"><span class="arch-mini">Crédito</span><h3>Correspondentes e originadores</h3><p>Simulação multibanco, pedidos, CRM Corban e acompanhamento da originação.</p><b>Conhecer CORBAN AI →</b></a>
      <a class="arch-card arch-link-card" href="#credituz-os"><span class="arch-mini">Outros setores</span><h3>Empresas que vendem a prazo ou cobram recorrente</h3><p>Análise de crédito, CRM de crédito e cobrança com IA sem depender de uma vertical específica.</p><b>Conhecer Credituz OS →</b></a>
    </div>
  </div>
</section>

<!-- CASE -->
<section class="arch-section arch-case">
  <div class="arch-inner arch-case-grid">
    <div><div class="section-tag">Aplicação por segmento</div><h2>Profundidade vertical sem limitar a plataforma.</h2><p class="arch-lead">As páginas de segmento mostram como a mesma infraestrutura se adapta a jornadas específicas. No mercado imobiliário, a NJS Engenharia já usa a Credituz para ganhar controle operacional.</p></div>
    <blockquote>“Saímos de uma situação de baixo controle para o <strong>controle total da nossa carteira</strong>. Hoje sabemos exatamente o status de cada unidade, cada contrato e cada repasse.”<footer>Adson Soares · Gestor de Incorporação · NJS Engenharia</footer><a href="./pages/cases/njs-engenharia-credituz.html">Ver case completo →</a></blockquote>
  </div>
</section>

<!-- PRICING -->
<section class="arch-section arch-pricing" id="pricing">
  <div class="arch-inner">
    <div class="section-tag">Preços</div>
    <h2>Escolha a infraestrutura que <em>sua operação precisa.</em></h2>
    <p class="arch-lead">Credituz OS e CORBAN AI são produtos independentes. O Enterprise combina produtos e módulos conforme a necessidade da empresa.</p>
    <div class="arch-grid arch-grid-3 arch-price-grid">
      <article class="arch-price-card arch-price-featured"><span class="arch-mini">Análise + CRM + cobrança</span><h3>Credituz OS</h3><div class="arch-price"><strong>R$ 297</strong><span>/mês + R$ 16 por análise</span></div><p>Para empresas que precisam decidir melhor para quem vender e automatizar a cobrança.</p><ul class="arch-list"><li>Análise de crédito</li><li><strong>CRM de crédito</strong></li><li>Credituz Score por R$ 16</li><li>Cobrança com IA em WhatsApp e e-mail</li><li>R$ 0,15 por envio</li><li>Recebíveis, baixa e conciliação</li><li>Analytics</li><li><strong>Até 3 usuários</strong></li></ul><a class="arch-btn arch-btn-primary" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=home-pricing-os" target="_blank" rel="noopener" data-track="cta_pricing_os">Começar agora</a></article>
      <article class="arch-price-card"><span class="arch-mini">Embedded credit</span><h3>CORBAN AI</h3><div class="arch-price arch-price-text"><strong>Modelo comercial</strong><span>conforme a operação</span></div><p>Para empresas que querem oferecer crédito aos próprios clientes.</p><ul class="arch-list"><li>Simulação multibanco</li><li>Pedido de crédito</li><li><strong>CRM Corban</strong></li><li>Documentos, pendências e status</li><li>Embedded credit</li><li>Acompanhamento da originação</li></ul><a class="arch-btn" href="https://wa.me/5511936209409" target="_blank" rel="noopener" data-track="cta_pricing_corban">Falar com vendas</a></article>
      <article class="arch-price-card arch-price-enterprise"><span class="arch-mini">Infraestrutura customizada</span><h3>Enterprise</h3><div class="arch-price arch-price-text"><strong>Sob medida</strong><span>contrato anual</span></div><p>Monte a infraestrutura financeira e a gestão operacional que sua empresa precisa.</p><ul class="arch-list"><li>Credituz OS e/ou CORBAN AI</li><li>Usuários e volumes customizados</li><li>Construtor de contratos com IA</li><li>Assinatura digital</li><li>Cartório digital</li><li>SMS</li><li>API, White Label e SSO</li><li>Multiempresa e integrações</li><li>Soluções customizadas com IA</li><li>SLA e atendimento dedicado</li></ul><a class="arch-btn" href="https://wa.me/5511936209409" target="_blank" rel="noopener" data-track="cta_pricing_enterprise">Falar com um especialista</a></article>
    </div>
    <div class="arch-score-note"><strong>Precisa apenas de uma consulta?</strong> Credituz Score custa R$ 27,70 por análise, sem mensalidade. <a href="./pages/credituz-score.html">Fazer uma análise →</a></div>
  </div>
</section>

'''

new_faq = '''<!-- FAQ -->
<section id="faq" class="arch-section arch-faq">
  <div class="arch-inner">
    <div class="section-tag">Perguntas frequentes</div>
    <h2>Entenda como os produtos <em>se encaixam.</em></h2>
    <div class="faq">
      <div class="faq-item"><button class="faq-q"><h4>Qual a diferença entre Credituz OS e CORBAN AI?</h4><span>+</span></button><div class="faq-a"><p>O Credituz OS reúne análise de crédito, CRM de crédito e cobrança com IA. O CORBAN AI é a solução de embedded credit para simular, solicitar e acompanhar crédito multibanco, com CRM Corban próprio.</p></div></div>
      <div class="faq-item"><button class="faq-q"><h4>Preciso contratar os dois?</h4><span>+</span></button><div class="faq-a"><p>Não. Credituz OS e CORBAN AI podem ser contratados de acordo com a necessidade da operação. No Enterprise, eles também podem ser combinados.</p></div></div>
      <div class="faq-item"><button class="faq-q"><h4>Qual a diferença entre CRM de crédito e CRM Corban?</h4><span>+</span></button><div class="faq-a"><p>O CRM de crédito pertence ao Credituz OS e organiza clientes, análises e decisões de crédito. O CRM Corban pertence ao CORBAN AI e acompanha simulações, pedidos de crédito, documentos, pendências, bancos, status e contratação.</p></div></div>
      <div class="faq-item"><button class="faq-q"><h4>Onde ficam contratos com IA, assinatura digital e cartório digital?</h4><span>+</span></button><div class="faq-a"><p>Essas funcionalidades passam a fazer parte das soluções Enterprise e podem ser combinadas com Credituz OS, CORBAN AI, integrações e fluxos específicos.</p></div></div>
      <div class="faq-item"><button class="faq-q"><h4>O Enterprise pode ser customizado?</h4><span>+</span></button><div class="faq-a"><p>Sim. O Enterprise é a camada mais customizável da Credituz: pode combinar produtos, módulos, usuários, volumes, integrações, API, White Label, SSO e soluções específicas com IA.</p></div></div>
      <div class="faq-item"><button class="faq-q"><h4>A Credituz atende somente o mercado imobiliário?</h4><span>+</span></button><div class="faq-a"><p>Não. A Credituz pode atender empresas que precisam analisar clientes, automatizar cobrança ou incorporar crédito à própria jornada. O mercado imobiliário continua com páginas específicas para suas necessidades.</p></div></div>
      <div class="faq-item"><button class="faq-q"><h4>Quanto custa começar?</h4><span>+</span></button><div class="faq-a"><p>Uma análise avulsa no Credituz Score custa R$ 27,70. O Credituz OS custa R$ 297/mês mais R$ 16 por análise, para até 3 usuários. CORBAN AI tem modelo comercial conforme a operação e Enterprise é sob medida.</p></div></div>
    </div>
  </div>
</section>

'''

new_cta = '''<!-- CTA FINAL -->
<section class="cta-final">
    <div class="cta-final-inner">
        <h2>Sua operação financeira pode <em>trabalhar melhor.</em></h2>
        <p>Analise melhor, cobre automaticamente e incorpore crédito à experiência dos seus clientes com a infraestrutura da Credituz.</p>
        <div class="arch-final-actions"><a href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=home-final-os" class="btn-final" target="_blank" rel="noopener" data-track="cta_final">Começar com Credituz OS</a><a href="https://wa.me/5511936209409" class="arch-final-link" target="_blank" rel="noopener" data-track="cta_final_sales">Falar sobre CORBAN AI ou Enterprise →</a></div>
    </div>
</section>'''

arch_css = r'''
<style id="home-architecture-v3">
.arch-section{max-width:none;width:100%;padding:88px 24px;margin:0}.arch-inner{max-width:1120px;margin:0 auto}.arch-section h2{font-size:clamp(32px,4.8vw,52px);max-width:900px;margin:8px 0 16px}.arch-section h2 em{font-style:normal;color:var(--lime)}.arch-lead{font-size:18px;line-height:1.6;color:var(--gray-2);max-width:820px;margin:0 0 34px}.arch-grid{display:grid;gap:18px}.arch-grid-2{grid-template-columns:repeat(2,minmax(0,1fr))}.arch-grid-3{grid-template-columns:repeat(3,minmax(0,1fr))}.arch-grid-4{grid-template-columns:repeat(4,minmax(0,1fr))}.arch-card,.arch-product,.arch-price-card,.arch-calc{background:#fff;border:1px solid var(--gray-soft);border-radius:22px;padding:26px}.arch-card h3,.arch-product h3,.arch-price-card h3{font-size:23px;margin:10px 0}.arch-card p,.arch-product p,.arch-price-card p{color:var(--gray-2);line-height:1.55}.arch-num{font-size:13px;font-weight:750;color:var(--lime)}.arch-pill,.arch-badges span{display:inline-flex;margin-top:18px;padding:7px 11px;border-radius:999px;background:var(--accent-soft);color:var(--lime-deep);font-size:12.5px;font-weight:700}.arch-problem{background:var(--paper-warm)}.arch-statement{margin-top:22px;background:var(--ink);color:#fff;border-radius:20px;padding:22px 24px;font-size:clamp(18px,2.5vw,27px)}.arch-products{background:#fff}.arch-product{display:flex;flex-direction:column;min-height:100%}.arch-product-os{border-color:#9bc8f7}.arch-product-top{display:flex;justify-content:space-between;gap:14px;align-items:flex-start}.arch-product-label{font-size:14px;font-weight:800;color:var(--lime)}.arch-product-price{font-size:14px;font-weight:800}.arch-product-price-small{color:var(--gray-2);font-weight:650}.arch-product h3{font-size:clamp(28px,3vw,40px);margin-top:24px}.arch-flow{display:flex;gap:8px;align-items:center;flex-wrap:wrap;margin:22px 0;padding:14px 16px;border-radius:16px;background:var(--paper-warm);font-size:12.5px;font-weight:650}.arch-flow i{font-style:normal;color:var(--gray-3)}.arch-list{list-style:none;margin:18px 0 26px;padding:0}.arch-list li{position:relative;padding:7px 0 7px 22px;line-height:1.45}.arch-list li:before{content:'✓';position:absolute;left:0;color:var(--good);font-weight:800}.arch-btn{display:inline-flex;align-items:center;justify-content:center;width:max-content;max-width:100%;padding:13px 18px;border:1px solid var(--ink);border-radius:999px;color:var(--ink);text-decoration:none;font-weight:750;margin-top:auto}.arch-btn-primary{background:var(--ink);color:#fff}.arch-split-note{margin-top:18px;display:flex;justify-content:center;gap:8px;flex-wrap:wrap;padding:18px;background:var(--paper-warm);border-radius:16px}.arch-score{background:var(--paper-warm)}.arch-score-grid{display:grid;grid-template-columns:.9fr 1.1fr;gap:34px;align-items:center}.arch-score-price{display:flex;align-items:baseline;gap:8px;margin:18px 0}.arch-score-price strong{font-size:42px;letter-spacing:-.04em}.arch-score-price span,.arch-muted{color:var(--gray-2)}.arch-calc{background:#fff}.arch-mini{font-size:12px;font-weight:750;color:var(--lime);display:block;margin-bottom:8px}.arch-calc label{display:block;font-weight:700;margin-top:12px}.arch-calc input{width:100%;margin:14px 0}.arch-calc-volume{display:flex;align-items:baseline;gap:8px}.arch-calc-volume strong{font-size:38px}.arch-calc-volume span{color:var(--gray-2)}.arch-calc-results{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:18px 0}.arch-calc-results div{background:var(--paper-warm);padding:14px;border-radius:14px}.arch-calc-results span{display:block;font-size:11px;color:var(--gray-2)}.arch-calc-results strong{display:block;margin-top:4px}.arch-calc #scoreMessage{font-weight:650}.arch-calc #scoreMessage span{color:var(--lime)}.arch-calc small{display:block;color:var(--gray-2);margin-top:10px;line-height:1.45}.arch-collection{background:#fff}.arch-collection-flow{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:26px 0}.arch-collection-flow span{padding:14px 18px;border-radius:14px;background:var(--paper-warm);font-weight:750}.arch-collection-flow i{font-style:normal;color:var(--gray-3)}.arch-badges{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:24px}.arch-badges span{margin-top:0}.arch-enterprise{background:#050506;color:#fff}.arch-enterprise .section-tag{color:var(--accent-bright)}.arch-enterprise h2 em{color:var(--accent-bright)}.arch-enterprise .arch-lead{color:#b8b8bd}.arch-card-dark{background:#121214;border-color:#2b2b30;color:#fff}.arch-card-dark p,.arch-card-dark li{color:#d2d2d7}.arch-card-dark .arch-mini{color:var(--accent-bright)}.arch-enterprise-close{margin-top:22px;padding:24px;border:1px solid #2b2b30;border-radius:20px;display:flex;align-items:center;justify-content:space-between;gap:20px}.arch-enterprise-close strong{max-width:720px;font-size:18px}.arch-btn-light{background:#fff;color:#111;border-color:#fff}.arch-segments{background:var(--paper-warm)}.arch-link-card{text-decoration:none;color:var(--ink);transition:transform .15s ease}.arch-link-card:hover{transform:translateY(-2px)}.arch-link-card b{display:block;margin-top:18px;color:var(--lime)}.arch-case{background:#fff}.arch-case-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:38px;align-items:center}.arch-case blockquote{margin:0;padding:30px;border-radius:22px;background:var(--paper-warm);font-size:21px;line-height:1.5}.arch-case blockquote footer{font-size:13px;color:var(--gray-2);margin-top:16px}.arch-case blockquote a{display:inline-block;margin-top:12px;font-size:14px;color:var(--lime);text-decoration:none;font-weight:700}.arch-pricing{background:var(--paper-warm)}.arch-price-card{display:flex;flex-direction:column}.arch-price-featured{border-color:#87bdf3;box-shadow:0 0 0 3px rgba(0,113,227,.05)}.arch-price-enterprise{background:var(--ink);color:#fff;border-color:var(--ink)}.arch-price-enterprise p,.arch-price-enterprise li{color:#d2d2d7}.arch-price-enterprise .arch-btn{border-color:#fff;color:#fff}.arch-price{margin:18px 0}.arch-price strong{display:block;font-size:36px;letter-spacing:-.04em}.arch-price span{display:block;color:var(--gray-2);font-size:13px;margin-top:2px}.arch-price-enterprise .arch-price span{color:#a1a1a6}.arch-price-text strong{font-size:28px}.arch-score-note{margin-top:18px;text-align:center;padding:18px;border-radius:16px;background:#fff}.arch-score-note a{color:var(--lime);font-weight:700;text-decoration:none}.arch-faq{background:#fff}.arch-final-actions{display:flex;align-items:center;justify-content:center;gap:18px;flex-wrap:wrap}.arch-final-link{color:#fff;text-decoration:none;font-weight:700}.arch-final-link:hover{text-decoration:underline}@media(max-width:980px){.arch-grid-4,.arch-grid-3{grid-template-columns:repeat(2,minmax(0,1fr))}.arch-score-grid,.arch-case-grid{grid-template-columns:1fr}}@media(max-width:720px){.arch-section{padding:64px 20px}.arch-grid-2,.arch-grid-3,.arch-grid-4{grid-template-columns:1fr}.arch-lead{font-size:16px}.arch-product-top,.arch-enterprise-close{align-items:flex-start;flex-direction:column}.arch-calc-results{grid-template-columns:1fr}.arch-flow{align-items:flex-start}.arch-btn{width:100%}.arch-final-actions{align-items:stretch;flex-direction:column}.arch-final-link{text-align:center}}
</style>
'''

html = INDEX.read_text(encoding='utf-8')
html = sub1(html, r'<title>.*?</title>', '<title>Credituz · Análise de crédito, cobrança e embedded finance com IA</title>', 'title')
html = sub1(html, r'<meta name="description" content="[^"]*">', '<meta name="description" content="Analise clientes, automatize cobranças e ofereça crédito multibanco com Credituz OS e CORBAN AI. Enterprise combina infraestrutura financeira, gestão operacional e soluções customizadas com IA.">', 'meta description', flags=0)
html = sub1(html, r'<script type="application/ld\+json">.*?</script>', '<script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False, separators=(',', ':')) + '</script>', 'json-ld')
html = sub1(html, r'<nav id="nav">.*?</nav>', new_nav, 'navigation')
html = sub1(html, r'<p class="hero-kicker">.*?</p>', '<p class="hero-kicker">Crédito, cobrança e embedded finance com IA</p>', 'hero kicker')
html = sub1(html, r'<h1 class="hero-title" id="heroTitle">.*?</h1>', '<h1 class="hero-title" id="heroTitle">Decida para quem vender. <em>Receba melhor. Ofereça crédito.</em></h1>', 'hero title')
html = sub1(html, r'<p class="hero-sub" id="heroSub">.*?</p>', '<p class="hero-sub" id="heroSub">Analise clientes, organize sua operação de crédito, automatize cobranças e ofereça crédito multibanco com IA usando Credituz OS e CORBAN AI.</p>', 'hero subtitle')
html = sub1(html, r'<div class="hero-meta">.*?</div>', '<div class="hero-meta">Análise de crédito · CRM de crédito · Cobrança com IA · Embedded credit multibanco</div>', 'hero meta')
html = html.replace('Grupo Valore · NJS Engenharia · Bilha Imóveis e outras operações que já vendem e cobram com a Credituz', 'Grupo Valore · NJS Engenharia · Bilha Imóveis e outras empresas que já operam com a Credituz')

start = html.find('<!-- DOR -->')
faq = html.find('<!-- FAQ -->', start)
if start < 0 or faq < 0:
    raise SystemExit('home body markers not found')
html = html[:start] + body_architecture + html[faq:]

faq_start = html.find('<!-- FAQ -->')
cta_start = html.find('<!-- CTA FINAL -->', faq_start)
if faq_start < 0 or cta_start < 0:
    raise SystemExit('FAQ/CTA markers not found')
html = html[:faq_start] + new_faq + html[cta_start:]

cta_start = html.find('<!-- CTA FINAL -->')
cta_section = html.find('<section class="cta-final">', cta_start)
cta_end = html.find('</section>', cta_section)
if min(cta_start, cta_section, cta_end) < 0:
    raise SystemExit('final CTA section not found')
cta_end += len('</section>')
html = html[:cta_start] + new_cta + html[cta_end:]

if 'id="home-architecture-v3"' not in html:
    html = html.replace('</head>', arch_css + '</head>', 1)

INDEX.write_text(html, encoding='utf-8')

home_md = '''# Credituz — Análise de crédito, cobrança e embedded finance com IA

> A Credituz é uma plataforma brasileira de crédito e cobrança com IA para empresas. O Credituz OS reúne análise de crédito, CRM de crédito e cobrança. O CORBAN AI permite simular, solicitar e acompanhar crédito multibanco com CRM Corban. O Enterprise combina esses produtos com infraestrutura financeira, gestão operacional e soluções customizadas.

- Canonical: https://www.credituz.ai/
- Language: pt-BR
- Updated: 2026-09

---

## O que é a Credituz?

A Credituz atende empresas que precisam tomar decisões de crédito, automatizar recebimentos ou incorporar crédito à própria jornada. A home apresenta os produtos de forma horizontal; páginas de segmento aprofundam aplicações específicas para mercados como construção e incorporação imobiliária, imobiliárias e operações de originação de crédito.

## Posicionamento

**Título da home:** “Decida para quem vender. Receba melhor. Ofereça crédito.”

**Subtítulo:** “Analise clientes, organize sua operação de crédito, automatize cobranças e ofereça crédito multibanco com IA usando Credituz OS e CORBAN AI.”

A arquitetura comercial separa claramente os produtos:

- **Credituz OS:** análise de crédito + CRM de crédito + cobrança com IA.
- **CORBAN AI:** embedded credit + simulação multibanco + pedido de crédito + CRM Corban.
- **Enterprise:** infraestrutura financeira e gestão operacional sob medida, podendo combinar Credituz OS, CORBAN AI e módulos específicos.
- **Credituz Score:** análise de crédito avulsa para quem ainda não precisa de uma operação recorrente.

## O problema que a Credituz resolve

- **Risco de crédito fragmentado:** empresas vendem antes de reunir análise, capacidade de pagamento e política de crédito em um fluxo consistente.
- **Cobrança reativa:** vencimentos e atrasos dependem de acompanhamento manual.
- **Jornada de financiamento terceirizada:** quando o cliente precisa de crédito, muitas empresas perdem visibilidade ao mandar a operação para terceiros.
- **Operação financeira espalhada:** crédito, CRM, cobrança, bancos e processos internos acabam em sistemas desconectados.

## Credituz OS

**Analise. Acompanhe. Cobre.**

O Credituz OS é o sistema operacional para empresas que precisam decidir melhor para quem vender e automatizar o relacionamento financeiro depois da venda.

Fluxo: **Cliente → Análise → Política de crédito → CRM de crédito → Cobrança → Recebimento**.

Inclui:
- análise de crédito e política de crédito;
- **CRM de crédito**;
- análises Credituz Score por **R$ 16 cada**;
- régua de cobrança com IA em WhatsApp e e-mail;
- cobrança por **R$ 0,15 por envio**;
- recebíveis, baixa e conciliação;
- analytics;
- **até 3 usuários**.

Preço: **R$ 297/mês + R$ 16 por análise**.

## CORBAN AI

**Simule. Solicite. Financie.**

CORBAN AI é a solução de embedded credit para empresas que querem oferecer crédito aos próprios clientes sem construir uma operação financeira do zero.

Fluxo: **Cliente → Simulação → Bancos → Pedido de crédito → CRM Corban → Contratação**.

Inclui:
- simulação de crédito multibanco;
- pedido e acompanhamento de crédito;
- **CRM Corban** para simulações, pedidos, documentos, pendências, bancos, status e contratação;
- jornada de embedded credit;
- acompanhamento da originação dentro da experiência da empresa.

Modelo comercial: **conforme a operação**.

## Credituz Score

Para quem precisa apenas de uma consulta de crédito, o Credituz Score custa **R$ 27,70 por análise**, sem assinatura ou mensalidade. Considerando apenas mensalidade e consultas, a partir de 26 análises por mês o Credituz OS já fica mais barato que comprar todas as análises avulsas.

## Cobrança com IA

No Credituz OS, a régua de cobrança automatiza contatos em **WhatsApp e e-mail** por **R$ 0,15 por envio**. SMS fica disponível em projetos **Enterprise sob medida**.

## Enterprise

**Monte a infraestrutura financeira e a gestão operacional que sua empresa precisa.**

O Enterprise é a oferta mais customizável da Credituz. Pode combinar Credituz OS, CORBAN AI e módulos específicos conforme a operação.

Possibilidades:
- Credituz OS e/ou CORBAN AI;
- usuários e volumes customizados;
- **construtor de contratos com IA**;
- assinatura digital;
- serviços de cartório digital;
- SMS e canais adicionais;
- políticas e fluxos customizados;
- API e integrações específicas;
- White Label e SSO;
- multiempresa;
- **soluções customizadas com IA**;
- SLA e atendimento dedicado.

Preço: **sob medida**, com contrato anual.

## CRM de crédito x CRM Corban

- **CRM de crédito:** pertence ao Credituz OS e organiza clientes, análises e decisões de crédito.
- **CRM Corban:** pertence ao CORBAN AI e acompanha simulações, pedidos de crédito, documentos, pendências, bancos, status e contratação.

## Segmentos

A Credituz não é limitada ao mercado imobiliário. A plataforma pode atender empresas que vendem a prazo, cobram de forma recorrente ou querem incorporar crédito à própria experiência. Existem páginas específicas para construtoras e incorporadoras e para imobiliárias, além do CORBAN AI para operações de originação e embedded credit.

## Planos e preços na home

A comparação principal da home tem três produtos:

1. **Credituz OS — R$ 297/mês + R$ 16 por análise**, para até 3 usuários.
2. **CORBAN AI — modelo comercial conforme a operação**.
3. **Enterprise — sob medida**, com infraestrutura financeira e gestão operacional customizadas.

O **Credituz Score — R$ 27,70 por análise** permanece como porta de entrada self-service, fora da comparação principal de três produtos.

## Perguntas frequentes

### Qual a diferença entre Credituz OS e CORBAN AI?
O Credituz OS reúne análise de crédito, CRM de crédito e cobrança com IA. O CORBAN AI cuida de embedded credit, simulação multibanco, pedido de crédito e CRM Corban.

### Preciso contratar os dois?
Não. Os produtos podem ser usados separadamente. O Enterprise também pode combinar os dois.

### Onde ficam contratos com IA, assinatura digital e cartório digital?
Essas funcionalidades fazem parte de soluções Enterprise.

### A Credituz atende somente o mercado imobiliário?
Não. A Credituz atende empresas que precisam analisar clientes, automatizar cobrança ou incorporar crédito à própria jornada. As páginas de segmento detalham aplicações específicas.

### Quanto custa começar?
Uma análise avulsa no Credituz Score custa R$ 27,70. O Credituz OS custa R$ 297/mês mais R$ 16 por análise, para até 3 usuários. CORBAN AI tem modelo conforme a operação e Enterprise é sob medida.

## Contato e site

- Website: https://www.credituz.ai
- Blog: https://www.credituz.ai/pages/blog.html
- WhatsApp: https://wa.me/5511936209409
'''
HOME_MD.write_text(home_md, encoding='utf-8')

full = LLMS_FULL.read_text(encoding='utf-8')
blog_marker = '\n\n\n---\n\n# Blog Credituz — Conteúdo completo'
idx = full.find(blog_marker)
if idx < 0:
    raise SystemExit('blog marker not found in llms-full.txt')
LLMS_FULL.write_text(home_md.rstrip() + full[idx:], encoding='utf-8')

llms = LLMS.read_text(encoding='utf-8')
llms = sub1(llms, r'^# Credituz\n\n> .*?\n\n## Principais páginas', '# Credituz\n\n> Plataforma de análise de crédito, cobrança e embedded finance com IA para empresas. Credituz OS reúne análise de crédito, CRM de crédito e cobrança; CORBAN AI reúne simulação multibanco, pedido de crédito e CRM Corban; Enterprise combina infraestrutura financeira, gestão operacional e soluções customizadas.\n\n## Principais páginas', 'llms intro')
llms = llms.replace('visão geral, 5 agentes de IA, planos e preços', 'visão geral de Credituz OS, CORBAN AI, Enterprise, Credituz Score e preços')
LLMS.write_text(llms, encoding='utf-8')

HOME_JSON.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Assertions for the approved product architecture.
check = INDEX.read_text(encoding='utf-8')
required = [
    'Decida para quem vender.',
    'CRM de crédito',
    'CRM Corban',
    'Dois produtos. <em>Uma infraestrutura financeira.</em>',
    'R$ 297/mês',
    'Até 3 usuários',
    'R$ 0,15 por envio',
    'Monte a infraestrutura financeira e a <em>gestão operacional</em> que sua empresa precisa.',
    'Construtor de contratos com IA',
    'Soluções customizadas com IA',
    'Embedded credit'
]
for item in required:
    if item not in check:
        raise SystemExit(f'missing required copy: {item}')

for stale in [
    'O imóvel é vendido.',
    'CRM de crédito + CORBAN AI',
    'Contratos com IA, assinatura digital e cartório digital</li>',
    'Da simulação</em> à entrega das chaves',
    'Uma camada de IA que conecta toda a operação.'
]:
    if stale in check:
        raise SystemExit(f'stale home copy remains: {stale}')

print('home horizontal product architecture applied successfully')
