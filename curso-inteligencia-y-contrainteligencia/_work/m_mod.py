from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':1080})
    pg.goto('http://127.0.0.1:8790/landing.html',wait_until='networkidle'); pg.wait_for_timeout(1000)
    print(pg.evaluate('''()=>{const e=document.querySelector('.ak-mod-intro');const t=document.querySelector('.ak-plan-acc details[open] .e-n-accordion-item-title-header');
      return [getComputedStyle(e).marginTop, Math.round(e.getBoundingClientRect().top+scrollY), Math.round(t.getBoundingClientRect().bottom+scrollY)]}'''))
    b.close()
