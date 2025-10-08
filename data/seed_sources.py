import json
import psycopg2
import google.generativeai as genai
import os
import sys

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY environment variable not set")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

DB_CONFIG = {
    'host': os.getenv('POSTGRES_HOST', 'localhost'),
    'database': os.getenv('POSTGRES_DB', 'academic_helper'),
    'user': os.getenv('POSTGRES_USER', 'student'),
    'password': os.getenv('POSTGRES_PASSWORD', 'secure_password'),
    'port': 5432
}

def generate_embedding(text):
    try:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="retrieval_document"
        )
        return result['embedding']
    except Exception as e:
        print(f"⚠️ Warning: Could not generate embedding via Gemini API: {e}")
        # Return a dummy 768-dim vector for testing
        return [0.0] * 768


def seed_academic_sources():
    print("Loading sample academic sources...")
    with open('/data/sample_academic_sources.json', 'r') as f:
        sources = json.load(f)

    print(f"Connecting to database at {DB_CONFIG['host']}...")
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    print("Checking if sources already exist...")
    cursor.execute("SELECT COUNT(*) FROM academic_sources")
    count = cursor.fetchone()[0]

    if count > 0:
        print(f"Found {count} existing sources. Skipping seed.")
        cursor.close()
        conn.close()
        return

    print("Inserting academic sources with embeddings...")
    for idx, source in enumerate(sources, 1):
        print(f"Processing {idx}/{len(sources)}: {source['title']}")

        text_for_embedding = f"{source['title']}. {source['abstract']}. {source['full_text'][:1000]}"
        embedding = generate_embedding(text_for_embedding)

        cursor.execute("""
            INSERT INTO academic_sources
            (title, authors, publication_year, abstract, full_text, source_type, embedding)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            source['title'],
            source['authors'],
            source['publication_year'],
            source['abstract'],
            source['full_text'],
            source['source_type'],
            embedding
        ))

    conn.commit()
    print(f"Successfully inserted {len(sources)} academic sources!")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    seed_academic_sources()
