import sys
from playwright.sync_api import sync_playwright
url=sys.argv[1]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1920,'height':900})
    pg.goto(url,wait_until='domcontentloaded',timeout=90000); pg.wait_for_timeout(5000)
    print(pg.evaluate("""()=>{const out={vw:innerWidth, docW:document.documentElement.clientWidth};
      const sec=document.querySelector('.ak-prog')||document.querySelector('.ak-war');
      if(!sec) return out;
      const r=e=>{const b=e.getBoundingClientRect();return [Math.round(b.left),Math.round(b.right)]};
      out.sec=r(sec); out.chain=[];
      let e=sec.parentElement;
      while(e && e!==document.documentElement){const cs=getComputedStyle(e);
        out.chain.push([e.tagName.toLowerCase()+'.'+[...e.classList].slice(0,3).join('.'), r(e), cs.paddingLeft, cs.marginLeft, cs.maxWidth]); e=e.parentElement;}
      return out}"""))
    b.close()
