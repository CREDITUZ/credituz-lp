from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_css = ".arch-case{background:#fff}.arch-case-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:38px;align-items:center}.arch-case blockquote{margin:0;padding:30px;border-radius:22px;background:var(--paper-warm);font-size:21px;line-height:1.5}.arch-case blockquote footer{font-size:13px;color:var(--gray-2);margin-top:16px}.arch-case blockquote a{display:inline-block;margin-top:12px;font-size:14px;color:var(--lime);text-decoration:none;font-weight:700}.arch-pricing"
new_css = ".arch-case{background:#fff}.arch-case-grid{display:grid;grid-template-columns:.8fr 1.2fr;gap:38px;align-items:center}.arch-case blockquote{margin:0;padding:30px;border-radius:24px;background:linear-gradient(180deg,#f7f7f9 0%,#f2f3f5 100%);border:1px solid #e7e8eb;box-shadow:0 18px 45px rgba(29,29,31,.06);font-size:21px;line-height:1.5}.arch-case-meta{margin-top:24px;padding:16px 18px;background:#fff;border:1px solid #e4e6ea;border-radius:16px;display:flex;align-items:center;justify-content:space-between;gap:18px;box-shadow:0 8px 24px rgba(29,29,31,.04)}.arch-case-person{display:flex;align-items:center;gap:12px;min-width:0}.arch-case-avatar{width:42px;height:42px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;flex:0 0 auto;background:var(--accent-soft);color:var(--lime-deep);font-size:13px;font-weight:800;letter-spacing:.02em}.arch-case-person-copy{display:flex;flex-direction:column;min-width:0}.arch-case-person-copy strong{font-size:15px;line-height:1.25}.arch-case-person-copy span{margin-top:3px;font-size:13px;color:var(--gray-2);line-height:1.35}.arch-case-link{display:inline-flex;align-items:center;white-space:nowrap;font-size:14px;color:var(--lime);text-decoration:none;font-weight:750}.arch-case-link:hover{text-decoration:underline}@media(max-width:720px){.arch-case-meta{align-items:flex-start;flex-direction:column}.arch-case-link{white-space:normal}}.arch-pricing"
if old_css not in s:
    raise SystemExit('target case CSS not found')
s = s.replace(old_css, new_css, 1)

old_html = '<blockquote>“Saímos de uma situação de baixo controle para o <strong>controle total da nossa carteira</strong>. Hoje sabemos exatamente o status de cada unidade, cada contrato e cada repasse.”<footer>Adson Soares · Gestor de Incorporação · NJS Engenharia</footer><a href="./pages/cases/njs-engenharia-credituz.html">Ver case completo →</a></blockquote>'
new_html = '<blockquote>“Saímos de uma situação de baixo controle para o <strong>controle total da nossa carteira</strong>. Hoje sabemos exatamente o status de cada unidade, cada contrato e cada repasse.”<div class="arch-case-meta"><div class="arch-case-person"><span class="arch-case-avatar" aria-hidden="true">AS</span><div class="arch-case-person-copy"><strong>Adson Soares</strong><span>Gestor de Incorporação · NJS Engenharia</span></div></div><a class="arch-case-link" href="./pages/cases/njs-engenharia-credituz.html">Ver case completo →</a></div></blockquote>'
if old_html not in s:
    raise SystemExit('target case HTML not found')
s = s.replace(old_html, new_html, 1)

p.write_text(s, encoding='utf-8')
print('Adson case card visual fixed')
