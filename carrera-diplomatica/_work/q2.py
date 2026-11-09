# Igual que q.py pero con alto de ventana: python q2.py archivo.html ancho alto "sel" ...
import sys
from playwright.sync_api import sync_playwright
f, w, h, sels = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': h})
    pg.goto('http://127.0.0.1:8790/' + f, wait_until='networkidle'); pg.wait_for_timeout(1200)
    for s in sels:
        r = pg.evaluate('''(s) => [...document.querySelectorAll(s)].slice(0,12).map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]; })''', s)
        print(s, r)
    b.close()
