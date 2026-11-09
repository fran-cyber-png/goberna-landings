# Resuelve los url() relativos de cada hoja capturada contra su href y descarga el recurso
import re,os,urllib.request,urllib.parse,hashlib
W=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(W,'prev')
css=open(os.path.join(W,'base.css'),encoding='utf-8').read()
parts=re.split(r'(/\* (?:https?://\S+|[^ ]+) \*/)',css)
out=[];href=None;n=0
def fetch(u):
    base=u.split('?')[0].split('#')[0]
    name='rel-'+re.sub(r'[^A-Za-z0-9._-]','_',os.path.basename(base))
    dst=os.path.join(P,'a',name)
    if not os.path.exists(dst):
        try: open(dst,'wb').write(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=60).read())
        except Exception as e: print('FAIL',u,e); return None
    return 'a/'+name+(('#'+u.split('#')[1]) if '#' in u else '')
for p in parts:
    m=re.match(r'/\* (https?://\S+) \*/',p)
    if m: href=m.group(1); out.append(p); continue
    if p.startswith('/* '): href=None; out.append(p); continue
    if href:
        def rw(mm):
            global n
            u=mm.group(2)
            if u.startswith(('data:','a/','http','#')): return mm.group(0)
            loc=fetch(urllib.parse.urljoin(href,u))
            if not loc: return mm.group(0)
            n+=1; return 'url('+mm.group(1)+loc+mm.group(1)+')'
        p=re.sub(r'url\(\s*(["\']?)([^"\')]+)\1\s*\)',rw,p)
    out.append(p)
open(os.path.join(W,'base.css'),'w',encoding='utf-8').write(''.join(out)); print('reescritas',n)
