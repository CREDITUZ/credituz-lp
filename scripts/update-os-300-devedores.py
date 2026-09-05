from pathlib import Path
import json


def replace_once(text, old, new, label):
    if old not in text:
        raise SystemExit(f'missing target: {label}')
    return text.replace(old, new, 1)

# Home HTML
p = Path('index.html')
s = p.read_text(encoding='utf-8')

s = replace_once(
    s,
    'R$ 297 por mês mais R$ 16 por análise, para até 3 usuários. Inclui análise de crédito, CRM de crédito e régua de cobrança com IA em WhatsApp e e-mail por R$ 0,15 por envio.',
    'R$ 297 por mês mais R$ 16 por análise, para até 3 usuários. Inclui análise de crédito, CRM de crédito e régua de cobrança com IA em WhatsApp e e-mail para até 300 devedores por mês.',
    'schema OS offer',
)
s = replace_once(
    s,
    'O Credituz OS custa R$ 297 por mês, mais R$ 16 por análise de crédito, para até 3 usuários. A régua de cobrança em WhatsApp e e-mail custa R$ 0,15 por envio.',
    'O Credituz OS custa R$ 297 por mês, mais R$ 16 por análise de crédito, para até 3 usuários. A régua de cobrança em WhatsApp e e-mail atende até 300 devedores por mês, com os momentos de contato definidos pela própria operação.',
    'schema OS faq',
)
s = replace_once(
    s,
    '<li><strong>R$ 0,15 por envio</strong></li>',
    '<li><strong>Cobre até 300 devedores por mês</strong></li>',
    'OS product card collection limit',
)
s = replace_once(
    s,
    '<p class="arch-lead">Configure a jornada e deixe a Credituz executar os contatos automaticamente por WhatsApp e e-mail. A operação ganha consistência sem aumentar o trabalho manual.</p>\n    <div class="arch-collection-flow"><span>D-3</span><i>→</i><span>D0</span><i>→</i><span>D+3</span><i>→</i><span>Novos follow-ups</span></div>\n    <div class="arch-badges"><span>WhatsApp</span><span>E-mail</span><span>R$ 0,15 por envio</span><span>SMS no Enterprise sob medida</span></div>',
    '<p class="arch-lead">Configure a jornada e deixe a Credituz executar os contatos automaticamente por WhatsApp e e-mail. Você pode usar uma régua como D-3, D0 e D+3 ou definir exatamente quando cada cobrança deve acontecer.</p>\n    <span class="arch-mini">Exemplo de configuração</span>\n    <div class="arch-collection-flow"><span>D-3</span><i>→</i><span>D0</span><i>→</i><span>D+3</span><i>→</i><span>Novos follow-ups</span></div>\n    <div class="arch-badges"><span>WhatsApp</span><span>E-mail</span><span>Até 300 devedores/mês</span><span>Você define quando cobrar</span><span>SMS no Enterprise sob medida</span></div>',
    'home collection section',
)
s = replace_once(
    s,
    '<li>R$ 0,15 por envio</li>',
    '<li><strong>Cobre até 300 devedores por mês</strong></li>',
    'OS pricing card collection limit',
)

p.write_text(s, encoding='utf-8')

# Machine-readable home content
for fname in ['home.md', 'llms-full.txt']:
    fp = Path(fname)
    text = fp.read_text(encoding='utf-8')
    text = replace_once(
        text,
        '- cobrança por **R$ 0,15 por envio**;',
        '- cobrança de até **300 devedores por mês**;',
        f'{fname} OS bullet',
    )
    text = replace_once(
        text,
        'No Credituz OS, a régua de cobrança automatiza contatos em **WhatsApp e e-mail** por **R$ 0,15 por envio**. SMS fica disponível em projetos **Enterprise sob medida**.',
        'No Credituz OS, a régua de cobrança automatiza contatos em **WhatsApp e e-mail** para até **300 devedores por mês**. A operação pode usar uma configuração como **D-3, D0 e D+3** ou definir outros dias e intervalos de cobrança. O limite de devedores é mensal e não cumulativo. SMS fica disponível em projetos **Enterprise sob medida**.',
        f'{fname} collection section',
    )
    text = replace_once(
        text,
        '1. **Credituz OS — R$ 297/mês + R$ 16 por análise**, para até 3 usuários.',
        '1. **Credituz OS — R$ 297/mês + R$ 16 por análise**, para até 3 usuários e cobrança de até 300 devedores por mês.',
        f'{fname} pricing summary',
    )
    fp.write_text(text, encoding='utf-8')

