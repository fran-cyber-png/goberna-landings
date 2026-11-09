# Vista previa del efecto de scroll fijo: header, war room, plan y CTA reales de la página publicada + el efecto
import json, re, base64, urllib.request, sys, os
sys.stdout.reconfigure(encoding='utf-8')
H = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(H, '..', '..', '_artifact_pin')
os.makedirs(OUT, exist_ok=True)
d = json.loads(open(os.path.join(H, 'live_dump.json'), encoding='utf-8').read())
if isinstance(d, str): d = json.loads(d)
css, html = d['css'], d['html']
css = re.sub(r'@font-face\s*\{[^}]*\}', '', css)
html = re.sub(r'<script\b.*?</script>|<noscript>.*?</noscript>', '', html, flags=re.S)
# imágenes incrustadas (el visor bloquea otros dominios)
cache = {}
def data_uri(u):
    if u not in cache:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        try: b = urllib.request.urlopen(req, timeout=60).read()
        except Exception as ex: print('sin', u, ex); cache[u] = u; return u
        mime = {'png': 'image/png', 'webp': 'image/webp', 'jpg': 'image/jpeg', 'jpeg': 'image/jpeg', 'svg': 'image/svg+xml'}[u.rsplit('.', 1)[1].lower()]
        cache[u] = f'data:{mime};base64,' + base64.b64encode(b).decode()
    return cache[u]
IMG = r'https://grupogoberna\.com/wp-content/uploads/[^"\')\s]+\.(?:png|webp|jpe?g|svg)'
css = re.sub(IMG, lambda m: data_uri(m.group(0)), css)
html = re.sub(IMG, lambda m: data_uri(m.group(0)), html)
# envolver la sección de módulos (igual que en el JSON)
m = re.search(r'<div[^>]*class="[^"]*\bak-plan\b[^"]*"[^>]*>', html)
s = m.start(); depth = 0
for t in re.finditer(r'<div\b|</div>', html[s:]):
    depth += 1 if t.group(0) == '<div' else -1
    if depth == 0: e = s + t.end(); break
plan = html[s:e].replace(' id="modulos"', '', 1)
pin_js = open(os.path.join(H, 'pin.js.html'), encoding='utf-8').read()
html = html[:s] + '<div class="ak-plan-pin" id="modulos">' + plan + pin_js + '</div>' + html[e:]
pin_css = open(os.path.join(H, 'pin.css'), encoding='utf-8').read().replace('selector', '.ak-plan-pin')
# header fijo como en la web (el sticky de Elementor es JS): 90 px arriba, 70 px al bajar
hdr = json.load(open(os.path.join(H, '..', '..', 'secciones-director-seguridad', '01-header.json'), encoding='utf-8'))['content'][0]
hcss = hdr['settings']['custom_css'].replace('selector', '.elementor-93575 .elementor-element.elementor-element-13bd66b9')
FONTS = 'https://fonts.googleapis.com/css2?family=Barlow:ital,wght@0,400;0,500;0,600;0,700;0,800;1,400&family=Montserrat:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap'
page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Módulos con scroll fijo</title><link rel="stylesheet" href="{FONTS}">
<style>{css}</style>
<style>{hcss}
.elementor-93575 > .ak-hd {{ position: fixed !important; top: 0; left: 0; right: 0; width: 100% !important; z-index: 99; }}
{pin_css}
html,body{{margin:0}}</style></head>
<body class="{d['body']}">
<div data-elementor-id="93575" class="elementor elementor-93575">{html}</div>
<script>
(function(){{
  // header fijo con un espaciador del alto inicial, como el sticky de Elementor
  var h=document.querySelector('.ak-hd'), sp=document.createElement('div');
  h.parentNode.insertBefore(sp,h);
  function size(){{ var on=h.classList.contains('elementor-sticky--effects'); h.classList.remove('elementor-sticky--effects'); h.style.transition='none'; sp.style.height=h.offsetHeight+'px'; h.offsetHeight; h.style.transition=''; h.classList.toggle('elementor-sticky--effects',on); }}
  function f(){{ h.classList.toggle('elementor-sticky--effects', scrollY>90); }}
  size(); f(); addEventListener('scroll',f,{{passive:true}}); addEventListener('resize',size);
}})();
</script>
</body></html>'''
open(os.path.join(OUT, 'seccion.html'), 'w', encoding='utf-8').write(page)
print(len(page), len(cache))
