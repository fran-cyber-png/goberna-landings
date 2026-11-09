import os, re, sys
from playwright.sync_api import sync_playwright
from PIL import Image, ImageChops
sys.stdout.reconfigure(encoding="utf-8")

SP = os.path.dirname(os.path.abspath(__file__))
ENT = r"C:\Users\Consultoría\Documents\consultor-politico\entregas"
CAP = os.path.join(ENT, "capturas")
NEW = os.path.join(ENT, "04-diploma-preview.html")
BASE = os.path.join(SP, "baseline-preview.html")
ICONS = os.path.join(SP, "icons")
os.makedirs(CAP, exist_ok=True)

fails = []
notes = []

def check(cond, msg):
    print(("PASS " if cond else "FAIL ") + msg)
    if not cond:
        fails.append(msg)

def route(r):
    url = r.request.url
    if url.startswith("file:"):
        return r.continue_()
    if url.endswith(".svg"):
        name = url.rsplit("/", 1)[-1]
        p = os.path.join(ICONS, name)
        if os.path.exists(p):
            return r.fulfill(path=p, content_type="image/svg+xml")
    return r.abort()

STATE_JS = """(root) => {
  const titles = [...document.querySelectorAll(root + ' .e-n-tab-title')];
  const panels = [...document.querySelectorAll(root + ' .e-n-tabs-content > .e-con')];
  return titles.map((t, i) => {
    const p = panels[i];
    return {
      sel: t.getAttribute('aria-selected'),
      exp: t.getAttribute('aria-expanded'),
      tab: t.getAttribute('tabindex'),
      active: p.classList.contains('e-active'),
      visible: getComputedStyle(p).display !== 'none',
      arrow: getComputedStyle(t, '::after').transform,
    };
  });
}"""

def states(page, root="#diploma"):
    return page.evaluate(STATE_JS, root)

def open_idx(st):
    return [i for i, s in enumerate(st) if s["sel"] == "true"]

def arrow_is_down(a):
    # rotate(135deg) => matrix(-0.7071, 0.7071, -0.7071, -0.7071, 0, 0)
    m = re.findall(r"-?[\d.]+(?:e-?\d+)?", a or "")
    return len(m) >= 4 and abs(float(m[0]) + 0.7071) < 0.01 and abs(float(m[3]) + 0.7071) < 0.01

def arrow_is_right(a):
    # rotate(45deg) => matrix(0.7071, 0.7071, -0.7071, 0.7071, 0, 0)
    m = re.findall(r"-?[\d.]+(?:e-?\d+)?", a or "")
    return len(m) >= 4 and abs(float(m[0]) - 0.7071) < 0.01 and abs(float(m[3]) - 0.7071) < 0.01

