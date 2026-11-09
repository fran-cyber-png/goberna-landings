# Mide posiciones (relativas a la página) de selectores en la vista previa. Uso: python measure.py ancho alto
import sys, json
from playwright.sync_api import sync_playwright
w, h = int(sys.argv[1]), int(sys.argv[2])
SEL = json.loads(open('measure_sel.json', encoding='utf-8').read())
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h})
    pg.goto('http://127.0.0.1:8791/landing.html', wait_until='networkidle'); pg.wait_for_timeout(1500)
    r = pg.evaluate('''(S) => { const o = {}; for (const [k, s] of Object.entries(S)) { const e = document.querySelector(s); if (!e) { o[k] = null; continue; }
        const b = e.getBoundingClientRect(); o[k] = [Math.round(b.left), Math.round(b.top + scrollY), Math.round(b.width), Math.round(b.height)]; } return o; }''', SEL)
    for k, v in r.items(): print(k, v)
    b.close()
