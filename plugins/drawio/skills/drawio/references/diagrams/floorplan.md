# Floor plans and site plans

A space seen from directly above: rooms and furniture, or a yard, lot or garden with its ground
surfaces and structures. draw.io's own guide: `DOCS/diagram-types/floorplans/` (docs map).

## Shapes

Indoor shapes come from draw.io's Floorplan library. The live editor's shape tools don't load it,
so use `add-rectangle` or XML with this style, from `Sidebar-Floorplan.js`:

```
verticalLabelPosition=bottom;html=1;verticalAlign=top;align=center;shape=mxgraph.floorplan.<name>
```

| Thing | `<name>` (+ extra keys) | Size |
|---|---|---|
| Wall | `wall;fillColor=strokeColor` (`direction=south` for vertical) | length × 10 |
| Room outline | `room;fillColor=strokeColor` | any |
| Door | `doorLeft;aspect=fixed` / `doorRight` / `doorDouble` / `doorSlidingGlass;dx=0.25` | 80 × 85 |
| Window | `window` | length × 10 |
| Stairs | `stairs` | 300 × 100 |
| Furniture | `table`, `chair`, `sofa`, `couch`, `bed_double`, `bed_single`, `desk_corner`, `bookcase` | see the sidebar |
| Kitchen, bath | `refrigerator`, `range_1`, `sink_1`, `toilet_2`, `bathtub2`, `shower2` | see the sidebar |
| Tree, shrub | `plant` | 47 × 51 |

Outdoors there is no landscape library. Ground is plain filled boxes, structures are basic shapes:

| Thing | Style |
|---|---|
| Concrete, paving | `fillColor=#D6D6D6;strokeColor=#9E9E9E;` |
| Dirt, bare ground | `fillColor=#E8D5B5;strokeColor=#C8A27A;` |
| Lawn | `fillColor=#C8E6C9;strokeColor=#81C784;` |
| Garden bed, planned area | `dashed=1;fillColor=#E8F5E9;strokeColor=#82b366;` |
| Fence or property line | an unfilled box: `fillColor=none;strokeColor=#8D6E63;strokeWidth=6;` |
| Gazebo | `shape=mxgraph.basic.octagon2;dx=30;` (draw.io has no gazebo shape) |
| Shed, garage, house | a plain box with a 2 px stroke |

Measurements: `shape=dimension;whiteSpace=wrap;html=1;align=center;points=[];verticalAlign=bottom;spacingBottom=3;labelBackgroundColor=none;`
(100 × 40, label above). Vertical: add `direction=north;horizontal=0;` and swap the size.

## Layout

- Pick a scale and say it on the page: one 10 px grid square = 1 ft (or 0.5 m). Without real
  sizes, draw plausible ones and label them estimates so the user knows to correct them.
- Say which way is which: "house at the bottom, back fence at the top", or a north arrow.
- Layers, bottom to top: ground surfaces, walls or fence, structures and furniture, notes and
  dimensions. Things that sit on each other (a gazebo on a slab) belong on different layers, which
  is also why `check.py` doesn't call them overlapping.
- Dimension lines sit outside the boundary. One page per floor.

## Gotchas

- `import-diagram` in `new-page` mode didn't always take the page name from `<diagram name>`:
  check with `list-pages` and `rename-page`.
