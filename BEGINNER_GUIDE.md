# Beginner's Guide - Getting Started

This guide assumes you're new to Docker and APIs. Follow these steps exactly!

---

## ✅ What You Need First

1. **Docker Desktop** - Download and install from:
   - Windows: https://www.docker.com/products/docker-desktop/
   - Mac: https://www.docker.com/products/docker-desktop/
   - Linux: Already have it!

2. **A text editor** - Any will work:
   - VS Code (recommended): https://code.visualstudio.com/
   - Notepad++ (Windows)
   - TextEdit (Mac)

3. **A terminal/command prompt**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Mac: Press `Cmd + Space`, type `terminal`, press Enter
   - Linux: You know this already!

4. **Google Gemini API Key** (FREE):
   - Go to: https://makersuite.google.com/app/apikey
   - Sign in with Google account
   - Click "Create API Key"
   - Copy it somewhere safe

---

## 🚀 Step-by-Step Setup (15 minutes)

### Step 1: Open Terminal and Navigate to Project

```bash
# Go to the project folder
cd /tmp/cc-agent/58088597/project

# Check you're in the right place (should show files)
ls
```

You should see: `README.md`, `docker-compose.yml`, etc.

---

### Step 2: Add Your Gemini API Key

Open the `.env` file in your text editor:

```bash
# If you have VS Code
code .env

# Or use nano (Linux/Mac)
nano .env

# Or use notepad (Windows)
notepad .env
```

**Find this line:**
```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Replace it with your actual key:**
```
GEMINI_API_KEY=AIzaSyABC123...your-key-here
```

**Save and close the file.**

---

### Step 3: Start Docker Desktop

1. Open Docker Desktop application
2. Wait until it says "Docker Desktop is running"
3. Leave it open in the background

---

### Step 4: Start All Services

In your terminal, run:

```bash
docker-compose up -d
```

This will:
- Download necessary software (first time only, takes 5-10 minutes)
- Start 5 services
- Set up the database

**What you'll see:**
```
[+] Running 5/5
✔ Container academic_postgres  Started
✔ Container academic_redis     Started
✔ Container academic_n8n       Started
✔ Container academic_backend   Started
✔ Container academic_pgadmin   Started
```

---

### Step 5: Wait for Services to Start (IMPORTANT!)

Wait **30 seconds** for everything to initialize, then check:

```bash
docker-compose ps
```

**All services should show "Up":**
```
NAME                  STATUS
academic_backend      Up
academic_postgres     Up
academic_redis        Up
academic_n8n          Up
academic_pgadmin      Up
```

If any show "starting" or "unhealthy", wait another 30 seconds.

---

### Step 6: Seed the Database

This adds sample academic papers for testing:

```bash
docker-compose exec backend python /data/seed_sources.py
```

**What you'll see:**
```
Loading sample academic sources...
Connecting to database...
Processing 1/10: Deep Learning: Methods and Applications
Processing 2/10: Climate Change and Global Warming
...
Successfully inserted 10 academic sources!
```

**If you get an error**, wait 30 more seconds and try again.

---

### Step 7: Test if Backend is Working

Open your web browser and go to:

```
http://localhost:8000/health
```

**You should see:**
```json
{
  "status": "healthy",
  "service": "academic-assignment-helper"
}
```

✅ **If you see this, your backend is working!**

---

### Step 8: See the API Documentation

Open your browser to:

```
http://localhost:8000/docs
```

You'll see a nice interface showing all available endpoints:
- `/auth/register` - Create account
- `/auth/login` - Login
- `/upload` - Upload assignment
- `/analysis/{id}` - Get results
- `/sources` - Search papers

**This is your API!** You can click on any endpoint to test it.

---

## 🧪 Testing Your Backend (The Easy Way)

I've created a test script that does everything automatically!

### Run the Test Script

```bash
python test_api.py
```

**What it does:**
1. ✅ Checks if backend is healthy
2. ✅ Creates a test student account
3. ✅ Logs in and gets authentication token
4. ✅ Creates a sample assignment file
5. ✅ Uploads the assignment
6. ✅ Waits for analysis
7. ✅ Retrieves and displays results
8. ✅ Searches for relevant academic sources

**What you'll see:**
```
============================================================
Academic Assignment Helper - API Test Suite
============================================================