with sync_playwright() as p:
    browser = p.chromium.launch()
    errors = []

    def new_page(width, height=900, url=NEW):
        ctx = browser.new_context(viewport={"width": width, "height": height}, device_scale_factor=1)
        pg = ctx.new_page()
        pg.route("**/*", route)
        pg.on("pageerror", lambda e: errors.append(str(e)))
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.goto("file:///" + url.replace("\\", "/"), wait_until="load")
        pg.wait_for_timeout(300)
        return ctx, pg

    # ---------- MÓVIL 375 ----------
    ctx, pg = new_page(375, 812)
    st = states(pg)
    check(open_idx(st) == [], "375 carga: todas las opciones cerradas")
    check(all(not s["visible"] for s in st), "375 carga: ningún panel visible")
    check(all(s["tab"] == "0" for s in st), "375 carga: las 3 opciones enfocables (tabindex 0)")
    check(all(s["exp"] == "false" for s in st), "375 carga: aria-expanded=false en las 3")
    check(all(arrow_is_right(s["arrow"]) for s in st), "375 cerrado: flecha › (rotate 45deg)")
    check(pg.evaluate("document.documentElement.scrollWidth") <= 375, "375: sin scroll horizontal")
    pg.locator("#diploma").screenshot(path=os.path.join(CAP, "01-375-todo-cerrado.png"))

    titles = pg.locator("#diploma .e-n-tab-title")
    panels = pg.locator("#diploma .e-n-tabs-content > .e-con")

    # Opción 1 abierta
    titles.nth(0).click()
    pg.wait_for_timeout(500)
    st = states(pg)
    check(open_idx(st) == [0], "375 clic opción 1: solo la 1 abierta")
    check(st[0]["visible"] and not st[1]["visible"] and not st[2]["visible"], "375 opción 1: solo su panel visible")
    check(arrow_is_down(st[0]["arrow"]), "375 opción 1 abierta: flecha ⌄ (rotate 135deg)")
    check(arrow_is_right(st[1]["arrow"]), "375 opción 2 cerrada: flecha ›")
    b = [titles.nth(i).bounding_box() for i in range(3)]
    pb = panels.nth(0).bounding_box()
    check(b[0]["y"] < pb["y"] < b[1]["y"], "375 opción 1: su descripción queda JUSTO debajo de su título y encima de la 2")
    pg.locator("#diploma").screenshot(path=os.path.join(CAP, "02-375-opcion1-abierta.png"))

    # Clic en la 1 otra vez => cierra
    titles.nth(0).click()
    pg.wait_for_timeout(450)
    st = states(pg)
    check(open_idx(st) == [], "375 clic de nuevo en la abierta: se cierra")

    # Opción 3 abierta
    titles.nth(2).click()
    pg.wait_for_timeout(500)
    st = states(pg)
    check(open_idx(st) == [2], "375 clic opción 3: solo la 3 abierta")
    check(arrow_is_down(st[2]["arrow"]), "375 opción 3 abierta: flecha ⌄")
    check(arrow_is_right(st[0]["arrow"]), "375 opción 1 (ahora cerrada): flecha vuelve a ›")
    b = [titles.nth(i).bounding_box() for i in range(3)]
    pb = panels.nth(2).bounding_box()
    check(b[2]["y"] < pb["y"] and pb["y"] + pb["height"] <= pg.evaluate("document.querySelector('#diploma').getBoundingClientRect().bottom") + 1, "375 opción 3: descripción debajo de su título")
    pg.locator("#diploma").screenshot(path=os.path.join(CAP, "03-375-opcion3-abierta.png"))

    # Cambio directo 3 -> 2 y cierre de la 2
    titles.nth(1).click()
    pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [1], "375 clic opción 2 con la 3 abierta: solo la 2 abierta")
    titles.nth(1).click()
    pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [], "375 cerrar la 2: queda todo cerrado")

    # Teclado: Enter / Espacio abren y cierran
    titles.nth(1).focus()
    pg.keyboard.press("Enter"); pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [1], "375 teclado: Enter abre la 2")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [], "375 teclado: Enter sobre la abierta la cierra")
    pg.keyboard.press("Space"); pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [1], "375 teclado: Espacio abre la 2")
    pg.keyboard.press("Space"); pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [], "375 teclado: Espacio sobre la abierta la cierra")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(450)
    pg.keyboard.press("Tab"); pg.keyboard.press("Shift+Tab")
    focus_ok = pg.evaluate("document.activeElement.getAttribute('data-tab-index')") == "2"
    check(focus_ok and open_idx(states(pg)) == [1], "375 teclado: tras Tab+Shift+Tab el foco vuelve a la 2, que sigue abierta")
    pg.keyboard.press("Enter"); pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [], "375 teclado: Enter con foco en la 2 abierta la cierra")

    # Cambio de viewport 375 -> 1440 con todo cerrado: escritorio debe volver a tener una pestaña activa
    titles.nth(0).click(); pg.wait_for_timeout(450)
    titles.nth(0).click(); pg.wait_for_timeout(450)
    check(open_idx(states(pg)) == [], "375 previo al cambio de viewport: todo cerrado")
    pg.set_viewport_size({"width": 1440, "height": 900})
    pg.wait_for_timeout(400)
    st = states(pg)
    check(open_idx(st) == [0], "resize a 1440 desde todo cerrado: escritorio restaura la pestaña 1 (como nativo)")
    ctx.close()

    # ---------- ESCRITORIO 1440 (captura) ----------
    ctx, pg = new_page(1440, 900)
    st = states(pg)
    check(open_idx(st) == [0], "1440 carga: pestaña 1 activa (igual que nativo)")
    pg.locator("#diploma").screenshot(path=os.path.join(CAP, "04-1440-escritorio.png"))
    ctx.close()

    # ---------- INSTANCIAS MÚLTIPLES: dos secciones en la misma página ----------
    html = open(NEW, encoding="utf-8").read()
    # El último <script> del body es la réplica de Elementor (el del widget HTML va dentro de la sección)
    body_inner = html[html.index("<body>\n") + len("<body>\n"): html.rindex("<script>")]
    dup = html.replace(body_inner, body_inner + body_inner.replace('id="diploma"', 'id="diploma2"'), 1)
    dup_path = os.path.join(SP, "multi-preview.html")
    open(dup_path, "w", encoding="utf-8").write(dup)
    ctx, pg = new_page(375, 812, url=dup_path)
    pg.locator("#diploma .e-n-tab-title").nth(0).click(); pg.wait_for_timeout(450)
    check(open_idx(states(pg, "#diploma")) == [0] and open_idx(states(pg, "#diploma2")) == [], "2 instancias: abrir en la 1 no afecta a la 2")
    pg.locator("#diploma2 .e-n-tab-title").nth(2).click(); pg.wait_for_timeout(450)
    check(open_idx(states(pg, "#diploma2")) == [2] and open_idx(states(pg, "#diploma")) == [0], "2 instancias: cada una mantiene su estado")
    ctx.close()

    # ---------- REGRESIÓN ESCRITORIO: píxel a píxel contra la línea base original ----------
    diffs = {}
    for w in [1440, 1366, 1024, 800, 768]:
        shots = {}
        for name, url in [("base", BASE), ("new", NEW)]:
            ctx, pg = new_page(w, 900, url=url)
            pg.wait_for_timeout(300)
            path = os.path.join(SP, f"cmp_{name}_{w}.png")
            pg.screenshot(path=path, full_page=True)
            shots[name] = path
            ctx.close()
        a = Image.open(shots["base"]).convert("RGB")
        b = Image.open(shots["new"]).convert("RGB")
        if a.size != b.size:
            diffs[w] = f"tamaños distintos {a.size} vs {b.size}"
            continue
        bbox = ImageChops.difference(a, b).getbbox()
        diffs[w] = "idéntico" if bbox is None else f"DIFIERE en {bbox}"
    for w, r in diffs.items():
        check(r == "idéntico", f"regresión {w}px vs original: {r}")

    # Mismo chequeo en móvil: el original y la entrega deben diferir (la entrega sí cambia móvil)
    ctx, pg = new_page(375, 812, url=BASE)
    base_mobile_state = states(pg)
    ctx.close()
    notes.append("base original a 375 (referencia de cambio): " + str([s['sel'] for s in base_mobile_state]))

    browser.close()

print("\nerrores de consola/página:", errors if errors else "ninguno")
print("regresión escritorio:", diffs)
print("\nRESULTADO:", "OK" if not fails else f"{len(fails)} FALLOS")
for f in fails:
    print(" -", f)
