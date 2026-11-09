import sys, json
from playwright.sync_api import sync_playwright
W=int(sys.argv[1]); H=int(sys.argv[2]) if len(sys.argv)>2 else 1080
SEL=json.loads(open('m_sel.json',encoding='utf-8').read())
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':H})
    pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1500)
    r=pg.evaluate('''(S)=>{const o={};for(const [k,s] of Object.entries(S)){const e=document.querySelector(s);if(!e){o[k]=null;continue}const b=e.getBoundingClientRect();o[k]=[Math.round(b.left),Math.round(b.top+scrollY),Math.round(b.width),Math.round(b.height)]}return o}''',SEL)
    for k,v in r.items(): print(k,v)
    b.close()
