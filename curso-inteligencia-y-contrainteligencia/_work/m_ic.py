from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1200)
    el=pg.query_selector('.ak-stats-row'); el.scroll_into_view_if_needed(); pg.wait_for_timeout(400); el.screenshot(path='cmp/icons.png'); b.close()
