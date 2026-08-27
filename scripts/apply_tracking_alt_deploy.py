from pathlib import Path
import re

# ---------- Home ----------
p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Add alt="" only to img tags that have no alt attribute at all.
def ensure_alt(match):
    tag = match.group(0)
    if re.search(r'\balt\s*=', tag, flags=re.I):
        return tag
    return tag[:-1] + ' alt="">' if tag.endswith('>') else tag
s = re.sub(r'<img\b[^>]*>', ensure_alt, s, flags=re.I)

# Replace the existing attribution helper block to preserve paid-media parameters.
start = s.find('    var DEFAULT_REF = "saas-credituzai";')
if start != -1:
    end_marker = '    applyRef();'
    end = s.find(end_marker, start)
    if end != -1:
        end = end + len(end_marker)
        new_block = '''    var DEFAULT_REF = "saas-credituzai";
    var MAX_LEN = 64;
    var DASH_BASE = "https://dashboard.usecredituz.com/auth/login?screen_hint=signup";
    var ATTR_KEYS = ["utm_source","utm_medium","utm_campaign","utm_content","utm_term","gclid","fbclid","msclkid"];

    function safe(v, maxLen) {
        if (v == null) return "";
        return String(v).replace(/[<>\"']/g, "").slice(0, maxLen || 180);
    }
    function resolveRef() {
        var params = new URLSearchParams(window.location.search);
        var raw = params.get("ref");
        if (raw == null) return DEFAULT_REF;
        var clean = raw.replace(/[^A-Za-z0-9-]/g, "");
        if (clean.length > MAX_LEN) clean = clean.slice(0, MAX_LEN);
        return clean.length ? clean : DEFAULT_REF;
    }
    function attribution() {
        var params = new URLSearchParams(window.location.search), out = {};
        ATTR_KEYS.forEach(function(k){ var v = safe(params.get(k)); if(v) out[k] = v; });
        try {
            var saved = JSON.parse(sessionStorage.getItem("credituz_attribution") || "{}");
            Object.keys(saved).forEach(function(k){ if(!out[k]) out[k] = saved[k]; });
            sessionStorage.setItem("credituz_attribution", JSON.stringify(out));
        } catch(e) {}
        return out;
    }
    var REF = resolveRef();
    var ATTR = attribution();
    function dashboardUrl() {
        var u = new URL(DASH_BASE);
        u.searchParams.set("ref", REF);
        Object.keys(ATTR).forEach(function(k){u.searchParams.set(k, ATTR[k]);});
        return u.toString();
    }
    function applyRef(root) {
        var scope = root || document;
        var links = scope.querySelectorAll('a[href^="https://dashboard.usecredituz.com"]');
        for (var i = 0; i < links.length; i++) links[i].setAttribute("href", dashboardUrl());
    }
    applyRef();'''
        s = s[:start] + new_block + s[end:]

# Add explicit marketing event layer once.
if 'event: "marketing_cta_click"' not in s:
    tracking = '''\n<script id="credituz-marketing-events">\n(function(){\n  function attrs(){try{return JSON.parse(sessionStorage.getItem('credituz_attribution')||'{}')}catch(e){return {}}}\n  function push(name, params){\n    window.dataLayer=window.dataLayer||[];\n    var payload=Object.assign({event:name,page_path:location.pathname,page_title:document.title},attrs(),params||{});\n    window.dataLayer.push(payload);\n    if(window.fbq && window.credituzConsent && window.credituzConsent.ler && window.credituzConsent.ler()==='all'){\n      try{window.fbq('trackCustom', name, payload)}catch(e){}\n    }\n  }\n  document.addEventListener('click',function(e){\n    var el=e.target.closest('[data-track],a[href^="https://dashboard.usecredituz.com"],a[href^="https://wa.me/"]');\n    if(!el)return;\n    var href=el.getAttribute('href')||'';\n    var label=el.getAttribute('data-track')||'unlabeled_cta';\n    push('marketing_cta_click',{cta_id:label,cta_text:(el.textContent||'').trim().slice(0,120),destination:href.slice(0,500)});\n    if(href.indexOf('dashboard.usecredituz.com')>-1){\n      push('signup_start',{cta_id:label,product:label.indexOf('score')>-1?'credituz_score':'credituz_os'});\n      if(window.fbq && window.credituzConsent && window.credituzConsent.ler && window.credituzConsent.ler()==='all'){try{window.fbq('track','InitiateCheckout',{content_name:label})}catch(e){}}\n    } else if(href.indexOf('wa.me/')>-1){\n      push('contact_start',{cta_id:label,channel:'whatsapp'});\n      if(window.fbq && window.credituzConsent && window.credituzConsent.ler && window.credituzConsent.ler()==='all'){try{window.fbq('track','Contact',{content_name:label})}catch(e){}}\n    }\n  },true);\n  push('landing_view',{ref:(new URLSearchParams(location.search)).get('ref')||'saas-credituzai'});\n})();\n</script>\n'''
    s = s.replace('</body>', tracking + '</body>')

