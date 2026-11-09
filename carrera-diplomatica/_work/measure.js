() => { const o = {};
  document.querySelectorAll('[data-id]').forEach(e => { const r = e.getBoundingClientRect(); o[e.dataset.id] = [Math.round(r.left), Math.round(r.top + scrollY), Math.round(r.width), Math.round(r.height)]; });
  return o; }