=== Testing Health Endpoint ===
Status: 200
Response: {'status': 'healthy', 'service': 'academic-assignment-helper'}

=== Testing Student Registration ===
Status: 200
Response: {
  "id": 1,
  "email": "testuser@university.edu",
  "full_name": "Test User",
  "student_id": "TEST2025"
}

=== Testing Login ===
Status: 200
Access Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

✅ Authentication successful!

=== Testing Assignment Upload ===
Status: 200
Response: {
  "assignment_id": 1,
  "message": "Assignment uploaded successfully and analysis started",
  "status": "processing"
}

✅ Upload successful!
Assignment ID: 1

⏳ Waiting for n8n workflow to process...

=== Testing Get Analysis ===
Attempt 1/10...
Status: 200

✅ Analysis Complete!
{
  "id": 1,
  "assignment_id": 1,
  "suggested_sources": [...],
  "plagiarism_score": 0.15,
  "research_suggestions": "...",
  "confidence_score": 0.85
}

✅ Source search successful!

============================================================
Test Suite Complete!
============================================================
```

---

## 🌐 Manual Testing with Browser

### 1. Open the API Documentation

Go to: `http://localhost:8000/docs`

### 2. Register a Student

1. Click on `POST /auth/register`
2. Click "Try it out"
3. Edit the request body:
```json
{
  "email": "john@university.edu",
  "password": "MyPassword123",
  "full_name": "John Doe",
  "student_id": "JOHN001"
}
```
4. Click "Execute"
5. Check the response shows status 200

### 3. Login

1. Click on `POST /auth/login`
2. Click "Try it out"
3. Enter:
```json
{
  "email": "john@university.edu",
  "password": "MyPassword123"
}
```
4. Click "Execute"
5. **COPY the `access_token` from the response!**

### 4. Authorize

1. Scroll to top of page
2. Click the green "Authorize" button
3. Paste your token
4. Click "Authorize"
5. Click "Close"

Now you can test protected endpoints!

### 5. Upload Assignment

First, create a text file on your computer with some content:

**Create file: `my_assignment.txt`**
```
Machine Learning Essay

Introduction:
Machine learning is a subset of artificial intelligence that enables
computers to learn from data without being explicitly programmed.
This essay explores the fundamental concepts.

Deep Learning:
Deep learning uses neural networks with multiple layers to process
complex patterns in data. Applications include image recognition
and natural language processing.

Conclusion:
Machine learning continues to advance rapidly with new applications
emerging across all industries.
```

Then in the API docs:
1. Click on `POST /upload`
2. Click "Try it out"
3. Click "Choose File" and select your `my_assignment.txt`
4. Click "Execute"
5. **Save the `assignment_id` from the response!**

### 6. Get Analysis

1. Click on `GET /analysis/{assignment_id}`
2. Click "Try it out"
3. Enter your assignment_id (probably `1` or `2`)
4. Click "Execute"
5. See your results!

---

## 📊 View Your Data in Database

### Open Database GUI

Go to: `http://localhost:5050`

**Login:**
- Email: `admin@admin.com`
- Password: `admin123`

### Connect to Database

1. Right-click "Servers" in left panel
2. Click "Register" → "Server"
3. **General tab:**
   - Name: `Academic DB`
4. **Connection tab:**
   - Host: `postgres`
   - Port: `5432`
   - Database: `academic_helper`
   - Username: `student`
   - Password: `secure_password`
5. Click "Save"

### View Your Data

1. Expand: Servers → Academic DB → Databases → academic_helper → Schemas → public → Tables
2. Right-click `students` → View/Edit Data → All Rows
3. You'll see your test student!
4. Check other tables: `assignments`, `analysis_results`, `academic_sources`

---

## 🔄 View the n8n Workflow

### Open n8n

Go to: `http://localhost:5678`

**Login:**
- Username: `admin`
- Password: `admin123`

### Import Workflow

1. Click "Import from File"
2. Click "Select a file to import"
3. Navigate to project folder → `workflows` → `assignment_analysis_workflow.json`
4. Click "Open"
5. You'll see the workflow diagram!

### Configure Credentials (IMPORTANT!)

