from pathlib import Path
import re


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'missing expected block: {label}')
    return text.replace(old, new, 1)


def clean_pt(path: Path):
    s = path.read_text(encoding='utf-8')

    s, n = re.subn(r'\n\s*<div class="hero-ttv">.*?</div>\n\s*<div class="hero-actions">', '\n    <div class="hero-actions">', s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('hero time-to-value block not found')

    s = s.replace('Criar minha conta\n            <svg width="18"', 'Começar com Credituz OS\n            <svg width="18"', 1)

    old_widget = '''    <div class="hero-widget">
        <div class="widget-header">
            <div class="widget-avatar"></div>
            <div class="widget-info">
                <div class="widget-name">CORBAN AI · Credituz</div>
                <div class="widget-status">comparando 8 instituições</div>
            </div>
        </div>

        <div class="msg msg-user">Oi, preciso financiar R$ 380k. Consigo aprovar?</div>
        <div class="msg msg-bot">Simulei com a sua renda e o FGTS. Melhor condição abaixo, já com a proposta pronta.</div>

        <div class="widget-card">
            <div class="widget-card-row"><span class="bank"><img src="/assets/banks/icon-bradesco.png" alt="" aria-hidden="true">Bradesco</span><span>9,80% a.a.</span></div>
            <div class="widget-card-row"><span class="bank"><img src="/assets/banks/icon-inter.png" alt="" aria-hidden="true">Inter</span><span>9,89% a.a.</span></div>
            <div class="widget-card-row"><span class="bank"><img src="/assets/banks/icon-santander.png" alt="" aria-hidden="true">Santander</span><span>10,15% a.a.</span></div>
            <div class="widget-card-row highlight"><span>Pré-aprovado</span><span>R$ 304k</span></div>
            <div class="widget-card-row highlight"><span>Parcela</span><span>R$ 2.940/mês</span></div>
        </div>

        <div class="widget-steps">
            <div class="widget-step done"><span><b>Crédito pré-aprovado</b> · 8 instituições em 30s</span></div>
            <div class="widget-step done"><span><b>Contrato digital</b> gerado e enviado</span></div>
            <div class="widget-step now"><span><b>Régua de cobrança</b> ativa na carteira</span></div>
        </div>
    </div>'''

    new_widget = '''    <div class="hero-widget">
        <div class="widget-header">
            <div class="widget-avatar"></div>
            <div class="widget-info">
                <div class="widget-name">CORBAN AI · Credituz</div>
                <div class="widget-status">simulação multibanco + CRM Corban</div>
            </div>
        </div>

        <div class="msg msg-user">Meu cliente precisa de crédito para fechar uma compra. Consigo simular e acompanhar por aqui?</div>
        <div class="msg msg-bot">Sim. O CORBAN AI compara opções, envia o pedido e mantém o status da operação no CRM Corban.</div>

        <div class="widget-card">
            <div class="widget-card-row"><span>Simulação multibanco</span><span>disponível</span></div>
            <div class="widget-card-row"><span>Pedido de crédito</span><span>centralizado</span></div>
            <div class="widget-card-row highlight"><span>CRM Corban</span><span>status e pendências</span></div>
        </div>

        <div class="widget-steps">
            <div class="widget-step done"><span><b>Simulação</b> criada</span></div>
            <div class="widget-step done"><span><b>Pedido de crédito</b> enviado</span></div>
            <div class="widget-step now"><span><b>CRM Corban</b> acompanhando a operação</span></div>
        </div>
    </div>'''
    s = replace_once(s, old_widget, new_widget, 'hero CORBAN widget')

    s = s.replace('O sistema operacional de crédito e cobrança, com agentes de IA em português.', 'Plataforma de análise de crédito, cobrança e embedded finance com IA para empresas.', 1)

    old_footer = '''      <h4>Soluções</h4>
      <ul>
          <li><a href="./pages/credituz-score.html">Score de crédito</a></li>
          <li><a href="./pages/crm-de-credito.html">CRM de crédito</a></li>
          <li><a href="./pages/contratos-imobiliarios-digitais.html">Contratos e assinatura</a></li>
          <li><a href="./pages/cobranca-e-recebiveis-imobiliarios.html">Cobrança e recebíveis</a></li>
          <li><a href="./pages/portal-vendas-empreendimentos.html">Portal de vendas</a></li>
          <li><a href="./pages/gestao-de-unidades-imobiliarias.html">Gestão de unidades</a></li>
      </ul>'''
    new_footer = '''      <h4>Soluções</h4>
      <ul>
          <li><a href="./pages/credituz-score.html">Análise de crédito</a></li>
          <li><a href="./pages/crm-de-credito.html">CRM de crédito</a></li>
          <li><a href="#cobranca-ai">Cobrança com IA</a></li>
          <li><a href="#corban-ai">Embedded credit</a></li>
      </ul>'''
    s = replace_once(s, old_footer, new_footer, 'footer solutions')

    path.write_text(s, encoding='utf-8')


def clean_en(path: Path):
    if not path.exists():
        return
    s = path.read_text(encoding='utf-8')
    s, n = re.subn(r'\n\s*<div class="hero-ttv">.*?</div>\n\s*<div class="hero-actions">', '\n    <div class="hero-actions">', s, count=1, flags=re.S)
    if n != 1:
        raise SystemExit('EN hero time-to-value block not found')

    s = s.replace('Create my account\n', 'Start with Credituz OS\n', 1)
    s = s.replace('comparing 8 institutions', 'multi-bank simulation + Corban CRM', 1)
    s = s.replace('Hi, I need to finance R$380k. Can I get approved?', 'My customer needs credit to complete a purchase. Can I simulate and track it here?', 1)
    s = s.replace('I simulated it with your income and FGTS. Best condition below, with the proposal already ready.', 'Yes. CORBAN AI compares options, submits the credit request and keeps the operation status in Corban CRM.', 1)

    old_rows = '''            <div class="widget-card-row"><span class="bank"><img src="/assets/banks/icon-bradesco.png" alt="" aria-hidden="true"/>Bradesco</span><span>9.80% p.a.</span></div>
            <div class="widget-card-row"><span class="bank"><img src="/assets/banks/icon-inter.png" alt="" aria-hidden="true"/>Inter</span><span>9.89% p.a.</span></div>
            <div class="widget-card-row"><span class="bank"><img src="/assets/banks/icon-santander.png" alt="" aria-hidden="true"/>Santander</span><span>10.15% p.a.</span></div>
            <div class="widget-card-row highlight"><span>Pre-approved</span><span>R$ 304k</span></div>
            <div class="widget-card-row highlight"><span>Installment</span><span>R$ 2,940/month</span></div>'''
    new_rows = '''            <div class="widget-card-row"><span>Multi-bank simulation</span><span>available</span></div>
            <div class="widget-card-row"><span>Credit request</span><span>centralized</span></div>
            <div class="widget-card-row highlight"><span>Corban CRM</span><span>status and pending items</span></div>'''
    if old_rows in s:
        s = s.replace(old_rows, new_rows, 1)

    s = s.replace('<div class="widget-step done"><span><b>Pre-approved credit</b> · 8 institutions in 30s</span></div>', '<div class="widget-step done"><span><b>Simulation</b> created</span></div>', 1)
    s = s.replace('<div class="widget-step done"><span><b>Digital contract</b> generated and sent</span></div>', '<div class="widget-step done"><span><b>Credit request</b> submitted</span></div>', 1)
    s = s.replace('<div class="widget-step now"><span><b>Collection schedule</b> active in portfolio</span></div>', '<div class="widget-step now"><span><b>Corban CRM</b> tracking the operation</span></div>', 1)
    s = s.replace('The credit and collections operating system, with AI agents in Portuguese.', 'Credit analysis, collections and embedded finance with AI for companies.', 1)

    path.write_text(s, encoding='utf-8')


clean_pt(Path('index.html'))
clean_en(Path('en/index.html'))

pt = Path('index.html').read_text(encoding='utf-8')
for stale in ['Primeiro contrato gerado', '8 instituições em 30s', 'Simulei com a sua renda e o FGTS', 'Contratos e assinatura</a>', 'Portal de vendas</a>', 'Gestão de unidades</a>']:
    if stale in pt:
        raise SystemExit(f'stale horizontal-home copy remains: {stale}')
for required in ['Start' if False else 'Começar com Credituz OS', 'simulação multibanco + CRM Corban', 'Cobrança com IA</a>', 'Embedded credit</a>']:
    if required not in pt:
        raise SystemExit(f'missing expected home copy: {required}')
print('horizontal home consistency cleanup applied')
