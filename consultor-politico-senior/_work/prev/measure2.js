async (W) => {
  // Compara cada texto del Figma (anchors.json) con su elemento en la vista previa, relativo al inicio de su sección.
  const A = await (await fetch('anchors.json')).json();
  const F = [['ak-hero', 90, 879], ['ak-bar', 856, 180], ['ak-met', 1036, 791], ['ak-prog', 1827, 717], ['ak-war', 2544, 1027], ['ak-pf', 3571, 340],
             ['ak-plan', 3911, 956], ['ak-cta', 4867, 447], ['ak-ponente', 5314, 1027], ['ak-pres', 6341, 867], ['ak-cert', 7208, 1056],
             ['ak-inv', 8264, 941], ['ak-faq', 9205, 780]];
  const scale = W ? W / 1920 : 1;
  const sec = {}; for (const [c] of F) { const e = document.querySelector('.' + c); if (e) { const r = e.getBoundingClientRect(); sec[c] = { top: r.top + scrollY, h: r.height }; } }
  // la barra: medir desde su caja blanca
  const bb = document.querySelector('.ak-bar .e-con-inner > .e-con, .ak-bar > .e-con-inner > .e-con'); if (bb) { const r = bb.getBoundingClientRect(); sec['ak-bar'] = { top: r.top + scrollY, h: r.height }; }
  const norm = s => s.replace(/\s+/g, ' ').trim().toLowerCase();
  const cands = [...document.querySelectorAll('.elementor-heading-title, .elementor-widget-text-editor p, .elementor-widget-text-editor li, .elementor-button-text, .e-n-tab-title-text, .e-n-accordion-item-title-text, label')];
  const used = new Set(); const rows = [];
  for (const [c, fy, fh] of F) rows.push(['##', c, 'figma h', fh * scale, 'web h', sec[c] ? Math.round(sec[c].h) : null, 'dh', sec[c] ? Math.round(sec[c].h - fh * scale) : null]);
  for (const a of A) {
    const t = norm(a.t); if (t.length < 3) continue;
    const s = F.find(([c, fy, fh]) => a.y >= fy && a.y < fy + fh); if (!s || !sec[s[0]]) continue;
    let best = null;
    for (const el of cands) { if (used.has(el)) continue; const r = el.getBoundingClientRect(); if (!r.width) continue; const et = norm(el.textContent); if (et === t || (t.length > 25 && et.startsWith(t.slice(0, 25)))) { best = el; break; } }
    if (!best) continue; used.add(best);
    const r = best.getBoundingClientRect(); const cs = getComputedStyle(best);
    const fcy = (a.y - s[1] + a.h / 2) * scale, wcy = r.top + scrollY - sec[s[0]].top + r.height / 2;
    rows.push([s[0], a.id, a.t.slice(0, 34), 'dy', Math.round(wcy - fcy), 'dx', Math.round(r.left - a.x * scale), 'h', Math.round(a.h * scale), Math.round(r.height), 'fs', +(a.fs * scale).toFixed(1), parseFloat(cs.fontSize)]);
  }
  return rows.map(r => r.join(' ')).join('\n');
}