**PostgreSQL:**
1. Click any PostgreSQL node (purple boxes)
2. In right panel, find "Credentials"
3. Click dropdown → "Create New"
4. Enter:
   - Name: `PostgreSQL Academic DB`
   - Host: `postgres`
   - Database: `academic_helper`
   - User: `student`
   - Password: `secure_password`
   - Port: `5432`
5. Click "Save"

**Gemini AI:**
1. Click the "AI Analysis (Gemini)" node (green box)
2. In right panel, find "Credentials"
3. Click dropdown → "Create New"
4. Enter:
   - Name: `Gemini API`
   - API Key: (paste your Gemini key)
5. Click "Save"

### Activate Workflow

1. Toggle switch in top-right corner (should turn green)
2. Now your workflow is active!

---

## ❓ Common Problems & Solutions

### Problem: "Cannot connect" error

**Solution:**
```bash
# Check if Docker is running
docker ps

# If not, open Docker Desktop and wait for it to start
```

### Problem: "Port already in use"

**Solution:**
```bash
# Stop all services
docker-compose down

# Start again
docker-compose up -d
```

### Problem: Backend shows "unhealthy"

**Solution:**
```bash
# Check what's wrong
docker-compose logs backend

# Usually just need to wait longer or restart
docker-compose restart backend
```

### Problem: "seed_sources.py" fails

**Causes:**
1. Database not ready yet
2. Wrong Gemini API key

**Solution:**
```bash
# Wait 30 seconds, then try again
sleep 30
docker-compose exec backend python /data/seed_sources.py

# Check your .env file has correct API key
cat .env | grep GEMINI_API_KEY
```

### Problem: Analysis never completes

**Solution:**
1. Check n8n is running: `http://localhost:5678`
2. Make sure workflow is ACTIVATED (green toggle)
3. Check credentials are configured correctly

### Problem: "command not found: docker-compose"

**Solution:**
```bash
# Try with dash instead
docker compose up -d

# Or install docker-compose
pip install docker-compose
```

---

## 🎉 Success Checklist

You know it's working when:

- [ ] `http://localhost:8000/health` shows "healthy"
- [ ] `http://localhost:8000/docs` shows API documentation
- [ ] `python test_api.py` completes successfully
- [ ] You can register and login via browser
- [ ] You can upload an assignment
- [ ] You receive analysis results
- [ ] n8n workflow is activated
- [ ] Database shows your data in PgAdmin

---

## 🛑 Stopping Everything

When you're done testing:

```bash
# Stop all services (data is kept)
docker-compose down

# Stop and DELETE all data (fresh start)
docker-compose down -v
```

---

## 📝 Quick Reference Commands

```bash
# Start everything
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs backend

# Restart a service
docker-compose restart backend

# Stop everything
docker-compose down

# Run test
python test_api.py
```

---

## 🆘 Still Need Help?

1. **Check logs:**
   ```bash
   docker-compose logs backend
   ```

2. **Restart everything:**
   ```bash
   docker-compose down
   docker-compose up -d
   ```

3. **Check if ports are free:**
   - Backend: http://localhost:8000
   - n8n: http://localhost:5678
   - PgAdmin: http://localhost:5050

4. **Verify .env file:**
   ```bash
   cat .env
   ```
   Make sure GEMINI_API_KEY is set!

---

## 🎓 What Each Service Does

- **Backend (port 8000)**: Your API - handles registration, login, uploads
- **PostgreSQL (port 5432)**: Database - stores students, assignments, analysis
- **Redis (port 6379)**: Cache - makes embeddings faster
- **n8n (port 5678)**: Automation - processes assignments automatically
- **PgAdmin (port 5050)**: Database GUI - view your data visually

---

## 🚀 Next Steps

Once everything works:

1. ✅ Read `README.md` for API details
2. ✅ Review `TECHNICAL_DOCUMENTATION.md` to understand architecture
3. ✅ Check `DEMO_GUIDE.md` for creating your demo video
4. ✅ Experiment with different assignments
5. ✅ Try the RAG source search feature
6. ✅ Explore the n8n workflow

---

**You're ready to go! 🎉**

If `python test_api.py` runs successfully, your system is working perfectly!
