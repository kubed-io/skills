# draw.io docs map

Where to look online for any draw.io fact. Fetch the page instead of guessing. URLs were checked on 2026-10-27.

**Fetch rules**
- `raw.githubusercontent.com` URLs are plain text. Fetch them whole or grep them, and prefer them over the `github.com/.../blob/...` page.
- `www.drawio.com/docs/...` pages are 30–400 KB of HTML. Fetch them with a `question`, or take the same page out of `llms-full.txt` (see "Docs index").
- The old `drawio.com/doc/faq/<slug>` and `diagrams.net/doc/faq/<slug>` links now 301 to `/docs/reference/<slug>` or `/docs/manual/...`. Some, such as `drawio-style-reference.html`, now 404, so always link to `/docs/`.
- Default branches: **jgraph/drawio `dev`**, **jgraph/drawio-desktop `dev`**, **jgraph/drawio-diagrams `dev`**, **jgraph/drawio-mcp `main`**, **jgraph/drawio-tools `main`**, **jgraph/drawio-react `main`**, **lgazo/drawio-mcp-server `main`**. jgraph/mxgraph is on `master` and is **archived**.

Short prefixes used below:
- `DOCS` = `https://www.drawio.com/docs`
- `MCP` = `https://raw.githubusercontent.com/jgraph/drawio-mcp/main`
- `SRC` = `https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp`
- `LG` = `https://raw.githubusercontent.com/lgazo/drawio-mcp-server/main`

## Docs index: start here when you don't know which page you need

| URL | What it answers | Cheap fetch |
|---|---|---|
| `https://www.drawio.com/llms.txt` | Curated index (about 6 KB) of the docs, the AI-generation pages and the MCP pages | Fetch it whole |
| `https://www.drawio.com/llms-full.txt` | Every docs page as Markdown in one 2.7 MB file. Each page starts with a `Source: <url>` line | Never read it whole. `curl` it and cut one page out with `awk -v u="Source: $URL" '$0==u{f=1;next} f&&/^Source: /{exit} f'`, or grep it for a key |
| `https://www.drawio.com/sitemap.xml` | Every docs URL (about 530 under `/docs/`) | Grep `<loc>` for a slug |
| `DOCS/` | Docs home: manual, reference, tutorials, troubleshooting | Usually not needed; use llms.txt |
| `DOCS/reference/` | Index of the technical reference: embed mode, URL params, configuration, shortcuts, plugins | Use it to find the slug, then fetch that page |

## Styles: keys, values, shapes, edges, perimeters

| URL | What it answers | Cheap fetch |
|---|---|---|
| `MCP/shared/style-reference.md` | **Authoritative style list**, taken from the draw.io source. Covers the style-string format, core and extended shapes, all property groups (fill/stroke, geometry, text, edges, arrows, connection points, containers, image, sketch, behaviour, data), edgeStyles, perimeters, colours and validation | 1,060 lines. Grep `^##` for the section, then grep the key, e.g. `strokeWidth` |
| `DOCS/reference/diagram-generation/style-reference/` | The same document as an HTML page | Prefer the raw `.md` above |
| `SRC/mxgraph/src/util/mxConstants.js` | Every `STYLE_*`, `SHAPE_*`, `EDGESTYLE_*`, `PERIMETER_*` and `ARROW_*` constant with its string value and JSDoc, in draw.io's maintained mxGraph fork | Grep `STYLE_<NAME> =` |
| `SRC/js/grapheditor/Graph.js`, `Shapes.js`, `Format.js` | Style keys that only draw.io has (they are not in mxGraph), custom shape classes, and the keys the Format panel edits | Large files; grep the key |
| `SRC/styles/default.xml` (`dark-default.xml`) | The default stylesheet: what `text`, `label`, `edgeStyle` and the other named style classes expand to | Small; fetch whole |
| `DOCS/manual/styles/shape-styles/` and `DOCS/manual/styles/connector-styles/` | Changing styles from the UI. Edit Style is Ctrl+E | Fetch with a question |
| `https://jgraph.github.io/mxgraph/docs/js-api/files/util/mxConstants-js.html` | Legacy mxGraph API docs. The repo is archived, but the constant docs are still valid | Prefer the raw `mxConstants.js` above |

## Shape names and stencils, e.g. the exact AWS, K8s or GCP style string

