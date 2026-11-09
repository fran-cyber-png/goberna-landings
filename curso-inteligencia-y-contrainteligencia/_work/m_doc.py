from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1500)
    el=pg.query_selector('.ak-doc'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(500)
    print(pg.evaluate("()=>[...document.querySelectorAll('.ak-doc .swiper-slide')].map(s=>s.innerText.split(String.fromCharCode(10)).filter(Boolean).slice(0,2).join(' | '))"))
    print('puntos', pg.evaluate("()=>document.querySelectorAll('.ak-doc .swiper-pagination-bullet').length"))
    pg.click('.ak-doc .elementor-swiper-button-next'); pg.wait_for_timeout(1200)
    el.screenshot(path='cmp/doc_next.png')
    b.close()
