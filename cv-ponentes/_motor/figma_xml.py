"""Lee el XML de get_metadata de Figma (guardado en archivo) y lo convierte en árbol de nodos."""
import json, re

TAG = re.compile(r'<(/?)([\w-]+)((?:\s+[\w-]+="[^"]*")*)\s*(/?)>', re.S)
ATTR = re.compile(r'([\w-]+)="([^"]*)"', re.S)


class Node:
    def __init__(self, tag, a, parent=None):
        self.tag, self.a, self.parent, self.kids = tag, a, parent, []
        self.id, self.name = a.get('id', ''), a.get('name', '')
        self.x, self.y = float(a.get('x', 0)), float(a.get('y', 0))
        self.w, self.h = float(a.get('width', 0)), float(a.get('height', 0))
        self.hidden = a.get('hidden') == 'true'

    def walk(self):
        yield self
        for k in self.kids:
            yield from k.walk()

    def find(self, pred):
        return [n for n in self.walk() if pred(n)]

    def first(self, pred):
        r = self.find(pred)
        return r[0] if r else None

    def abs_xy(self, upto=None):
        """Posición relativa a `upto` (un ancestro). En el XML de Figma x/y son relativos al padre."""
        x, y, n = self.x, self.y, self.parent
        while n is not None and n is not upto:
            x += n.x; y += n.y; n = n.parent
        return x, y

    def __repr__(self):
        return f'<{self.tag} {self.id} "{self.name[:40]}" {self.x:.1f},{self.y:.1f} {self.w:.1f}x{self.h:.1f}>'


def parse(xml):
    root = Node('root', {})
    cur = root
    for m in TAG.finditer(xml):
        close, tag, attrs, selfclose = m.groups()
        if close:
            cur = cur.parent or root
            continue
        n = Node(tag, dict(ATTR.findall(attrs)), cur)
        cur.kids.append(n)
        if not selfclose:
            cur = n
    return root


def load_tool_result(path):
    """Archivo guardado por la herramienta (JSON [{type,text}]) o XML plano."""
    raw = open(path, encoding='utf-8').read()
    if raw.lstrip().startswith('['):
        raw = ''.join(x.get('text', '') for x in json.loads(raw) if x.get('type') == 'text')
    return parse(raw)


def frame(root, fid):
    n = root.first(lambda n: n.id == fid)
    if n is None:
        raise KeyError(f'no existe el nodo {fid}')
    # el frame de nivel superior tiene x/y absolutos en el lienzo: se toma como origen
    n.parent = None
    return n
