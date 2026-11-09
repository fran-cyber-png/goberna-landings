"""Saca de get_metadata (desktop 1920 y móvil 430) todas las medidas que cambian entre ponentes
y las posiciones esperadas para la verificación con Playwright.

Uso: python medidas.py <xml_desktop> <id_desktop> <xml_movil> <id_movil> [salida.json]
Los xml son los archivos que guarda get_metadata (JSON [{type,text}] o XML plano)."""
import json, re, sys
from figma_xml import load_tool_result, frame

def r2(v): return round(v, 2)

def text_lines(h, lh): return max(1, round(h / lh))

# ---------------------------------------------------------------- desktop
def desktop(root):
    out, exp = {}, {}
    out['alto_total'] = r2(root.h)
    hero = root.first(lambda n: n.name == 'Frame 5' and abs(n.h - 850) < 1)
    assert hero, 'no encuentro la portada (Frame 5, alto 850)'
    sub = hero.first(lambda n: n.tag == 'text' and n.parent.name == 'Frame 135' and n.y > 100)
    out['titular_lineas'] = text_lines(sub.h, 48)
    barra = hero.first(lambda n: n.tag == 'boolean-operation' and abs(n.w - 820) < 1 and abs(n.h - 170) < 1)
    bx, by = barra.abs_xy(hero)
    out['barra_top'] = r2(by)
    row = hero.first(lambda n: n.name == 'Frame 140')
    rx, ry = row.abs_xy(hero)
    out['esp_fila'] = [r2(ry - by), r2(row.h)]          # top relativo a la barra, alto
    items = sorted([k for k in row.kids if k.tag == 'frame'], key=lambda n: n.x)
    assert len(items) == 4, f'esperaba 4 especialidades, hay {len(items)}'
    icos, txt = [], []
    for it in items:
        ico = [k for k in it.kids if k.tag in ('frame', 'group', 'vector', 'instance') and k.y < 5]
        ico = ico[0]
        inner = ico.first(lambda n: n is not ico and n.tag in ('frame', 'vector', 'group') and n.h > 20)
        icos.append({'nodo': ico.id, 'nombre': ico.name, 'ancho': r2(ico.w), 'contenedor_alto': r2(ico.h),
                     'alto': r2(inner.h if (inner and 'Contenedor' in ico.name) else ico.h)})
        t = [k for k in it.kids if k.tag == 'text']
        txt.append(text_lines(t[0].h, 24) if t else None)
    out['esp_iconos_d'] = icos
    out['esp_lineas_d'] = txt
    out['esp_item_alto'] = r2(items[0].h)
    # foto: rectángulo con imagen de alto 749 en y=101 (no el logo ni el marcador "pendiente")
    fotos = [n for n in hero.walk() if n.tag == 'rounded-rectangle' and abs(n.h - 749) < 2 and not n.hidden
             and 'pendiente' not in n.name.lower()]
    out['foto_capa_d'] = [{'nodo': f.id, 'nombre': f.name, 'x': r2(f.x), 'y': r2(f.y), 'w': r2(f.w), 'h': r2(f.h)} for f in fotos]

    body = root.first(lambda n: n.name == 'Frame 3' and n.y >= 849)
    card = body.first(lambda n: n.name == 'Frame 1' and abs(n.w - 1519) < 1)
    out['tarjeta_alto'] = r2(card.h)
    line = card.first(lambda n: n.tag == 'line' and n.parent is card and abs(n.x - 972) < 2)
    out['linea_dorada'] = [r2(line.y), r2(max(line.h, line.w))]
    st = card.first(lambda n: n.name == 'Frame 15')
    stats = sorted([k for k in st.kids if k.tag == 'frame'], key=lambda n: n.y)
    out['cifras_d'] = []
    for s in stats:
        tt = sorted([k for k in s.kids if k.tag == 'text'], key=lambda n: n.y)
        out['cifras_d'].append({'top': r2(s.y), 'alto': r2(s.h), 'big_h': r2(tt[0].h), 'small_top': r2(tt[1].y),
                                'small_h': r2(tt[1].h), 'small_w': r2(tt[1].w)})
    out['cifras_frame'] = [r2(st.x), r2(st.y), r2(st.w), r2(st.h)]
    # secciones: Frame 144 (resumen), 145 (cargos), 148 (formación), 151 (aportes)
    secs = {}
    for key, nm in (('res', 'Frame 144'), ('car', 'Frame 145'), ('for', 'Frame 148'), ('apo', 'Frame 151')):
        f = card.first(lambda n, nm=nm: n.name == nm and n.parent is card)
        head = max([k for k in f.kids if k.tag == 'frame' and k.y < 1], key=lambda n: n.h)
        body_n = [k for k in f.kids if k is not head and k.y > 50 and k.tag in ('frame', 'text')]
        b = body_n[0]
        d = {'top': r2(f.y), 'x': r2(f.x), 'alto': r2(f.h), 'cuerpo_top': r2(b.y), 'cuerpo_x': r2(b.x), 'cuerpo_alto': r2(b.h),
             'titulo_nodo': head.id}
        if key != 'res':
            d.update(lista(b, 28))
        secs[key] = d
    out['secciones_d'] = secs
    lines = sorted([n for n in card.kids if n.tag == 'line' and n.w > 700], key=lambda n: n.y)
    out['divisores_d'] = [r2(l.y) for l in lines]
    return out

