# Arma landing.html (página completa) a partir de base.html/base.css transformados
import os
W=os.path.dirname(os.path.abspath(__file__)); P=os.path.join(W,'..','_preview')
FONTS='https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&family=Barlow:wght@400;500;600;700&family=Oswald:wght@400;500;600;700&family=Inder&display=swap'
def build(html,css,out='landing.html',title='Director de Seguridad'):
    SHIM=open(os.path.join(W,'shim.js'),encoding='utf-8').read()
    page=f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="{FONTS}">
<style>{css}
html,body{{margin:0;background:#fff}} .elementor-sticky__spacer{{display:none!important}}</style></head>
<body class="wp-singular single single-product woocommerce elementor-default elementor-kit-5 e--ua-blink e--ua-chrome e--ua-webkit">
{html}
<script src="https://cdnjs.cloudflare.com/ajax/libs/Swiper/8.4.7/swiper-bundle.min.js"></script>
<script>{SHIM}</script></body></html>'''
    open(os.path.join(P,out),'w',encoding='utf-8').write(page)
if __name__=='__main__':
    build(open(os.path.join(W,'base.html'),encoding='utf-8').read(),open(os.path.join(W,'base.css'),encoding='utf-8').read(),'base-preview.html','Base')
