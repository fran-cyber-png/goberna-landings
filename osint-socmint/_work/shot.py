# Captura la vista previa a un ancho dado: python shot.py archivo.html ancho salida.png
import sys, os
from playwright.sync_api import sync_playwright
f, w, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
H = int(sys.argv[4]) if len(sys.argv) > 4 else 900
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': H})
    pg.goto('http://127.0.0.1:8791/' + f, wait_until='networkidle'); pg.wait_for_timeout(2000)
    pg.add_style_tag(content='html{scrollbar-width:none}')
    # carga diferida
    h = pg.evaluate('document.body.scrollHeight')
    for y in range(0, h, 800): pg.evaluate(f'window.scrollTo(0,{y})'); pg.wait_for_timeout(60)
    pg.evaluate('window.scrollTo(0,0)'); pg.wait_for_timeout(800)
    pg.screenshot(path=out, full_page=True)
    print(pg.evaluate('''() => {const o={}; for (const c of ['ak-hd','ak-hero','ak-bar','ak-met','ak-prog','ak-war','ak-plan','ak-cta','ak-doc','ak-pres','ak-cert','ak-inv','ak-vsec','ak-faq']){const e=document.querySelector('.'+c); if(!e) continue; const r=e.getBoundingClientRect(); o[c]=[Math.round(r.top+scrollY),Math.round(r.height)];} return o;}'''))
    b.close()
