import re,sys,html
sys.stdout.reconfigure(encoding='utf-8')
t=open('v2-context.tsx',encoding='utf-8').read()
# each <p className="..." data-node-id="..."> ... </p> ; spans inside
for m in re.finditer(r'<p className="([^"]*)" data-node-id="([^"]+)"[^>]*>(.*?)</p>',t,re.S):
    cls,nid,body=m.groups()
    txt=re.sub(r'<br\s*/?>','⏎',body)
    txt=re.sub(r'<[^>]+>','',txt); txt=re.sub(r'\{[`"\']?\s*[`"\']?\}','',txt)
    txt=html.unescape(re.sub(r'\s+',' ',txt)).strip()
    font=re.findall(r"font-\['([^']+)'\]",cls); size=re.findall(r'text-\[(\d+(?:\.\d+)?px)\]',cls)
    col=re.findall(r'text-\[(#[0-9a-fA-F]{3,8}|rgba?\([^\]]+\))\]',cls)+re.findall(r'text-(white|black)\b',cls)
    lh=re.findall(r'leading-\[([^\]]+)\]',cls)
    print(f"{nid:>9} | {','.join(font)} {','.join(size)} lh{','.join(lh)} {','.join(col)} | {txt[:150]}")