# Ensure the untracked finance WhatsApp CTA has an id.
s = s.replace('class="fin-wa" href="https://wa.me/5511936209409"', 'class="fin-wa" href="https://wa.me/5511936209409" data-track="cta_financeiro_whatsapp"')
p.write_text(s, encoding='utf-8')

# ---------- Credituz Score ----------
p = Path('pages/credituz-score.html')
s = p.read_text(encoding='utf-8')
# Track primary and secondary CTAs.
s = s.replace('class="btn" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=credituz-score"', 'class="btn" data-track="score_buy_primary" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=credituz-score"', 1)
s = s.replace('class="btn secondary" href="#exemplo"', 'class="btn secondary" data-track="score_view_example" href="#exemplo"', 1)
# Last purchase CTA if still untracked.
s = s.replace('class="btn" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=credituz-score"', 'class="btn" data-track="score_buy_final" href="https://dashboard.usecredituz.com/auth/login?screen_hint=signup&ref=credituz-score"')

if 'id="credituz-score-tracking"' not in s:
    score_tracking = '''\n<script id="credituz-score-tracking">\n(function(w,d){\n  var consent=false;try{consent=localStorage.getItem('credituz_consent')==='all'}catch(e){}\n  w.dataLayer=w.dataLayer||[];function gtag(){w.dataLayer.push(arguments)}\n  gtag('consent','default',{ad_storage:consent?'granted':'denied',ad_user_data:consent?'granted':'denied',ad_personalization:consent?'granted':'denied',analytics_storage:consent?'granted':'denied',functionality_storage:'granted',security_storage:'granted'});\n  ['GTM-KN3GQNDJ','GTM-T2M9N4CR'].forEach(function(id){w.dataLayer.push({'gtm.start':Date.now(),event:'gtm.js'});var f=d.getElementsByTagName('script')[0],j=d.createElement('script');j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+id;f.parentNode.insertBefore(j,f)});\n  !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(w,d,'script','https://connect.facebook.net/en_US/fbevents.js');\n  if(!consent)w.fbq('consent','revoke');w.fbq('init','3261631577333056');w.fbq('track','PageView');\n  var keys=['utm_source','utm_medium','utm_campaign','utm_content','utm_term','gclid','fbclid','msclkid'];var q=new URLSearchParams(location.search),attr={};keys.forEach(function(k){var v=q.get(k);if(v)attr[k]=v.slice(0,180)});try{var prev=JSON.parse(sessionStorage.getItem('credituz_attribution')||'{}');Object.keys(prev).forEach(function(k){if(!attr[k])attr[k]=prev[k]});sessionStorage.setItem('credituz_attribution',JSON.stringify(attr))}catch(e){}\n  document.querySelectorAll('a[href^="https://dashboard.usecredituz.com"]').forEach(function(a){var u=new URL(a.href);Object.keys(attr).forEach(function(k){u.searchParams.set(k,attr[k])});a.href=u.toString()});\n  function emit(name,p){var x=Object.assign({event:name,page_path:location.pathname,page_title:document.title,product:'credituz_score'},attr,p||{});w.dataLayer.push(x);if(consent&&w.fbq)try{w.fbq('trackCustom',name,x)}catch(e){}}\n  d.addEventListener('click',function(e){var a=e.target.closest('[data-track]');if(!a)return;var id=a.getAttribute('data-track');emit('marketing_cta_click',{cta_id:id,cta_text:(a.textContent||'').trim().slice(0,120)});if(id.indexOf('score_buy')===0){emit('signup_start',{cta_id:id});if(consent&&w.fbq)try{w.fbq('track','InitiateCheckout',{value:27.70,currency:'BRL',content_name:'Credituz Score'})}catch(e){}}},true);\n  emit('landing_view',{ref:'credituz-score'});\n})(window,document);\n</script>\n'''
    s = s.replace('</head>', score_tracking + '</head>')
p.write_text(s, encoding='utf-8')
