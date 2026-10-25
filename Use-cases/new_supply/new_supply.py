import os
import subprocess
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.analytics import ManagedStreamingForKafka, Redshift
from diagrams.aws.database import Dynamodb, Aurora, ElastiCache
from diagrams.aws.compute import Lambda
from diagrams.generic.blank import Blank

os.makedirs("Use-cases/new_supply/output", exist_ok=True)

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
             filename="Use-cases/new_supply/output/new_supply",
             show=False, graph_attr=graph_attr):

    with Cluster("External Warehouse Data Sources", graph_attr=external_attr):
        fulfillment = Blank("Fulfillment Center Nodes\n(RFID scanners)")
        telematics = Blank("Logistics Fleet Telematics\n(GPS / milestones)")
        erp = Blank("Supply Chain ERP Systems\n(inbound POs, manifests)")

    with Cluster("Ingestion Tier", graph_attr=ingestion_attr):
        msk = ManagedStreamingForKafka("msk-inventory-events\n(Amazon MSK)")
        redis = ElastiCache("elasticache-fast-state\n(Amazon ElastiCache)")

    with Cluster("Continuous Processing Core", graph_attr=processing_attr):
        flink = Lambda("flink-metric-processor\n(Processing: Amazon Flink)")

    with Cluster("Persistence & Analytics", graph_attr=persistence_attr):
        ddb = Dynamodb("ddb-hot-inventory\n(Amazon DynamoDB)")
        aurora = Aurora("aurora-transaction-log\n(Amazon Aurora)")
        redshift = Redshift("redshift-historical-warehouse\n(Amazon Redshift)")

    # External -> Ingestion
    fulfillment >> Edge(label="event streams") >> msk
    telematics  >> Edge(label="telemetry events") >> msk
    erp        >> Edge(label="transaction events") >> msk

    # Ingestion -> Processing
    msk >> Edge(label="raw telemetry & update event stream") >> flink
    msk >> Edge(label="metrics feed") >> flink

    # Processing -> Low-latency stores
    flink >> Edge(label="low-latency active stock updates") >> ddb
    flink >> Edge(label="durable transaction logs") >> aurora
    flink >> Edge(label="cache updates (microsecond)") >> redis

    # Persistence -> Analytics
    ddb >> Edge(label="cold-tier replication") >> redshift
    aurora >> Edge(label="ETL / CDC -> historical warehouse") >> redshift

    # Node labels already include tool string and AWS service match per requirements

# Convert DOT to draw.io (requires graphviz2drawio on PATH)
try:
    subprocess.run([
        "graphviz2drawio",
        r"Use-cases/new_supply/output/new_supply.dot",
        "-o",
        r"Use-cases/new_supply/output/new_supply.drawio"
    ], check=True)
except Exception:
    pass
