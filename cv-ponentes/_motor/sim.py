"""Simula el marcado de Elementor (contenedores flex + widgets) a partir del JSON.
- _generador/sim.html: para medir con verificar.py (imágenes locales de ../imagenes/).
- _generador/<slug>-preview.html: el Artifact (la misma página dentro de un iframe a 1920 / 1366 / 375 + "Ver widgets").
No reemplaza a Elementor (no hay sticky de JS ni estilos del kit), pero lo que se ve es lo que dice el CSS del JSON."""
import base64, html, os

BIB = 'https://grupogoberna.com/wp-content/uploads/2026/10/'
BASE = '''
*,*::before,*::after{box-sizing:border-box}
body{margin:0;font-family:Arial,sans-serif}
.e-con{--gap:0px;display:flex;flex-direction:var(--flex-direction);flex-wrap:nowrap;gap:var(--gap);position:relative;width:100%;max-width:100%;padding:0;min-width:0}
.e-con>.elementor-widget{max-width:100%}
.elementor-widget{position:relative}
.elementor-widget:not(:last-child){margin-bottom:20px}
.elementor-heading-title{padding:0;margin:0;line-height:1}
.elementor-widget-image{text-align:center}
.elementor img{height:auto;max-width:100%;border:none}
'''
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@400&family=Montserrat:wght@400;700;800&family=Open+Sans:wght@400;700&family=Sora:wght@400;700&display=swap">'


def pagina(doc, img):
    root = doc['content'][0]

    def tag(cls, kind):
        ak = ' '.join(c for c in cls.split() if c.startswith('ak-'))
        return f' data-w="{html.escape(kind + (" · " + ak if ak else ""))}"'

    def render(e):
        s = e['settings']
        if e['elType'] == 'container':
            c = s.get('css_classes', '')
            cls = f"elementor-element elementor-element-{e['id']} e-con e-flex {'e-child' if e.get('isInner') else 'e-parent'} {c}"
            st = f"--flex-direction:{s.get('flex_direction', 'column')};"
            if s.get('background_image'):
                st += (f"background-color:{s['background_color']};background-image:url({img(s['background_image']['url'])});"
                       f"background-position:{s['background_position']};background-repeat:no-repeat;background-size:cover;")
            return f'<div class="{cls}" style="{st}"{tag(c, "Contenedor")}>' + ''.join(render(k) for k in e['elements']) + '</div>'
        w = e['widgetType']
        c = s.get('_css_classes', '')
        cls = f"elementor-element elementor-element-{e['id']} elementor-widget elementor-widget-{w} {c}"
        if w == 'heading':
            lv = s.get('header_size', 'h2')
            inner = f'<{lv} class="elementor-heading-title elementor-size-default">{s["title"]}</{lv}>'
        elif w == 'text-editor':
            inner = s['editor']
        elif w == 'image':
            inner = f'<img src="{img(s["image"]["url"])}" alt="{html.escape(s["image"].get("alt", ""))}">'
        nombre = {'heading': 'Título', 'text-editor': 'Texto', 'image': 'Imagen'}.get(w, w)
        return f'<div class="{cls}"{tag(c, nombre)}><div class="elementor-widget-container">{inner}</div></div>'

    css = root['settings']['custom_css'].replace('selector', f".elementor-element-{root['id']}")
    return (f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'{FONTS}<style>{BASE}</style><style>{css}</style></head><body><div class="elementor">{render(root)}</div></body></html>')


WIDGETS_CSS = ('body.show-w [data-w]{outline:1px dashed #e0457b;outline-offset:-1px}'
               'body.show-w [data-w]::after{content:attr(data-w);position:absolute;left:0;top:0;z-index:50;background:#e0457b;color:#fff;'
               'font:600 11px/1.35 Arial,sans-serif;letter-spacing:0;text-transform:none;padding:1px 4px;white-space:nowrap;pointer-events:none}')


