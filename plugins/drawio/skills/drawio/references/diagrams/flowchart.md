# Flowchart

A process with steps and decisions: a release, an approval, an algorithm.

## Shapes

| Thing | Style | Size |
|---|---|---|
| Start, end | `ellipse;whiteSpace=wrap;html=1;` or `rounded=1;arcSize=50;whiteSpace=wrap;html=1;` | 120 × 40 |
| Step | `rounded=1;whiteSpace=wrap;html=1;` | 140 × 50 |
| Decision | `rhombus;whiteSpace=wrap;html=1;` | 140 × 80 |
| Input or output | `shape=parallelogram;perimeter=parallelogramPerimeter;fixedSize=1;whiteSpace=wrap;html=1;` | 140 × 50 |
| Document | `shape=document;whiteSpace=wrap;html=1;boundedLbl=1;` | 120 × 60 |

## Layout

The main path runs top to bottom down one column, 40–60 px between shapes.
Failure or "no" branches leave a decision to the right and end there or loop
back. A final step can be the end; add a separate end shape only when several
paths meet there. Colour by role: success green, failure red, decisions yellow
(see style.md). No legend: the shapes and the yes/no labels already say it.

## Edges

`edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;`. Label every edge out of a
decision (`yes` / `no`). Pin the exit side with `exitX`/`exitY` so the yes path
stays in the column.

## Gotchas

- A legend's sample line is an edge with no ends; if one is needed, a text cell is simpler.
