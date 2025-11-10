PostgreSQL Students CRUD - Mini Demo

Tiny, self-contained CRUD with a Python CLI over a PostgreSQL students table.  

DB: PostgreSQL 14+
Runtime: Python 3.10+




Quick Start

```bash
#Create & activate venv
python -m venv .venv
#Windows
.venv\Scripts\activate
#macOS/Linux
source .venv/bin/activate



#Configure DB connection
cp .env.example .env
#then edit .env with your values

#Create table & seed data (run db.sql in psql or pgAdmin Query Tool)

#Try the CLI
python app.py get_all
python app.py add --first "Ana" --last "Lopez" --email "ana.lopez@example.com" --date "2024-09-01"
python app.py update_email --id 1 --email "johnny.doe@example.com"
python app.py delete --id 3
.
├─ app.py          # Python CLI for CRUD
├─ db.sql          # DDL + seed data
└─ README.md
