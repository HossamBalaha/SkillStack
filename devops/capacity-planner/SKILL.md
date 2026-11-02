---
name: capacity-planner
description: Plan capacity with Kubernetes resource requests/limits, HorizontalPodAutoscaler, VerticalPodAutoscaler, cluster autoscaler, and cost forecasting. Use this when the user asks to right-size pods, set HPA targets, design cluster autoscaling, or forecast cloud spend.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: devops
tags: [autoscaling, hpa, vpa, capacity, cost, cluster-autoscaler]
related: [devops/kubernetes-manifest-builder, devops/grafana-dashboard-builder, devops/disaster-recovery-planner]
prerequisites: [devops/kubernetes-manifest-builder]
outputs: [yaml, markdown]
difficulty: advanced
estimated_tokens: 1700
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Capacity Planner

## When To Use

- The user says "right-size my pods" or "set up HPA".
- The user is sizing a new cluster and needs to know node count, instance type, and cost.
- The user wants the cluster autoscaler to add nodes when pods go Pending.
- The user wants a 90-day cost forecast for budget approval.
- Trigger keywords: hpa, vpa, autoscaling, requests, limits, cluster-autoscaler, capacity, cost.

## Workflow

1. Measure: pull per-pod CPU/memory utilization from Prometheus over 14 days; identify the p50, p95, p99.
2. Right-size requests to p50 (steady-state headroom) and limits to p99 (burst headroom).
3. Set a `HorizontalPodAutoscaler` targeting CPU at 70% of request and memory at 80% of request.
4. For stateful or asymmetric loads, add a custom metric (requests-per-second) via the KEDA or Prometheus adapter.
5. Enable the Vertical Pod Autoscaler in `off` (recommendation) mode to gather right-sizing suggestions without
   mutating.
6. Configure the cluster autoscaler with `--scale-down-unneeded-time=10m` and node group minimums/maximums per
   environment.
7. Add PodDisruptionBudgets so voluntary disruptions (node drain) don't drop below the target replicas.
8. Forecast cost: sum (nodes × hourly × hours) + storage + egress; model a 30% buffer for autoscaling.
9. Validate with a load test (k6, Locust) that pushes to 2× expected peak and confirms HPA + cluster autoscaler keep up.
10. Document the right-sizing decisions, HPA targets, and the 30/90-day cost forecast in a README.

## Inputs

- Per-service CPU/memory utilization percentiles (p50, p95, p99) from Prometheus.
- Expected QPS and target latency for HPA custom metrics.
- Node group instance types and hourly costs (cloud or on-prem rates).
- SLO targets the capacity must protect.

## Outputs

- `requests-recommendation.md` — right-sized CPU/memory per service.
- `hpa.yaml` — HorizontalPodAutoscaler per service.
- `vpa-recommender.yaml` — VPA in recommendation mode.
- `cluster-autoscaler-values.yaml` — min/max per node group.
- `cost-forecast.md` — 30/90-day forecast with assumptions.
- `load-test.md` — k6/Locust scenario and pass criteria.

## Key Rules

- Requests must be set on every container; pods without requests get scheduled but starve neighbors.
- Limits must be larger than requests for bursty workloads, but never unbounded (`limits.cpu` unset = throttling risk on
  CPU, OOM risk on memory).
- HPA target CPU should be 60-70% of request so headroom exists before scaling kicks in.
- VPA must never run in `Auto` mode alongside HPA on CPU — they fight; use VPA for memory only or `Off`
  (recommendation).
- Cluster autoscaler scale-down delay (`--scale-down-unneeded-time`) must exceed the deploy window so nodes aren't
  churned mid-rollout.
- PodDisruptionBudgets must match the HPA min replicas so a node drain can't drop capacity below the floor.
- Forecast with a 30% buffer; cloud spend surprises usually come from egress or unbounded autoscaling.

## Examples

```yaml
# hpa.yaml — CPU + custom metric (requests per second).
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api
  namespace: prod
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 3
  maxReplicas: 30
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 30
      policies:
        - type: Percent
          value: 100
          periodSeconds: 30
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 50
          periodSeconds: 60
```

```text
# cost-forecast.md
Compute (nodes): 6 × c6i.2xlarge × $0.34/h × 24 × 90 = $13,257
Storage (EBS): 2 TB × $0.10/GB × 90 = $180
Egress: 500 GB/month × $0.09/GB × 3 = $135
Buffer (30%): $4,072
Total 90-day forecast: ~$17,644
```

```text
# requests-recommendation.md (from VPA / Prometheus)
| Service       | CPU req | CPU lim | Mem req | Mem lim | Action |
|---------------|---------|---------|---------|---------|--------|
| payments-api  | 250m    | 1000m   | 256Mi   | 1Gi     | keep   |
| search-api    | 500m    | 2000m   | 1Gi     | 4Gi     | raise  |
| ingest-worker | 100m    | 500m    | 512Mi   | 1Gi     | keep   |
```

## References

- Kubernetes Horizontal Pod Autoscaler: https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/
- Kubernetes Vertical Pod Autoscaler: https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler
- Kubernetes Cluster Autoscaler: https://github.com/kubernetes/autoscaler/tree/master/cluster-autoscaler
- PodDisruptionBudgets: https://kubernetes.io/docs/tasks/run-application/configure-pdb/
