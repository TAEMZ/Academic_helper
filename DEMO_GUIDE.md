# Demo Guide - Academic Assignment Helper

This guide will help you create a comprehensive 5-minute demo video showcasing all features of the Academic Assignment Helper system.

## 📹 Demo Structure (5 minutes)

### Introduction (30 seconds)
- Show the project overview
- Mention key technologies: Docker, FastAPI, PostgreSQL with pgvector, n8n, Gemini AI
- State the purpose: RAG-powered assignment analysis with plagiarism detection

---

## 🎬 Demo Script

### Section 1: Architecture Overview (45 seconds)

**Show:**
1. Open `README.md` and scroll through the architecture diagram
2. Show `docker-compose.yml` briefly
3. Run: `docker-compose ps` to show all services running

**Script:**
> "This system uses a microservices architecture with Docker. We have FastAPI for the backend, PostgreSQL with pgvector for vector similarity search, Redis for caching, and n8n for workflow automation. All services communicate seamlessly."

---

### Section 2: Service Status (30 seconds)

**Show:**
```bash
docker-compose ps
```

**Terminal Commands:**
```bash
# Show healthy services
docker-compose ps

# Quick health check
curl http://localhost:8000/health
```

**Script:**
> "All services are up and running. The backend is on port 8000, n8n on 5678, and PostgreSQL on 5432. Let's test the API."

---

### Section 3: Authentication Flow (60 seconds)

**Show API Documentation:**
1. Open browser to `http://localhost:8000/docs`
2. Show the Swagger UI with all endpoints

**Demo Registration:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@university.edu",
    "password": "DemoPass123",
    "full_name": "Demo Student",
    "student_id": "DEMO2025"
  }'
```

**Demo Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "demo@university.edu",
    "password": "DemoPass123"
  }'
```

**Script:**
> "First, we register a new student account. The system uses bcrypt for password hashing. After registration, we log in and receive a JWT token. This token is required for all protected endpoints."

**Copy the access_token from the response!**

---

### Section 4: Assignment Upload (45 seconds)

**Create a sample file:**
```bash
cat > /tmp/ml_assignment.txt << 'EOF'
Machine Learning Applications

Introduction:
Machine learning has revolutionized artificial intelligence. This paper explores
supervised and unsupervised learning techniques, including neural networks and
deep learning architectures.

Deep Learning:
Convolutional Neural Networks (CNNs) excel at image recognition tasks. They use
multiple layers to extract hierarchical features from visual data. Training
requires large datasets and significant computational resources.

Applications:
Machine learning is used in computer vision, natural language processing,
recommendation systems, and autonomous vehicles. These technologies continue
to advance rapidly.

References:
- Deep Learning by Goodfellow et al.
- Pattern Recognition by Bishop
EOF
```

**Upload the file:**
```bash
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "file=@/tmp/ml_assignment.txt"
```

**Script:**
> "Now I'll upload an assignment about machine learning. The system extracts the text, stores it in PostgreSQL, and triggers the n8n workflow for analysis. Notice we get an assignment ID back immediately."

**Save the assignment_id from the response!**

---

### Section 5: n8n Workflow (60 seconds)

**Show n8n Dashboard:**
1. Open browser to `http://localhost:5678`
2. Login with credentials (admin/admin123)
3. Show the workflow visualization
4. Click through the nodes to explain:
   - Webhook Trigger
   - Text Extraction
   - Database Update
   - RAG Source Search
   - AI Analysis with Gemini
   - Plagiarism Detection
   - Result Storage

**Script:**
> "The n8n workflow orchestrates the entire analysis pipeline. It receives the webhook from FastAPI, preprocesses the text, searches for relevant academic sources using vector similarity, sends the data to Gemini AI for analysis, detects plagiarism by comparing against our academic database, and stores the results. This all happens asynchronously."

---

### Section 6: RAG in Action (45 seconds)

**Show the Database:**
1. Open PgAdmin at `http://localhost:5050`
2. Login (admin@admin.com / admin123)
3. Connect to PostgreSQL server
4. Show the `academic_sources` table
5. Run query:
```sql
SELECT title, authors, source_type
FROM academic_sources
LIMIT 5;
```

**Demo Source Search:**
```bash
curl -X POST http://localhost:8000/sources \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "machine learning and neural networks",
    "limit": 3
  }'
```

**Script:**
> "The RAG system stores academic sources with vector embeddings. When we search for 'machine learning and neural networks', it uses cosine similarity to find the most relevant papers. Notice the similarity scores showing how closely each source matches our query."

---

### Section 7: Analysis Results (45 seconds)

