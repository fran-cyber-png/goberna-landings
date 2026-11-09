async (page) => {
  await page.setViewportSize({width:1920,height:1080});
  await page.goto('http://127.0.0.1:8765/landing.html?'+Date.now()); await page.waitForTimeout(2500);
  await page.screenshot({path:'C:/Users/Consultoría/Documents/Director-Seguridad/_work/ds1920.png', fullPage:true});
  return await page.evaluate(()=>{const o={}; for (const c of ['ak-hero','ak-bar','ak-met','ak-prog','ak-war','ak-plan','ak-cta','ak-doc','ak-pres','ak-cert','ak-inv','ak-vsec','ak-faq']){const e=document.querySelector('.'+c); const b=e.getBoundingClientRect(); o[c]=[Math.round(b.top+scrollY),Math.round(b.height)];} return o;});
}
