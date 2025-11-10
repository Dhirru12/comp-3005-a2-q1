postgreSQL Students CRUD

A tiny, self-contained demo that satisfies the assignment requirements:

SQL to create/seed a students table

Python CLI with four ops: getAllStudents, addStudent, updateStudentEmail, deleteStudent

A quick walkthrough for a ≤5-minute demo video

0) Requirements

PostgreSQL 14+

Python 3.10+

(Optional) pgAdmin for visual checks

1) Create the table and seed data

Run this in psql (or paste into pgAdmin → Query Tool):

-- Reset and create 'students' table
DROP TABLE IF EXISTS students;

CREATE TABLE students (
    student_id SERIAL PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name  TEXT NOT NULL,
    email      TEXT NOT NULL UNIQUE,
    enrollment_date DATE
);

INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES
('John', 'Doe', 'john.doe@example.com', '2023-09-01'),
('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),
('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');


Pro tip: Re-run the script before recording so your video starts from a clean slate.

2) App configuration

Copy .env.example → .env and fill in your connection values:

PGHOST=localhost
PGPORT=5432
PGDATABASE=YOUR_DB
PGUSER=YOUR_USER
PGPASSWORD=YOUR_PASS


Finding these in pgAdmin: right-click your server → Properties → check Host name/address and Port. For a database, open it and check its name; your user is the role you connect with.

3) Install dependencies
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

4) Run CRUD from the CLI

Each command prints the current table so graders can see the effect immediately.

List all:

python app.py get_all


Insert:

python app.py add --first "Ana" --last "Lopez" --email "ana.lopez@example.com" --date "2024-09-01"


Update email (by id):

python app.py update_email --id 1 --email "johnny.doe@example.com"


Delete (by id):

python app.py delete --id 3

5) Suggested video outline (≤ 5 minutes)

In pgAdmin, run db.sql; show the three seed rows (John/Jane/Jim).

In terminal, run get_all.

Run add (Ana Lopez); switch to pgAdmin to show the new row.

Run update_email (id=1); confirm the change in pgAdmin.

Run delete (id=3); confirm it’s gone in pgAdmin.

Final get_all to show the end state.

6) Project layout
pg-crud-students/
├─ app.py                # CRUD + simple CLI
├─ db.sql                # DDL + seed data
├─ requirements.txt
├─ .env.example
└─ README.md

Notes for TAs

Functions align 1:1 with rubric items:

getAllStudents: SELECT list

addStudent: INSERT ... RETURNING

updateStudentEmail: UPDATE by primary key

deleteStudent: DELETE by primary key

Constraints: SERIAL PK, NOT NULL fields, UNIQUE email, sensible types.

Code and SQL include explanatory comments.

Troubleshooting

psycopg connection errors: verify .env values and that PostgreSQL is running.

Email unique violation: change the test email or delete the existing row first.

Port/host issues in pgAdmin: check server Properties → host/port; ensure you’re connecting to the same DB the app uses.
