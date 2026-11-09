# Convierte el código de get_design_context (React+Tailwind) en HTML medible: misma geometría que el Figma
import re, sys
src = open(sys.argv[1], encoding='utf-8').read(); out = sys.argv[2]
consts = dict(re.findall(r'const (img\w+) = "([^"]+)";', src))
body = src[src.find('return (') + 8:src.rfind(');')]
body = re.sub(r'src=\{(img\w+)\}', lambda m: f'src="{consts.get(m.group(1), "")}"', body)
body = re.sub(r'\sstyle=\{\{.*?\}\}', '', body, flags=re.S)
body = body.replace('className=', 'class=')
# JSX permite <div /> autocerrado; en HTML quedaría abierto y anidaría todo lo siguiente
body = re.sub(r'<(div|p|span|a|section)\b([^<>]*?)\s*/>', lambda m: f'<{m.group(1)}{m.group(2)}></{m.group(1)}>', body)
body = re.sub(r'\{`([^`]*)`\}', lambda m: m.group(1), body)
body = re.sub(r'aria-hidden(?!=)', 'aria-hidden="true"', body)
W = {'Thin': 100, 'Light': 300, 'Regular': 400, 'Medium': 500, 'SemiBold': 600, 'Semi_Bold': 600, 'Bold': 700, 'ExtraBold': 800, 'Black': 900, 'Italic': 400}
def fnt(m):
    fam, sty = m.group(1), m.group(2)
    return f"font-['{fam.replace(' ', '_')}'] font-[{W.get(sty, 400)}]"
body = re.sub(r"font-\['([^':]+):([^']+)'\]", fnt, body)
H = sys.argv[3] if len(sys.argv) > 3 else '10285'
html = f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700;800&family=Barlow:wght@400;500;600;700&display=swap">
<script src="https://cdn.tailwindcss.com/3.4.17"></script>
<style>body{{margin:0}} #root{{position:relative;width:1920px;height:{H}px}}</style></head>
<body><div id="root">{body}</div></body></html>'''
open(out, 'w', encoding='utf-8').write(html); print(len(html))
