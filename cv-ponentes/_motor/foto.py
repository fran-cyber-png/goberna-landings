"""Recorta la foto original del Figma a la caja que se ve en pantalla, la voltea si hace falta y la guarda en webp.
Después la compara con la exportación de Figma de la capa (sobre fondo blanco).

Uso:
  python foto.py <slug> <raw.png> <export.png> <ancho_caja> <alto_caja> <img_w%> <img_h%> <left%> <top%> [--flip] [--salida nombre.webp]
    raw.png     imagen original (rawImages de download_assets: elige la que tiene canal alfa si hay dos del mismo tamaño)
    export.png  "export" de download_assets de la capa de la foto (lo que se ve en Figma)
    caja        ancho y alto de la caja de la foto en Figma (el div exterior de get_design_context: w-[694px] h-[749px])
    img_*%      del <img> interior de get_design_context: w-[113.01%] h-[113.89%] left-[-10.31%] top-[-1.6%]
                (si el <img> es object-cover sin porcentajes, pon: cover cover 0 0)
    --flip      si el contenedor lleva -scale-y-100 + rotate-180, o -scale-x-100 (foto volteada en horizontal)
Resultado: imagenes/<slug>.webp (o --salida) y la diferencia con Figma. Tiene que salir < 3 %."""
import os, subprocess, sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def magick(*a):
    return subprocess.run(['magick', *a], capture_output=True, text=True)


def size(p):
    w, h = magick('identify', '-format', '%w %h', p).stdout.split()
    return int(w), int(h)


def main():
    a = sys.argv[1:]
    flip = '--flip' in a
    if flip: a.remove('--flip')
    salida = None
    if '--salida' in a:
        i = a.index('--salida'); salida = a[i + 1]; del a[i:i + 2]
    slug, raw, exp, bw, bh, pw, ph, pl, pt = a
    bw, bh = float(bw), float(bh)
    rw, rh = size(raw)
    if pw == 'cover':
        s = max(bw / rw, bh / rh)
        x0, y0 = (rw * s - bw) / 2 / s, (rh * s - bh) / 2 / s
    else:
        pw, ph, pl, pt = (float(v) / 100 for v in (pw, ph, pl, pt))
        s = bw * pw / rw                      # escala raw -> pantalla
        s2 = bh * ph / rh
        if abs(s - s2) / s > 0.01:
            print(f'AVISO: la imagen está deformada en Figma (escala x {s:.4f} vs y {s2:.4f}); se usa la horizontal')
        x0, y0 = -pl * bw / s, -pt * bh / s
    cw, ch = bw / s, bh / s
    x0, y0, cw, ch = round(x0), round(y0), round(cw), round(ch)
    # recorte dentro de la imagen (si la caja se sale de la imagen, se rellena transparente)
    out = os.path.join(RAIZ, slug, 'imagenes', salida or f'{slug}.webp')
    args = [raw, '-background', 'none', '-gravity', 'NorthWest', '-extent', f'{max(rw, x0 + cw)}x{max(rh, y0 + ch)}',
            '-crop', f'{cw}x{ch}+{x0}+{y0}', '+repage']
    if flip: args.append('-flop')
    for q in (92, 90, 88):
        r = magick(*args, '-quality', str(q), '-define', 'webp:alpha-quality=100', '-define', 'webp:method=6', out)
        if r.returncode: print(r.stderr); sys.exit(1)
        if os.path.getsize(out) < 500 * 1024: break
    kb = os.path.getsize(out) // 1024
    w, h = size(out)
    tmp1, tmp2 = out + '.a.png', out + '.b.png'
    ew, eh = size(exp)
    magick(out, '-resize', f'{ew}x{eh}!', '-background', 'white', '-flatten', tmp1)
    magick(exp, '-background', 'white', '-flatten', tmp2)
    r = magick('compare', '-metric', 'RMSE', tmp1, tmp2, 'null:')
    os.remove(tmp1); os.remove(tmp2)
    txt = (r.stderr or r.stdout).strip()
    try:
        dif = float(txt.split('(')[1].split(')')[0]) * 100
    except Exception:
        dif = 999
    print(f'foto: {out}  {w}x{h}  {kb} KB  recorte {cw}x{ch}+{x0}+{y0}{" volteada" if flip else ""}')
    print(f'diferencia con Figma: {dif:.2f} %  ->  {"OK" if dif < 3 and kb < 500 else "REVISAR (prueba con/sin --flip, o la otra imagen raw)"}')


if __name__ == '__main__':
    main()
