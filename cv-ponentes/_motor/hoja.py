"""Compara el texto de <slug>-datos.json con la pestaña del ponente en la hoja de ponentes (solo el contenido de la hoja).
Uso: python hoja.py <slug> <gid>
Lista cada texto de los datos que NO aparece literal en la hoja, con la frase más parecida de la hoja y la diferencia.
No corrige nada: el Figma aprobado manda; las diferencias se reportan a Ponentes-WP."""
import csv, difflib, html, io, json, os, re, sys, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOJA = 'https://docs.google.com/spreadsheets/d/1ZmKvAhy4_9JQyknhlaG5tgePoWvf6LTB/export?format=csv&gid='


def norm(s):
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', '', s)
    s = html.unescape(s).replace('⁠', '').replace(' ', ' ')
    s = s.replace('•', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def main(slug, gid):
    sys.stdout.reconfigure(encoding='utf-8')
    D = json.load(open(os.path.join(RAIZ, slug, f'{slug}-datos.json'), encoding='utf-8'))
    raw = urllib.request.urlopen(HOJA + gid, timeout=30).read().decode('utf-8')
    celdas = [norm(c) for row in csv.reader(io.StringIO(raw)) for c in row if c.strip()]
    blob = ' '.join(celdas)
    frases = [f for c in celdas for f in re.split(r'(?<=[.;:])\s+', c) if f]
    textos = [('titular', D['titular'])] + [(f'especialidad {i + 1}', t) for i, t in enumerate(D['especialidades']['d'])]
    textos += [(f'resumen {i + 1}', t) for i, t in enumerate(D['resumen'])]
    for k in ('cargos', 'formacion', 'aportes'):
        textos += [(f'{k} {i + 1}', t) for i, t in enumerate(D[k])]
    textos += [(f'cifra {i + 1}', c['big'] + ' / ' + c['small']) for i, c in enumerate(D['cifras'])]
    dif = 0
    for nombre, t in textos:
        n = norm(t)
        if nombre.startswith('cifra'):
            continue  # las cifras son un resumen del diseño; no salen literales en la hoja
        if n in blob:
            continue
        # por oraciones: cada oración del dato tiene que estar en la hoja
        faltan = [o for o in re.split(r'(?<=[.;:])\s+', n) if o and o not in blob]
        if not faltan:
            continue
        dif += 1
        print(f'\n· {nombre}: no aparece igual en la hoja')
        for o in faltan:
            cerca = difflib.get_close_matches(o, frases, n=1, cutoff=0.3)
            print(f'   datos: {o}')
            if cerca:
                print(f'   hoja : {cerca[0]}')
                d = [x for x in difflib.ndiff(cerca[0].split(), o.split()) if x[0] in '+-']
                print(f'   cambio: {" ".join(d)[:300]}')
            else:
                print('   hoja : (sin frase parecida)')
    print(f'\n{"SIN DIFERENCIAS con la hoja" if not dif else f"{dif} textos con diferencias (revisar contra el Figma y reportar)"}')


if __name__ == '__main__':
    main(*sys.argv[1:3])
