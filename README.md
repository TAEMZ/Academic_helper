# Academic Assignment Helper & Plagiarism Detector

A comprehensive RAG-powered system that analyzes student assignments, provides research suggestions, and detects potential plagiarism using AI and vector similarity search.

---

## 🎯 For Beginners

**New to this?** Start here:

1. 📘 **[QUICK_START.md](QUICK_START.md)** - Get running in 5 minutes
2. 📗 **[BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)** - Detailed step-by-step guide
3. ✅ **[check_setup.py](check_setup.py)** - Validate your setup
4. 🧪 **[test_api.py](test_api.py)** - Automated testing

**Just want to test it?**
```bash
# 1. Add your Gemini API key to .env
# 2. Run these commands:
docker-compose up -d
sleep 30
python check_setup.py
docker-compose exec backend python /data/seed_sources.py
python test_api.py
```

---

## 🏗️ Architecture

The system consists of:
- **FastAPI Backend**: REST API with JWT authentication
- **PostgreSQL with pgvector**: Database with vector similarity search
- **n8n**: Workflow automation for assignment processing
- **Redis**: Caching for embeddings
- **Gemini AI**: Text embeddings and analysis

## 🔐 Security Features

- JWT-based authentication for all protected endpoints
- Bcrypt password hashing
- Row-level security through student ID verification
- CORS protection

## 📋 Prerequisites

- Docker and Docker Compose installed
- Gemini API key ([Get it here](https://makersuite.google.com/app/apikey))
- At least 4GB RAM available for Docker
- Ports 5432, 5678, 6379, 8000, 5050 available

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd academic-assignment-helper
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 3. Start All Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL with pgvector (port 5432)
- Redis (port 6379)
- n8n (port 5678)
- FastAPI backend (port 8000)
- PgAdmin (port 5050)

### 4. Wait for Services to be Ready

```bash
docker-compose logs -f backend
```

Wait until you see: `Application startup complete.`

### 5. Seed Academic Sources

```bash
docker-compose exec backend python /data/seed_sources.py
```

This populates the database with sample academic papers for RAG testing.

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Interactive API Docs
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Authentication Endpoints

#### Register New Student
```http
POST /auth/register
Content-Type: application/json

{
  "email": "student@university.edu",
  "password": "secure_password",
  "full_name": "John Doe",
  "student_id": "STU12345"
}
```

Response:
```json
{
  "id": 1,
  "email": "student@university.edu",
  "full_name": "John Doe",
  "student_id": "STU12345",
  "created_at": "2025-01-01T00:00:00"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "student@university.edu",
  "password": "secure_password"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Protected Endpoints (Require JWT Token)

#### Upload Assignment
```http
POST /upload
Authorization: Bearer <your_jwt_token>
Content-Type: multipart/form-data

file: <assignment.pdf|.docx|.txt>
```

Response:
```json
{
  "assignment_id": 1,
  "message": "Assignment uploaded successfully and analysis started",
  "status": "processing"
}
```

#### Get Analysis Results
```http
GET /analysis/{assignment_id}
Authorization: Bearer <your_jwt_token>
```

Response:
```json
{
  "id": 1,
  "assignment_id": 1,
  "suggested_sources": [
    {
      "title": "Machine Learning: A Probabilistic Perspective",
      "authors": "Kevin Murphy",
      "relevance": "high"
    }
  ],
  "plagiarism_score": 0.15,
  "flagged_sections": [],
  "research_suggestions": "Expand on theoretical foundations...",
  "citation_recommendations": "Use APA format for citations",
  "confidence_score": 0.85,
  "analyzed_at": "2025-01-01T00:00:00"
}
```

#### Search Academic Sources
```http
POST /sources
Authorization: Bearer <your_jwt_token>
Content-Type: application/json

{
  "query": "machine learning algorithms",
  "limit": 5
}
```

Response:
```json
[
  {
    "id": 1,
    "title": "Machine Learning: A Probabilistic Perspective",
    "authors": "Kevin Murphy",
    "publication_year": 2012,
    "abstract": "Comprehensive introduction to ML...",
    "source_type": "textbook",
    "similarity_score": 0.92
  }
]
```

## 🔄 n8n Workflow

### Access n8n Dashboard
```
http://localhost:5678
```

Credentials:
- Username: `admin`
- Password: `admin123`

### Import Workflow

1. Open n8n at http://localhost:5678
2. Click "Import from File"
3. Select `workflows/assignment_analysis_workflow.json`
4. Configure credentials:
   - PostgreSQL: Use connection details from `.env`
   - Google Gemini API: Add your Gemini API key
5. Activate the workflow

### Workflow Steps

1. **Webhook Trigger**: Receives assignment data from FastAPI
2. **Text Extraction**: Preprocesses and analyzes text
3. **Update Assignment**: Stores metadata in database
4. **RAG Source Search**: Queries vector database for relevant sources
5. **AI Analysis**: Uses Gemini to analyze assignment
6. **Plagiarism Detection**: Compares against academic sources
7. **Store Results**: Saves analysis to database
8. **Webhook Response**: Returns success status

## 🗄️ Database Schema

### Students Table
```sql
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Assignments Table
```sql
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id),
    filename TEXT NOT NULL,
    original_text TEXT,
    topic TEXT,
    academic_level TEXT,
    word_count INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Analysis Results Table
```sql
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER REFERENCES assignments(id),
    suggested_sources JSONB,
    plagiarism_score FLOAT DEFAULT 0.0,
    flagged_sections JSONB,
    research_suggestions TEXT,
    citation_recommendations TEXT,
    confidence_score FLOAT DEFAULT 0.0,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Academic Sources Table (RAG)
```sql
CREATE TABLE academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT DEFAULT 'paper',
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧪 Testing the System

### 1. Test with cURL

#### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@student.com",
    "password": "test123",
    "full_name": "Test Student",
    "student_id": "TEST001"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@student.com",
    "password": "test123"
  }'
```

Save the `access_token` from the response.

#### Upload Assignment
```bash
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@sample_assignment.pdf"
```

#### Get Analysis
```bash
curl -X GET http://localhost:8000/analysis/1 \
  -H "Authorization: Bearer <your_token>"
```

### 2. Test with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "python@test.com",
    "password": "test123",
    "full_name": "Python Test",
    "student_id": "PY001"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "python@test.com",
    "password": "test123"
})
token = response.json()["access_token"]

