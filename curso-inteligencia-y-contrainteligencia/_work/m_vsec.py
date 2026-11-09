from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (1920,375):
        pg=b.new_page(viewport={'width':w,'height':1000}); pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1000)
        e=pg.query_selector('.ak-vsec'); e.scroll_into_view_if_needed(); pg.wait_for_timeout(300); e.screenshot(path='cmp/vsec%d.png'%w)
        print(w, pg.evaluate("()=>[document.querySelectorAll('.ak-vt').length, document.querySelector('.ak-vsec').getBoundingClientRect().height|0]"))
        pg.close()
    b.close()