def render(P, slug, doc):
    G = os.path.join(P, '_generador')
    local = lambda url: '../imagenes/' + url.replace(BIB, '')
    open(os.path.join(G, 'sim.html'), 'w', encoding='utf-8').write(pagina(doc, local))
    cache = {}
    def data(url):
        f = url.replace(BIB, '')
        if f not in cache:
            cache[f] = 'data:image/webp;base64,' + base64.b64encode(open(os.path.join(P, 'imagenes', f), 'rb').read()).decode()
        return cache[f]
    inner = pagina(doc, data).replace('</style></head>', WIDGETS_CSS + '</style></head>')
    titulo = doc['title']
    prev = PREVIEW.replace('__TITULO__', html.escape(titulo)).replace('__SRCDOC__', html.escape(inner, quote=True))
    out = os.path.join(G, f'{slug}-preview.html')
    open(out, 'w', encoding='utf-8').write(prev)
    print(f'ok sim.html y {slug}-preview.html ({len(prev.encode()) // 1024} KB)')


PREVIEW = '''<title>__TITULO__</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* una sola versión clara, igual que el Figma */
:root{--bg:#f3f6fa;--card:#fff;--fg:#030a22;--muted:#5b646c;--line:#e3e7ee;--gold:#d6a752;color-scheme:light}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 'Open Sans',Arial,sans-serif;padding-block:20px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.bar{display:flex;flex-wrap:wrap;gap:10px 16px;align-items:center;margin-bottom:14px;font-size:13px}
.bar h1{font:600 15px 'Open Sans',Arial,sans-serif;margin:0 auto 0 0}
.bar p{margin:0;color:var(--muted);flex-basis:100%}
.seg{display:flex;gap:6px;flex-wrap:wrap}
button{font:600 13px 'Open Sans',Arial,sans-serif;padding:7px 14px;border:1px solid var(--line);border-radius:6px;background:var(--card);color:var(--fg);cursor:pointer}
button[aria-pressed="true"]{background:var(--gold);border-color:var(--gold);color:#030a22}
button:focus-visible{outline:2px solid var(--gold);outline-offset:2px}
#wrap{position:relative;overflow:hidden;border:1px solid var(--line);background:#fff;margin:0 auto}
#f{border:0;display:block;transform-origin:0 0}
</style>
<div class="bar"><h1>Landing CV · __TITULO__</h1>
<div class="seg" role="group" aria-label="Ancho de pantalla">
<button type="button" data-w="1920" aria-pressed="true">Desktop 1920</button>
<button type="button" data-w="1366" aria-pressed="false">Laptop 1366</button>
<button type="button" data-w="375" aria-pressed="false">Mobile 375</button></div>
<button type="button" id="wb" aria-pressed="false">Ver widgets</button>
<p>Es la misma página que genera el JSON de Elementor, mostrada al ancho elegido (y reducida para que quepa). Las cifras de la derecha quedan fijas al hacer scroll en desktop y laptop (sticky nativo de Elementor; aquí no se simula). Con "Ver widgets" cada recuadro rosa es un contenedor o widget de Elementor con su clase ak-….</p></div>
<div id="wrap"><iframe id="f" title="Vista previa de la landing" srcdoc="__SRCDOC__"></iframe></div>
<script>
const f=document.getElementById('f'),wrap=document.getElementById('wrap');let W=1920;
function fit(){
  const avail=Math.min(wrap.parentElement.clientWidth,W);const s=avail/W;
  f.style.width=W+'px';
  let h=1000;try{h=f.contentDocument.documentElement.scrollHeight}catch(e){}
  f.style.height=h+'px';f.style.transform='scale('+s+')';
  wrap.style.width=(W*s)+'px';wrap.style.height=(h*s)+'px';
}
document.querySelectorAll('.seg button').forEach(b=>b.addEventListener('click',()=>{
  W=+b.dataset.w;document.querySelectorAll('.seg button').forEach(x=>x.setAttribute('aria-pressed',String(x===b)));
  fit();setTimeout(fit,150);setTimeout(fit,600);
}));
document.getElementById('wb').addEventListener('click',e=>{
  try{const on=f.contentDocument.body.classList.toggle('show-w');e.currentTarget.setAttribute('aria-pressed',String(on));}catch(err){}
});
f.addEventListener('load',()=>{fit();try{f.contentDocument.fonts.ready.then(fit)}catch(e){}setTimeout(fit,800)});
window.addEventListener('resize',fit);
</script>
'''
