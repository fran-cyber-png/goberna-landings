# Arma la página de vista previa a partir del HTML/CSS renderizado (transformados)
import os,json,re,base64
W=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(W,'prev')
FONTS='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&family=Barlow:wght@400;500;600;700&display=swap'
snap=json.load(open(os.path.join(W,'snap-93575.json'),encoding='utf-8'))
if isinstance(snap,str): snap=json.loads(snap)
BODY=snap['bodyClass']
def inline_programa_masks(css):
    # solo vista previa: las máscaras de "El programa" se incrustan como data URI (en el Artifact, el CSS
    # carga a/ desde otro origen y CORS las bloquea; en Elementor y en local sí se ven)
    # la base trae las mismas máscaras con la URL absoluta de WordPress (uploads/2026/09/programa-*.svg): mismo archivo
    def rep(m):
        data=base64.b64encode(open(os.path.join(P,'a','202609-'+m.group(2)),'rb').read()).decode('ascii')
        return f'url("data:image/svg+xml;base64,{data}")'
    css,n=re.subn(r'url\(\s*([\'"]?)(?:a/202609-|https://grupogoberna\.com/wp-content/uploads/2026/09/)(programa-[\w-]+\.svg)\1\s*\)',rep,css)
    print(f'máscaras de "El programa" incrustadas: {n}')
    return css
def build(html,css,out='landing.html',title='Consultor Político Senior'):
    SHIM=open(os.path.join(W,'shim.js'),encoding='utf-8').read()
    css=inline_programa_masks(css)
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="{FONTS}">
<style>{css}
html,body{{margin:0;background:#fff}} .elementor-sticky__spacer{{display:none!important}}</style></head>
<body class="{BODY}">
{html}
<script src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/8.4.7/swiper-bundle.min.js"></script>
<script>{SHIM}</script></body></html>'''
    open(os.path.join(P,out),'w',encoding='utf-8').write(page)
if __name__=='__main__':
    build(open(os.path.join(W,'base.html'),encoding='utf-8').read(),open(os.path.join(W,'base.css'),encoding='utf-8').read(),'base-preview.html','Base')
