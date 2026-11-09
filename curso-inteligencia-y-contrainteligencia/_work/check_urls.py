# Comprueba que cada URL de imagen, SVG o video del JSON responda (guía: sin 404 antes de entregar)
import re, urllib.request, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
t = open(os.path.join(ROOT, 'curso-inteligencia-y-contrainteligencia.json'), encoding='utf-8').read()
pat = r'https://(?:grupogoberna\.com/wp-content|cms\.goberna\.club)/[A-Za-z0-9_./%-]+'
urls = sorted(set(re.findall(pat, t)))
bad = []
for u in urls:
    try:
        c = urllib.request.urlopen(urllib.request.Request(u, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'}), timeout=30).status
    except Exception as e:
        c = getattr(e, 'code', str(e)[:40])
    if c != 200: bad.append((c, u))
print(len(urls), 'URLs;', len(bad), 'no responden:')
for c, u in bad: print(' ', c, u)
for k in ['Director', 'director', 'Carrera', 'htmlCache', 'Élite']:
    print(k, len(re.findall(k, t)))
