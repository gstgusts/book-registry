# Web Library (Flask)

Server-rendered Flask app for **Authors** and **Books** with:
- List pages (with search)
- Create/Edit pages (simple HTML forms)
- Split blueprints: `authors` and `books`

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python run.py
# Open http://127.0.0.1:5000/
```

## Pages
- Authors: `/authors`, `/authors/new`, `/authors/<id>/edit`
- Books: `/books`, `/books/new`, `/books/<id>/edit`

## Notes
- SQLite DB stored at `app.db` in project root by default. Override with `DATABASE_URL`.

## Docker
cd H:\SynologyDrive\Documents\RTU\2025\ProjektesanasLab\book-registry
docker build -t book-registry:latest .
docker run --rm -p 8000:8000 book-registry:latest

## Enable Alembic
cd H:\SynologyDrive\Documents\RTU\2025\ProjektesanasLab\book-registry
flask --app run db init
flask --app run db migrate -m "init schema"
flask --app run db upgrade

## Alembic fix datetime
Fix the migration file
Open the failing migration:
H:\SynologyDrive\Documents\RTU\2025\ProjektesanasLab\book-registry\migrations\versions\75a135f0e1f6_init_schema.py
At the top, import your type directly:
from app.models.types import EpochMsDate
Replace every app.models.types.EpochMsDate() with just:
EpochMsDate()
(If Alembic rendered it without parentheses, EpochMsDate is fine too—your models use the class directly.)
Run the upgrade again:
cd H:\SynologyDrive\Documents\RTU\2025\ProjektesanasLab\book-registry
flask --app run db upgrade

## Alembic new version
flask --app run db migrate -m "describe the change"
flask --app run db upgrade
