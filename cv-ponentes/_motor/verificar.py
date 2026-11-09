"""Mide _generador/sim.html con Playwright a 1920, 1366 y 375 y lo compara con el Figma (medidas.json).
Uso: python verificar.py <slug>      -> imprime cada comprobación y deja _generador/verificacion.txt
Sale con código 1 si algo no cuadra (tolerancia 1,5 px en unidades del Figma)."""
import json, os, sys
from playwright.sync_api import sync_playwright

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOL = 1.5

JS = r'''() => {
  const q = s => document.querySelector(s), qa = s => [...document.querySelectorAll(s)];
  const R = e => { const r = e.getBoundingClientRect(); return {x: r.left + scrollX, y: r.top + scrollY, w: r.width, h: r.height}; };
  const vis = e => e && getComputedStyle(e).display !== 'none' && e.offsetParent !== null;
  const out = {vw: innerWidth, cw: document.documentElement.clientWidth, sw: document.documentElement.scrollWidth,
               docH: document.documentElement.scrollHeight};
  if (vis(q('.ak-d-hero'))) {
    out.v = 'd';
    const card = R(q('.ak-d-card'));
    const rel = e => { const r = R(e); return {x: r.x - card.x, y: r.y - card.y, w: r.w, h: r.h}; };
    out.hero = R(q('.ak-d-hero')).h; out.card = card;
    out.sub = R(q('.ak-d-sub p')).h;
    out.foto = R(q('.ak-d-foto'));
    out.n2 = R(q('.ak-d-n2 .elementor-heading-title'));
    out.esp = qa('.ak-d-it-t p').map(p => R(p).h);
    out.heads = Object.fromEntries(['res','car','for','apo'].map(k => [k, rel(q('.ak-d-h-' + k))]));
    out.res = rel(q('.ak-d-res'));
    out.lists = Object.fromEntries(['car','for','apo'].map(k => { const ul = q('.ak-d-l-' + k + ' ul'); const b = R(ul);
       return [k, {top: rel(ul).y, h: b.h, items: [...ul.children].map(li => { const r = R(li); return [r.y - b.y, r.h]; })}]; }));
    out.hrs = qa('.ak-d-hr').map(e => rel(e).y);
    out.stin = rel(q('.ak-d-stats-in'));
    out.stats = qa('.ak-d-stat').map(e => ({y: rel(e).y, h: R(e).h, sh: R(e.querySelector('.ak-d-small p')).h,
                                            sw: e.querySelector('.ak-d-small p').scrollWidth}));
  } else {
    out.v = 'm';
    const card = R(q('.ak-m-card'));
    const rel = e => { const r = R(e); return {x: r.x - card.x, y: r.y - card.y, w: r.w, h: r.h}; };
    out.hero = R(q('.ak-m-hero')).h; out.card = card;
    out.sub = R(q('.ak-m-sub p')); out.foto = R(q('.ak-m-foto'));
    out.n2 = R(q('.ak-m-n2 .elementor-heading-title'));
    out.cells = qa('.ak-m-cell-t p').map(p => R(p).h);
    out.heads = Object.fromEntries(['res','car','for','apo'].map(k => [k, rel(q('.ak-m-h-' + k))]));
    out.res = rel(q('.ak-m-res'));
    out.datos = rel(q('.ak-m-datos'));
    out.dato = qa('.ak-m-dato').map(e => ({y: rel(e).y, h: R(e).h}));
    out.lists = Object.fromEntries(['car','for','apo'].map(k => { const ul = q('.ak-m-l-' + k + ' ul'); const b = R(ul);
       return [k, {top: rel(ul).y, h: b.h, items: [...ul.children].map(li => { const r = R(li); return [r.y - b.y, r.h]; })}]; }));
    out.hrs = qa('.ak-m-hr').map(e => rel(e).y);
  }
  return out;
}'''


