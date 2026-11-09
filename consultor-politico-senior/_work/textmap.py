import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
J=json.load(open(sys.argv[1] if len(sys.argv)>1 else 'base.json',encoding='utf-8'))
def walk(e,sec,d=0):
    s=e['settings']; w=e.get('widgetType','')
    t=None
    for k in ('title','editor','text','tab_title','item_title','button_text','html'):
        if isinstance(s.get(k),str) and s[k].strip(): t=(k,s[k]); break
    if w=='nested-tabs': t=('tabs',' | '.join(x['tab_title'] for x in s['tabs']))
    if w=='nested-accordion': t=('items',' | '.join(x['item_title'] for x in s['items']))
    if w=='form': t=('form',' | '.join(f"{x.get('field_label','')}/{x.get('placeholder','')}" for x in s.get('form_fields',[]))+' || '+str(s.get('button_text'))+' || '+str(s.get('form_name')))
    cls=s.get('_css_classes') or s.get('css_classes') or ''
    if t: print(f"{sec:2} {e['id']:>8} {w[:12]:12} {cls[:22]:22} {t[0][:5]}: {re.sub(r'\s+',' ',t[1])[:230]}")
    elif e['elType']=='container' and cls: print(f"{sec:2} {e['id']:>8} {'[cont]':12} {cls[:22]:22}")
    for c in e.get('elements',[]): walk(c,sec,d+1)
for i,e in enumerate(J['content']): walk(e,i)
