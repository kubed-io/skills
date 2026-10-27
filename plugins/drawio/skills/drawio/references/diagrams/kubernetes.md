# Kubernetes

Workloads, Services, Ingress and storage, usually grouped by namespace or cluster.

## Shapes

The live editor's shape library has **no Kubernetes category**, so
`get-shape-by-name` returns nothing. Use `add-rectangle` (or XML) with this style,
taken from draw.io's own sidebar:

```
aspect=fixed;html=1;dashed=0;whiteSpace=wrap;verticalLabelPosition=bottom;verticalAlign=top;fillColor=#2875E2;strokeColor=#ffffff;shape=mxgraph.kubernetes.icon2;prIcon=<icon>
```

Size 50 × 48. The label sits under the icon. `kubernetesLabel=1` is the sidebar's
variant that marks the kind on the icon itself.

| Kind | `prIcon` | Kind | `prIcon` |
|---|---|---|---|
| Pod | `pod` | Ingress | `ing` |
| Deployment | `deploy` | Service | `svc` |
| ReplicaSet | `rs` | Endpoints | `ep` |
| StatefulSet | `sts` | NetworkPolicy | `netpol` |
| DaemonSet | `ds` | ConfigMap | `cm` |
| Job | `job` | Secret | `secret` |
| CronJob | `cronjob` | ServiceAccount | `sa` |
| HorizontalPodAutoscaler | `hpa` | Role / ClusterRole | `role` / `c_role` |
| PersistentVolumeClaim | `pvc` | RoleBinding / ClusterRoleBinding | `rb` / `crb` |
| PersistentVolume | `pv` | CustomResourceDefinition | `crd` |
| StorageClass | `sc` | Namespace | `ns` |
| Volume | `vol` | Node | `node` |
| ResourceQuota / LimitRange | `quota` / `limits` | User | `user` |

Control plane: `api`, `sched`, `c_m`, `c_c_m`, `etcd`, `kubelet`, `k_proxy`,
`control_plane`. The full list is `Sidebar-Kubernetes.js` (see the docs map).

A namespace or cluster is a container, not an icon:

```
rounded=1;arcSize=4;dashed=1;fillColor=none;strokeColor=#2875E2;strokeWidth=2;fontColor=#2875E2;fontStyle=1;align=left;verticalAlign=top;spacingLeft=10;spacingTop=4;html=1;container=1;collapsible=0;pointerEvents=0
```

## Layout

Traffic runs left to right: Ingress → Service → Deployment, one row per tier.
Put storage (PVC, PV) under the workload that mounts it, and pin that edge to
the icons' sides (`exitX=1;exitY=0.5;entryX=1;entryY=0.5`) so it doesn't cross
the workload's label. Space icons about 150 px apart. A 50 px icon fits a short
label only: write name and kind on two lines, `api&lt;br&gt;Deployment`. Children of the namespace
box use coordinates relative to the box; leave 40 px at the top for its title.

## Edges

Orthogonal, labelled with the relationship: `routes`, `selects`, `calls`,
`mounts`. A Service-to-workload edge can be dashed to show it is a selector,
not a connection.

## Gotchas

- `get-shape-categories` costs about 4 KB and lists no Kubernetes shapes. Skip it.
- The older `shape=mxgraph.kubernetes.icon` still renders; the sidebar uses `icon2`.
