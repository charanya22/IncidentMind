# 🧠 IncidentMind

### AI-Powered Root Cause Analysis with Persistent Operational Memory

IncidentMind is an intelligent incident-response system that investigates production-style incidents, correlates operational evidence, identifies probable root causes, and uses **Hindsight** as persistent memory to learn from previously validated incidents.

Instead of starting every investigation from zero, IncidentMind recalls relevant operational experience and reuses validated knowledge during future investigations.

---

## 🌐 Live Demo

🚀 **Try IncidentMind:**  
[Open Live Application](https://incidentmind-diyfpvuzdzyyqu6qdz8ren.streamlit.app/)

> Select an incident, investigate the available evidence, compare Hindsight Memory ON/OFF, and validate the generated root cause analysis.

---

## ✨ Key Features

- 🔍 Automated incident investigation
- 📜 Log analysis
- 📊 Metrics correlation
- 🚀 Deployment analysis
- 💻 Code-change analysis
- 🎯 Evidence-based Root Cause Analysis
- 🧠 Persistent operational memory with Hindsight
- 🔄 Hindsight Memory ON/OFF comparison
- 👨‍💻 Human validation and feedback
- 💾 Validated knowledge retention
- 📈 Dynamic evidence-based confidence
- 🧪 Controlled RCA evaluation

---

## 🚨 Problem

Production incidents are difficult to diagnose because engineers often need to investigate information scattered across:

- Application logs
- System metrics
- Deployments
- Code changes
- Incident history
- Previous resolutions

Even when a similar incident has already occurred, the knowledge gained from resolving it may not be immediately available during the next incident.

**IncidentMind turns previous incident experience into reusable operational memory.**

---

## 💡 Solution

IncidentMind follows an investigation and learning loop:

```text
Incident
   ↓
Evidence Collection
   ↓
Pattern Detection
   ↓
Evidence Scoring
   ↓
Hindsight Recall
   ↓
Root Cause Analysis
   ↓
Engineer Validation
   ↓
Hindsight Retain
   ↓
Future Investigation
```

For every incident, IncidentMind:

1. Retrieves incident details.
2. Collects relevant logs.
3. Analyzes operational metrics.
4. Checks deployment changes.
5. Checks related code changes.
6. Detects possible failure patterns.
7. Scores candidate root causes using evidence.
8. Recalls relevant operational experience through Hindsight.
9. Produces a root cause analysis with confidence information.
10. Allows an engineer to validate or correct the analysis.
11. Retains validated learning for future investigations.

---

## 🧠 Hindsight — Persistent Operational Memory

Hindsight acts as IncidentMind's long-term operational memory layer.

IncidentMind uses:

- **Recall** — retrieves relevant previous operational experience.
- **Retain** — stores validated incident knowledge.
- **Reflect** — supports reflection over stored knowledge when explicitly used.

### Memory OFF

```text
Current Incident
      ↓
Current Evidence
      ↓
RCA Engine
      ↓
Root Cause
```

The investigation uses the evidence available for the current incident.

### Memory ON

```text
Current Incident
      ↓
Current Evidence ─────────┐
                          ↓
                  Hindsight Recall
                          ↓
               Historical Experience
                          ↓
                      RCA Engine
                          ↓
                     Root Cause
```

This demonstrates the difference between:

**Current evidence only**

and

**Current evidence + learned operational experience**

---

## 🔍 Evidence Correlation

IncidentMind investigates multiple evidence sources:

| Evidence | Purpose |
|---|---|
| 📜 Logs | Detect errors and failure signatures |
| 📊 Metrics | Identify abnormal operational behavior |
| 🚀 Deployments | Detect recent production changes |
| 💻 Code Changes | Identify potentially related modifications |
| 🧠 Hindsight | Recall relevant previous incident experience |

The RCA engine combines these signals rather than relying on a single evidence source.

---

## 🎯 Root Cause Analysis

The evidence-based RCA engine evaluates several failure patterns, including:

- Database connection pool exhaustion
- Cache configuration and eviction problems
- Authentication and identity-provider timeouts
- Queue backlog and consumer concurrency problems

Each investigation can produce:

- Candidate root causes
- Probable root cause
- Supporting evidence
- Recommended remediation
- Confidence level
- Hindsight contribution

Confidence is calculated from the available evidence and recalled experience rather than being displayed as a fixed value.

---

## 🔁 Continuous Learning

IncidentMind includes a human-in-the-loop learning process:

```text
RCA Generated
     ↓
Engineer Review
     ↓
Confirm / Correct
     ↓
Validated Resolution
     ↓
Hindsight Retain
     ↓
Persistent Operational Memory
     ↓
Future Hindsight Recall
```

Validated knowledge can include:

- Service
- Incident symptoms
- Failure pattern
- Root cause
- Resolution
- Recommended remediation
- Engineer feedback

This creates an operational learning loop where useful knowledge can be reused during future investigations.

---

## 🧪 Evaluation

IncidentMind includes a controlled synthetic evaluation pipeline.

Run:

```bash
python evaluate.py
```

The evaluation compares:

```text
Expected Root Cause
        vs
Predicted Root Cause
```

and reports:

- Total evaluated incidents
- Correct predictions
- Overall accuracy
- Failed cases

Reported accuracy represents performance on the project's **controlled synthetic evaluation dataset** and should not be interpreted as production incident-resolution accuracy.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────┐
                    │   Incident ID   │
                    └────────┬────────┘
                             ↓
              ┌──────────────────────────┐
              │    Evidence Collection   │
              │                          │
              │ Logs       Metrics       │
              │ Deploys    Code Changes  │
              └────────────┬─────────────┘
                           ↓
              ┌──────────────────────────┐
              │     RCA Pattern Engine   │
              │   + Evidence Scoring     │
              └────────────┬─────────────┘
                           ↓
              ┌──────────────────────────┐
              │     Hindsight Recall     │
              │    Previous Experience   │
              └────────────┬─────────────┘
                           ↓
              ┌──────────────────────────┐
              │    Root Cause Analysis   │
              └────────────┬─────────────┘
                           ↓
              ┌──────────────────────────┐
              │   Engineer Validation    │
              └────────────┬─────────────┘
                           ↓
              ┌──────────────────────────┐
              │     Hindsight Retain     │
              │    Validated Learning    │
              └──────────────────────────┘
```

---

## 🛠️ Technology Stack

- **Python**
- **Streamlit** — interactive investigation dashboard
- **DuckDB** — local analytical database
- **Pandas** — data processing and evaluation
- **Hindsight Python Client** — persistent operational memory
- **python-dotenv** — environment configuration
- **JSON** — local development memory fallback

---

## 📁 Project Structure

```text
IncidentMind/
│
├── app.py
├── database.py
├── rca_engine.py
├── hindsight_memory.py
│
├── data_generator.py
├── seed_memory.py
├── evaluate.py
│
├── data/
│   └── local_memory.json
│
├── fake_repo/
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/charanya22/IncidentMind.git
cd IncidentMind
```

Create a virtual environment:

```bash
python -m venv .venv
```

### Windows

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file based on `.env.example`:

```env
HINDSIGHT_API_KEY=your_api_key_here
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=incidentmind
```

> ⚠️ Never commit API keys or your real `.env` file to a public repository.

---

## ▶️ Running Locally

Generate the synthetic dataset if required:

```bash
python data_generator.py
```

Seed initial operational memory:

```bash
python seed_memory.py
```

Start IncidentMind:

```bash
streamlit run app.py
```

---

## 🎬 Demo Workflow

```text
Select Incident
      ↓
Analyze Evidence
      ↓
View RCA
      ↓
Compare Memory OFF / ON
      ↓
Inspect Hindsight Recall
      ↓
Engineer Validation
      ↓
Retain Validated Learning
      ↓
Reuse Knowledge in Future Investigations
```

The core idea:

> **IncidentMind doesn't just investigate incidents — it remembers what engineers learned from them.**

---

## 🔒 Safety & Transparency

**Evidence First** — Root-cause conclusions should be supported by observable incident evidence.

**Human Validation** — Engineers validate or correct the generated RCA.

**Transparent Confidence** — Confidence is derived from evidence rather than hard-coded.

**Persistent Learning** — Validated operational knowledge can become reusable memory.

---

## 🚀 Future Improvements

- LLM-assisted RCA reasoning
- Automated log summarization
- Distributed tracing integration
- Real-time observability integrations
- Service dependency graphs
- Incident similarity search
- Post-incident report generation
- Hindsight reflection integrated directly into RCA
- Human-approved automated remediation

---

## 🎯 Vision

Traditional incident response:

```text
Incident → Manual Investigation → Resolution → Knowledge Lost
```

IncidentMind:

```text
Incident
   ↓
Automated Evidence Collection
   ↓
Root Cause Analysis
   ↓
Operational Memory
   ↓
Engineer Validation
   ↓
Continuous Learning
   ↓
Faster Future Investigations
```

**IncidentMind transforms incident resolution from a one-time activity into reusable operational knowledge.**

---

## 👥 Team
Pixel Perfect
**IncidentMind**
An engineering project focused on AI-assisted incident investigation, persistent operational memory, and evidence-based root cause analysis.
