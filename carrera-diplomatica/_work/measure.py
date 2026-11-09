# Mide elementos clave de una vista previa: python measure.py archivo.html ancho
import sys, json
from playwright.sync_api import sync_playwright
f, w = sys.argv[1], int(sys.argv[2])
JS = open('measure.js', encoding='utf-8').read()
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': w, 'height': 900})
    pg.goto('http://127.0.0.1:8790/' + f, wait_until='networkidle'); pg.wait_for_timeout(1500)
    print(json.dumps(pg.evaluate(JS), ensure_ascii=False))
    b.close()