# Structured home JSON
hp = Path('home.json')
data = json.loads(hp.read_text(encoding='utf-8'))
changed = False
for node in data.get('@graph', []):
    if node.get('@type') == 'SoftwareApplication':
        for offer in node.get('offers', []):
            if offer.get('name') == 'Credituz OS':
                offer['description'] = 'R$ 297 por mês mais R$ 16 por análise, para até 3 usuários. Inclui análise de crédito, CRM de crédito e régua de cobrança com IA em WhatsApp e e-mail para até 300 devedores por mês.'
                changed = True
if not changed:
    raise SystemExit('Credituz OS offer not found in home.json')
hp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

# Dedicated collection pages
p = Path('pages/regua-de-cobranca-imobiliaria.html')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    'Automatize cobranças de parcelas imobiliárias por WhatsApp e e-mail com IA. Cada envio custa R$ 0,15. SMS está disponível exclusivamente no Enterprise, sob medida.',
    'Automatize cobranças de parcelas imobiliárias por WhatsApp e e-mail com IA para até 300 devedores por mês. Defina quando cada contato deve acontecer. SMS está disponível exclusivamente no Enterprise, sob medida.',
    'regua meta description',
)
s = replace_once(
    s,
    'A Credituz permite configurar uma régua de cobrança com IA para parcelas de entrada, recebíveis e cobranças recorrentes, com mensagens automáticas por WhatsApp e e-mail por R$ 0,15 por envio. SMS está disponível exclusivamente no Enterprise, sob medida.',
    'A Credituz permite configurar uma régua de cobrança com IA para parcelas de entrada, recebíveis e cobranças recorrentes por WhatsApp e e-mail, cobrindo até 300 devedores por mês. Use uma configuração como D-3, D0 e D+3 ou escolha livremente os dias e intervalos de cada contato. SMS está disponível exclusivamente no Enterprise, sob medida.',
    'regua lead',
)
p.write_text(s, encoding='utf-8')

p = Path('pages/cobranca-e-recebiveis-imobiliarios.html')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    'Automatize a cobrança imobiliária com IA por WhatsApp e e-mail, por R$ 0,15 por envio, além de Pix, boleto, baixa e conciliação. SMS está disponível no Enterprise sob medida.',
    'Automatize a cobrança imobiliária com IA por WhatsApp e e-mail para até 300 devedores por mês, além de Pix, boleto, baixa e conciliação. SMS está disponível no Enterprise sob medida.',
    'collection hub meta',
)
s = replace_once(
    s,
    'Configure uma régua de cobrança com IA por WhatsApp e e-mail. Cada envio custa R$ 0,15. SMS está disponível exclusivamente no Enterprise, sob medida.',
    'Configure uma régua de cobrança com IA por WhatsApp e e-mail para até 300 devedores por mês. Você escolhe quando cobrar e pode usar sequências como D-3, D0 e D+3 ou definir outros momentos. SMS está disponível exclusivamente no Enterprise, sob medida.',
    'collection hub card',
)
p.write_text(s, encoding='utf-8')

# Segment pages
p = Path('pages/construtoras.html')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    'Régua de cobrança com IA em WhatsApp e e-mail para as parcelas da entrada, por R$ 0,15 por envio, com boleto, Pix, baixa e conciliação. SMS está disponível no Enterprise sob medida.',
    'Régua de cobrança com IA em WhatsApp e e-mail para as parcelas da entrada, cobrindo até 300 devedores por mês, com boleto, Pix, baixa e conciliação. A operação define os momentos de cobrança. SMS está disponível no Enterprise sob medida.',
    'construtoras collection copy',
)
p.write_text(s, encoding='utf-8')

p = Path('pages/imobiliarias.html')
s = p.read_text(encoding='utf-8')
s = replace_once(
    s,
    'Régua de cobrança com IA para aluguel e parcelas em WhatsApp e e-mail, por R$ 0,15 por envio, com boleto, Pix, baixa, conciliação, NFe e repasse ao proprietário. SMS está disponível no Enterprise sob medida.',
    'Régua de cobrança com IA para aluguel e parcelas em WhatsApp e e-mail, cobrindo até 300 devedores por mês, com boleto, Pix, baixa, conciliação, NFe e repasse ao proprietário. A operação define os momentos de cobrança. SMS está disponível no Enterprise sob medida.',
    'imobiliarias collection copy',
)
p.write_text(s, encoding='utf-8')

print('Updated Credituz OS collection packaging to 300 debtors/month and configurable schedule')
