import json,sys,re
sys.stdout.reconfigure(encoding='utf-8')
J=json.load(open('base.json',encoding='utf-8'))
NOISE=re.compile(r'^(typography_(font_family|font_weight|text_transform|letter_spacing.*|line_height.*|font_size.*)|_margin.*|_padding.*|padding.*|margin.*|flex_gap.*|width.*|_element.*|_flex.*)$')
def short(s):
    out={}
    for k,v in s.items():
        if k in ('custom_css','htmlCache') or v in ('',[],{},None): continue
        out[k]=v
    return out
def show(e,d=0,full=False):
    s=e.get('settings',{})
    txt=json.dumps(short(s),ensure_ascii=False)
    print('  '*d+f"[{e['elType']}{(':'+e['widgetType']) if e.get('widgetType') else ''} {e['id']}] {txt[:900 if not full else 100000]}")
    if s.get('custom_css'): print('  '*d+'  CSS> '+s['custom_css'].replace('\n',' ')[:6000])
    for c in e.get('elements',[]): show(c,d+1,full)
for i in sys.argv[1:]:
    show(J['content'][int(i)])
