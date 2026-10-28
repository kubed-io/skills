# Mind maps and trees

A central idea with branches and sub-topics, or any hierarchy someone will keep growing by hand.

## Shapes

These are draw.io's own Mindmap template styles (`plugins/trees/trees.js`):

| Thing | Style | Size |
|---|---|---|
| Central idea | `ellipse;whiteSpace=wrap;html=1;align=center;collapsible=0;container=1;recursiveResize=0;`, as an `<object>` with `treeRoot="1"` | 100–160 × 40–60 |
| Branch | `whiteSpace=wrap;html=1;shape=partialRectangle;top=0;left=0;bottom=1;right=0;points=[[0,1],[1,1]];fillColor=none;align=center;verticalAlign=bottom;routingCenterY=0.5;snapToPoint=1;collapsible=0;container=1;recursiveResize=0;autosize=1;` | 80 × 20 |
| Sub-topic | `whiteSpace=wrap;html=1;rounded=1;arcSize=50;align=center;verticalAlign=middle;collapsible=0;container=1;recursiveResize=0;strokeWidth=1;autosize=1;spacing=4;` | 72 × 26 |
| Link | `edgeStyle=entityRelationEdgeStyle;startArrow=none;endArrow=none;segment=10;curved=1;`, source = parent, target = child | — |

## Layout

Root in the middle, branches left and right, sub-topics fanned beside their branch about 40 px
apart. Every node sits on the layer (not inside its parent); the tree is the edges.

## The `trees` plugin

With the user's `trees` plugin on, a tree under a `treeRoot="1"` cell gets: Tab adds a child,
Enter a sibling, Shift+Tab a parent, arrows move between nodes, and Alt+Shift+X/T/P/S select
children/subtree/parent/siblings; moving a node moves its subtree. None of that is callable through
the MCP, so draw the structure right and let the user drive it.

## Gotchas

- `treeRoot` lives in `<object>` data: import with `new-page`, or `set-cell-data` it afterwards
  (an `add` import drops it).