def lista(b, lh):
    """Ítems de una lista: plantilla nueva (frames Item) o antigua (un texto + elipses/flechas)."""
    items = sorted([k for k in b.kids if k.tag == 'frame' and k.name == 'Item'], key=lambda n: n.y)
    if items:
        tops = [r2(i.y) for i in items]; hs = [r2(i.h) for i in items]
        gaps = sorted({r2(tops[i + 1] - tops[i] - hs[i]) for i in range(len(items) - 1)})
        return {'estilo': 'items', 'n': len(items), 'item_tops': tops, 'item_altos': hs, 'gap': gaps}
    marks = sorted([k for k in b.kids if k.tag in ('ellipse', 'vector')], key=lambda n: n.y)
    t = [k for k in b.kids if k.tag == 'text']
    return {'estilo': 'texto+marcas', 'n': len(marks), 'marca_tops': [r2(m.y) for m in marks],
            'marca_tam': [r2(marks[0].w), r2(marks[0].h)] if marks else None,
            'texto_alto': r2(t[0].h) if t else None}

# ---------------------------------------------------------------- móvil
def movil(root):
    out = {}
    out['alto_total'] = r2(root.h)
    hero = root.first(lambda n: n.name == 'Frame 5' and abs(n.h - 931) < 2)
    assert hero, 'no encuentro la portada móvil (Frame 5, alto 931)'
    out['portada_alto'] = r2(hero.h)
    sub = [n for n in hero.kids if n.tag == 'text' and abs(n.x - 24) < 1 and 150 < n.y < 260]
    out['titular_lineas'] = text_lines(sub[0].h, 28) if sub else None
    out['titular_top'] = r2(sub[0].y) if sub else None
    nombre = [n for n in hero.kids if n.tag == 'text' and abs(n.x - 24) < 1 and 80 < n.y < 120]
    out['nombre'] = [r2(nombre[0].w), r2(nombre[0].h)] if nombre else None
    barra = hero.first(lambda n: n.tag == 'boolean-operation' and abs(n.w - 382) < 1)
    out['barra'] = [r2(barra.x), r2(barra.y), r2(barra.w), r2(barra.h)]
    icos = sorted([n for n in hero.kids if n.tag in ('frame', 'group', 'instance') and 300 < n.y < 480 and n.h < 30],
                  key=lambda n: (round(n.y / 40), n.x))
    out['esp_iconos_m'] = []
    for i in icos:
        inner = i.first(lambda n: n is not i and n.tag in ('frame', 'vector', 'group') and n.h > 10)
        out['esp_iconos_m'].append({'nodo': i.id, 'x': r2(i.x), 'y': r2(i.y), 'w': r2(i.w),
                                    'contenedor_alto': r2(i.h), 'alto': r2(inner.h if (inner and 'Contenedor' in i.name) else i.h)})
    labels = sorted([n for n in hero.kids if n.tag == 'text' and 340 < n.y < 470], key=lambda n: (round(n.y / 40), n.x))
    out['esp_textos_m'] = [{'x': r2(t.x), 'y': r2(t.y), 'w': r2(t.w), 'lineas': text_lines(t.h, 13)} for t in labels]
    fotos = [n for n in hero.walk() if n.tag == 'rounded-rectangle' and n.y >= 500 and n.h > 300 and not n.hidden
             and 'pendiente' not in n.name.lower()]
    out['foto_capa_m'] = [{'nodo': f.id, 'nombre': f.name, 'x': r2(f.abs_xy(hero)[0]), 'y': r2(f.abs_xy(hero)[1]),
                           'w': r2(f.w), 'h': r2(f.h)} for f in fotos]
    card = root.first(lambda n: n.name == 'Frame 1' and abs(n.w - 390) < 1)
    out['tarjeta'] = [r2(card.y), r2(card.h)]
    inner = card.first(lambda n: n.name == 'Frame 12' and n.parent is card)
    out['interior'] = [r2(inner.x), r2(inner.y), r2(inner.h)]
    secs = sorted([k for k in inner.kids if k.tag == 'frame'], key=lambda n: n.y)
    assert len(secs) == 4, f'esperaba 4 secciones en móvil, hay {len(secs)}'
    res = secs[0]
    rt = [k for k in res.kids if k.tag == 'text' and k.y > 30]
    datos = res.first(lambda n: n.name == 'Datos')
    out['resumen_m'] = {'top': r2(res.y), 'alto': r2(res.h), 'texto': [r2(rt[0].y), r2(rt[0].h)] if rt else None,
                        'datos': [r2(datos.x), r2(datos.y), r2(datos.w), r2(datos.h)],
                        'dato': [{'top': r2(d.y), 'alto': r2(d.h),
                                  'big_h': r2(sorted([t for t in d.kids if t.tag == 'text'], key=lambda n: n.y)[0].h),
                                  'small_top': r2(sorted([t for t in d.kids if t.tag == 'text'], key=lambda n: n.y)[1].y),
                                  'small_h': r2(sorted([t for t in d.kids if t.tag == 'text'], key=lambda n: n.y)[1].h)}
                                 for d in sorted([k for k in datos.kids if k.tag == 'frame'], key=lambda n: n.y)]}
    out['secciones_m'] = {}
    for key, s in zip(('car', 'for', 'apo'), secs[1:]):
        title = s.first(lambda n: n.tag == 'text' and n.y < 10)
        lst = s.first(lambda n: n.name == 'Lista')
        d = {'top': r2(s.y), 'alto': r2(s.h), 'titulo_alto': r2(title.h), 'titulo_lineas': text_lines(title.h, 33),
             'lista_top': r2(lst.y), 'lista_alto': r2(lst.h)}
        d.update(lista(lst, 28))
        out['secciones_m'][key] = d
    lines = sorted([k for k in inner.kids if k.tag == 'line'], key=lambda n: n.y)
    out['divisores_m'] = [r2(l.y) for l in lines]
    return out


if __name__ == '__main__':
    xd, idd, xm, idm = sys.argv[1:5]
    d = desktop(frame(load_tool_result(xd), idd))
    m = movil(frame(load_tool_result(xm), idm))
    res = {'figma': {'desktop': idd, 'mobile': idm}, 'desktop': d, 'movil': m}
    s = json.dumps(res, ensure_ascii=False, indent=1)
    if len(sys.argv) > 5:
        open(sys.argv[5], 'w', encoding='utf-8').write(s)
    sys.stdout.reconfigure(encoding='utf-8')
    print(s)
