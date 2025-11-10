# PostgreSQL Students CRUD — Mini Demo

Tiny, self-contained CRUD with a Python CLI over a PostgreSQL `students` table.  
Designed for a ≤5-minute walkthrough.

- **DB:** PostgreSQL 14+
- **Runtime:** Python 3.10+
- **Optional:** pgAdmin for visual checks




## Quick Start

```bash
# 1) Create & activate venv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install deps
pip install -r requirements.txt

# 3) Configure DB connection
cp .env.example .env
# then edit .env with your values

# 4) Create table & seed data (run db.sql in psql or pgAdmin Query Tool)

# 5) Try the CLI
python app.py get_all
python app.py add --first "Ana" --last "Lopez" --email "ana.lopez@example.com" --date "2024-09-01"
python app.py update_email --id 1 --email "johnny.doe@example.com"
python app.py delete --id 3
.
├─ app.py          # Python CLI for CRUD
├─ db.sql          # DDL + seed data
└─ README.md
