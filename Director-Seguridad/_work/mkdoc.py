import re
P='../_preview'
h=open(P+'/landing.html',encoding='utf-8').read()
head=h[:h.index('<body')]
m=re.search(r'<div[^>]*\bdata-id="5b40c644"',h); s=m.start(); d=0
for t in re.finditer(r'<div\b|</div>',h[s:]):
    d+=1 if t.group(0)=='<div' else -1
    if d==0: e=s+t.end(); break
tail=h[h.index('<script src="https://cdnjs'):]
page=head.replace('<title>Director de Seguridad</title>','<title>Ponentes Director de Seguridad</title>')+re.search(r'<body[^>]*>',h).group(0)+'\n<div data-elementor-id="93083" class="elementor elementor-93083">'+h[s:e]+'</div>\n'+tail
page=page.replace('</head>','<style>html,body{background:#090909!important}</style></head>',1)  # solo vista previa: debajo de la sección no hay más página
open(P+'/docentes.html','w',encoding='utf-8').write(page)
