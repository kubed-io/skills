# draw.io XML (mxGraph) authoring reference

The same XML goes into a `.drawio` file and into `import-diagram`; the same `style`
strings go into `add-cell-of-shape` and `edit-cell`.

1. [Skeleton](#skeleton) · 2. [Vertices](#vertices) · 3. [Edges](#edges) · 4. [IDs](#ids)
5. [Labels and escaping](#labels-and-escaping) · 6. [Containers](#containers-groups-swimlanes)
7. [Layers](#layers) · 8. [Tags, metadata, links](#tags-metadata-links)
9. [Pages and compressed diagrams](#pages-and-compressed-diagrams)
10. [Well-formedness](#well-formedness) · 11. [Common mistakes](#common-mistakes-and-fixes)

## Skeleton

Minimal model (what `import-diagram` needs):

```xml
<mxGraphModel adaptiveColors="auto">
  <root>
    <mxCell id="0"/>
    <mxCell id="1" parent="0"/>
  </root>
</mxGraphModel>
```

File form: wrap it as `<mxfile><diagram id="p1" name="Page-1"><mxGraphModel>…</mxGraphModel></diagram></mxfile>`.
One `<diagram>` per page, each with a unique `id`.

- `id="0"` is the root, has no parent. `id="1"` is the default layer, `parent="0"`. Both always exist.
- Content cells go on a layer (`parent="1"`) or inside a container (`parent="<container id>"`).
- `adaptiveColors="auto"` lets draw.io adapt explicit colors for dark mode. Optional `mxGraphModel`
  attributes: `grid="1" gridSize="10" page="1" pageWidth="850" pageHeight="1100"` and
  `background="#hex"` (page color).
- Coordinates: origin top-left, x right, y down. Keep everything at x,y ≥ 0.
- Always write uncompressed XML.

## Vertices

```xml
<mxCell id="api" value="Orders API" style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
  <mxGeometry x="40" y="40" width="140" height="60" as="geometry"/>
</mxCell>
```

- `vertex="1"` and `edge="1"` are mutually exclusive.
- Every vertex needs an `mxGeometry` with numeric `x y width height` and `as="geometry"`.
- Style is `key=value;` pairs, case-sensitive, no spaces around `=`/`;`, booleans are `0`/`1`.
  A bare token (`ellipse;`, `rhombus;`, `swimlane;`, `text;`, `group;`) is a style class that sets
  shape plus defaults. Unknown keys are ignored silently, so a typo fails quietly.
- Non-rectangular shapes need the matching `perimeter=` (e.g. `shape=hexagon;perimeter=hexagonPerimeter2;`)
  or edges stop at the bounding box. `ellipse` and `rhombus` classes already include theirs.

## Edges

```xml
<mxCell id="e-api-db" value="reads" style="edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;"
        edge="1" parent="1" source="api" target="db">
  <mxGeometry relative="1" as="geometry"/>
</mxCell>
```

- **Never self-closing.** An edge without `<mxGeometry relative="1" as="geometry"/>` does not render.
- `source`/`target` must be ids of existing cells (for an `object`/`UserObject`, the wrapper's id).
- **Default: declare source and target, nothing else.** draw.io routes it. Its router is simple:
  straight or one right-angle path, and it does not avoid shapes. Fix crossings by placement first.
- **Fixed connection points** pin where an edge leaves/enters, as fractions of the shape box:
  `exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;`
  (0,0 top-left; 0.5,1 bottom-centre). Use them when several edges share a side (spread them:
  0.25/0.5/0.75), or to force a straight vertical/horizontal run. Exits must point outward from
  the side they leave. A 1–2 px misalignment between exit and entry renders as an S-wiggle; compute
  `entryX = (sourceCentreX - target.x) / target.width` exactly rather than rounding.
- **Waypoints** (absolute coordinates in the edge parent's frame), only when an edge must detour:

  ```xml
  <mxGeometry relative="1" as="geometry">
    <Array as="points"><mxPoint x="300" y="150"/><mxPoint x="300" y="250"/></Array>
  </mxGeometry>
  ```
- **Obstacle-avoiding routing:** `edgeStyle=orthogonalEdgeStyle;libavoidRouting=1;` asks a recent
  draw.io editor to route around shapes (`libavoidSpacing=16` default). Viewers that lack it fall
  back to plain orthogonal. Manual waypoints and `libavoidRouting` do not mix.
- **Floating edge** (no terminals): `<mxPoint x=".." y=".." as="sourcePoint"/>` and `as="targetPoint"`
  inside the geometry. Needed when an end attaches to nothing (e.g. an arrow into a text block).
- **Edge label** is the edge's `value`. Position along the edge with geometry `x` (−1 at source,
  0 middle, 1 at target), perpendicular shift with `y`, and a pixel nudge with
  `<mxPoint x="0" y="-20" as="offset"/>`. A decision outcome on a long edge sits near the start
  (`x="-0.6"`).
- **Extra labels on one edge** (multiplicities, roles) are child vertices of the edge:

  ```xml
  <mxCell id="e1-src" value="1..*" style="edgeLabel;html=1;align=left;resizable=0;inheritText=1;"
          vertex="1" connectable="0" parent="e1">
    <mxGeometry x="-0.8" relative="1" as="geometry"><mxPoint x="0" y="-10" as="offset"/></mxGeometry>
  </mxCell>
  ```
- **Edge parent:** the innermost container holding both ends; `parent="1"` if either end is outside
  every container. Layout passes read edge points in the parent's frame.
- Arrowheads: `endArrow`/`startArrow` = `classic` (default end), `block`, `open`, `oval`, `diamond`,
  `diamondThin`, `none`, `ERmandOne`, `ERmany`, `ERzeroToMany`…; `endFill=0` for hollow; `endSize=8`.

## IDs

- Unique within a page. Never give content cells `0` or `1`.
- Prefer stable, meaningful ids (`svc-orders`, `e-orders-db`) over counters: later edits address
  cells by id (`edit-cell`, `delete-cell-by-id`), and a diff of the file stays readable.
- With an `object`/`UserObject` wrapper the id lives on the wrapper, not the inner `mxCell`.

## Labels and escaping

- Put `html=1` in every style. It enables `<b> <i> <u> <br> <font> <hr> <ul> <table> <sub> <sup>`
  and does nothing harmful to plain text. Without it, tags render literally.
- Labels are attribute values, so markup must be XML-escaped:
  `value="&lt;b&gt;Orders&lt;/b&gt;&lt;br&gt;Spring Boot"`. Escape `&` as `&amp;` ("R&amp;D"),
  `"` as `&quot;`. `&nbsp;` is not an XML entity; use `&#160;`.
- Line break: `&lt;br&gt;` (with html=1) or `&#xa;` (works either way). Never a literal `\n`.
- `whiteSpace=wrap` wraps text inside the box; without it long labels spill out.
- Whole-label emphasis: `fontStyle` bitmask (1 bold, 2 italic, 4 underline, add to combine).
  Use `<b>` only for part of a label. Do not use both for the same effect.
- Label outside the shape (icons): `verticalLabelPosition=bottom;verticalAlign=top;`. Add
  `labelPerimeter=1` so edges arriving from below stop at the label, not inside it.

## Containers, groups, swimlanes

Children set `parent="<container id>"` and use coordinates **relative to the container's
top-left**. Placing a shape on top of a bigger shape is not containment; draw.io will not move them
together.

| Need | Style |
|---|---|
| Titled box, may itself have edges | `swimlane;startSize=30;html=1;` (header height = `startSize`) |
| Lane with header on the left | `swimlane;horizontal=0;startSize=110;html=1;` |
| Invisible grouping | `group;` (no fill/stroke, ignores pointer events) |
| Any shape as container | append `container=1;pointerEvents=0;` |
| No collapse button | `collapsible=0;` |

- The container must be big enough for its children. Child y should clear the header:
  `y ≥ startSize + 10`. Leave ~20–30 px padding on every side.
- `pointerEvents=0` keeps a container from swallowing clicks/connections meant for its children.
  Leave it off (use `swimlane`) only when the container itself is an edge endpoint.
- Edges from a child to something outside naturally cross the container border; no special routing.
- Nesting (VPC → AZ → subnet → instance) is just containers inside containers, each child relative
  to its immediate parent.
- `childLayout=stackLayout;horizontalStack=0;resizeParent=1;` stacks children (lists, UML members).
- Two-axis grid (actor × phase): `shape=table;childLayout=tableLayout;startSize=0;collapsible=0;`
  with rows `shape=tableRow;horizontal=0;startSize=0;collapsible=0;` and plain cells inside rows.
  Steps go inside a cell (`parent` = cell). Cross-cell edges use `parent="1"`.
- Do not hand-write `<mxRectangle as="alternateBounds">`; draw.io adds it when a box is collapsed.

## Layers

A layer is an `mxCell` with `parent="0"` and no `vertex`/`edge`:

```xml
<mxCell id="lyr-notes" value="Annotations" parent="0"/>
<mxCell id="n1" value="deprecated" style="text;html=1;" vertex="1" parent="lyr-notes">…</mxCell>
```

Later layers draw on top. `visible="0"` on the layer hides it. Every cell is on exactly one layer
(through its top-level ancestor). Use layers for toggleable views (physical vs logical vs security).

## Tags, metadata, links

Wrap the cell in `<object>` (or `<UserObject>`, same meaning) to attach data. The wrapper takes
`id` and `label` (instead of `value`); the inner `mxCell` keeps style, parent, vertex/edge, geometry.

```xml
<object id="svc-auth" label="&lt;b&gt;%name%&lt;/b&gt;&lt;br&gt;%owner%" placeholders="1"
        name="Auth" owner="platform" tags="critical v2" tooltip="Issues tokens">
  <mxCell style="rounded=1;whiteSpace=wrap;html=1;" vertex="1" parent="1">
    <mxGeometry x="40" y="40" width="160" height="60" as="geometry"/>
  </mxCell>
</object>
```

- Custom properties are plain attributes. `placeholders="1"` substitutes `%key%` in the label;
  lookup walks up the parents. Built-ins: `%id% %page% %pagenumber% %date%`; `%%` is a literal %.
- `tags` is space-separated; viewers filter by tag (Edit ▸ Tags). Tags do not affect structure.
- `link="https://…"` makes the shape a hyperlink; `link="data:page/id,<diagram id>"` jumps to
  another page (drill-down from overview to detail).
- Style values can't read data in the shipped editor. jgraph's style reference describes
  `stylePlaceholders=1` (`fillColor=%color%`), but draw.io 32.6 doesn't implement it and the
  placeholder is drawn literally. Write the colour into the style.

## Pages and compressed diagrams

- Each `<diagram>` is a page. Its body is either a plain `<mxGraphModel>` or a compressed blob;
  pages in one file can differ, so detect per page (body starts with `<` or not).
- Decode a blob: base64 → raw inflate (no zlib header) → URL-decode.

  ```python
  import base64, zlib, urllib.parse
  xml = urllib.parse.unquote(zlib.decompress(base64.b64decode(blob), -15).decode())
  ```
  Node: `decodeURIComponent(zlib.inflateRawSync(Buffer.from(blob, "base64")).toString())`.
- Write pages back uncompressed. The same encoding (deflateRaw of the URL-encoded XML, base64)
  is what `https://app.diagrams.net/#R<urlencoded blob>` links carry.

## Well-formedness

- No XML comments in generated diagrams. They waste tokens, and `--` inside one is illegal XML.
- All attribute values double-quoted and escaped (`&amp; &lt; &gt; &quot;`).
- Nothing outside the root element: no code fences, prose, or stray closing tags around the XML.
- Every `parent`, `source`, `target` resolves to an id on the same page.
- No negative width/height; vertices have full geometry; edges have relative geometry.

## Common mistakes and fixes

Drawn from what draw.io's own repair and normalization passes fix, and from linters in the
community skills. Each one is silent: the diagram loads, it just looks wrong or empty.

| Symptom | Cause | Fix |
|---|---|---|
| Whole diagram blank | Default layer written as `<mxCell id="1" parent="1"/>` | `parent="0"` |
| Whole diagram blank / rejected | Missing cell `0` or `1`; text around the XML | Add both; strip everything outside `<mxfile>`/`<mxGraphModel>` |
| Parse error on import | Raw `<b>` in `value`, bare `&` ("R&D"), `&nbsp;` | Escape to `&lt;b&gt;`, `&amp;`, `&#160;` |
| Edge missing | Self-closing edge, no `mxGeometry` | Add `<mxGeometry relative="1" as="geometry"/>` |
| Edge missing or dangling | `source`/`target` id typo, or points at the inner mxCell of an object | Use an existing id (the wrapper's) |
| Cell vanishes | `parent` points at a nonexistent id | Point at a real layer/container |
| Child drawn outside its box | Child coords written as absolute, or container too small | Make coords relative; grow the container |
| Edge jumps out of its container after layout | Edge parked on `parent="1"` while both ends are inside one container | Parent = innermost common container |
| Labels show `<b>` literally | `html=1` missing | Add `html=1` |
| Label shows `\n` | Literal backslash-n | `&lt;br&gt;` or `&#xa;` |
| Text spills past the box | No `whiteSpace=wrap`, or box too small | Add wrap; enlarge box rather than shrink font |
| Icon renders as empty box | Guessed `shape=mxgraph.*` name | Look up the exact style (shape search); never guess |
| Edge stops short of a diamond/hexagon outline | Missing `perimeter=` | Add the matching perimeter |
| Line runs through a shape | Default router ignores obstacles | Move the shape, pin exit/entry, add waypoints, or `libavoidRouting=1` |
| Arrowhead sits on a bend | Final segment < ~20 px | More spacing, or move the bend |
| Two nodes stacked on one spot | Same x,y | One grid cell per node |
| Edges pile onto one point | Many edges, same side, floating ends | Spread with exit/entry 0.25/0.5/0.75 |
| Image icons broken outside the editor | `image=img/lib/...` relative path | Use an absolute `https://app.diagrams.net/img/lib/...` URL or a data URI |
| Reserved id clash | Content cell with id `0`/`1` | Renumber |
| Duplicate ids | Copy-paste of a cell block | Unique ids per page |
