# Saca el markup del template 93575 (Director de Seguridad publicado) y el CSS capturado; descarga los recursos y reescribe las URLs
import json, re, os, urllib.request, hashlib
W = os.path.dirname(os.path.abspath(__file__)); P = os.path.join(W, '..', '_preview')
snap = json.load(open(os.path.join(W, 'snap.json'), encoding='utf-8'))
src = snap['html']
i = src.find('<div data-elementor-type="jet-woo-builder" data-elementor-id="93575"')
depth = 0; j = i
for m in re.finditer(r'<div\b|</div>', src[i:]):
    depth += 1 if m.group(0) == '<div' else -1
    if depth == 0: j = i + m.end(); break
html = src[i:j]
html = re.sub(r'<noscript>.*?</noscript>', '', html, flags=re.S)
html = re.sub(r'\ssrc="data:image/svg\+xml[^"]*"', '', html)
html = html.replace('data-lazy-src=', 'src=').replace('data-lazy-srcset=', 'srcset=').replace('data-lazy-sizes=', 'sizes=')
html = re.sub(r'\s(srcset|sizes)="[^"]*"', '', html)
css = snap['css']
os.makedirs(os.path.join(P, 'a'), exist_ok=True)
def fetch(u):
    clean = u.replace('&amp;', '&')
    base = clean.split('?')[0].split('#')[0]
    ext = os.path.splitext(base)[1][:6] or '.bin'
    name = re.sub(r'[^A-Za-z0-9._-]', '_', os.path.basename(base))
    if len(name) > 60: name = hashlib.md5(base.encode()).hexdigest()[:10] + ext
    # misma imagen en distintos meses: la clave es la ruta completa (guía 12.3)
    if '/uploads/' in base:
        ym = re.search(r'/uploads/(\d{4})/(\d{2})/', base)
        if ym and ym.group(0) != '/uploads/2026/10/': name = ym.group(1) + ym.group(2) + '_' + name
    out = os.path.join(P, 'a', name)
    if not os.path.exists(out):
        try:
            req = urllib.request.Request(clean, headers={'User-Agent': 'Mozilla/5.0'})
            open(out, 'wb').write(urllib.request.urlopen(req, timeout=60).read())
        except Exception as e:
            print('FAIL', clean, e); return None
    return 'a/' + name + (('#' + u.split('#')[1]) if '#' in u else '')
cache = {}
def rw(m):
    u = m.group(1)
    if u not in cache: cache[u] = fetch(u)
    return m.group(0).replace(u, cache[u]) if cache[u] else m.group(0)
pat = r'["\'(](https://grupogoberna\.com/wp-content/[^"\')\s]+\.(?:webp|png|jpe?g|svg|gif|woff2?|ttf|eot|mp4)(?:\?[^"\')\s#]*)?(?:#[^"\')\s]*)?)'
pat2 = r'url\(\s*["\']?(https://grupogoberna\.com/wp-content/[^"\')\s]+)'
css = re.sub(pat2, rw, css)
html = re.sub(pat, rw, html)
open(os.path.join(W, 'base.html'), 'w', encoding='utf-8').write(html)
open(os.path.join(W, 'base.css'), 'w', encoding='utf-8').write(css)
print(len(html), len(css), len(cache))
