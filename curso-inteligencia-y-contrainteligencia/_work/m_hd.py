from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for W in (1366,1440,1280,1025):
        pg=b.new_page(viewport={'width':W,'height':800})
        pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(800)
        print(W, pg.evaluate('''()=>{const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.right)]};
          const a=[...document.querySelectorAll('.ak-hd-nav .elementor-nav-menu--main > ul > li > a, .ak-hd-nav nav.elementor-nav-menu--main a.elementor-item')].map(r);
          const nav=document.querySelector('.ak-hd-nav'); const cta=document.querySelector('.ak-hd-cta .elementor-button');
          const s=getComputedStyle(document.querySelector('.ak-hd-nav a.elementor-item'));
          return {nav:r(nav),items:a.slice(0,7),cta:r(cta),pad:s.paddingLeft+' '+s.paddingRight,fs:s.fontSize,ls:s.letterSpacing}}'''))
        pg.close()
    b.close()
