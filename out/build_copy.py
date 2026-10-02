import html, json, importlib.util, sys
spec=importlib.util.spec_from_file_location("b","build.py"); b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)
e=html.escape
secs=[("m%d"%i,t,l,None) for i,(t,l) in enumerate(b.main)]+[("s"+n,t,l,n) for n,t,l in b.sub]
def row(x):
    if isinstance(x,tuple): lab,txt=x; return f'<li><span class="r"><b>{e(lab)}:</b> {e(txt)}</span><button type="button" data-t="{e(txt)}">نسخ</button></li>'
    return f'<li><span class="r">{e(x)}</span><button type="button" data-t="{e(x)}">نسخ</button></li>'
nav="".join(f'<a href="#{i}">{(n+") " if n else "")}{e(t)}</a>' for i,t,l,n in secs)
body="".join(f'<section id="{i}"><h2>{(f"<span>{n}</span>" if n else "")}{e(t)}</h2><ul>{"".join(row(x) for x in l)}</ul></section>' for i,t,l,n in secs)
page=f'''<title>ردود Mega Furniture</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Arabic:wght@400;600;700&display=swap">
<style>
/* single column of reply rows, each with its own copy button */
:root{{--bg:#fbfaf8;--fg:#17140f;--mut:#5d564c;--card:#fff;--line:#e4ded4;--acc:#c2410c;--accfg:#fff;--ok:#15803d;font-family:"IBM Plex Sans Arabic",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16130f;--fg:#f3efe8;--mut:#b3aa9c;--card:#201c16;--line:#3a342b;--acc:#fb923c;--accfg:#1a1208;--ok:#4ade80;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#16130f;--fg:#f3efe8;--mut:#b3aa9c;--card:#201c16;--line:#3a342b;--acc:#fb923c;--accfg:#1a1208;--ok:#4ade80;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);padding-inline:16px;padding-block:20px 60px;font-size:17px;line-height:1.8}}
main{{max-width:760px;margin-inline:auto}}
h1{{font-size:1.7rem;margin:0;text-wrap:balance}}
.sub{{color:var(--mut);margin:4px 0 16px}}
#q{{width:100%;box-sizing:border-box;font:inherit;padding:10px 14px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg)}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin-block:16px 8px}}
nav a{{font-size:.85rem;font-weight:600;color:var(--fg);text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:2px 12px}}
nav a:hover{{border-color:var(--acc);color:var(--acc)}}
section{{margin-top:28px;scroll-margin-top:12px}}
h2{{font-size:1.3rem;font-weight:700;margin:0 0 10px;padding-bottom:4px;border-bottom:2px solid var(--acc);display:flex;gap:10px;align-items:baseline}}
h2 span{{color:var(--acc)}}
ul{{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:12px}}
li{{display:flex;gap:12px;align-items:center;justify-content:space-between;background:var(--card);border:1px solid var(--line);border-radius:8px;padding:8px 14px}}
.r{{min-width:0;font-weight:600;user-select:text}}
.r b{{color:var(--acc)}}
button{{flex:none;font:inherit;font-size:.85rem;font-weight:700;cursor:pointer;border:1px solid var(--acc);background:transparent;color:var(--acc);border-radius:6px;padding:2px 14px}}
button:hover,button:focus-visible{{background:var(--acc);color:var(--accfg);outline:none}}
button.done{{background:var(--ok);border-color:var(--ok);color:var(--accfg)}}
li[hidden],section[hidden]{{display:none!important}}
@media(max-width:480px){{li{{flex-direction:column;align-items:stretch}}button{{align-self:flex-start}}}}
</style>
<main dir="rtl" lang="ar">
<h1>مكتبة ردود جاهزة للرسائل - Mega Furniture</h1>
<p class="sub">اضغط "نسخ" جنب أي رد وهيتنسخ بالعربي صح، جاهز للصق.</p>
<input id="q" type="search" placeholder="دوّر على رد..." aria-label="بحث في الردود">
<nav>{nav}</nav>
{body}
</main>
<script>
function fallback(t,btn){{var s=document.createElement('textarea');s.value=t;s.style.position='fixed';s.style.opacity='0';document.body.appendChild(s);s.select();var ok=false;try{{ok=document.execCommand('copy')}}catch(e){{}}document.body.removeChild(s);return ok}}
document.addEventListener('click',function(ev){{
 var b=ev.target.closest('button[data-t]');if(!b)return;var t=b.dataset.t;
 function mark(ok){{b.textContent=ok?'تم النسخ':'اتحدد النص، انسخه يدوي';b.classList.toggle('done',ok);setTimeout(function(){{b.textContent='نسخ';b.classList.remove('done')}},1400)}}
 if(navigator.clipboard&&navigator.clipboard.writeText){{navigator.clipboard.writeText(t).then(function(){{mark(true)}},function(){{mark(fallback(t))}})}}else mark(fallback(t));
}});
document.getElementById('q').addEventListener('input',function(e){{
 var v=e.target.value.trim();
 document.querySelectorAll('section').forEach(function(s){{var any=false;s.querySelectorAll('li').forEach(function(li){{var m=!v||li.textContent.indexOf(v)>-1;li.hidden=!m;if(m)any=true}});s.hidden=!any}})
}});
</script>'''
open("copy_page.html","w",encoding="utf-8").write(page)
txt="\n\n".join(f"## {t}\n\n"+"\n\n".join((x[0]+": "+x[1]) if isinstance(x,tuple) else x for x in l) for i,t,l,n in secs)
open("Mega_Furniture_Replies.txt","w",encoding="utf-8").write(txt+"\n")
