# IncidentMind — Hindsight Incident Response Agent

Incident Response Agent prototype.

## What it demonstrates

Incident ID → evidence collection → candidate root causes → evidence scoring → Hindsight recall → RCA → engineer correction → Hindsight retain → better future investigation.

The demo uses controlled synthetic incidents so the RCA can be evaluated quantitatively. It does **not** hard-code a fake 99% confidence value.

## Stack

- Python
- Streamlit
- DuckDB
- pandas
- Hindsight Python client
- Local JSON fallback memory when Hindsight credentials are absent

Hindsight's official Python client supports `create_bank`, `retain`, `recall`, and `reflect`. See:
https://hindsight.vectorize.io/sdks/python

## Setup

### Windows PowerShell

```powershell
mkdir incidentmind
cd incidentmind
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
python data_generator.py
python seed_memory.py
streamlit run app.py
```

### macOS/Linux

```bash
mkdir incidentmind
cd incidentmind
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python data_generator.py
python seed_memory.py
streamlit run app.py
```

If PowerShell blocks activation, run:
```powershell
Set-ExecutionPolicy -Scope Process Bypass
```

## Hindsight

Put your Hindsight API key in `.env`:

```text
HINDSIGHT_API_KEY=...
HINDSIGHT_BASE_URL=https://api.hindsight.vectorize.io
HINDSIGHT_BANK_ID=incidentmind
```

Without a key, the application still runs using `data/local_memory.json`, so you can build the UI and RCA engine first.

## Demo

1. Open the dashboard.
2. Investigate `INC-1012`.
3. Show evidence and the high-confidence RCA.
4. Submit engineer feedback.
5. Click **Learn from this incident**.
6. Investigate a later similar incident such as `INC-1057`.
7. Show Hindsight recalling the previous correction.
8. Open **Evaluation** to show the 100-incident benchmark.

## Important claim

Use wording such as:

> "99% RCA accuracy on our controlled 100-incident benchmark."

Do not claim 99% accuracy on production incidents unless you have evaluated it on a representative real-world dataset.
