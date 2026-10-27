# Illustrations and scenes

A picture rather than a diagram: a scene, a mascot, an icon. Nothing connects; shapes overlap
on purpose and the order they are drawn in is the art.

## Shapes

| Thing | How |
|---|---|
| Round things (snowballs, moons, glows) | `ellipse` with a `gradientColor`; a glow is a larger ellipse with `opacity=15`–`25` |
| Organic outlines (flames, hills, scarves, bows) | `python3 scripts/stencil.py --fill "<svg path>"`, then `fillColor`/`gradientColor`/`strokeColor=none` |
| Lines with a hand-drawn feel (branches, smiles) | `stencil.py` without `--fill`, plus `fillColor=none;strokeColor=…;strokeWidth=…` |
| Simple solids (hat, box, log) | plain boxes; `rounded=1;arcSize=50` for a log, `rotation` to tilt |
| Something made of parts (a present and its ribbon) | the main shape with `container=1;collapsible=0`, the parts as its children, so they move together |

Draw paths in a 100 × 100 box (or pass `--box W H` for the box you drew in): a curve is
`C x1 y1 x2 y2 x y`, close a filled shape with `Z`. Gradients take `gradientDirection` =
`north`, `south`, `east` or `west`.

## Layout

- One layer per subject (sky, fire, snowman, presents, notes), bottom to top. Within a layer,
  later cells are drawn on top, so add the back first.
- `move-cell-to-layer` puts a cell on top of its new layer; plan the order instead of moving later.
- Keep a sketch of the coordinates (or a script) — every position is absolute to the page.

## Checking

`check.py --allow-overlap`. Geometry in XML can't show whether a stencil or gradient looks right;
when that is the question, one SVG export and a search of it (for the `path` of a stencil, or a
literal `%` in a `fill`) answers it.

## Gotchas

- `fillColor=%color%` with `stylePlaceholders=1` is not substituted by the shipped editor.
