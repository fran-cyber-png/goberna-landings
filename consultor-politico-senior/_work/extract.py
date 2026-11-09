# Igual que Director-Seguridad/_work/extract.py, sobre la captura de la plantilla 93575 publicada
import json,re,os,urllib.request,hashlib
W=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(W,'prev')
html=open(os.path.join(W,'live.html'),encoding='utf-8').read()
css=open(os.path.join(W,'live.css'),encoding='utf-8').read()
html=re.sub(r'<noscript>.*?</noscript>','',html,flags=re.S)
html=re.sub(r'\ssrc="data:image/svg\+xml[^"]*"','',html)
html=html.replace('data-lazy-src=','src=').replace('data-lazy-srcset=','srcset=').replace('data-lazy-sizes=','sizes=')
html=re.sub(r'\s(srcset|sizes)="[^"]*"','',html)
def fetch(u):
    clean=u.replace('&amp;','&'); base=clean.split('?')[0].split('#')[0]
    ext=os.path.splitext(base)[1][:6] or '.bin'
    # nombre con la ruta AAAA/MM para que no se pisen imágenes con el mismo nombre (guía 12.3)
    m=re.search(r'/uploads/(\d{4})/(\d{2})/',base)
    name=re.sub(r'[^A-Za-z0-9._-]','_',os.path.basename(base))
    if m: name=m.group(1)+m.group(2)+'-'+name
    if len(name)>70: name=hashlib.md5(base.encode()).hexdigest()[:10]+ext
    out=os.path.join(P,'a',name)
    if not os.path.exists(out):
        try:
            req=urllib.request.Request(clean,headers={'User-Agent':'Mozilla/5.0'})
            open(out,'wb').write(urllib.request.urlopen(req,timeout=60).read())
        except Exception as e:
            print('FAIL',clean,e); return None
    return 'a/'+name+(('#'+u.split('#')[1]) if '#' in u else '')
cache={}
def rw(m):
    u=m.group(1)
    if u not in cache: cache[u]=fetch(u)
    return m.group(0).replace(u,cache[u]) if cache[u] else m.group(0)
pat=r'["\'(](https://grupogoberna\.com/wp-content/[^"\')\s]+\.(?:webp|png|jpe?g|svg|gif|woff2?|ttf|eot|mp4|pdf)(?:\?[^"\')\s#]*)?(?:#[^"\')\s]*)?)'
pat2=r'url\(\s*["\']?(https://grupogoberna\.com/wp-content/[^"\')\s]+)'
css=re.sub(pat2,rw,css); html=re.sub(pat,rw,html)
open(os.path.join(W,'base.html'),'w',encoding='utf-8').write(html)
open(os.path.join(W,'base.css'),'w',encoding='utf-8').write(css)
print(len(html),len(css),len(cache))
