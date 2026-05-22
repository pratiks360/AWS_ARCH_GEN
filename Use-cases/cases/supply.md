# Architecture Diagram Instructions: Supply Chain Visibility

## Scenario
Create an AWS architecture diagram for GCC supply chain visibility
for a regional IT distributor operating across UAE, KSA, Kuwait,
Qatar, Bahrain, and Oman.

One AWS account (Middle East region — me-central-1), one VPC, four tiers:
data sources, ingestion, storage core, and analytics.

---

## Resources

1. **Data Sources (External)**
   - ERP / WMS Systems (SAP/Oracle) — per GCC country warehouse
   - Logistics & Carrier APIs (Aramex, DHL, FedEx, Agility)
   - IoT / RFID Sensors — smart shelves, GPS fleet trackers, barcode scanners

2. **Ingestion & Event Streaming**
   - Amazon MSK (Managed Kafka): "msk-supplychain-events"
     Unified event bus for all GCC warehouse and logistics events
   - AWS IoT Core: "iot-warehouse-sensors"
     Managed MQTT broker for device telemetry from sensors and GPS trackers

3. **Storage Layer — Managed Databases**
   - Amazon Aurora (MySQL): "aurora-inventory-db"
     Master inventory DB — SKU catalogue, stock levels per GCC country,
     purchase orders, supplier contracts. Multi-AZ for high availability.
   - Amazon ElastiCache (Redis): "elasticache-inventory-cache"
     Live inventory cache for sales and distributor portals.
     Prevents Aurora overload during peak order bursts.
   - Amazon Timestream: "timestream-iot-telemetry"
     Time-series DB for shipment telemetry, sensor readings, GPS pings.
     Tracks warehouse temperature and humidity for sensitive IT equipment.

4. **Analytics & Visibility Layer**
   - Amazon Redshift: "redshift-supplychain-dw"
     Historical supply chain warehouse — demand forecasting, vendor
     performance, GCC regional sales trends, slow-moving SKU analysis.
   - Amazon QuickSight: "quicksight-ops-dashboard"
     Live ops dashboards — GCC map views, stock heatmaps, SLA breach
     alerts, supplier scorecards.
   - Amazon DynamoDB: "ddb-alert-state"
     Alert state management — SLA breach counters, stockout flags,
     shipment delay notifications per partner.

---

## Connections
- ERP/WMS → MSK (inventory change events)
- Carrier APIs → MSK (shipment status events)
- IoT Sensors → IoT Core → MSK (telemetry events)
- MSK → Aurora (inventory updates)
- MSK → Timestream (sensor time-series)
- Aurora → ElastiCache (cache warm-up)
- ElastiCache → Distributor Portal (read cache)
- MSK → Redshift (historical load via S3/Firehose)
- Timestream → Redshift (aggregated telemetry)
- Redshift → QuickSight (analytics dashboards)
- MSK → DynamoDB (alert state writes)
- DynamoDB → SNS → Operations Team (breach notifications)

---

## Layout Rules
- Top: Data Sources (External) — ERP left, Carriers centre, IoT right
- Below: Ingestion Tier — MSK left, IoT Core right
- Middle: Storage Core — Aurora left, ElastiCache centre, Timestream right
- Bottom: Analytics Tier — Redshift left, QuickSight centre, DynamoDB right
- Draw all flows top to bottom
- Group Storage Core in a green cluster (#E8F5E9)
- Group Analytics in a purple cluster (#F3E5F5)
- Group External Sources in a dashed grey cluster (#ECEFF1)
- Group Ingestion in an amber cluster (#FFF8E1)

---

## Output Format Required
- List each cluster with its background color
- List each resource with its label and AWS service name
- List all arrows with direction and label (e.g., "inventory events", "cache warm-up")
- Make layout instructions explicit (top/middle/bottom, left/right)
- Use AWS icons for every resource following the icon imports in `aws_managed_db_agent.md`

---

## Python Script Template

Save as: `Use-cases/supply_chain_visibility/supply_chain_visibility.py`
Output goes to: `Use-cases/supply_chain_visibility/output/`

```python
import os
import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka, Quicksight, Redshift
from diagrams.aws.database import Aurora, ElastiCache, Dynamodb, Timestream
from diagrams.aws.iot import IotCore
from diagrams.aws.integration import SNS

os.makedirs("Use-cases/supply_chain_visibility/output", exist_ok=True)

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
storage_attr   = {"bgcolor": "#E8F5E9", "style": "rounded", "fontsize": "12", "margin": "15"}
analytics_attr = {"bgcolor": "#F3E5F5", "style": "rounded", "fontsize": "12", "margin": "15"}

with Diagram("Supply Chain Visibility — GCC Distribution", outformat=["png", "dot"],
             filename="Use-cases/supply_chain_visibility/output/supply_chain_visibility",
             graph_attr=graph_attr, show=False):

    with Cluster("External Data Sources — GCC", graph_attr=external_attr):
        erp     = Aurora("ERP / WMS\n(SAP/Oracle)")
        carrier = Aurora("Carrier APIs\n(Aramex, DHL)")
        iot_dev = Aurora("IoT / RFID\nSensors & GPS")

    with Cluster("Ingestion & Event Streaming", graph_attr=ingestion_attr):
        msk      = ManagedStreamingForKafka("Amazon MSK\nmsk-supplychain-events")
        iot_core = IotCore("IoT Core\niot-warehouse-sensors")

    with Cluster("Storage Layer — Managed Databases", graph_attr=storage_attr):
        aurora      = Aurora("Aurora MySQL\naurora-inventory-db")
        elasticache = ElastiCache("ElastiCache Redis\nelasticache-inventory-cache")
        timestream  = Timestream("Timestream\ntimestream-iot-telemetry")

    with Cluster("Analytics & Visibility", graph_attr=analytics_attr):
        redshift   = Redshift("Redshift\nredshift-supplychain-dw")
        quicksight = Quicksight("QuickSight\nquicksight-ops-dashboard")
        dynamodb   = Dynamodb("DynamoDB\nddb-alert-state")
        sns        = SNS("SNS Alerts")

    # Connections
    erp      >> Edge(label="inventory events")     >> msk
    carrier  >> Edge(label="shipment events")      >> msk
    iot_dev  >> Edge(label="telemetry")            >> iot_core
    iot_core >> Edge(label="MQTT → Kafka")         >> msk

    msk        >> Edge(label="inventory updates")    >> aurora
    msk        >> Edge(label="sensor time-series")   >> timestream
    aurora     >> Edge(label="cache warm-up")        >> elasticache
    msk        >> Edge(label="historical load")      >> redshift
    timestream >> Edge(label="aggregated telemetry") >> redshift
    redshift   >> Edge(label="dashboards")           >> quicksight
    msk        >> Edge(label="alert writes")         >> dynamodb
    dynamodb   >> Edge(label="breach notifications") >> sns

subprocess.run([
    "graphviz2drawio",
    r"Use-cases\supply_chain_visibility\output\supply_chain_visibility.dot",
    "-o",
    r"Use-cases\supply_chain_visibility\output\supply_chain_visibility.drawio"
], check=True)
```