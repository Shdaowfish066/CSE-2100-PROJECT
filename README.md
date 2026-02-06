# Anonymous Content Sharing Platform - Backend

## Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env with your Supabase credentials
```

### 4. Run Database Migrations
```bash
# Execute SQL from app/schemas/database.py in Supabase SQL Editor
```

### 5. Start Development Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation
Access interactive API docs at: http://localhost:8000/docs

## Project Structure
```
backend/
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Environment config
│   ├── database.py          # Supabase connection
│   ├── models/              # Pydantic models
│   ├── schemas/             # Database schemas
│   ├── routers/             # API endpoints
│   ├── utils/               # Utility functions
│   └── middleware/          # Middleware
└── requirements.txt
```
