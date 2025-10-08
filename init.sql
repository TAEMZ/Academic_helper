-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    student_id TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assignments table
CREATE TABLE IF NOT EXISTS assignments (
    id SERIAL PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    filename TEXT NOT NULL,
    original_text TEXT,
    topic TEXT,
    academic_level TEXT,
    word_count INTEGER DEFAULT 0,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Analysis results table
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    suggested_sources JSONB,
    plagiarism_score FLOAT DEFAULT 0.0,
    flagged_sections JSONB,
    research_suggestions TEXT,
    citation_recommendations TEXT,
    confidence_score FLOAT DEFAULT 0.0,
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Academic sources table (for RAG)
CREATE TABLE IF NOT EXISTS academic_sources (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    authors TEXT,
    publication_year INTEGER,
    abstract TEXT,
    full_text TEXT,
    source_type TEXT DEFAULT 'paper',
    embedding vector(768),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_students_student_id ON students(student_id);
CREATE INDEX IF NOT EXISTS idx_assignments_student_id ON assignments(student_id);
CREATE INDEX IF NOT EXISTS idx_analysis_assignment_id ON analysis_results(assignment_id);
CREATE INDEX IF NOT EXISTS idx_academic_sources_type ON academic_sources(source_type);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_academic_sources_embedding ON academic_sources
USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Insert sample student for testing
INSERT INTO students (email, password_hash, full_name, student_id)
VALUES ('test@student.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYqJxrzZW6K', 'Test Student', 'STU001')
ON CONFLICT (email) DO NOTHING;
