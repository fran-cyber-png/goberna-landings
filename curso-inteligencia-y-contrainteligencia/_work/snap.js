async () => {
  const NL = String.fromCharCode(10), out = [];
  const abs = (t, base) => t.replace(/url\(\s*(['"]?)(?!data:|https?:|\/\/|#)([^'")]+)\1\s*\)/g, (m, q, u) => 'url("' + new URL(u, base).href + '")');
  for (const s of document.styleSheets) {
    if (s.href) {
      const name = s.href.split('/').pop().split('?')[0];
      try { const t = await (await fetch(s.href)).text(); out.push('/* ' + name + ' */' + NL + abs(t, s.href)); }
      catch (e) { out.push('/* FAIL ' + s.href + ' */'); }
    } else {
      const n = s.ownerNode, id = (n && n.id) || 'inline';
      out.push('/* ' + id + ' */' + NL + abs((n && n.textContent) || '', location.href));
    }
  }
  return out.join(NL);
}
