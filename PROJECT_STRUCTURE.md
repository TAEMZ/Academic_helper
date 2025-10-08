# Project Structure

```
academic-assignment-helper/
│
├── README.md                          # Main documentation
├── SETUP_INSTRUCTIONS.md              # Step-by-step setup guide
├── TECHNICAL_DOCUMENTATION.md         # Architecture and design decisions
├── DEMO_GUIDE.md                      # Video demo creation guide
├── PROJECT_STRUCTURE.md               # This file
│
├── .env                               # Environment variables (DO NOT COMMIT)
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
│
├── docker-compose.yml                 # Multi-service orchestration
├── init.sql                           # Database schema initialization
│
├── backend/                           # FastAPI application
│   ├── main.py                        # API endpoints and FastAPI app
│   ├── auth.py                        # JWT authentication & authorization
│   ├── models.py                      # SQLAlchemy database models
│   ├── schemas.py                     # Pydantic request/response schemas
│   ├── database.py                    # Database connection setup
│   ├── config.py                      # Configuration management
│   ├── rag_service.py                 # RAG implementation with embeddings
│   ├── file_processor.py              # PDF/DOCX/TXT text extraction
│   ├── requirements.txt               # Python dependencies
│   └── Dockerfile                     # Backend container definition
│
├── workflows/                         # n8n automation
│   └── assignment_analysis_workflow.json  # Complete analysis pipeline
│
├── data/                              # Sample data and scripts
│   ├── sample_academic_sources.json   # 10 academic papers for RAG
│   └── seed_sources.py                # Database seeding script
│
├── uploads/                           # Student assignment files
│   └── .gitkeep                       # Keep empty directory in git
│
└── test_api.py                        # Automated API testing script
```

## File Descriptions

### Root Level

**README.md**
- Quick start guide
- API documentation
- Testing instructions
- Technology stack overview

**SETUP_INSTRUCTIONS.md**
- Detailed setup process
- Prerequisites
- Configuration steps
- Troubleshooting guide

**TECHNICAL_DOCUMENTATION.md**
- System architecture
- RAG pipeline implementation
- AI prompting strategy
- Database design rationale
- Security implementation details

**DEMO_GUIDE.md**
- 5-minute demo script
- Recording tips
- Section-by-section walkthrough
- Submission checklist

**docker-compose.yml**
- Service definitions: PostgreSQL, Redis, n8n, FastAPI, PgAdmin
- Network configuration
- Volume mounts
- Health checks

**init.sql**
- Database schema (students, assignments, analysis_results, academic_sources)
- pgvector extension setup
- Indexes for performance
- Sample data

### Backend Directory

**main.py** (7KB)
- FastAPI application setup
- API endpoints:
  - `POST /auth/register` - Student registration
  - `POST /auth/login` - JWT authentication
  - `POST /upload` - Assignment upload
  - `GET /analysis/{id}` - Retrieve results
  - `POST /sources` - RAG source search
- CORS middleware
- File handling

**auth.py** (2.6KB)
- bcrypt password hashing
- JWT token creation and verification
- `get_current_student` dependency
- Token expiration handling

**models.py** (2.4KB)
- SQLAlchemy ORM models:
  - `Student` - User accounts
  - `Assignment` - Uploaded assignments
  - `AnalysisResult` - Analysis data
  - `AcademicSource` - RAG knowledge base
- Relationships and foreign keys

**schemas.py** (1.5KB)
- Pydantic validation schemas:
  - `StudentRegister` - Registration input
  - `StudentLogin` - Login input
  - `Token` - JWT response
  - `AssignmentUploadResponse` - Upload result
  - `AnalysisResponse` - Analysis output
  - `SourceSearchRequest` - RAG query

**database.py** (532 bytes)
- SQLAlchemy engine setup
- Session management
- `get_db` dependency

**config.py** (600 bytes)
- Pydantic settings management
- Environment variable loading
- Type-safe configuration

**rag_service.py** (4.4KB)
- Embedding generation with Gemini
- Redis caching for embeddings
- Vector similarity search
- Plagiarism detection logic
- Academic source management

**file_processor.py** (1.9KB)
- PDF text extraction (PyPDF2)
- DOCX text extraction (python-docx)
- TXT file reading
- Word count calculation

**requirements.txt** (343 bytes)
- FastAPI and Uvicorn
- Authentication libraries (PyJWT, Passlib)
- Database drivers (psycopg2, SQLAlchemy)
- AI libraries (google-generativeai)
- File processing (PyPDF2, python-docx)

**Dockerfile** (315 bytes)
- Python 3.11 slim base image
- Dependency installation
- Application setup

### Workflows Directory

