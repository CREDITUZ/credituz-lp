from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
old = '<h1 class="hero-title" id="heroTitle">Análise crédito, cobrança e financiamento com <em>agentes de IA.</em></h1>'
new = '<h1 class="hero-title" id="heroTitle">Análise de crédito, cobrança e financiamento com <em>agentes de IA.</em></h1>'
if old not in s:
    raise SystemExit('hero title to replace was not found')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')
print('hero title corrected')