def medir(path):
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for vw in (1920, 1366, 375):
            pg = b.new_page(viewport={'width': vw, 'height': 900})
            pg.goto('file:///' + path.replace('\\', '/'))
            pg.wait_for_load_state('networkidle')
            # cargar explícitamente todas las fuentes y pesos antes de medir (si no, a veces mide con la fuente de reserva)
            pg.evaluate('''async () => { await Promise.all(['400 18px "Open Sans"', '700 18px "Open Sans"', '800 37px Montserrat',
                '700 26px Montserrat', '400 25px Montserrat', '400 16px Manrope', '700 26px Sora', '400 13px Sora']
                .map(f => document.fonts.load(f))); await document.fonts.ready; }''')
            pg.wait_for_timeout(300)
            res[vw] = pg.evaluate(JS)
            if vw == 1920:
                pg.screenshot(path=os.path.join(os.path.dirname(path), 'captura-1920.png'), full_page=True)
            if vw == 375:
                pg.screenshot(path=os.path.join(os.path.dirname(path), 'captura-375.png'), full_page=True)
            pg.close()
        b.close()
    return res


def main(slug):
    P = os.path.join(RAIZ, slug)
    M = json.load(open(os.path.join(P, '_fuentes-figma', 'medidas.json'), encoding='utf-8'))
    D = json.load(open(os.path.join(P, f'{slug}-datos.json'), encoding='utf-8'))
    md, mm = M['desktop'], M['movil']
    R = medir(os.path.join(P, '_generador', 'sim.html'))
    filas, fallas = [], 0

    def chk(vista, que, real, esperado, tol=TOL):
        nonlocal fallas
        ok = real is not None and abs(real - esperado) <= tol
        fallas += 0 if ok else 1
        filas.append(f"{'OK   ' if ok else 'FALLA'} {vista:7} {que:42} medido {real if real is None else round(real, 2):>9}   Figma {round(esperado, 2):>9}")

    for vw, vista in ((1920, 'desktop'), (1366, 'laptop')):
        r = R[vw]; k = vw / 1920
        if r.get('v') != 'd':
            filas.append(f'FALLA {vista}: no se ve la versión desktop'); fallas += 1; continue
        chk(vista, 'sin scroll horizontal (ancho de página)', r['sw'], r['cw'], 0)
        chk(vista, 'alto total', r['docH'] / k, md['alto_total'], 2)
        chk(vista, 'portada', r['hero'] / k, 850)
        chk(vista, 'tarjeta: alto', r['card']['h'] / k, md['tarjeta_alto'])
        if vw == 1920:
            chk(vista, 'titular: líneas', r['sub'] / 48, md['titular_lineas'], 0.05)
            for i, (h, n) in enumerate(zip(r['esp'], md['esp_lineas_d'])):
                chk(vista, f'especialidad {i + 1}: líneas', h / 24, n, 0.05)
            fd = D['foto']['d']
            chk(vista, 'foto: x', r['foto']['x'], fd[0]); chk(vista, 'foto: ancho', r['foto']['w'], fd[2])
            chk(vista, 'nombre línea 2 cabe en 820', min(r['n2']['w'], 820), r['n2']['w'], 0.5)
        S = md['secciones_d']
        for key in ('res', 'car', 'for', 'apo'):
            chk(vista, f'título {key}: top en la tarjeta', r['heads'][key]['y'] / k, S[key]['top'])
        chk(vista, 'resumen: alto', r['res']['h'] / k, S['res']['cuerpo_alto'])
        for key in ('car', 'for', 'apo'):
            L = r['lists'][key]
            chk(vista, f'lista {key}: top', L['top'] / k, S[key]['top'] + S[key]['cuerpo_top'])
            chk(vista, f'lista {key}: alto', L['h'] / k, S[key]['cuerpo_alto'])
            if S[key]['estilo'] == 'items' and vw == 1920:
                for i, ((y, h), ey, eh) in enumerate(zip(L['items'], S[key]['item_tops'], S[key]['item_altos'])):
                    chk(vista, f'lista {key} ítem {i + 1}: top / alto', y + h / 1000, ey + eh / 1000, 0.6)
        for i, (y, e) in enumerate(zip(r['hrs'], md['divisores_d'])):
            chk(vista, f'divisor {i + 1}: top', y / k, e)
        chk(vista, 'línea dorada: top', r['stin']['y'] / k, md['linea_dorada'][0])
        chk(vista, 'línea dorada: alto', r['stin']['h'] / k, md['linea_dorada'][1])
        for i, (s, e) in enumerate(zip(r['stats'], md['cifras_d'])):
            chk(vista, f'cifra {i + 1}: top', s['y'] / k, md['linea_dorada'][0] + 7 + e['top'])
            chk(vista, f'cifra {i + 1}: alto de la descripción', s['sh'] / k, e['small_h'])

    r = R[375]; k = 375 / 430
    if r.get('v') != 'm':
        filas.append('FALLA móvil: no se ve la versión móvil'); fallas += 1
    else:
        chk('móvil', 'sin scroll horizontal (ancho de página)', r['sw'], r['cw'], 0)
        from motor import BANNER
        dh = mm['portada_alto'] - BANNER['hero_m']   # el banner móvil estándar es más bajo que el Figma
        chk('móvil', 'alto total', r['docH'] / k, mm['alto_total'] - dh, 2)
        chk('móvil', 'portada (estándar)', r['hero'] / k, BANNER['hero_m'])
        chk('móvil', 'foto: abajo = fin del banner', (r['foto']['y'] + r['foto']['h']) / k, BANNER['hero_m'])
        chk('móvil', 'tarjeta: alto', r['card']['h'] / k, mm['tarjeta'][1])
        chk('móvil', 'titular: líneas', r['sub']['h'] / k / 28, mm['titular_lineas'], 0.05)
        for i, (h, t) in enumerate(zip(r['cells'], mm['esp_textos_m'])):
            chk('móvil', f'especialidad {i + 1}: líneas', h / k / 13, t['lineas'], 0.05)
        fm = D['foto']['m']
        chk('móvil', 'foto: alto', r['foto']['h'] / k, fm[3])
        chk('móvil', 'nombre línea 2 cabe en 382', min(r['n2']['w'] / k, 382), r['n2']['w'] / k, 0.5)
        base = mm['interior'][1]
        rm = mm['resumen_m']
        chk('móvil', 'resumen: alto del texto', r['res']['h'] / k, rm['texto'][1])
        chk('móvil', 'cifras: top', r['datos']['y'] / k, base + rm['datos'][1])
        chk('móvil', 'cifras: alto', r['datos']['h'] / k, rm['datos'][3])
        for i, (d, e) in enumerate(zip(r['dato'], rm['dato'])):
            chk('móvil', f'cifra {i + 1}: alto', d['h'] / k, e['alto'])
        S = mm['secciones_m']
        for key in ('car', 'for', 'apo'):
            chk('móvil', f'título {key}: top en la tarjeta', r['heads'][key]['y'] / k, base + S[key]['top'])
            L = r['lists'][key]
            chk('móvil', f'lista {key}: top', L['top'] / k, base + S[key]['top'] + S[key]['lista_top'])
            chk('móvil', f'lista {key}: alto', L['h'] / k, S[key]['lista_alto'])
            if S[key]['estilo'] == 'items':
                for i, ((y, h), ey, eh) in enumerate(zip(L['items'], S[key]['item_tops'], S[key]['item_altos'])):
                    chk('móvil', f'lista {key} ítem {i + 1}: top / alto', y / k + h / k / 1000, ey + eh / 1000, 0.8)
        for i, (y, e) in enumerate(zip(r['hrs'], mm['divisores_m'])):
            chk('móvil', f'divisor {i + 1}: top', y / k, base + e)

    txt = '\n'.join(filas) + f"\n\n{'TODO CUADRA' if not fallas else f'{fallas} COMPROBACIONES FALLAN'} ({len(filas)} comprobaciones)\n"
    open(os.path.join(P, '_generador', 'verificacion.txt'), 'w', encoding='utf-8').write(txt)
    sys.stdout.reconfigure(encoding='utf-8')
    print(txt if fallas else '\n'.join(filas[-5:]) + '\n\n' + txt.split('\n\n')[-1])
    return fallas


if __name__ == '__main__':
    sys.exit(1 if main(sys.argv[1]) else 0)