| URL | What it answers | Cheap fetch |
|---|---|---|
| `MCP/shape-search/search-index.json` | ~10,800 shapes as `{style,w,h,title,tags,type}`, built from the live app's sidebars and regenerated after each release. Powers the drawio-mcp `search_shapes` tool | 4.7 MB. Run `curl -s … \| jq -r '.[] \| select(.title\|test("lambda";"i")) \| .title+" \| "+.style'`. Prefer `aws4` over legacy `aws3` |
| `https://icons.diagrams.net/api/icons/search?q=<terms>&p=0&c=10` | The editor's icon service for brand logos and generic icons that are not in any library. Returns SVG URLs; use them as `shape=image;image=<url>` | JSON, small |
| `SRC/js/diagramly/sidebar/Sidebar-<Lib>.js` | One file per sidebar library (`AWS4`, `Kubernetes`, `GCP2`, `GCPIcons`, `Azure2`, `Cisco19`, `C4`, `BPMN`, `UML25`, …) with the exact style prefix and the per-shape suffix | Grep `createVertexTemplateEntry`. Base style vars sit at the top, e.g. `shape=mxgraph.kubernetes.` + `icon2;prIcon=pod` |
| `https://api.github.com/repos/jgraph/drawio/contents/src/main/webapp/js/diagramly/sidebar?ref=dev` | Lists every `Sidebar-*.js` (about 70 libraries) | Or `gh api` the tree and grep `Sidebar-` |
| `https://app.diagrams.net/stencils/<lib>.xml` (e.g. `kubernetes.xml`, `aws4.xml` at 6.6 MB, `gcp2.xml`) | Stencil geometry. `<shapes name="mxgraph.<lib>">` holds `<shape name="…">` entries. Style = `shape=mxgraph.<lib>.<name>` (lower-case, spaces become `_`) | Grep `<shape [^>]*name=`. The stencil XMLs are no longer in the drawio repo: they are bundled in `SRC/js/stencils.min.js` and served by the app |
| `SRC/js/diagramly/Editor.js` | Maps style prefixes to stencil files (`mxStencilRegistry.libraries[...]`) | Grep `mxStencilRegistry.libraries\['` |
| `MCP/plugins/claude-code/skills/drawio/scripts/find-shapes.js` | jgraph's offline shape-search script that ships with their skill | Read it to see how the index is queried |
| `DOCS/manual/shapes/shape-search/` and `DOCS/manual/editor/panels/shapes-panel/` | Finding shapes in the editor UI | Fetch with a question |

## File format: mxfile, compression, decoding

| URL | What it answers | Cheap fetch |
|---|---|---|
| `DOCS/reference/diagram-generation/` | File format overview, the simplified mxGraphModel-only form, the **Compressed format** recipe (encodeURIComponent → raw DEFLATE → Base64), the `#create` URL and layouts at open time | 270-line page; ask about "compressed format" or "#create" |
| `MCP/shared/mxfile.xsd` | XML Schema for `mxfile` / `diagram` / `mxGraphModel` / `mxCell` / `mxGeometry` / `UserObject` | 670 lines; grep the element |
| `MCP/shared/style-reference.md` §1, §14 | Minimal valid file, plus the `mxGraphModel` attributes (grid, page, `adaptiveColors`, …) | Grep `^## 1\.` / `^## 14\.` |
| `DOCS/manual/editor/save-file-formats/`, `DOCS/manual/export/xml-in-png/` | `.drawio` vs `.xml`, `.drawio.svg` / `.drawio.png` with the diagram embedded | Short pages |
| `DOCS/reference/style-compression/` | The opt-in "Compress Styles" mode (shared `<def>` entries) and which versions can read it | Short page |
| `https://jgraph.github.io/drawio-tools/` | Browser tools: decode/encode (`tools/text-tools.html`; `convert.html` redirects there), `mxfile-tools`, `merge`, `csv`, `viewer` | Human tools. Decode inline instead (below) |

Decode a compressed `<diagram>` body: `urllib.parse.unquote(zlib.decompress(base64.b64decode(s), -15).decode())`. That is raw inflate with wbits `-15`, not zlib. For a `#R`/`#S` URL hash, drop the leading letter first.

## AI generation references published by jgraph

| URL | What it answers | Cheap fetch |
|---|---|---|
| `MCP/shared/xml-essentials.md` | 10-line cheat sheet: skeleton, vertex, edge, labels, grid math, containers, lanes | Fetch whole |
| `MCP/shared/xml-reference.md` | Full XML generation guide: common styles, themes, HTML labels, edges, containers and swimlanes, **layers, tags, metadata and placeholders, dark-mode colours**, routing and layout passes, well-formedness | 540 lines; grep `^##` |
| `MCP/shared/mermaid-reference.md` | Mermaid hints for all 28 types draw.io parses, with ELK and styling notes | Grep `^## <Type>` |
| `MCP/shared/style-reference.md` | The "AI style reference" (see Styles) | — |
| `MCP/README.md`, `MCP/mcp-tool-server/README.md`, `MCP/mcp-app-server/README.md` | jgraph's own MCP servers (`create_diagram`, `search_shapes`, `get_drawio_reference`, `open_drawio_xml`) and how the index is built | Grep the tool name |
| `MCP/plugins/claude-code/skills/drawio/SKILL.md` | jgraph's Claude Code skill: Mermaid vs XML, the ELK/libavoid pipeline, desktop CLI export, URL output | 390 lines; grep `^##` |
| `https://www.drawio.com/mcp/` and `DOCS/manual/generate/drawio-mcp-server/` | Overview of the hosted MCP (`https://mcp.draw.io/mcp`), plugins and output formats | Fetch with a question |