**Wait a moment for processing, then retrieve results:**
```bash
curl -X GET http://localhost:8000/analysis/1 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Script:**
> "After the workflow completes, we can retrieve the analysis results. We get suggested academic sources, a plagiarism score, flagged sections if any similarities are detected, research suggestions, and citation recommendations. The system also provides a confidence score for the analysis."

**Show the JSON response and highlight:**
- `suggested_sources`: Relevant papers from RAG
- `plagiarism_score`: Similarity percentage
- `research_suggestions`: AI-generated improvements
- `citation_recommendations`: Format guidance

---

### Section 8: Security Features (30 seconds)

**Demonstrate Authorization:**
```bash
# Try without token (should fail)
curl -X GET http://localhost:8000/analysis/1

# Try with invalid token (should fail)
curl -X GET http://localhost:8000/analysis/1 \
  -H "Authorization: Bearer invalid_token"
```

**Script:**
> "Security is built-in. All protected endpoints require valid JWT authentication. Requests without tokens or with invalid tokens are rejected with 401 Unauthorized. Students can only access their own assignments through row-level security checks."

---

### Conclusion (15 seconds)

**Summary:**
> "This system demonstrates a complete RAG-powered academic assistant with JWT authentication, vector similarity search, AI analysis with Gemini, automated workflows with n8n, and comprehensive plagiarism detection. The entire stack runs in Docker containers for easy deployment."

---

## 🎥 Recording Tips

### Before Recording:
1. ✅ All Docker services running: `docker-compose up -d`
2. ✅ Database seeded: `docker-compose exec backend python /data/seed_sources.py`
3. ✅ Browser tabs ready:
   - `http://localhost:8000/docs` (Swagger UI)
   - `http://localhost:5678` (n8n)
   - `http://localhost:5050` (PgAdmin)
4. ✅ Terminal with clean history
5. ✅ Test script ready: `python test_api.py`

### Recording Setup:
- **Screen Resolution**: 1920x1080 (Full HD)
- **Recording Tool**: OBS Studio, QuickTime, or Loom
- **Audio**: Clear microphone, no background noise
- **Cursor**: Make it visible and easy to follow

### During Recording:
1. Speak clearly and at a moderate pace
2. Zoom in on important code sections
3. Use split-screen for terminal + browser
4. Pause briefly between sections
5. Show responses in formatted JSON (use `jq` or `python -m json.tool`)

### Formatting JSON Output:
```bash
curl ... | python -m json.tool
```

---

## 📝 Automated Demo Script

Run the automated test to demonstrate everything:

```bash
python test_api.py
```

This will:
1. Check health endpoint
2. Register a test student
3. Login and get JWT token
4. Upload a sample assignment
5. Retrieve analysis results
6. Search for relevant sources

Perfect for a quick demo or validation!

---

## 🎨 Visual Enhancements

### Terminal Styling:
```bash
# Colorize JSON output
curl ... | python -m json.tool | pygmentize -l json

# Pretty table for sources
curl ... | jq -r '.[] | "\(.title) - \(.authors)"'
```

### Screenshots to Show:
1. All services running (`docker-compose ps`)
2. Swagger UI with endpoints
3. n8n workflow diagram
4. Database with vector embeddings
5. Analysis results with plagiarism score
6. RAG source search results

---

## 🚀 Alternative: Quick Demo

If short on time, run:

```bash
# Terminal 1: Start services
docker-compose up

# Terminal 2: Run automated test
python test_api.py

# Terminal 3: Show logs
docker-compose logs -f n8n
```

Show the three terminals side-by-side while the test runs!

---

## 📤 Submission Checklist

Before submitting your demo video:

- [ ] Video is 5 minutes or less
- [ ] Audio is clear and audible
- [ ] All features demonstrated:
  - [ ] JWT authentication
  - [ ] Assignment upload
  - [ ] n8n workflow execution
  - [ ] RAG source suggestions
  - [ ] Plagiarism detection
  - [ ] Database storage
  - [ ] Docker services interaction
- [ ] Code shown is clean and readable
- [ ] Terminal output is visible
- [ ] Browser UI is responsive
- [ ] No errors during demo
- [ ] Video format: MP4, MOV, or WebM
- [ ] File size: Under 100MB (compress if needed)

---

## 🎓 Good Demo Practices

### DO:
✅ Prepare and rehearse
✅ Test everything before recording
✅ Use a clean environment
✅ Explain what you're doing
✅ Show end-to-end workflows
✅ Highlight key features
✅ Keep it concise and focused

### DON'T:
❌ Include long pauses or dead air
❌ Show debugging or troubleshooting
❌ Use cursing or inappropriate language
❌ Rush through complex parts
❌ Forget to show actual results
❌ Skip the plagiarism detection demo
❌ Neglect to show n8n workflow

---

Good luck with your demo! 🎉
