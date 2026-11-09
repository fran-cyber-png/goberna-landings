# Muestra los ajustes de elementos: python show.py id1 id2 ...
import json, sys
J = json.load(open('base.json', encoding='utf-8'))
E = {}
def w(n): E[n['id']] = n; [w(c) for c in n.get('elements', [])]
[w(n) for n in J['content']]
for i in sys.argv[1:]:
    s = dict(E[i]['settings']); cc = s.pop('custom_css', None)
    print('==', i, E[i].get('widgetType', E[i]['elType']), json.dumps(s, ensure_ascii=False)[:2500])
