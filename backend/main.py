from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
import shutil
from datetime import timedelta
import requests

from database import get_db, engine, Base
from models import Student, Assignment, AnalysisResult, AcademicSource
from schemas import (
    StudentRegister,
    StudentLogin,
    Token,
    StudentResponse,
    AssignmentUploadResponse,
    AnalysisResponse,
    SourceSearchRequest,
    AcademicSourceResponse
)
from auth import (
    get_password_hash,
    authenticate_student,
    create_access_token,
    get_current_student
)
from config import settings
from rag_service import rag_service
from file_processor import file_processor

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Academic Assignment Helper API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {
        "message": "Academic Assignment Helper API",
        "version": "1.0.0",
        "endpoints": {
            "auth": ["/auth/register", "/auth/login"],
            "assignments": ["/upload", "/analysis/{id}"],
            "sources": ["/sources"]
        }
    }

@app.post("/auth/register", response_model=StudentResponse)
def register(student_data: StudentRegister, db: Session = Depends(get_db)):
    existing_student = db.query(Student).filter(
        (Student.email == student_data.email) | (Student.student_id == student_data.student_id)
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or Student ID already registered"
        )

    hashed_password = get_password_hash(student_data.password)

    new_student = Student(
        email=student_data.email,
        password_hash=hashed_password,
        full_name=student_data.full_name,
        student_id=student_data.student_id
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student

@app.post("/auth/login", response_model=Token)
def login(login_data: StudentLogin, db: Session = Depends(get_db)):
    student = authenticate_student(db, login_data.email, login_data.password)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    access_token = create_access_token(
        data={"sub": student.email, "student_id": student.id},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/upload", response_model=AssignmentUploadResponse)
async def upload_assignment(
    file: UploadFile = File(...),
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided"
        )

    allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported. Allowed: {', '.join(allowed_extensions)}"
        )

    file_path = os.path.join(UPLOAD_DIR, f"{current_student.id}_{file.filename}")

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        text, word_count = file_processor.extract_text(file_path, file.filename)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing file: {str(e)}"
        )

    assignment = Assignment(
        student_id=current_student.id,
        filename=file.filename,
        original_text=text,
        word_count=word_count
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    
    print(f"[UPLOAD] Assignment uploaded: id={assignment.id}, student_id={current_student.id}")
    print(f"[UPLOAD] Original text preview: {text[:100]}")  # first 100 chars

    try:
        webhook_data = {
            "assignment_id": assignment.id,
            "student_id": current_student.id,
            "student_email": current_student.email,
            "filename": file.filename,
            "file_path": file_path,
            "text": text,
            "word_count": word_count
        }

        response = requests.post(
            settings.N8N_WEBHOOK_URL,
            json=webhook_data,
            timeout=10
        )
        print("[WEBHOOK] Payload sent to n8n:", webhook_data)
        print("[WEBHOOK] Response from n8n:", response.status_code, response.text)

        if response.status_code != 200:
            print(f"n8n webhook warning: {response.status_code}")

    except Exception as e:
        print(f"Error calling n8n webhook: {str(e)}")

    return {
        "assignment_id": assignment.id,
        "message": "Assignment uploaded successfully and analysis started",
        "status": "processing"
    }

@app.get("/analysis/{assignment_id}")
def get_analysis(
    assignment_id: int,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    assignment = db.query(Assignment).filter(
        Assignment.id == assignment_id,
        Assignment.student_id == current_student.id
    ).first()

    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    analysis = db.query(AnalysisResult).filter(
        AnalysisResult.assignment_id == assignment_id
    ).first()

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not ready")

    # Simple dictionary return - no Pydantic model
    return {
        "assignment_id": analysis.assignment_id,
        "plagiarism_score": float(analysis.plagiarism_score) if analysis.plagiarism_score else 0.0,
        "confidence_score": float(analysis.confidence_score) if analysis.confidence_score else 0.0,
        "research_suggestions": analysis.research_suggestions or "No suggestions available",
        "citation_recommendations": analysis.citation_recommendations or "Use APA format",
        "suggested_sources": analysis.suggested_sources or [],
        "flagged_sections": analysis.flagged_sections or [],
        "analyzed_at": analysis.analyzed_at.isoformat() if analysis.analyzed_at else None
    }

@app.post("/sources", response_model=List[AcademicSourceResponse])
def search_sources(
    search_request: SourceSearchRequest,
    current_student: Student = Depends(get_current_student),
    db: Session = Depends(get_db)
):
    sources = rag_service.search_similar_sources(
        db,
        search_request.query,
        search_request.limit
    )

    return [
        AcademicSourceResponse(
            id=source['id'],
            title=source['title'],
            authors=source['authors'],
            publication_year=source['publication_year'],
            abstract=source['abstract'],
            source_type=source['source_type'],
            similarity_score=source['similarity_score']
        )
        for source in sources
    ]

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "academic-assignment-helper"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