**assignment_analysis_workflow.json** (10KB)
- n8n workflow export
- 8 nodes:
  1. Webhook trigger
  2. Text extraction and preprocessing
  3. Assignment metadata update
  4. RAG source retrieval
  5. AI prompt preparation
  6. Gemini analysis
  7. Result structuring
  8. Database storage and response

### Data Directory

**sample_academic_sources.json** (15KB)
- 10 academic papers across domains:
  - Machine Learning
  - Climate Change
  - Psychology
  - Economics
  - AI
  - Environmental Science
- Each with title, authors, year, abstract, full_text, source_type

**seed_sources.py** (2KB)
- Connects to PostgreSQL
- Generates embeddings for each source
- Inserts into academic_sources table
- Idempotent (won't duplicate if run multiple times)

### Test Files

**test_api.py** (7KB)
- Automated testing script
- Tests all endpoints in sequence:
  1. Health check
  2. Registration
  3. Login
  4. Upload
  5. Analysis retrieval
  6. Source search
- Creates sample assignment
- Retries analysis until ready

## Data Flow

```
1. Student uploads assignment (PDF/DOCX/TXT)
   ↓
2. Backend extracts text and saves to database
   ↓
3. Backend triggers n8n webhook with assignment data
   ↓
4. n8n workflow:
   a. Preprocesses text (topic detection, level assessment)
   b. Updates assignment metadata
   c. Searches RAG database for relevant sources
   d. Prepares AI prompt with context
   e. Calls Gemini for analysis
   f. Detects plagiarism via similarity search
   g. Structures results as JSON
   h. Stores in analysis_results table
   ↓
5. Student retrieves analysis via GET /analysis/{id}
```

## Database Schema Flow

```
students (id, email, password_hash, full_name, student_id)
    ↓ 1:N
assignments (id, student_id, filename, original_text, topic, word_count)
    ↓ 1:1
analysis_results (id, assignment_id, suggested_sources, plagiarism_score, ...)

academic_sources (id, title, authors, abstract, embedding[768])
    ↑
    Used by RAG for similarity search
```

## Technology Stack by File

| File | Technologies |
|------|-------------|
| `main.py` | FastAPI, SQLAlchemy, requests |
| `auth.py` | PyJWT, Passlib (bcrypt) |
| `rag_service.py` | Gemini AI, pgvector, Redis |
| `file_processor.py` | PyPDF2, python-docx |
| `docker-compose.yml` | Docker, PostgreSQL, Redis, n8n |
| `init.sql` | PostgreSQL, pgvector extension |
| `workflow.json` | n8n, Gemini AI |

## Configuration Files

**.env** (Private - Not committed)
- Actual credentials and API keys
- Used by Docker Compose and backend

**.env.example** (Committed)
- Template showing required variables
- No actual secrets

**.gitignore**
- Excludes: .env, __pycache__, uploads/*, *.log
- Includes: uploads/.gitkeep (empty directory tracking)

## Entry Points

1. **Docker Compose**: `docker-compose up -d`
   - Starts all services
   - Initializes database
   - Waits for health checks

2. **FastAPI**: `http://localhost:8000`
   - API endpoints
   - Swagger docs at `/docs`

3. **n8n**: `http://localhost:5678`
   - Workflow dashboard
   - Credential management

4. **Testing**: `python test_api.py`
   - Automated end-to-end test

## Development Workflow

1. Modify backend code in `backend/`
2. Changes auto-reload (uvicorn --reload)
3. Update workflow in n8n UI
4. Export workflow to `workflows/`
5. Test with `test_api.py`
6. Commit changes (excluding .env)

## Production Considerations

Files to modify for production:
- `.env` - Strong passwords, real API keys
- `docker-compose.yml` - Resource limits, replicas
- `backend/main.py` - CORS allowed origins
- `backend/config.py` - Additional security settings

## Size Overview

| Component | Size |
|-----------|------|
| Backend code | ~30KB |
| Documentation | ~45KB |
| Docker configs | ~5KB |
| Sample data | ~20KB |
| Workflow | ~10KB |
| **Total** | ~110KB |

## Lines of Code

| Language | Files | Lines |
|----------|-------|-------|
| Python | 10 | ~800 |
| SQL | 1 | ~70 |
| JSON | 2 | ~400 |
| YAML | 1 | ~100 |
| Markdown | 5 | ~1500 |
| **Total** | 19 | ~2870 |

## External Dependencies

- **Docker Images**: postgres:15, redis:7, n8nio/n8n, python:3.11-slim
- **Python Packages**: 17 (see requirements.txt)
- **APIs**: Google Gemini AI (embedding-001, gemini-pro)

---

This structure follows best practices for microservices, clear separation of concerns, and maintainability.
