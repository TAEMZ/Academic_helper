from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class StudentRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    student_id: str

class StudentLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    student_id: Optional[int] = None

class StudentResponse(BaseModel):
    id: int
    email: str
    full_name: str
    student_id: str
    created_at: datetime

    class Config:
        from_attributes = True

class AssignmentUploadResponse(BaseModel):
    assignment_id: int
    message: str
    status: str


class AnalysisResponse(BaseModel):
    assignment_id: int
    plagiarism_score: float
    confidence_score: float
    research_suggestions: Optional[str] = None
    citation_recommendations: Optional[str] = None
    suggested_sources: Optional[List[Dict[str, Any]]] = None
    flagged_sections: Optional[List[Dict[str, Any]]] = None
    analyzed_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # This is important for ORM compatibility

class SourceSearchRequest(BaseModel):
    query: str
    limit: int = 5

class AcademicSourceResponse(BaseModel):
    id: int
    title: str
    authors: Optional[str]
    publication_year: Optional[int]
    abstract: Optional[str]
    source_type: str
    similarity_score: Optional[float] = None

    class Config:
        from_attributes = True
