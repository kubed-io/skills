# draw.io styling and layout

1. [Color](#color) · 2. [Fonts and text](#fonts-and-text) · 3. [Sizes and spacing](#sizes-and-spacing)
4. [Edges](#edges) · 5. [Choosing a shape](#choosing-a-shape) · 6. [Looks](#looks) · 7. [Self-review](#self-review)

## Color

**Role palette** (draw.io's own swatches; `fill / stroke`). One color per role, two to four roles
per diagram. Same role, same color, everywhere.

| Role | fillColor | strokeColor |
|---|---|---|
| Step, service, component | `#dae8fc` | `#6c8ebf` |
| Start/end, success, output | `#d5e8d4` | `#82b366` |
| Decision, queue, warning | `#fff2cc` | `#d6b656` |
| External system, gateway, waiting | `#ffe6cc` | `#d79b00` |
| Error, alert, cancel | `#f8cecc` | `#b85450` |
| Security, special step | `#e1d5e7` | `#9673a6` |
| Neutral, out of scope | `#f5f5f5` | `#666666` (add `dashed=1` for external) |

- Containers and lanes take a pale tint of their content's color, or `fillColor=none`. Pale lane
  fills: `#f5f5f5 #e8f4f8 #fff0e6 #e8f5e9 #fff9e6 #fce4ec`.
- Add a small legend only when colour carries a meaning the shapes and labels don't already show,
  listing only the roles actually used.
- Never let color be the only signal; pair it with shape, dash or label.

**Light and dark.** With `adaptiveColors="auto"` on `mxGraphModel`, draw.io renders unset colors
(`default`) black-on-white or white-on-black, and derives a dark variant of every explicit hex color
automatically. Usually that is enough. When the derived color is poor, give both:
`fillColor=light-dark(#dae8fc,#1e3a5f)`. For a deliberately dark page that should not adapt, set
`background="#0F172A"` and `adaptiveColors="none"`, then set `fontColor` on every cell and
`strokeColor`/`fontColor` on every edge (they default to black and vanish):

| Dark-page role | fill / stroke | Text and edges |
|---|---|---|
| Step | `#1E293B` / `#60A5FA` | `fontColor=#F1F5F9` |
| Decision | `#1E293B` / `#FBBF24` | edges `strokeColor=#94A3B8;fontColor=#E2E8F0` |
| Start/end | `#064E3B` / `#34D399` | edge labels `labelBackgroundColor=#0F172A` |
| Error | `#450A0A` / `#F87171` | |

Useful color keywords: `none` (transparent), `default` (theme color), `inherit` (parent's),
`parentFillColor`, `fillColor=strokeColor` (solid fill in the stroke color).

## Fonts and text

- Default `fontFamily=Helvetica;fontSize=12`. Titles and container headers `fontSize=14;fontStyle=1`.
  Edge labels 11. For slides or PDFs, go larger (16–18).
- Web font: `fontFamily=Inter;fontSource=https%3A%2F%2Ffonts.googleapis.com%2Fcss%3Ffamily%3DInter;`
  (the CSS URL, URL-encoded). Put the font on every cell; there is no reliable page-wide default.
- Label budget: roughly 7 px per Latin character at 12 px; ~2× that for CJK. If text does not fit,
  enlarge the box or shorten the text. Do not shrink the font.
- Two-line labels: name on line one, detail on line two (`&lt;b&gt;Name&lt;/b&gt;&lt;br&gt;detail`).
  Drop redundant words ("ECR Container Registry" → "ECR").
- Match the label language to the user's language.
- `text;html=1;` is a frameless label (titles, notes); `align=left;verticalAlign=top;` for blocks.

## Sizes and spacing

Snap every x, y, width and height to multiples of 10.

| Element | Size |
|---|---|
| Process / service box | 140×60 (120–160 wide) |
| Decision diamond | 140×80 to 160×90 |
| Circle / start-end | 60×60 (`aspect=fixed`) or ellipse 120×60 |
| Cylinder (database) | 100×70 |
| Document, note | 120×80 |
| Vendor icon | 48–78 square, label below, one free row under each icon row |
| Swimlane header | `startSize=30` (top) or 110 (left, `horizontal=0`) |

**Grid placement** keeps hand layouts honest: column x = `40 + col×180`, row y = `40 + row×120`,
one node per cell. That leaves ~40 px horizontal and ~60 px vertical between 140×60 boxes —
enough for unlabeled edges.

- **Widen when edges carry labels or the graph is dense:** 200 px gaps for ≤5 nodes, 280 for 6–10,
  350 for more; ≥220 px between icons whose edges are labeled. Leave an ~80 px empty corridor
  between rows/columns where long edges can run.
- **Flow direction:** pick one. Top-down for hierarchies and ≥4 tiers; left-right for pipelines,
  request paths and swimlane processes. Users/clients at the start, data stores at the end,
  auxiliary paths (monitoring, DLQ, errors) below the main flow.
- **Hubs in the middle:** put a bus/broker/gateway between the nodes that use it, so edges stay
  short and radial instead of crossing the canvas. Route many-to-many dependencies through it.
- **Align centres:** a child directly under its parent shares its centre x; that is what makes
  the connector straight.
- **Container padding:** ≥20–30 px between a container border and its children, plus the header.
- **Lanes:** stacked at x=0, y=`lane×150`, height 150; nodes inside at x=`120+col×180`, y=45.
  Cross-lane edges belong to the layer, not a lane.
- More than ~15–20 nodes: stop hand-placing; use Mermaid with an ELK layout or split into pages.

## Edges

| Diagram | Edge style |
|---|---|
| Flowchart, architecture, cloud, k8s, swimlane | `edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;` |
| Org chart, tree | `edgeStyle=orthogonalEdgeStyle;endArrow=none;html=1;` |
| ER | `edgeStyle=entityRelationEdgeStyle;html=1;` + `startArrow`/`endArrow` from `ERmandOne ERone ERmany ERoneToMany ERzeroToOne ERzeroToMany` |
| UML class | orthogonal; inheritance `endArrow=block;endFill=0;`, realisation adds `dashed=1`, composition `endArrow=diamondThin;endFill=1;`, aggregation `endFill=0` |
| State, use case | straight (no `edgeStyle`); `endArrow=open;` / `endArrow=none;` |
| Network cable | straight, `endArrow=none;`, `dashed=1` for wireless/VPN |
| Mind map | `curved=1;endArrow=none;` |

- Labels: one to three words. Skip labels that repeat the obvious. Put explanations in node text.
- Add `labelBackgroundColor=default;defaultLabelBackgroundColor=page;` so the line breaks around
  the text instead of under a white chip; `labelPlacement=auto` lets newer draw.io place it.
- One meaning per line style, and say it in a legend: e.g. solid = sync call, dashed = async/optional,
  red dashed (`strokeColor=#b85450`) = error path. `strokeWidth=2` for the main flow only.
- Prefer two one-way arrows over one double-headed arrow when the two directions differ.
- Unavoidable crossings: `jumpStyle=arc;jumpSize=10;` draws a bridge.
- Main-flow arrowheads `endArrow=block;endSize=8` read clearly; thin heads look like they pierce
  the target.
- Decision branches: label every outgoing edge (Yes/No). Exits leave outward from the vertex they use.

## Choosing a shape

Start from the semantic shape; reach for a vendor stencil only when identity matters.

| Meaning | Style |
|---|---|
| Process / service | `rounded=1;whiteSpace=wrap;html=1;` |
| Decision | `rhombus;whiteSpace=wrap;html=1;` |
| Start / end | `ellipse;` or `rounded=1;arcSize=50;` |
| Database, storage | `shape=cylinder3;boundedLbl=1;size=15;` |
| Document | `shape=document;` · note `shape=note;` · card `shape=card;` |
| Input/output | `shape=parallelogram;perimeter=parallelogramPerimeter;` |
| Queue / step | `shape=process;` · chevron `shape=step;perimeter=stepPerimeter;` |
| Cloud, internet | `ellipse;shape=cloud;` (add `perimeter=cloudPerimeter;`) |
| Person | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;` |
| Hexagon | `shape=hexagon;perimeter=hexagonPerimeter2;` |
| Free text | `text;html=1;` |
| Container | `swimlane;startSize=30;` / `group;` |
| Sequence lifeline | `shape=umlLifeline;perimeter=lifelinePerimeter;container=1;` (Mermaid is easier) |
| ER table | `shape=table;childLayout=tableLayout;startSize=30;container=1;` with `shape=tableRow` rows |

**Vendor stencils: never guess the name.** A wrong `mxgraph.*` name renders an empty box with no
error. Look it up in the shape library (by id, e.g. `mxgraph.aws4.athena`) and copy the returned
style and size verbatim. Known shapes of the major libraries:

- **AWS (`mxgraph.aws4`)**, two patterns. Service icon:
  `shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=#ED7100;strokeColor=#ffffff;`
  78×78, label below. The white stroke draws the glyph; without it the icon is a blank square.
  Resource icon: `shape=mxgraph.aws4.lambda_function;fillColor=#ED7100;strokeColor=none;` 48×48.
  Category fills: compute `#ED7100`, database `#C925D1`, networking/analytics `#8C4FFF`, storage
  `#7AA116`, security `#DD344C`, integration `#E7157B`, ML `#01A88D`. Groups:
  `shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc;strokeColor=#8C4FFF;fillColor=none;`
  (also `group_aws_cloud_alt`, `group_region`, `group_availability_zone`, `group_public_subnet`,
  `group_private_subnet`, `group_security_group`). Group boxes stay unfilled. Renamed services
  keep old stencil names (OpenSearch is `elasticsearch_service`).
- **Kubernetes:** see [diagrams/kubernetes.md](diagrams/kubernetes.md).
- **GCP:** current product icons are `shape=image` styles carrying an inline SVG, not
  `mxgraph.gcp2.<product>` stencils. Copy the style from the library; do not write a name.
  `mxgraph.gcp2.*` holds generic pictograms and product cards.
- **Azure:** `image;aspect=fixed;html=1;image=img/lib/azure2/<category>/<Name>.svg;`. The relative
  `img/lib/…` path only resolves inside the editor; in a standalone file use
  `https://app.diagrams.net/img/lib/…`.
- **Networks:** `shape=mxgraph.networks.{router,switch,firewall,server,load_balancer,cloud}`;
  Cisco `mxgraph.cisco19.*`; racks `mxgraph.rack.*`; BPMN `mxgraph.bpmn.*`; flowchart
  `mxgraph.flowchart.*`; UI mockups `mxgraph.mockup.*`.

## Looks

Apply a requested look to every cell, not just the first few. Keep one look per diagram, and keep
it when making later changes.

| Look | Keys |
|---|---|
| Rounded | `rounded=1;arcSize=10` (5–50) |
| Shadow | `shadow=1` |
| Hand-drawn | `sketch=1;curveFitting=1;jiggle=2;` + `fontFamily=Architects Daughter` with its `fontSource` |
| Hatched fill | `sketch=1;fillStyle=hachure;` (`cross-hatch`, `dots`, `zigzag-line`) |
| Gradient | `gradientColor=#7ea6e0;gradientDirection=south;` |
| Faded | `opacity=50` (or `fillOpacity`, `strokeOpacity`, `textOpacity`) |
| Stack of copies | `multiple=1;multipleCount=3;` (replicas, instances) |
| Animated flow | `flowAnimation=1;` on an edge (animates the line in the editor and SVG export) |
| Monochrome / print | fills `#FFFFFF`/`#F3F4F6`, strokes and text `#111827`, errors dashed |

## Self-review

Check after every draft, and again after every batch of edits. Read the model back (the touched
ids, or the page as XML) rather than trusting what you meant to write; a screenshot can both miss
defects and invent them.

- [ ] Every vertex has a label; nothing sits at the same x,y as a sibling; no sibling boxes overlap.
- [ ] Children lie fully inside their container, with padding and below the header.
- [ ] Every edge has a source and target that exist; nothing dangles or floats unintentionally.
- [ ] No edge passes through a shape it does not connect; crossings are minimal and bridged if kept.
- [ ] Several edges on one side are spread out, not stacked; final segments ≥20 px before arrowheads.
- [ ] Labels fit their boxes (no spill, no surprise wrap); edge labels touch no shape, line or label.
- [ ] Centres aligned along the flow; spacing even; one flow direction.
- [ ] Each color and line style means one thing; a legend says what when the shapes and labels don't.
- [ ] Vendor icons render (no empty boxes) and use the current library's names.
- [ ] Decision branches all labeled; external systems visibly outside the system boundary.
- [ ] Stop after two or three repair rounds; report what remains instead of looping.
