# Architecture Diagram Instructions: AML & Fraud Detection

## Scenario
Create an AWS architecture diagram for real-time AML and fraud detection
in Gulf banking.

One AWS account, one VPC, four tiers: data sources, ingestion,
detection core, and compliance reporting.

---

## Resources

1. **Data Sources (External)**
   - Core Banking System (on-premises or 3rd party)
   - Card & Payment Networks (SWIFT, UAEFTS, SARIE)
   - KYC / Sanctions Data (OFAC, UN, PEP databases)

2. **Ingestion & Enrichment**
   - Amazon MSK (Managed Kafka): "msk-fraud-events"
     High-throughput event streaming, decouples source systems
   - AWS Lambda: "lambda-event-enricher"
     Normalize event schema, enrich with KYC data, route events

3. **Detection Core — Managed Databases**
   - Amazon Neptune: "neptune-fraud-graph"
     Graph DB — maps account relationships, beneficial ownership chains,
     circular fund flows, layering pattern detection
   - Amazon DynamoDB: "ddb-rule-engine"
     Real-time rule engine state — per-account velocity counters,
     threshold tracking, live alert flags at single-digit ms latency
   - Amazon SageMaker: "sagemaker-fraud-model"
     ML scoring — anomaly detection, behavioural risk scoring,
     unusual geolocation patterns

4. **Compliance Reporting & Analytics**
   - Amazon Redshift: "redshift-aml-warehouse"
     Historical transaction warehouse — SAR reports, CBUAE/SAMA
     regulatory submissions, trend analytics, audit trails
   - Amazon QuickSight: "quicksight-compliance"
     Compliance dashboards for AML officers — risk heatmaps,
     case management views, executive reporting

---

## Connections
- Core Banking → MSK → Lambda (event enrichment)
- Card Networks → MSK
- KYC Data → Lambda (enrichment lookup)
- Lambda → Neptune (relationship graph update)
- Lambda → DynamoDB (velocity counter update)
- Lambda → SageMaker (ML risk scoring)
- Neptune + DynamoDB + SageMaker → Redshift (alerts + raw data)
- Redshift → QuickSight (dashboards)

---

## Layout Rules
- Top: Data Sources (External) — three boxes side by side
- Below: Ingestion Tier — MSK left, Lambda right
- Middle: Detection Core — Neptune left, DynamoDB centre, SageMaker right
- Bottom: Analytics Tier — Redshift left, QuickSight right
- Draw all flows top to bottom
- Group Detection Core in a single cluster with a blue background (#E3F2FD)
- Group Analytics in a single cluster with a purple background (#F3E5F5)
- Group External Sources in a dashed grey cluster (#ECEFF1)
- Group Ingestion in an amber cluster (#FFF8E1)

---

## Output Format Required
- List each cluster with its background color
- List each resource with its label and AWS service name
- List all arrows with direction and label (e.g., "event stream", "ML inference")
- Make layout instructions explicit (top/middle/bottom, left/right)
- Use AWS icons for every resource following the icon imports in `aws_managed_db_agent.md`

---

## Python Script Template

Save as: `Use-cases/aml_fraud_detection/aml_fraud_detection.py`
Output goes to: `Use-cases/aml_fraud_detection/output/`

```python
import os
import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka, Quicksight, Redshift
from diagrams.aws.database import Dynamodb, Neptune
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import Sagemaker

os.makedirs("Use-cases/aml_fraud_detection/output", exist_ok=True)

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
detection_attr = {"bgcolor": "#E3F2FD", "style": "rounded", "fontsize": "12", "margin": "15"}
analytics_attr = {"bgcolor": "#F3E5F5", "style": "rounded", "fontsize": "12", "margin": "15"}

with Diagram("AML & Fraud Detection — Gulf Banking", outformat=["png", "dot"],
             filename="Use-cases/aml_fraud_detection/output/aml_fraud_detection",
             graph_attr=graph_attr, show=False):

    with Cluster("External Data Sources", graph_attr=external_attr):
        cbs  = Lambda("Core Banking\nSystem")
        card = Lambda("Card & Payment\nNetworks")
        kyc  = Lambda("KYC / Sanctions\nData")

    with Cluster("Ingestion & Enrichment", graph_attr=ingestion_attr):
        msk = ManagedStreamingForKafka("Amazon MSK\nmsk-fraud-events")
        lmb = Lambda("Lambda\nlambda-event-enricher")

    with Cluster("Detection Core", graph_attr=detection_attr):
        neptune   = Neptune("Neptune\nneptune-fraud-graph")
        dynamodb  = Dynamodb("DynamoDB\nddb-rule-engine")
        sagemaker = Sagemaker("SageMaker\nsagemaker-fraud-model")

    with Cluster("Compliance & Analytics", graph_attr=analytics_attr):
        redshift   = Redshift("Redshift\nredshift-aml-warehouse")
        quicksight = Quicksight("QuickSight\nquicksight-compliance")

    # Connections
    [cbs, card] >> Edge(label="event stream")       >> msk
    msk         >> Edge(label="raw events")         >> lmb
    kyc         >> Edge(label="enrichment")         >> lmb
    lmb         >> Edge(label="graph update")       >> neptune
    lmb         >> Edge(label="velocity counter")   >> dynamodb
    lmb         >> Edge(label="risk scoring")       >> sagemaker
    [neptune, dynamodb, sagemaker] >> Edge(label="alerts + data") >> redshift
    redshift    >> Edge(label="dashboards")         >> quicksight

subprocess.run([
    "graphviz2drawio",
    r"Use-cases\aml_fraud_detection\output\aml_fraud_detection.dot",
    "-o",
    r"Use-cases\aml_fraud_detection\output\aml_fraud_detection.drawio"
], check=True)
```