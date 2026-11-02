---
name: data-lineage-tracker
description: Track data lineage as a provenance graph from source through transforms to sink, where each dataset carries a unique ID, version, source URI, transform function reference, parent dataset IDs, and a content hash (md5/sha256). Use this skill to output a lineage DAG as JSON or Graphviz, integrating with OpenLineage, Apache Atlas, or Amundsen.
metadata:
  author: custom-skills-repo
  version: "1.0"
  theme: data-engineering
tags: [lineage, provenance, openlineage, atlas, dag]
related: [data-engineering/etl-pipeline-builder, data-engineering/incremental-loader]
prerequisites: []
outputs: [python, json]
difficulty: advanced
estimated_tokens: 1500
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Data Lineage Tracker

## When To Use
- An audit (regulatory or incident) asks "where did this row come from?".
- A column breakage downstream must be traced back to the producing transform.
- A pipeline has multiple sources, transforms, and sinks that must be graphed.
- You are integrating with OpenLineage, Apache Atlas, or Amundsen.
- Each dataset version must carry an immutable content hash for replay.

## Workflow
1. Assign every dataset a unique ID plus a version and source URI.
2. Compute a content hash (sha256) of the dataset's bytes or row representation.
3. Reference the transform function (module + function name + version) that produced it.
4. Record parent dataset IDs so the graph can be traversed backward.
5. Append a lineage node to the provenance graph on every transform.
6. At sink time, persist the full DAG from roots to this dataset.
7. Render the DAG as JSON (machine) and Graphviz (human) on request.
8. Integrate with OpenLineage emitters so the graph is queryable by catalog tools.

## Inputs
- The dataset to register (path, table, or in-memory frame).
- The transform that produced it (function reference and version).
- The list of parent dataset IDs.
- The run context (run_id, job name, timestamp).

## Outputs
- A lineage node record (dataset ID, version, hash, parents, transform).
- A lineage DAG (JSON) from roots to the sink.
- A Graphviz rendering (DOT or PNG) of the DAG.
- An OpenLineage event payload emitted to the configured backend.

## Key Rules
- Every dataset carries an immutable content hash; equal hashes mean equal content.
- Parent IDs are recorded at write time so the graph is always reconstructable.
- The transform reference includes module, function name, and version.
- The DAG is append-only: revisions add new versions, never overwrite old ones.
- Emits an OpenLineage event so downstream catalogs (Atlas, Amundsen) stay in sync.
- Lineage is recorded at sink time, not just at source read time.

## Examples

```python
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DatasetNode:
  # One node in the provenance graph.
  DatasetId: str
  Version: str
  SourceUri: str
  ContentHash: str
  TransformRef: str
  ParentIds: list = field(default_factory=list)
  CreatedAt: str = ""


def HashContent(bytesPayload):
  # SHA-256 of the raw bytes so identical content collides.
  return hashlib.sha256(bytesPayload).hexdigest()


def RegisterDataset(datasetId, version, sourceUri, contentBytes, transformRef, parentIds):
  # Build an immutable node capturing everything needed for replay.
  return DatasetNode(
    DatasetId=datasetId,
    Version=version,
    SourceUri=sourceUri,
    ContentHash=HashContent(contentBytes),
    TransformRef=transformRef,
    ParentIds=list(parentIds),
    CreatedAt=datetime.now(timezone.utc).isoformat(),
  )


class LineageGraph:
  # Append-only provenance graph keyed by DatasetId plus Version.
  def __init__(self):
    self.Nodes = {}

  def Add(self, node):
    key = (node.DatasetId, node.Version)
    self.Nodes[key] = node

  def ToJson(self):
    return json.dumps(
      [{"DatasetId": n.DatasetId, "Version": n.Version, "SourceUri": n.SourceUri,
        "ContentHash": n.ContentHash, "TransformRef": n.TransformRef,
        "ParentIds": n.ParentIds, "CreatedAt": n.CreatedAt}
       for n in self.Nodes.values()],
      indent=2,
    )

  def ToDot(self):
    # Render the DAG in Graphviz DOT format for human review.
    lines = ["digraph lineage {"]
    for node in self.Nodes.values():
      nodeId = f'"{node.DatasetId}@{node.Version}"'
      if (not node.ParentIds):
        # Root node: no incoming edge.
        lines.append(f"  {nodeId};")
      else:
        for parentId in node.ParentIds:
          lines.append(f'  "{parentId}" -> {nodeId};')
    lines.append("}")
    return "\n".join(lines)


def EmitOpenLineageEvent(node, runId, jobName):
  # Build a minimal OpenLineage event for external catalogs.
  return {
    "EventType": "COMPLETE",
    "Run": {"RunId": runId},
    "Job": {"Name": jobName, "Namespace": "default"},
    "Outputs": [{
      "Namespace": "default",
      "Name": node.DatasetId,
      "Facets": {
        "version": {"_Producer": "data-lineage-tracker", "Version": node.Version},
        "dataSource": {"_Producer": "data-lineage-tracker", "SourceUri": node.SourceUri},
      },
    }],
  }
```

## References
- OpenLineage: https://openlineage.io
- Apache Atlas: https://atlas.apache.org
- Amundsen: https://www.amundsen.io
- Graphviz DOT: https://graphviz.org/doc/info/lang.html