## Import: Mermaid, CSV, PlantUML, other formats

| URL | What it answers | Cheap fetch |
|---|---|---|
| `DOCS/manual/mermaid/` and its subpages `mermaid-syntax/`, `mermaid-supported-diagram-types/`, `mermaid-layout-engine/` (ELK), `mermaid-config/` | Mermaid in draw.io: native conversion vs image, supported types, ELK | Short pages |
| `DOCS/manual/insert/insert-mermaid/` | Arrange ▸ Insert ▸ Mermaid dialog | Short |
| `https://github.com/jgraph/drawio/discussions/5643` | Canonical notes on the Mermaid dialog and Mermaid group, linked from mermaid-reference.md | Heavy GitHub page; ask a question |
| `DOCS/manual/insert/insert-from-csv/` | **CSV import config syntax**: `# label:`, `# style:`, `# parentstyle:`, `# namespace:`, `# connect: {json}`, `# layout:`, `# width/height`, `# identity`, … plus an org-chart example | Grep `^# ` in the llms-full section. (`DOCS/manual/import/insert-from-csv/` is only a stub) |
| `DOCS/manual/insert/insert_plantuml/` | Insert or convert PlantUML. Note the underscore in the slug | Short |
| `DOCS/manual/import/import-formats/` | Every importable format (vsdx, Gliffy, Lucidchart, SVG, …) | Short |

## Embed mode, URL parameters, editor configuration, libraries

| URL | What it answers | Cheap fetch |
|---|---|---|
| `DOCS/reference/embed-mode/` | **postMessage JSON protocol** (`proto=json`): `init`/`load` messages, the response format, autosave, and actions (`merge`, `patch`, `getDiff`, `dialog`, `prompt`, `template`, `layout`, `draft`, `status`, `spinner`, `export` with `xml\|json\|svg\|xmlsvg\|png`) | 600 lines; take the llms-full section and grep `^#### <action>` |
| `https://raw.githubusercontent.com/jgraph/drawio-react/main/src/protocol.ts` | The same protocol as TypeScript types, the most compact spec | Fetch whole (21 KB) |
| `DOCS/reference/supported-url-parameters/` | Every URL parameter (`libs`, `lightbox`, `chrome`, `ui`, `dark`, `create`, `layout`, …) | Grep the param name |
| `DOCS/reference/supported-location-hash-properties/` and `DOCS/manual/export/export-to-url/` | `#R`, `#U`, `#create` hashes: putting a diagram in a link | Short |
| `DOCS/reference/configure-diagram-editor/` | Configuration JSON: fonts, colours, `defaultVertexStyle`/`defaultEdgeStyle`, `defaultLibraries`, `customPresetColors`, CSS, … | 640 lines; grep the key |
| `DOCS/reference/format-custom-shape-library/` | `<mxlibrary>[{xml,w,h,title,aspect}]` JSON format, plus the template library format | Short |
| `DOCS/manual/advanced/custom-shape-libraries/` and `DOCS/manual/shapes/shape-complex-create-edit/` | Building libraries and stencil XML (`<shape><foreground>…`) | The stencil page is 220 KB; ask a question |
| `DOCS/reference/plugins/` | Editor plugins (`p=` param) | Short |

## Layout

| URL | What it answers | Cheap fetch |
|---|---|---|
| `DOCS/reference/json-layout-specification/` | **Layout JSON** for `layout=` / embed / CLI: `elkLayered`, `elkTree`, `elkRadial`, `elkOrganic`, `elkStress`, `elkDisco`, `elkBox` with `elk.*` options, legacy mx layouts, presets | 430 lines; grep `^### ` |
| `DOCS/manual/editor/menus/arrange-layout-menu/` | Arrange ▸ Layout menu items: flow, tree, circle, organic, org chart, parallels, custom | Short |
| `DOCS/manual/layouts/` and its subpages (`flow-layouts/`, `tree-layouts/`, `organic-layout/`, `radial-tree-layout/`, `org-chart-layout/`) | Layout dialogs and common options | Short |
| `SRC/js/diagramly/ElkLayout.js` | How draw.io maps ELK options onto cells | 33 KB; grep `elk.` |

