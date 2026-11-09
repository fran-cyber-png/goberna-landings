# Captura la página publicada de Director de Seguridad: HTML completo + todo el CSS aplicado
import json, os, sys
from playwright.sync_api import sync_playwright
W = os.path.dirname(os.path.abspath(__file__))
URL = 'https://grupogoberna.com/diploma-de-elite-internacional-de-seguridad/'
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    pg.goto(URL, wait_until='networkidle', timeout=120000)
    html = pg.content()
    css = pg.evaluate(open(os.path.join(W, 'snap.js'), encoding='utf-8').read())
    body = pg.evaluate('document.body.className')
    json.dump({'html': html, 'css': css, 'bodyClass': body}, open(os.path.join(W, 'snap.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print(len(html), len(css), body[:200])
    b.close()
