from pathlib import Path
import json

p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = s.replace('<title>Credituz · Análise de crédito, cobrança e embedded finance com IA</title>', '<title>Credituz · Análise de crédito, cobrança e financiamento com agentes de IA</title>', 1)
s = s.replace('<p class="hero-kicker">Crédito, cobrança e embedded finance com IA</p>', '<p class="hero-kicker">Sistema operacional e financeiro</p>', 1)
s = s.replace('<h1 class="hero-title" id="heroTitle">Decida para quem vender. <em>Receba melhor. Ofereça crédito.</em></h1>', '<h1 class="hero-title" id="heroTitle">Análise crédito, cobrança e financiamento com <em>agentes de IA.</em></h1>', 1)

current_widget = '''        <div class="widget-header">
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
        </div>'''

previous_widget = '''        <div class="widget-header">
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
        </div>'''

if current_widget not in s:
    raise SystemExit('current hero phone widget not found')
s = s.replace(current_widget, previous_widget, 1)

s = s.replace('Grupo Valore · NJS Engenharia · Bilha Imóveis e outras empresas que já operam com a Credituz', 'Grupo Valore · NJS Engenharia · Bilha Imóveis e outras operações que já vendem e cobram com a Credituz', 1)

p.write_text(s, encoding='utf-8')

for fname in ['home.md', 'llms-full.txt']:
    fp = Path(fname)
    text = fp.read_text(encoding='utf-8')
    text = text.replace('# Credituz — Análise de crédito, cobrança e embedded finance com IA', '# Credituz — Análise de crédito, cobrança e financiamento com agentes de IA', 1)
    text = text.replace('**Título da home:** “Decida para quem vender. Receba melhor. Ofereça crédito.”', '**Título da home:** “Análise crédito, cobrança e financiamento com agentes de IA.”', 1)
    marker = '> A Credituz é uma plataforma brasileira de crédito e cobrança com IA para empresas.'
    if marker in text:
        text = text.replace(marker, '> A Credituz é um sistema operacional e financeiro com agentes de IA para análise de crédito, cobrança e financiamento de empresas.', 1)
    fp.write_text(text, encoding='utf-8')

hp = Path('home.json')
data = json.loads(hp.read_text(encoding='utf-8'))
for node in data.get('@graph', []):
    if node.get('@type') == 'Organization':
        node['description'] = 'Sistema operacional e financeiro com agentes de IA para análise de crédito, cobrança e financiamento de empresas.'
    if node.get('@type') == 'SoftwareApplication':
        node['description'] = 'Sistema operacional e financeiro com agentes de IA. O Credituz OS reúne análise de crédito, CRM de crédito e cobrança; o CORBAN AI reúne simulação, pedido de crédito multibanco e CRM Corban; e o Enterprise adiciona infraestrutura financeira, gestão operacional e soluções customizadas.'
hp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# LLM index: restore broad institutional phrase without narrowing the product architecture.
lt = Path('llms.txt')
text = lt.read_text(encoding='utf-8')
first = text.splitlines()
if first:
    for i, line in enumerate(first):
        if line.startswith('> '):
            first[i] = '> Sistema operacional e financeiro com agentes de IA para análise de crédito, cobrança e financiamento. Credituz OS para analisar e cobrar, CORBAN AI para financiar e Enterprise para customizar a operação.'
            break
lt.write_text('\n'.join(first) + ('\n' if text.endswith('\n') else ''), encoding='utf-8')

print('hero, phone visual, social proof and machine-readable positioning updated')
