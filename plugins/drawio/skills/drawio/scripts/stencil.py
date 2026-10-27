"""Turn SVG path data into a draw.io stencil style: smooth custom shapes, the format the
freehand tool writes.

usage: python3 stencil.py [--fill | --stroke] [--box W H] "<path d>" ["<path d>" ...]

Coordinates are in a W x H box (default 100 x 100) that draw.io stretches to the cell's size:
set --box to the size you drew the path in, or the shape comes out scaled by the difference.
Absolute M, L, C, Q and Z only. Each path is a subpath of one shape; --fill fills and strokes them
with the cell's fillColor/strokeColor (gradients work), --stroke only strokes (the default).
Prints the style fragment to put in front of the cell's other keys.
"""
import base64
import re
import sys
import urllib.parse
import zlib

ARGS = {"M": 2, "L": 2, "Q": 4, "C": 6, "Z": 0}
TAGS = {"M": "move", "L": "line", "Q": "quad", "C": "curve"}
KEYS = {"M": "x y", "L": "x y", "Q": "x1 y1 x2 y2", "C": "x1 y1 x2 y2 x3 y3"}


def path_xml(d):
    tokens = re.findall(r"[MLQCZ]|-?\d*\.?\d+(?:e-?\d+)?", d.replace(",", " "))
    out, i = [], 0
    while i < len(tokens):
        cmd = tokens[i]
        if cmd not in ARGS:
            raise SystemExit(f"unsupported token {cmd!r}: use absolute M, L, Q, C, Z")
        i += 1
        if cmd == "Z":
            out.append("<close/>")
            continue
        n = ARGS[cmd]
        while i + n <= len(tokens) and tokens[i] not in ARGS:
            vals = tokens[i:i + n]
            attrs = " ".join(f'{k}="{v}"' for k, v in zip(KEYS[cmd].split(), vals))
            out.append(f"<{TAGS[cmd]} {attrs}/>")
            i += n
            cmd = "L" if cmd == "M" else cmd  # extra pairs after M are lines, as in SVG
    return "".join(out)


def main(argv):
    mode, w, h, paths = "stroke", "100", "100", []
    it = iter(argv)
    for a in it:
        if a == "--fill":
            mode = "fillstroke"
        elif a == "--stroke":
            mode = "stroke"
        elif a == "--box":
            w, h = next(it), next(it)
        else:
            paths.append(a)
    if not paths:
        raise SystemExit(__doc__)
    body = "<path>" + "".join(path_xml(p) for p in paths) + "</path>"
    xml = f'<shape w="{w}" h="{h}" aspect="variable" strokewidth="inherit"><foreground>{body}<{mode}/></foreground></shape>'
    raw = urllib.parse.quote(xml, safe="~()*!.'")
    packed = base64.b64encode(zlib.compress(raw.encode(), 9)[2:-4]).decode()
    print(f"shape=stencil({packed});")


if __name__ == "__main__":
    main(sys.argv[1:])
