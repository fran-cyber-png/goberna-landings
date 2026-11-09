import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':900})
    r=pg.goto(url,wait_until='domcontentloaded',timeout=90000); pg.wait_for_timeout(6000)
    print('status', r.status, pg.url, pg.title())
    print(pg.evaluate("""()=>{const a=[...document.querySelectorAll('[class*="ak-"]')].slice(0,15).map(e=>[...e.classList].filter(c=>c.startsWith('ak-')).join(' '));
      const el=[...document.querySelectorAll('[data-elementor-id]')].map(e=>e.getAttribute('data-elementor-type')+':'+e.getAttribute('data-elementor-id'));
      return {ak:a, docs:el, body:document.body.className.slice(0,300)}}"""))
    pg.screenshot(path='cmp/live_top.png')
    b.close()
