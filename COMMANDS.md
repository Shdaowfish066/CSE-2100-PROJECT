# Quick Command Reference

## Virtual Environment

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application (Uvicorn)

### Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Start Production Server
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Kill Server (if running in background)
```bash
pkill -f "uvicorn app.main:app"
```

---

## Database Migrations (Alembic)

### Initialize Migration (First Time)
```bash
alembic init migrations
```

### Create New Migration (Auto-detect)
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Create Manual Migration
```bash
alembic revision -m "Description of changes"
```

### Apply Migrations to Database
```bash
alembic upgrade head
```

### Rollback Last Migration
```bash
alembic downgrade -1
```

### View Migration History
```bash
alembic history
```

### Check Current Database Version
```bash
alembic current
```

---

## Git Commands

### Check Git Status
```bash
git status
```

### Stage All Changes
```bash
git add .
```

### Commit Changes
```bash
git commit -m "Your commit message here"
```

### Push to GitHub
```bash
git push origin main
```

### Pull Latest Changes
```bash
git pull origin main
```

### View Commit Log
```bash
git log --oneline
```

### Create New Branch
```bash
git checkout -b branch-name
```

### Switch to Branch
```bash
git checkout branch-name
```

### Push New Branch to GitHub
```bash
git push origin branch-name
```

---

## Useful Shortcuts

### Full Setup from Scratch
```bash
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Push to GitHub (Quick)
```bash
git add .
git commit -m "Update"
git push origin main
```

### Check If Server is Running
```bash
lsof -i :8000
```

### Force Kill Port 8000
```bash
lsof -ti:8000 | xargs kill -9
```

---

## Python Testing

### Run All Tests
```bash
python test_endpoints.py
```

### Check Python Version
```bash
python --version
```

### Run Python Script
```bash
python script_name.py
```

---

## Environment Variables

### View .env File
```bash
cat .env
```

### Edit .env File
```bash
nano .env
```

---

## Common Issues

### Port 8000 Already in Use
```bash
lsof -ti:8000 | xargs kill -9
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Connection Issues
```bash
alembic current
alembic upgrade head
```

### Virtual Environment Not Activating
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Project Structure

```
/Users/tahsanuddin/Desktop/Project CSE 2100/
├── app/
│   ├── main.py              # FastAPI entry point
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── models/              # SQLAlchemy models
│   ├── schemas/             # Pydantic schemas
│   ├── routers/             # API endpoints
│   ├── utils/               # Utility functions
│   └── middleware/          # Middleware
├── migrations/              # Alembic migrations
├── uploads/                 # File uploads directory
├── venv/                    # Virtual environment
├── requirements.txt         # Dependencies
├── alembic.ini             # Alembic config
└── .env                    # Environment variables
```

---

## API Information

- **Base URL**: http://localhost:8000
- **Endpoints**: 40 total (10 per developer)
- **Test Pass Rate**: 100% (39/39)
- **Developers**:
  - Shihab (2303147): Auth, Users, Reports
  - Arpon (2303134): Posts, Post Voting
  - Emon (2303173): Comments, Comment Voting, Reports
  - Tahsan (2303133): Messages, Files
