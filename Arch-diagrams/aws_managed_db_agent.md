# Agent Instructions: AWS Managed Database Architecture Diagram Generation

## Overview
This workspace contains tools to automatically generate AWS managed database architecture diagrams from scenario descriptions. Diagrams are created using Python's `diagrams` library, rendered with GraphViz, and converted to editable draw.io format.

---

## Environment Setup

### Python Environment
- **Location**: `AWS_MANAGEDDB\venv`
- **Python Version**: 3.12.x
- **Activation**: `.\venv\Scripts\Activate.ps1` (PowerShell)

### Installed Packages (Exact Versions)
```
diagrams==0.24.4
graphviz==0.20.3
pygraphviz==1.14
graphviz2drawio==1.1.0
puremagic==1.30
svg.path==7.0
```

### Initial Setup from Scratch
```powershell
# 1. Create virtual environment
cd "AWS_MANAGEDDB"
python -m venv venv
.\venv\Scripts\Activate.ps1

# 2. Install pygraphviz with GraphViz paths (requires MSVC Build Tools)
$env:GRAPHVIZ_DIR = "C:\Program Files\Graphviz"
pip install --config-settings="--global-option=build_ext" `
  --config-settings="--global-option=-IC:\Program Files\Graphviz\include" `
  --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz

# 3. Install remaining packages
pip install diagrams  graphviz2drawio pygraphviz   --config-settings="--global-option=build_ext"   --config-settings="--global-option=-IC:\Program Files\Graphviz\include" --config-settings="--global-option=-LC:\Program Files\Graphviz\lib"

```

### GraphViz Installation
- **Location**: `C:\Program Files\Graphviz\bin`
- **Version**: 14.0.2
- **Critical**: Must add to PATH before running diagram scripts
  ```powershell
  $env:PATH += ";C:\Program Files\Graphviz\bin"
  ```

### VS Code Extensions
- **Draw.io**: `hediet.vscode-drawio` — for viewing/editing `.drawio` files

---

## Folder Structure

```
AWS_MANAGEDDB/
├── .venv/                              # Python virtual environment
├── venv/                               # Python virtual environment (alternate)
├── Arch_diagrams/
│   ├── aws_managed_db_agent.md         # THIS FILE — Agent instructions
│   └── requirements.txt                # Python package dependencies
└── Use-cases/
    └── <usecase-name>/                 # One folder per use case (e.g., aml_fraud_detection)
        ├── instructions.md             # Scenario description, resources, layout rules
        ├── <usecase_name>.py           # Python diagram generation script
        └── output/                     # All generated files go here
            ├── <usecase_name>.png      # Static image
            ├── <usecase_name>.dot      # GraphViz DOT source
            └── <usecase_name>.drawio   # Editable draw.io file
```

---

## Diagram Generation Workflow

### Complete Process (3 Steps)

#### Step 1: Read the use case `instructions.md`
Each use case folder contains an `instructions.md` with:
- Scenario description
- Resources and AWS services
- Connections between services
- Layout rules (top/middle/bottom, left/right, cluster colors)

Use this file as the input spec to write the Python diagram script.

#### Step 2: Write and run the Python diagram script
- Save the script as `<usecase_name>.py` inside the use case folder
- Set the output path to the `output/` subfolder of that use case
- Import required AWS components from `diagrams.aws.*`
- Use proper icon class names (see Common AWS Icon Imports below)
- Configure graph attributes:
  ```python
  graph_attr = {
      "splines": "ortho",
      "nodesep": "0.8",
      "ranksep": "1.2",
      "fontsize": "14",
      "bgcolor": "white",
      "pad": "0.5"
  }
  ```
- Use `Cluster` for logical grouping (tiers, VPC, subnets, availability zones)
- Apply color coding per tier (see Color Coding section below)
- Set output format: `outformat=["png", "dot"]`

Run the script:
```powershell
cd "AWS_MANAGEDDB"
.\venv\Scripts\Activate.ps1
$env:PATH += ";C:\Program Files\Graphviz\bin"
python Use-cases\<usecase-name>\<usecase_name>.py
```

#### Step 3: Convert DOT to Draw.io
Add this at the end of every script, pointing to the use case `output/` folder:
```python
import subprocess
subprocess.run([
    "graphviz2drawio",
    r"Use-cases\<usecase-name>\output\<usecase_name>.dot",
    "-o",
    r"Use-cases\<usecase-name>\output\<usecase_name>.drawio"
], check=True)
```

---

## Common AWS Icon Imports