## Export

| URL | What it answers | Cheap fetch |
|---|---|---|
| `https://raw.githubusercontent.com/jgraph/drawio-desktop/dev/src/main/args.js` | **Authoritative desktop CLI flags**: `-x/--export`, `-f` (`pdf\|png\|jpg\|svg\|xml\|html`, default pdf, inferred from `-o` extension), `-o`, `-e` embed diagram, `-b` border, `-s` scale, `--width/--height`, `-a`, `-p`, `-g`, `-l`, `-t`, `-u`, `--layout`, `--crop`, `--theme`, `--html-*`, `-c/--create`, `-k/--check` | Grep `long:`. The desktop README has no CLI section; `drawio --help` prints the same table |
| `MCP/plugins/claude-code/skills/drawio/SKILL.md` § "draw.io CLI" | Locating the CLI per OS (WSL2 too) and worked `drawio -x -f png -e -b 10 …` commands | Grep `-x -f` |
| `DOCS/manual/export/` and `export-diagram/`, `export-to-png/`, `export-to-svg/`, `export-to-pdf/`, `export-to-html/`, `export-to-json/` | Exporting from the web editor and its options | Short pages |
| `LG/TOOLS.md` § `export-diagram` | Exporting from the live editor through the MCP (svg/png/xml, scale, `embed_xml`, `output_path`) | Grep `export-diagram` |

## lgazo/drawio-mcp-server, the live editor this skill drives

| URL | What's there |
|---|---|
| `LG/README.md` | Overview, quick start (built-in editor or browser extension), features, the experimental Desktop note |
| `LG/TOOLS.md` | **Every tool's parameters and returns.** Document targeting (`target_document`), page targeting (`target_page` `{index}`/`{id}`), which tools are UI-bound, `list-paged-model` filters, `import-diagram`/`import-mermaid` modes |
| `LG/CONFIG.md` | CLI flags and env vars (`--editor`, `--transport`, ports 3333/3000, TLS, `--websocket-url`), configs for each MCP client |
| `LG/PROMPTS.md` | Two example prompts, including multi-page parallel agents |
| `LG/ARCHITECTURE.md` | WebSocket bridge and the per-document FIFO queue for live calls |
| `LG/TROUBLESHOOTING.md` | Debug logs, server down, port in use, HTTP transport |
| `LG/DESKTOP.md` | draw.io Desktop plugin setup; blocked by the desktop CSP (`connect-src 'self'`) |
| `LG/docs/PLUGINS.md` | Claude Code plugin and `drawio-mcp-server install <host>` |
| `LG/packages/drawio-mcp-server/docs/examples/LAYER_EXAMPLES.md` | Layer tool usage examples |

## Everything else

| Need | URL | Note |
|---|---|---|
| Keyboard shortcuts | `DOCS/reference/shortcuts/` (`SRC/shortcuts.svg` is the printable sheet) | Subpages per shortcut |
| Connectors and routing | `DOCS/manual/connectors/`, plus `waypoints-connectors/`, `connector-fixed-vs-floating/`, `connectors-auto-route/` | `style-reference.md` §5 lists the edgeStyle values |
| Containers, swimlanes, tables | `DOCS/manual/shapes/container-shapes/`, `DOCS/diagram-types/swimlane-diagrams/`, `DOCS/manual/shapes/tables/` | `xml-reference.md` "Containers and groups" for the XML |
| Layers | `DOCS/manual/layers/` (and `how-layers-work/`) | `xml-reference.md` "Layers" |
| Tags, tooltips, links | `DOCS/manual/links-tooltips-tags/` and `tags-in-diagrams/` | `xml-reference.md` "Tags" |
| Shape data and placeholders | `DOCS/manual/shapes/shape-data/`, `DOCS/manual/advanced/placeholders/`, `DOCS/reference/predefined-placeholders/` (`%page%`, `%date%`, …) | `placeholders=1` style key |
| Data-driven style rules | `DOCS/manual/pages/style-rules/` | Restyles shapes from their data |
| Dark mode and adaptive colours | `DOCS/manual/editor/appearance/adaptive-colours/`, `dark-mode/`, `dark-mode-design/` | `light-dark(#light,#dark)` values; `adaptiveColors` on mxGraphModel |
| Math labels | `DOCS/manual/text/math-typesetting/` | `math="1"` on the model |
| Example diagrams | `https://github.com/jgraph/drawio-diagrams` (`dev`: `examples/`, `templates/`) and `SRC/templates/` | Real styles to copy |
| Repo READMEs | `https://raw.githubusercontent.com/jgraph/drawio/dev/README.md`, `https://raw.githubusercontent.com/jgraph/drawio-desktop/dev/README.md` | Licences, scope, self-hosting |
