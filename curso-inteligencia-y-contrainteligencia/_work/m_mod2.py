import sys
from playwright.sync_api import sync_playwright
W=int(sys.argv[1])
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':W,'height':1080})
    pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1000)
    print(pg.evaluate('''()=>{const R=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.top+scrollY),Math.round(b.width),Math.round(b.height)]};
      const d=document.querySelectorAll('.ak-plan-acc details');const o={n:d.length};
      const b0=d[0].querySelector('.ak-mod-body');o.item1=R(d[0]);o.intro=R(b0.querySelector('.ak-mod-intro'));
      const cards=b0.querySelectorAll(':scope > .e-con > .e-con');o.card1=R(cards[0]);o.card2=R(cards[1]);o.item2=R(d[1]);
      o.cardTitle=R(cards[0].querySelector('.elementor-heading-title'));o.cardTxt=R(cards[0].querySelector('p'));return o}'''))
    b.close()