```python
from diagrams import Diagram, Cluster, Edge

# Database (Managed)
from diagrams.aws.database import (
    Aurora,           # Amazon Aurora (MySQL / PostgreSQL compatible)
    RDS,              # Amazon RDS (multi-engine)
    Dynamodb,         # Amazon DynamoDB (NoSQL key-value)
    ElastiCache,      # Amazon ElastiCache (Redis / Memcached)
    Redshift,         # Amazon Redshift (data warehouse / OLAP)
    Neptune,          # Amazon Neptune (graph database)
    Keyspaces,        # Amazon Keyspaces (Cassandra-compatible)
    DocumentDB,       # Amazon DocumentDB (MongoDB-compatible)
    Timestream,       # Amazon Timestream (time-series)
    QLDB,             # Amazon QLDB (immutable ledger)
    DatabaseMigrationService  # AWS DMS
)

# Streaming & Messaging
from diagrams.aws.analytics import ManagedStreamingForKafka  # Amazon MSK
from diagrams.aws.integration import SQS, SNS, Eventbridge

# Analytics & BI
from diagrams.aws.analytics import (
    Quicksight,        # Amazon QuickSight (BI dashboards)
    KinesisDataStreams,
    GlueDataCatalog,
    Athena
)

# Compute
from diagrams.aws.compute import Lambda, ECS, EKS, EC2

# Networking
from diagrams.aws.network import VPC, PrivateSubnet, PublicSubnet, APIGateway, CloudFront

# Security & Identity
from diagrams.aws.security import IAM, KMS, SecretsManager, Shield, WAF

# Storage
from diagrams.aws.storage import S3

# ML
from diagrams.aws.ml import Sagemaker

# IoT
from diagrams.aws.iot import IotCore

# Management & Monitoring
from diagrams.aws.management import Cloudwatch, Cloudtrail
```

**Important**: Always verify actual class names using:
```python
from diagrams.aws import database
print([x for x in dir(database) if not x.startswith('_')])
```

---

## Color Coding for Tiers

Use consistent background colors to distinguish architectural layers:

```python
# External / Data Sources
external_attr = {
    "fontsize": "13",
    "bgcolor": "#ECEFF1",   # Light Grey
    "style": "dashed",
    "margin": "15"
}

# Ingestion / Streaming Tier
ingestion_attr = {
    "fontsize": "13",
    "bgcolor": "#FFF8E1",   # Light Amber
    "style": "rounded",
    "margin": "15"
}

# Detection / Processing Tier
processing_attr = {
    "fontsize": "13",
    "bgcolor": "#E3F2FD",   # Light Blue
    "style": "rounded",
    "margin": "15"
}

# Database / Storage Tier
database_attr = {
    "fontsize": "13",
    "bgcolor": "#E8F5E9",   # Light Green
    "style": "rounded",
    "margin": "15"
}

# Analytics / Reporting Tier
analytics_attr = {
    "fontsize": "13",
    "bgcolor": "#F3E5F5",   # Light Purple
    "style": "rounded",
    "margin": "15"
}

# ML / Inference Tier
ml_attr = {
    "fontsize": "13",
    "bgcolor": "#FCE4EC",   # Light Pink/Red
    "style": "rounded",
    "margin": "15"
}
```

Apply to clusters:
```python
with Cluster("Tier Name", graph_attr=tier_attr):
    # add nodes here
```

---

## Troubleshooting

### GraphViz Not Found
**Error**: `ExecutableNotFound: failed to execute WindowsPath('dot')`

**Solution**: Add GraphViz to PATH before running:
```powershell
$env:PATH += ";C:\Program Files\Graphviz\bin"
```

### Import Errors
**Error**: `cannot import name 'ManagedStreamingForKafka'`

**Solution**: MSK lives under `diagrams.aws.analytics`, not `diagrams.aws.database`:
```python
from diagrams.aws.analytics import ManagedStreamingForKafka
```

Always verify with:
```python
from diagrams.aws import analytics
print([x for x in dir(analytics) if not x.startswith('_')])
```

### Cluttered Layout
**Issue**: Auto-generated diagrams have messy node placement.

**Solutions**:
1. Adjust `nodesep` and `ranksep` in `graph_attr`
2. Switch direction: `"rankdir": "TB"` (top-bottom) or `"LR"` (left-right)
3. Simplify cluster nesting depth
4. **Best approach**: Auto-generate, then manually refine in draw.io

### Missing AWS Icons
Some AWS services don't have a dedicated icon in the `diagrams` library. Use the closest logical equivalent or a generic placeholder. Check available icons:
```python
import diagrams.aws.database as db
print(dir(db))
```

---

## Output Files

Each diagram generation produces 3 files, all inside `Use-cases/<usecase-name>/output/`:

| File | Format | Purpose |
|------|--------|---------|
| `*.png` | Static image | Documentation, presentations, AWS MAP proposals |
| `*.dot` | GraphViz DOT (text) | Version control, diff tracking |
| `*.drawio` | Editable diagram | Manual refinement, client-facing polish |

---

## Key Principles

1. **One folder per use case** — Each use case lives under `Use-cases/<usecase-name>/` with its own `instructions.md`, script, and `output/` folder.
2. **Auto-generate first, refine later** — Use Python scripts for 95% of the diagram, polish in draw.io.
3. **Version control DOT files** — Text-based, shows changes clearly in Git diffs.
4. **Color code tiers** — Makes data flow immediately readable.
5. **Use clusters liberally** — Group by logical tier: ingestion, storage, analytics, external.
6. **Label every edge** — Annotate connections with data type (e.g., `"event stream"`, `"cache warm-up"`).
7. **Always add GraphViz to PATH** — Critical step before running any script.
8. **AWS Middle East (UAE) region** — Use `me-central-1` for Gulf deployments.