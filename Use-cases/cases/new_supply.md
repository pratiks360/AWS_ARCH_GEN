# Architecture Diagram Instructions: Real-Time Inventory & Supply Chain Logistics

## Scenario
Create an AWS architecture diagram for the Redington Data Motion Implementation Package, specialized for Real-Time Inventory & Supply Chain Logistics in the Gulf market.

The architecture spans one AWS account across multiple Availability Zones (Multi-AZ) and organizes components into four clear horizontal tiers: external warehouse data sources, high-throughput ingestion, continuous stream processing, and multi-engine persistence/analytics.

---

## Resources

1. **Warehouse Data Sources (External)**
   - Fulfillment Center Nodes (RFID scanners, automated picking systems)
   - Logistics Fleet Telematics (GPS coordinates, transit milestones)
   - Supply Chain ERP Systems (Inbound purchase orders, stock manifestos)

2. **Ingestion Tier**
   - Amazon MSK (Managed Kafka): `msk-inventory-events`
     High-throughput, multi-zone event streaming cluster that decouples physical warehouses from the cloud engine.
   - Amazon ElastiCache (Redis): `elasticache-fast-state`
     Microsecond-latency in-memory layer providing immediate caching for active transaction metadata and real-time dashboard UI elements.

3. **Continuous Processing Core**
   - Amazon Managed Service for Apache Flink: `flink-metric-processor`
     Serverless stream processing running tumbling window metrics to compute rolling inventory counts, detect stockouts, and flag delivery drops.

4. **Multi-Engine Persistence & Analytics**
   - Amazon DynamoDB: `ddb-hot-inventory`
     Single-digit millisecond NoSQL storage serving hot inventory counts directly to client-facing mobile web applications.
   - Amazon Aurora (MySQL/PostgreSQL): `aurora-transaction-log`
     Multi-AZ relational storage acting as the durable source of truth for transaction logs, compliance auditing, and structured reporting.
   - Amazon Redshift: `redshift-historical-warehouse`
     Fully managed cloud data warehouse for historical logistics aggregation, seasonal trend optimization, and supply chain reporting.

---

## Connections
- Fulfillment Nodes + Fleet Telematics + ERP Systems → MSK (inventory event ingestion)
- MSK → Apache Flink (raw telemetry & update event stream)
- Apache Flink → DynamoDB (low-latency active stock updates)
- Apache Flink → Amazon Aurora (durable relational transaction logging)
- Apache Flink → ElastiCache Redis (microsecond dashboard cache state)
- DynamoDB + Amazon Aurora → Redshift (automated historical cold-tier replication)

---

## Layout Rules
- **Top:** Warehouse Data Sources (External) — three boxes aligned horizontally.
- **Upper-Middle:** Ingestion Tier — MSK positioned on the left, ElastiCache Redis positioned on the right.
- **Lower-Middle:** Continuous Processing Core — Apache Flink centered to act as the primary operational hub.
- **Bottom:** Multi-Engine Persistence & Analytics — DynamoDB on the left, Aurora in the center, Redshift on the right.
- **Flow Direction:** Draw all lines descending top-to-bottom to represent fluid data motion.
- **Cluster Customization:**
  - Group External Sources in a dashed grey cluster (`#ECEFF1`).
  - Group Ingestion in a warm amber cluster (`#FFF8E1`).
  - Group Processing Core in a cool blue cluster (`#E3F2FD`).
  - Group Persistence & Analytics in a rich purple cluster (`#F3E5F5`).

---

## Output Format Required
- Define each functional tier inside its own colored cluster.
- Identify every tool with its exact string name, label, and AWS service match.
- Map directional flows with explicit metadata edge labels (e.g., "event streams", "metrics push").
- Keep visual placement instructions strictly aligned horizontally and vertically.
- Map to official library classes using imports from the Python `diagrams` framework.

---

## Python Script Template

Save as: `Use-cases/data_motion_inventory/data_motion_inventory.py`  
Output goes to: `Use-cases/data_motion_inventory/output/`

```python
import os
import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka, ManagedServiceForApacheFlink, Redshift
from diagrams.aws.database import Dynamodb, Aurora, ElastiCache
from diagrams.aws.compute import Lambda

os.makedirs("Use-cases/data_motion_inventory/output", exist_ok=True)

graph_attr = {
    "splines": "ortho",
    "nodesep": "0.8",
    "ranksep": "1.2",
    "fontsize": "14",
    "bgcolor": "white",
    "pad": "0.5",
    "rankdir": "TB"
}

external_attr  = {"bgcolor": "#ECEFF1", "style": "dashed",  "fontsize": "12", "margin": "15"}
ingestion_attr = {"bgcolor": "#FFF8E1", "style": "rounded", "fontsize": "12", "margin": "15"}
processing_attr = {"bgcolor": "#E3F2FD", "style": "rounded", "fontsize": "12", "margin": "15"}
persistence_attr = {"bgcolor": "#F3E5F5", "style": "rounded", "fontsize": "12", "margin": "15"}

with Diagram("Data Motion Implementation Package — Real-Time Inventory", outformat=["png", "dot"],
             filename="Use-cases/data_motion_inventory/output/data_motion_inventory",