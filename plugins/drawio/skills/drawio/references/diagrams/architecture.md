# System and cloud architecture

Clients, services, data stores and the traffic between them, often grouped by
network, account or region.

## Shapes

| Thing | Style | Size |
|---|---|---|
| Service, app | `rounded=1;whiteSpace=wrap;html=1;` | 120 × 60 |
| Database | `shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;size=10;` | 80 × 80 |
| Queue | `shape=mxgraph.basic.layered_rect;whiteSpace=wrap;html=1;` or a plain box labelled with the broker | 120 × 60 |
| Person | `shape=umlActor;verticalLabelPosition=bottom;verticalAlign=top;html=1;` | 30 × 60 |
| Boundary (VPC, account, region) | a container: `rounded=1;dashed=1;fillColor=none;verticalAlign=top;align=left;spacingLeft=10;html=1;container=1;collapsible=0` | — |

Vendor icons: in live mode `get-shape-by-name` knows AWS (`mxgraph.aws4.*`), GCP
(`mxgraph.gcp2.*`), Azure (`mxgraph.azure2.*`) and Cisco. Otherwise query the
shape index in the docs map. Prefer `aws4` over the legacy `aws3`. Kubernetes:
[kubernetes.md](kubernetes.md).

## Layout

Left to right in the order a request travels: clients, edge (DNS, CDN, load
balancer, ingress), services, data. Data stores sit at the right or the bottom.
One row or column per tier, 60–80 px between tiers.

## Edges

Orthogonal arrows in the direction of the request, labelled with the protocol or
verb (`HTTPS`, `SQL`, `publish`). A cache sits between a service and its store:
service → cache, cache → store labelled `miss`.

## Gotchas

- Adding to an existing diagram: put the new piece in free space (below the row,
  or at its end) rather than shifting the row to open a gap.
