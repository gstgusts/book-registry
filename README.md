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
