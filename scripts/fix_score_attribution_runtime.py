from pathlib import Path
p=Path('pages/credituz-score.html')
s=p.read_text(encoding='utf-8')
old='''  document.querySelectorAll('a[href^="https://dashboard.usecredituz.com"]').forEach(function(a){var u=new URL(a.href);Object.keys(attr).forEach(function(k){u.searchParams.set(k,attr[k])});a.href=u.toString()});
  function emit(name,p){'''
new='''  function applyAttribution(root){(root||d).querySelectorAll('a[href^="https://dashboard.usecredituz.com"]').forEach(function(a){var u=new URL(a.href);Object.keys(attr).forEach(function(k){u.searchParams.set(k,attr[k])});a.href=u.toString()})}
  if(d.readyState==='loading')d.addEventListener('DOMContentLoaded',function(){applyAttribution(d)},{once:true});else applyAttribution(d);
  d.addEventListener('click',function(e){var link=e.target&&e.target.closest?e.target.closest('a[href^="https://dashboard.usecredituz.com"]'):null;if(link){var u=new URL(link.href);Object.keys(attr).forEach(function(k){u.searchParams.set(k,attr[k])});link.href=u.toString()}},true);
  function emit(name,p){'''
if old not in s: raise SystemExit('score attribution marker not found')
s=s.replace(old,new,1)
p.write_text(s,encoding='utf-8')
