from pathlib import Path

p=Path('index.html')
s=p.read_text(encoding='utf-8')
old='''    applyRef();
    }

    // Rede de seguranca: garante o ref correto tambem em cliques (links tardios/dinamicos)
    document.addEventListener("click", function (e) {
        var a = e.target && e.target.closest ? e.target.closest('a[href^="https://dashboard.usecredituz.com"]') : null;
        if (a) a.setAttribute("href", DASH_URL);
    }, true);

    // Exposto para reuso por outros scripts, se necessario
    window.credituzDashboardUrl = function () { return DASH_URL; };
    window.credituzRef = function () { return REF; };
})();'''
new='''    applyRef();

    // Rede de seguranca: garante atribuicao/ref tambem em links tardios ou dinamicos.
    document.addEventListener("click", function (e) {
        var a = e.target && e.target.closest ? e.target.closest('a[href^="https://dashboard.usecredituz.com"]') : null;
        if (a) a.setAttribute("href", dashboardUrl());
    }, true);

    // Exposto para reuso por outros scripts.
    window.credituzDashboardUrl = function () { return dashboardUrl(); };
    window.credituzRef = function () { return REF; };
})();'''
if old not in s:
    raise SystemExit('target legacy block not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')

# Add syntax validation to deploy before publishing.
p=Path('.github/workflows/deploy.yml')
y=p.read_text(encoding='utf-8')
needle='''      - name: Configure Pages
        uses: actions/configure-pages@v5
'''
insert='''      - name: Validate inline JavaScript syntax
        run: |
          python3 - <<'PY'
          from pathlib import Path
          import re
          s=Path('index.html').read_text(encoding='utf-8')
          scripts=re.findall(r'<script(?![^>]*type=["\\\']application/ld\\+json["\\\'])[^>]*>(.*?)</script>',s,re.I|re.S)
          Path('/tmp/inline-js').mkdir(exist_ok=True)
          for i,x in enumerate(scripts,1):
              (Path('/tmp/inline-js')/f'{i:02d}.js').write_text(x,encoding='utf-8')
          PY
          for f in /tmp/inline-js/*.js; do node --check "$f"; done
      - name: Configure Pages
        uses: actions/configure-pages@v5
'''
if 'Validate inline JavaScript syntax' not in y:
    if needle not in y: raise SystemExit('deploy insertion marker not found')
    y=y.replace(needle,insert,1)
y=y.replace("node-version: '20'","node-version: '24'")
p.write_text(y,encoding='utf-8')
