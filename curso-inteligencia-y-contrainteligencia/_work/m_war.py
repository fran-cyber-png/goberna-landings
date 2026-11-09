import sys
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':int(sys.argv[1]),'height':1000})
    pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1200)
    print(pg.evaluate('''()=>{const o=[];for(const id of ['7a82957e','245ad6bc','15766917']){const e=document.querySelector('.elementor-element-'+id);const t=e.querySelector('.elementor-heading-title');const cs=getComputedStyle(t);const r=e.getBoundingClientRect();const n=e.nextElementSibling;const rn=n?n.getBoundingClientRect():null;
      o.push([id,Math.round(r.top+scrollY),Math.round(r.height),cs.fontSize,cs.lineHeight,getComputedStyle(e).marginBottom, getComputedStyle(e.querySelector('.elementor-widget-container')).margin, rn?Math.round(rn.top+scrollY):null]);}return o}'''))
    b.close()
