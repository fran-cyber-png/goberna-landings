# Vista previa de Inversión: markup y CSS de la página publicada + el fondo nuevo del JSON
import json, re, base64, os, sys
sys.stdout.reconfigure(encoding='utf-8')
W = 'C:/Users/Consultoría/Documents/Director-Seguridad/'
d = json.loads(open(W + '_work/inv/live_inv.json', encoding='utf-8').read())
if isinstance(d, str): d = json.loads(d)
css, html, sid = d['css'], d['html'], d['id']
html = re.sub(r'<script\b.*?</script>|<noscript>.*?</noscript>', '', html, flags=re.S)
J = json.load(open(W + 'secciones-director-seguridad/12-inversion-fondo-nuevo.json', encoding='utf-8'))['content'][0]['settings']
img = 'data:image/webp;base64,' + base64.b64encode(open(W + 'imagenes/inversion-fondo-director.webp', 'rb').read()).decode()
pos = J['background_position']; size = J['background_size']
sel = f'.elementor-93575 .elementor-element.elementor-element-{sid}'
over = f'{sel}{{background-image:url("{img}") !important;background-position:{pos} !important;background-size:{size} !important;background-repeat:no-repeat !important;background-color:{J["background_color"]} !important}}'
FONTS = 'https://fonts.googleapis.com/css2?family=Barlow:wght@400;500;600;700&family=Montserrat:wght@400;500;600;700&family=Inter:wght@400;500;600&display=swap'
css = re.sub(r'@font-face\s*\{[^}]*\}', '', css)
# fuente de íconos de Elementor (flecha del selector de país), incrustada
ei = base64.b64encode(open(W + '_work/inv/eicons.woff2', 'rb').read()).decode()
css = '@font-face{font-family:eicons;src:url(data:font/woff2;base64,' + ei + ') format("woff2");font-weight:400;font-style:normal;font-display:block}\n' + css
page = f'''<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Inversión fondo nuevo</title><link rel="stylesheet" href="{FONTS}">
<style>{css}</style><style>{over}
html,body{{margin:0;background:#15262F}}</style></head>
<body class="{d['body']}"><div data-elementor-id="93575" class="elementor elementor-93575">{html}</div></body></html>'''
open(W + '_artifact_inv/seccion.html', 'w', encoding='utf-8').write(page)
s = open(W + '_artifact_tes/index.html', encoding='utf-8').read()
s = s.replace('<title>Testimonios con video</title>', '<title>Inversión fondo nuevo</title>')
s = s.replace('Testimonios con video · otra landing<small>Estructura de Director de Seguridad con el estilo del bloque testimonios</small>', 'Inversión y admisión · fondo nuevo<small>Director de Seguridad · fondo tomado del Figma (frame 6112:373)</small>')
s = s.replace('title="Sección Testimonios con video"', 'title="Sección Inversión con fondo nuevo"')
s = re.sub(r'\s*<button type="button" class="pend".*?</button>', '', s, flags=re.S)
s = re.sub(r'\s*<div class="list" id="list" hidden>.*?</div>\n', '\n', s, flags=re.S)
s = s.replace("var pb=document.getElementById('pendBtn'), list=document.getElementById('list');\n  pb.addEventListener('click',function(){ list.hidden=!list.hidden; pb.setAttribute('aria-expanded', String(!list.hidden)); });\n", '')
# el marco toma el alto real de la sección (si no, queda una franja vacía debajo)
s = s.replace("frame.style.width=dev.w+'px'; frame.style.height=dev.h+'px';",
  "frame.style.width=dev.w+'px'; var fh=dev.h; try{ var d=ifr.contentDocument; if(d&&d.body){ fh=d.querySelector('.elementor').offsetHeight; } }catch(e){} frame.style.height=fh+'px';")
s = s.replace("var s=Math.min(1, aw/dev.w, ah/dev.h);", "var s=1;")
s = s.replace("frame.style.transform='translateX(-50%) scale('+s+')';", "s=Math.min(1, aw/dev.w, ah/parseFloat(frame.style.height)); frame.style.transform='translateX(-50%) scale('+s+')';")
s = s.replace("ifr.addEventListener('load',apply);", "ifr.addEventListener('load',function(){ apply(); fit(); try{ var el=ifr.contentDocument.querySelector('.elementor'); new ifr.contentWindow.ResizeObserver(function(){ fit(); }).observe(el); }catch(e){} });")
open(W + '_artifact_inv/index.html', 'w', encoding='utf-8').write(s)
print(len(page), 'pendBtn' in s)
