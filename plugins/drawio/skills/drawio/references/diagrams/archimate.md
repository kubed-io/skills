# ArchiMate

Enterprise architecture in ArchiMate 3: business, application and technology layers and the
relationships between them. No import needed: the styles below make the editor load the library.

## Shapes

Base style, with the layer's colour: `html=1;outlineConnect=0;whiteSpace=wrap;fillColor=<colour>;shape=mxgraph.archimate3.`
then the element. Size 150 × 75. From `Sidebar-ArchiMate3.js`.

| Layer | `fillColor` |
|---|---|
| Business | `#ffff99` |
| Application | `#99ffff` |
| Technology | `#AFFFAF` |
| Strategy | `#F5DEAA` |
| Motivation | `#CCCCFF` |
| Implementation & migration | `#FFE0E0` |

| Element | After the base |
|---|---|
| Actor | `application;appType=actor;archiType=square;` |
| Role | `application;appType=role;archiType=square;` |
| Component | `application;appType=comp;archiType=square;` |
| Service | `application;appType=serv;archiType=rounded;` |
| Data / passive object | `application;appType=passive;archiType=square;` |
| Node | `application;appType=node;archiType=square;` |

The full list (interfaces, processes, functions, events, devices, artifacts…) is in
`Sidebar-ArchiMate3.js` (docs map); grep its `createVertexTemplateEntry` lines.

## Edges

| Relationship | Style |
|---|---|
| Serving | `edgeStyle=elbowEdgeStyle;html=1;endArrow=open;elbow=vertical;endFill=1;` |
| Realization | `edgeStyle=elbowEdgeStyle;html=1;endArrow=block;elbow=vertical;endFill=0;dashed=1;` |
| Access | `edgeStyle=elbowEdgeStyle;html=1;endArrow=open;elbow=vertical;endFill=0;dashed=1;dashPattern=1 4;` |
| Assignment | `endArrow=block;html=1;endFill=1;startArrow=oval;startFill=1;edgeStyle=elbowEdgeStyle;elbow=vertical;` |
| Composition | `html=1;startArrow=diamondThin;startFill=1;edgeStyle=elbowEdgeStyle;elbow=vertical;startSize=10;endArrow=none;endFill=0;` |
| Aggregation | the same with `startFill=0` |
| Triggering | `edgeStyle=elbowEdgeStyle;html=1;endArrow=block;dashed=0;elbow=vertical;endFill=1;` |
| Flow | `edgeStyle=elbowEdgeStyle;html=1;endArrow=block;dashed=1;elbow=vertical;endFill=1;dashPattern=6 4;` |
| Specialization | `endArrow=block;html=1;endFill=0;edgeStyle=elbowEdgeStyle;elbow=vertical;` |
| Association | `edgeStyle=elbowEdgeStyle;html=1;endArrow=none;elbow=vertical;` |

## Layout

Business on top, application in the middle, technology at the bottom; one row per layer.
Serving points up the stack, realization from the implementer to what it realizes.

## Gotchas