# Upload
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("assignment.pdf", "rb")}
response = requests.post(f"{BASE_URL}/upload", headers=headers, files=files)
assignment_id = response.json()["assignment_id"]

# Get Analysis
response = requests.get(f"{BASE_URL}/analysis/{assignment_id}", headers=headers)
print(response.json())
```

## 🔍 PgAdmin Access

Access the database GUI at http://localhost:5050

Credentials:
- Email: `admin@admin.com`
- Password: `admin123`

Add Server:
- Host: `postgres`
- Port: `5432`
- Database: `academic_helper`
- Username: `student`
- Password: `secure_password`

## 🛠️ Development

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f n8n
docker-compose logs -f postgres
```

### Restart Services
```bash
docker-compose restart backend
```

### Rebuild Backend
```bash
docker-compose up -d --build backend
```

### Access Backend Shell
```bash
docker-compose exec backend bash
```

### Run Database Migrations
```bash
docker-compose exec postgres psql -U student -d academic_helper -f /docker-entrypoint-initdb.d/init.sql
```

## 📊 Project Structure

```
academic-assignment-helper/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── auth.py                 # JWT authentication
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database connection
│   ├── config.py               # Configuration
│   ├── rag_service.py          # RAG implementation
│   ├── file_processor.py       # File text extraction
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Backend container
├── workflows/
│   └── assignment_analysis_workflow.json
├── data/
│   ├── sample_academic_sources.json
│   └── seed_sources.py
├── uploads/                    # Assignment files
├── docker-compose.yml          # Service orchestration
├── init.sql                    # Database schema
├── .env.example                # Environment template
└── README.md
```

## 🔧 Troubleshooting

### Services won't start
```bash
docker-compose down -v
docker-compose up -d
```

### Backend can't connect to database
Wait 30 seconds for PostgreSQL to fully initialize, then:
```bash
docker-compose restart backend
```

### n8n webhook not working
1. Ensure n8n workflow is activated
2. Check webhook URL matches `.env` configuration
3. Verify PostgreSQL credentials in n8n

### Embedding generation fails
- Verify `GEMINI_API_KEY` is set correctly in `.env`
- Check Gemini API quota at https://makersuite.google.com/

## 📦 Technology Stack

- **Backend**: FastAPI, SQLAlchemy, psycopg2
- **Authentication**: PyJWT, Passlib (bcrypt)
- **AI/ML**: Google Generative AI (Gemini)
- **Database**: PostgreSQL 15 with pgvector extension
- **Cache**: Redis 7
- **Automation**: n8n
- **File Processing**: PyPDF2, python-docx

## 🎯 Key Features

✅ JWT-based authentication with bcrypt password hashing
✅ Multi-format assignment upload (PDF, DOCX, TXT)
✅ RAG-powered source recommendations using vector similarity
✅ AI-driven plagiarism detection with Gemini
✅ Automated workflow processing with n8n
✅ Comprehensive analysis with confidence scoring
✅ Citation format recommendations
✅ RESTful API with OpenAPI documentation

## 📧 Submission

Submit your implementation to: **yordanos.dev1@gmail.com**

Include:
1. GitHub repository link
2. 5-minute demo video
3. Technical documentation

## 📄 License

MIT License - Educational purposes only

## 👥 Support

For issues or questions, please open an issue on GitHub or contact the maintainer.

---

**Built with ❤️ for Academic Excellence**
