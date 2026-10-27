"""Check a draw.io file, or XML exported from the editor, for silent mistakes.

usage: python3 check.py <file.drawio | page.xml> [page name]

Prints one line per problem and exits 1, or prints "ok" and exits 0.
"""
import base64
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib


def pages(root):
    if root.tag == "mxGraphModel":
        yield "page", root
        return
    for d in root.iter("diagram"):
        model = d.find("mxGraphModel")
        if model is None and (d.text or "").strip():
            raw = zlib.decompress(base64.b64decode(d.text.strip()), -15).decode()
            model = ET.fromstring(urllib.parse.unquote(raw))
        if model is not None:
            yield d.get("name", d.get("id", "?")), model


def cells(model):
    root = model.find("root")
    for el in [] if root is None else root:
        inner = el if el.tag == "mxCell" else el.find("mxCell")
        if inner is not None:
            label = el.get("label") if el.tag != "mxCell" else el.get("value")
            yield el.get("id") or inner.get("id"), inner, label or ""


def boxes_overlap(a, b):
    return a[0] < b[0] + b[2] and b[0] < a[0] + a[2] and a[1] < b[1] + b[3] and b[1] < a[1] + a[3]


def check(name, model):
    found, ids = [], {}
    rows = list(cells(model))
    for cid, c, _ in rows:
        if cid in ids:
            found.append(f"duplicate id {cid!r}")
        ids[cid] = c
    roots = [cid for cid, c, _ in rows if c.get("parent") is None]
    if len(roots) != 1:
        found.append(f"expected one root cell (no parent), found {roots}")
    for cid, c, label in rows:
        parent = c.get("parent")
        if parent is not None and parent not in ids:
            found.append(f"{cid}: parent {parent!r} does not exist")
        if parent == cid:
            found.append(f"{cid}: is its own parent (the whole page will be blank)")
        geo = c.find("mxGeometry")
        if c.get("edge") == "1":
            for end in ("source", "target"):
                ref = c.get(end)
                if ref is not None and ref not in ids:
                    found.append(f"edge {cid}: {end} {ref!r} does not exist")
            if geo is None:
                found.append(f"edge {cid}: no <mxGeometry relative=\"1\" as=\"geometry\"/>, so it is not drawn")
            elif not (c.get("source") and c.get("target")):
                pts = {p.get("as") for p in geo.findall("mxPoint")}
                missing = [e for e in ("source", "target") if not c.get(e) and f"{e}Point" not in pts]
                if missing:
                    found.append(f"edge {cid}: no {' or '.join(missing)} cell or point")
        if c.get("vertex") == "1":
            if geo is None:
                found.append(f"vertex {cid}: no geometry")
            if re.search(r"<\s*(b|i|u|br|font|div|span)\b", label, re.I) and "html=1" not in (c.get("style") or ""):
                found.append(f"vertex {cid}: HTML in the label but no html=1 in the style")
    # sibling vertices that overlap (a container and its own children never count)
    by_parent = {}
    for cid, c, label in rows:
        g = c.find("mxGeometry")
        if c.get("vertex") == "1" and g is not None and g.get("relative") != "1":
            box = tuple(float(g.get(k, 0)) for k in ("x", "y", "width", "height"))
            by_parent.setdefault(c.get("parent"), []).append((cid, label, box))
    for sibs in by_parent.values():
        for i, (a, la, ba) in enumerate(sibs):
            for b, lb, bb in sibs[i + 1:]:
                if boxes_overlap(ba, bb):
                    found.append(f"shapes overlap: {la or a!r} and {lb or b!r}")
    return [f"[{name}] {f}" for f in found]


def main():
    try:
        root = ET.parse(sys.argv[1]).getroot()
    except ET.ParseError as e:
        print(f"not well-formed XML: {e}")
        sys.exit(1)
    want = sys.argv[2] if len(sys.argv) > 2 else None
    problems = []
    for name, model in pages(root):
        if want is None or name == want:
            problems += check(name, model)
    print("\n".join(problems) or "ok")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
