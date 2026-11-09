# Separa curso-inteligencia-y-contrainteligencia.json en un JSON por sección (plantillas de Elementor tipo "container"),
# con el mismo formato que las secciones de Director (version 0.4, page_settings vacío).
import json, os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
OUT = os.path.join(ROOT, 'secciones')
NAMES = [('ak-hd', 'header'), ('ak-hero', 'hero'), ('ak-bar', 'barra-datos'), ('ak-met', 'metodologia'),
         ('ak-prog', 'el-programa'), ('ak-war', 'war-room'), ('ak-plan-pin', 'plan-de-estudios'),
         ('ak-cta', 'banner-proxima-edicion'), ('ak-doc', 'docentes'), ('ak-pres', 'presencia-internacional'),
         ('ak-cert', 'certificacion'), ('ak-inv', 'inversion'), ('ak-vsec', 'experiencia-goberna'), ('ak-faq', 'preguntas-frecuentes')]
page = json.load(open(os.path.join(ROOT, 'curso-inteligencia-y-contrainteligencia.json'), encoding='utf-8'))
os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT):
    if f.endswith('.json'): os.remove(os.path.join(OUT, f))
by_cls = {}
for sec in page['content']:
    cls = (sec['settings'].get('css_classes') or '').split()
    key = next((c for c, _ in NAMES if c in cls), None)
    assert key and key not in by_cls, (sec['id'], cls)
    by_cls[key] = sec
assert len(by_cls) == len(NAMES) == len(page['content']), (len(by_cls), len(page['content']))
for n, (c, name) in enumerate(NAMES, 1):
    tpl = {'content': [by_cls[c]], 'page_settings': [], 'version': page.get('version', '0.4'),
           'title': '%s inteligencia y contrainteligencia' % name.replace('-', ' '), 'type': 'container'}
    fn = '%02d-%s-inteligencia-contrainteligencia.json' % (n, name)
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(json.dumps(tpl, ensure_ascii=False))
    print(fn, by_cls[c]['id'], os.path.getsize(os.path.join(OUT, fn)) // 1024, 'KB')
