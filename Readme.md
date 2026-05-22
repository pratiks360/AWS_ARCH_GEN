<p align="center">
  <h1 align="center">🏗️ AWS_ARCH_GEN</h1>
  <p align="center">
    <strong>AI-powered AWS architecture diagram generator — describe a use case, get a production-ready diagram.</strong>
  </p>
  <p align="center">
    <img src="https://img.shields.io/badge/Powered_by-Claude_Code-e11d48?style=for-the-badge" alt="Claude Code">
    <img src="https://img.shields.io/badge/Cloud-AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS">
    <img src="https://img.shields.io/github/last-commit/pratiks360/AWS_ARCH_GEN?style=for-the-badge&label=Last+Commit" alt="Last Commit">
    <img src="https://img.shields.io/github/license/pratiks360/AWS_ARCH_GEN?style=for-the-badge" alt="License">
  </p>
</p>

---

## 📋 Table of Contents

- [What Is This?](#-what-is-this)
- [Features](#-features)
- [How It Works](#-how-it-works)
- [Quick Start](#-quick-start)
- [Repository Structure](#-repository-structure)
- [Supported AWS Services](#️-supported-aws-services)
- [Use Case Examples](#-use-case-examples)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ What Is This?

**AWS_ARCH_GEN** is a Claude Code–powered toolkit that converts plain-language use case descriptions into detailed AWS architecture diagrams. Drop a use case markdown file into the `Use-cases/cases/` folder, point Claude Code at the relevant service reference in `Arch-diagrams/`, and get a structured architecture diagram generated for you — no diagramming tool required.

> 💡 **How to use →** Run Claude Code in this repo and feed it `prompt.txt` — it reads the use case and service definitions and renders an architecture diagram automatically.

---

## 🎯 Features

| Feature | Description |
|---|---|
| 🤖 **AI-Driven Generation** | Uses Claude Code to interpret use-case context and map it to AWS services automatically |
| 🗄️ **11 AWS DB Services Covered** | Comprehensive reference docs for RDS, Aurora, DynamoDB, Redshift, Neptune, and more |
| 📂 **Use-Case Library** | Pre-built use case files (e.g. supply chain) to bootstrap diagram generation |
| 📐 **Arch Diagram Templates** | Reference markdown files per AWS service for consistent, accurate diagrams |
| 🔍 **Service Selection Guidance** | Each service entry explains when to use it vs. alternatives — no more guessing |
| 🔄 **Extensible** | Add new use cases or service docs as plain `.md` files — no code changes needed |

---

## 🧩 How It Works

```
┌────────────────┐   reads prompt.txt   ┌───────────────────┐   maps services   ┌──────────────────┐
│                │  ─────────────────►  │                   │  ───────────────►  │                  │
│  Your Use Case │                      │   Claude Code     │                   │  Arch-diagrams/  │
│  (cases/*.md)  │                      │   Agent           │                   │  service docs    │
│                │  ◄─────────────────  │                   │  ◄───────────────  │                  │
└────────────────┘  outputs diagram     └───────────────────┘   resolves refs   └──────────────────┘
```

1. **Describe the use case** — Write or pick a use case file (e.g. `supply.md` for supply chain)
2. **Prompt Claude Code** — The `prompt.txt` instructs Claude to read the use case and relevant service reference docs
3. **Diagram is generated** — Claude Code outputs a structured AWS architecture diagram with service selection rationale

---

## 🚀 Quick Start

**Prerequisites:** [Claude Code](https://claude.ai/code) installed (`npm install -g @anthropic-ai/claude-code`)

```bash
# 1. Clone the repo
git clone https://github.com/pratiks360/AWS_ARCH_GEN.git
cd AWS_ARCH_GEN

# 2. Open Claude Code in the repo
claude

# 3. Paste or reference the prompt
# Inside Claude Code, run the instruction from prompt.txt:
# "Goto folder Arch-diagrams and understand aws_managed_db_agent.md
#  and in use-cases folder supply.md and create an architectural diagram for me"
```

### Adding Your Own Use Case

```bash
# Create a new use case file
touch Use-cases/cases/my_use_case.md
# Describe your system requirements in plain English, then run Claude Code
```

---

## 📁 Repository Structure

```
AWS_ARCH_GEN/
├── Arch-diagrams/               # Service reference docs for diagram generation
│   └── aws_managed_db_agent.md  # AWS managed database services reference
├── Use-cases/
│   └── cases/
│       └── supply.md            # Example: supply chain use case
├── prompt.txt                   # Master prompt for Claude Code
├── services.txt                 # Quick-reference for all 11 AWS DB services
└── .gitignore
```

---

## 🛠️ Supported AWS Services

The `services.txt` and `Arch-diagrams/` folder cover the full spectrum of AWS managed database services:

| Service | Type | Best For |
|---|---|---|
| **Amazon RDS** | Relational | MySQL, PostgreSQL, Oracle, SQL Server workloads |
| **Amazon Aurora** | Relational | High-throughput MySQL/PostgreSQL with multi-AZ |
| **Amazon DynamoDB** | NoSQL Key-Value | Single-digit ms at any scale |
| **Amazon ElastiCache** | In-Memory | Sessions, leaderboards, real-time analytics |
| **Amazon Redshift** | Data Warehouse | OLAP, analytics, exabyte-scale S3 queries |
| **Amazon Neptune** | Graph | Fraud detection, knowledge graphs, social networks |
| **Amazon Keyspaces** | Wide Column | Serverless Cassandra workloads |
| **Amazon DocumentDB** | Document | MongoDB-compatible apps |
| **Amazon Timestream** | Time-Series | IoT and operational telemetry |
| **Amazon QLDB** | Ledger | Audit trails, financial records |
| **Amazon MemoryDB for Redis** | Durable In-Memory | Ultra-fast + durable Redis workloads |

---

## 💡 Use Case Examples

The `Use-cases/cases/` folder includes pre-built scenarios to get started quickly:

**Supply Chain (`supply.md`)** — Models inventory tracking, supplier data, and logistics with a mix of relational (RDS/Aurora) and time-series (Timestream) services.

To add more use cases, create a `.md` file describing your system's data flows, scale requirements, and consistency needs — Claude Code will map the right AWS services automatically.

---

## 🐛 Troubleshooting

**Q: Claude Code says it can't find the file referenced in prompt.txt**
A: Make sure you're running Claude Code from the repo root (`cd AWS_ARCH_GEN`) so relative paths resolve correctly.

**Q: The generated diagram uses a service I didn't expect**
A: Check `services.txt` — Claude selects services based on the characteristics described there. Update your use case file to add constraints (e.g. "must be serverless" or "requires SQL").

**Q: How do I add a new AWS service category (e.g. compute, networking)?**
A: Add a new `.md` file to `Arch-diagrams/` following the same format as `aws_managed_db_agent.md`, then reference it in your prompt.

---

## 🤝 Contributing

Got a use case to share or a new AWS service reference to add? PRs are welcome! The project is intentionally simple — just markdown files and a prompt, so contributions are low-friction.

1. Fork the repo
2. Add your use case to `Use-cases/cases/` or a new service doc to `Arch-diagrams/`
3. Open a PR with a brief description of what you added

---

## 📄 License

This project is open source under the [MIT License](LICENSE).

---

<p align="center">
  <sub>Built with ❤️ for cloud architects and developers who'd rather describe than draw.</sub>
</p>
