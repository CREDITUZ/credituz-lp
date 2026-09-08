from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')
needle = '.arch-faq{background:#fff}'
replacement = '.arch-faq{background:#fff}.arch-faq .faq-q{background:transparent!important;border-radius:0!important;padding-left:0!important;padding-right:0!important;box-shadow:none!important}.arch-faq .faq-q:hover,.arch-faq .faq-item.open .faq-q{background:transparent!important}'
if needle not in s:
    raise SystemExit('arch-faq style target not found')
s = s.replace(needle, replacement, 1)
p.write_text(s, encoding='utf-8')
print('FAQ gray question backgrounds removed')
