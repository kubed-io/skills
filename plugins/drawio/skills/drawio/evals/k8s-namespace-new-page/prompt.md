---
tags: [drawio]
max_turns: 40
timeout_seconds: 900
---

In the draw.io diagram I have open, make a new page called `k8s-test` and draw how our shop app runs on Kubernetes: an Ingress routes to the frontend Service and Deployment, the frontend calls the api Service and Deployment, and the api stores its data in a Postgres StatefulSet with a PersistentVolumeClaim. Put it all inside a namespace box called `shop`.
