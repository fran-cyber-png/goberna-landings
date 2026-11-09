async () => {
  const A = await (await fetch('anchors.json')).json();
  const norm = s => s.replace(/\s+/g,' ').trim().toLowerCase();
  const cands = [...document.querySelectorAll('.elementor-heading-title, .elementor-widget-text-editor p, .elementor-widget-text-editor li, .elementor-button-text, .e-n-tab-title-text, .e-n-accordion-item-title-text, label, .elementor-widget-text-editor .elementor-widget-container')];
  const used = new Set(); const rows = [];
  for (const a of A) {
    const t = norm(a.t); if (t.length < 2) continue;
    let best = null;
    for (const el of cands) { if (used.has(el)) continue; const et = norm(el.textContent); if (et === t || (t.length > 25 && et.startsWith(t.slice(0, 25)))) { const r = el.getBoundingClientRect(); if (r.width === 0) continue; best = el; break; } }
    if (!best) { rows.push([a.id, a.t.slice(0, 38), a.y, null]); continue; }
    used.add(best);
    const r = best.getBoundingClientRect(); const cs = getComputedStyle(best);
    rows.push([a.id, a.t.slice(0, 38), a.x, Math.round(r.left), a.y, Math.round(r.top + scrollY), Math.round(r.top + scrollY - a.y), a.h, Math.round(r.height), a.fs, parseFloat(cs.fontSize), a.lh, cs.lineHeight]);
  }
  return rows;
}
