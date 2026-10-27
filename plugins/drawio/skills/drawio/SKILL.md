---
name: drawio
description: "Use when creating, reading or changing a draw.io (diagrams.net) diagram: one open in a live editor through the drawio MCP tools (list-documents, list-paged-model, edit-cell, add-edge, import-diagram), a .drawio file, or mxGraph XML. Also use when you need a draw.io shape or icon style (Kubernetes, AWS, GCP, Azure), a style key, or where draw.io documents something."
---

# draw.io

A draw.io diagram is mxGraph XML: cells with an id, a parent, a geometry and a
`key=value;` style string. Getting a diagram right is rarely the hard part. Doing
it without wasting a hundred thousand tokens, and without tripping over the live
editor, is what this skill is for.

## Pick the mode

| You have | Do |
|---|---|
| drawio MCP tools, and `list-documents` returns a document | **Live mode**, below. Edit the open diagram in place |
| No connected editor | **File mode**: write the `.drawio` XML yourself ([xml.md](references/xml.md)) |
| A whole new diagram to draw in live mode | Write the XML once, then one `import-diagram` with `mode: new-page` or `add`, instead of dozens of add calls |

## Live mode

The tools come from [lgazo/drawio-mcp-server](https://github.com/lgazo/drawio-mcp-server).
Each call acts on a draw.io tab someone has open, so what you change appears in
front of them.

**Load only the tools you need.** Where tool schemas load on demand (Claude
Code's ToolSearch), select them by name. Loading all thirty costs about 25 KB.
An edit needs `list-documents`, `list-pages`, `export-diagram`, `edit-cell`,
`add-rectangle`, `add-edge`, `edit-edge`; a new page needs `list-documents`,
`list-pages`, `import-diagram`, `export-diagram`.

**Target.** Call `list-documents` first. With one document connected,
`target_document` is optional; with several, pass it on every call. Its id is a
browser tab, not a file. Name pages by `{id}` from `list-pages`: indexes shift
when someone adds a page. Touch only the page you were asked about — another
person or agent may be working on the next one.

### Read the least you can

Cheapest first:

1. **`get-selected-cell`** — when the user says "this box", ask them to select it.
2. **`list-paged-model` with a `filter`** and a small `page_size`. Filter by
   `ids`, `parent_ids`, `cell_type`, or `attributes`, which also matches style
   keys: `["and", ["equal", "shape", "cylinder3"], ["equal", "fillColor", "#fff2cc"]]`.
   `cell_type: "vertex"` still returns the root and layer cells; skip them.
3. **`export-diagram` with `format: "xml"` and `size: "page"`** — the whole page
   in about half the bytes of `list-paged-model`'s JSON. Without `size: "page"`
   it exports every page.

Never export PNG or SVG to look at your work: that is 12–30 KB of markup you
cannot see. Check the geometry in the XML instead.

### Change

Leave what is already there where it is. Put new shapes in free space beside or
below; move or resize existing ones only when the user asks for a rearrangement.

| To | Use | Watch out |
|---|---|---|
| Put a shape between two connected ones | `add-rectangle`, then `edit-edge` to re-point the existing edge at it, then one `add-edge` | Re-pointing keeps the edge's id, style and label; `edit-edge` can relabel it in the same call |
| Add any shape | `add-rectangle` with a full `style` | Takes any style, not only rectangles. Use the id it returns: ids are generated, and on a copied page one can even be `"0"` |
| Add a library shape | `get-shape-by-name`, `add-cell-of-shape` | Takes the stencil id (`mxgraph.aws4.athena`), not a title like "Lambda". Lists only libraries the editor has loaded: general, AWS, GCP, Azure, Cisco. Kubernetes and the rest: `add-rectangle` with the style from [diagrams/](references/diagrams/) or the shape index in the [docs map](references/docs-map.md). A guessed `mxgraph.*` name renders an empty box with no error |
| Move, resize, relabel, restyle | `edit-cell` | `style` replaces the whole string. Read it, change one key, send all of it back |
| Connect two shapes | `add-edge` | Needs a source and a target cell. For a free line, add a vertex with `shape=line;rotation=<deg>` |
| Re-route or re-point an edge | `edit-edge` | `points: []` clears the waypoints |
| Put shapes in a box | a vertex with `container=1`, then `parent_id` on its children (or `set-cell-parent`) | Child `x`/`y` are relative to the container |
| Add many cells at once | `import-diagram` | **The default `mode` is `replace`, which wipes the page.** Pass `add` or `new-page`. `new-page` keeps your ids; check its name with `list-pages` (some editors ignore `<diagram name="…">`) and `rename-page` it; `add` gives the cells new ids, so read them back |
| Attach data (Edit Data) | `set-cell-data` | The first key wraps the shape in `<object>` and moves its text to the `label` key: change the text with `set-cell-data` `label` from then on. `placeholders=1` lets the label show `%key%`; `tooltip`, `link` and `tags` are keys too. Find shapes by them with the `attributes` filter |

Geometry: `x`/`y` is the top-left corner, relative to the parent. `rotation` is
degrees clockwise about the centre. Leave 40 px or more between shapes so edges
and their labels have room.

### Check, then say what is saved

- Re-read only the cells you touched (`list-paged-model` with `ids`), or the
  page as XML. Look for overlaps, edges missing a source or target, and empty
  labels.
- `export-diagram`'s `output_path` writes on the machine running the MCP server,
  not yours. A "directory does not exist" error means that machine; don't retry.
  To keep the export, use the text the call returns.
- `get-selected-cell`, `import-diagram` and selection exports work through the
  visible page and may switch what the user is looking at.
- Saving belongs to the editor's host (Nextcloud, VS Code, a browser tab), which
  may autosave. `save-document` triggers File ▸ Save and can open a prompt.
  Tell the user whether the change is saved.

## File mode

Write uncompressed XML with the skeleton in [xml.md](references/xml.md), then
check it: `python3 scripts/check.py <file>` (run from this skill's folder) reports
broken references, edges with a missing end, overlapping shapes and HTML labels
without `html=1`. It also checks XML exported from the live editor, and decodes
compressed pages.

## References

Load only the one you need.

| Need | Read |
|---|---|
| XML skeleton, cells, edges, containers, layers, decoding | [references/xml.md](references/xml.md) |
| Colours, shapes, sizes, spacing, a review checklist | [references/style.md](references/style.md) |
| A particular kind of diagram | [references/diagrams/](references/diagrams/) — one file per kind |
| Anything else: a style key, an icon name, CSV import, embed mode | [references/docs-map.md](references/docs-map.md). Look it up rather than guess |

## Common mistakes

| Mistake | Instead |
|---|---|
| `list-paged-model` with `page_size: 200` to find one shape | Filter, or ask the user to select it |
| SVG or PNG export to check the result | XML of the page, or the touched ids |
| Retrying `output_path` after "directory does not exist" | It is the server's disk. Use the returned text |
| `import-diagram` with no `mode` | `add` or `new-page`; the default replaces the page |
| `edit-cell` with only the key you wanted to change in `style` | Send the whole style string |
| Hunting the shape library for Kubernetes icons | [diagrams/kubernetes.md](references/diagrams/kubernetes.md) |
| Moving existing shapes to make room | Place the new one in free space |

## Add what you learn

When a tool surprises you, or a kind of diagram needs knowledge that isn't
here, write it down where the next agent will look: a row in Common mistakes, a
line in the matching `references/diagrams/` file, or a new file there copied
from `_template.md`. Keep each note to one or two lines. If you can't edit this
skill, tell the user what to add.
