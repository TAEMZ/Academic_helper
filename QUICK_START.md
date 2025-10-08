# Quick Start - 5 Minutes to Running System

Follow these exact steps. No experience needed!

---

## 📋 Before You Start

1. **Install Docker Desktop**: https://www.docker.com/products/docker-desktop/
2. **Get Gemini API Key** (FREE): https://makersuite.google.com/app/apikey

---

## 🚀 Setup (Copy & Paste These Commands)

### 1. Navigate to Project

```bash
cd /tmp/cc-agent/58088597/project
```

### 2. Add Your API Key

Open `.env` file and replace this line:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

With your actual key:
```
GEMINI_API_KEY=AIzaSy...your-key-here
```

### 3. Start Everything

```bash
docker-compose up -d
```

Wait 30 seconds ⏳

### 4. Check Setup

```bash
python check_setup.py
```

If everything shows ✅, continue!

### 5. Add Sample Data

```bash
docker-compose exec backend python /data/seed_sources.py
```

### 6. Test It Works

```bash
python test_api.py
```

---

## ✅ Is It Working?

### Check 1: Open in Browser
```
http://localhost:8000/health
```

Should show:
```json
{"status": "healthy", "service": "academic-assignment-helper"}
```

### Check 2: See API Docs
```
http://localhost:8000/docs
```

You'll see all the API endpoints!

### Check 3: Run Test Script
```bash
python test_api.py
```

Should show lots of ✅ checkmarks!

---

## 🎮 Try It Yourself

### Using the Browser (Easiest Way)

1. **Go to API docs**: http://localhost:8000/docs

2. **Register a student**:
   - Click `POST /auth/register`
   - Click "Try it out"
   - Edit the example data
   - Click "Execute"

3. **Login**:
   - Click `POST /auth/login`
   - Click "Try it out"
   - Enter your email/password
   - Click "Execute"
   - **COPY the access_token**

4. **Authorize**:
   - Click green "Authorize" button at top
   - Paste your token
   - Click "Authorize"

5. **Upload assignment**:
   - Click `POST /upload`
   - Click "Try it out"
   - Choose a .txt or .pdf file
   - Click "Execute"
   - **Note the assignment_id**

6. **Get results**:
   - Click `GET /analysis/{assignment_id}`
   - Click "Try it out"
   - Enter your assignment_id
   - Click "Execute"
   - See your analysis!

---

## 🔧 Configure n8n (Required for Full Functionality)

1. **Open n8n**: http://localhost:5678
2. **Login**: admin / admin123
3. **Import workflow**:
   - Click "Import from File"
   - Select: `workflows/assignment_analysis_workflow.json`
4. **Add PostgreSQL credentials**:
   - Click any PostgreSQL node
   - Credentials → Create New
   - Host: `postgres`, Database: `academic_helper`
   - User: `student`, Password: `secure_password`
5. **Add Gemini credentials**:
   - Click "AI Analysis" node
   - Credentials → Create New
   - Add your Gemini API key
6. **Activate workflow**: Toggle switch in top-right

---

## 🎯 What Can You Do Now?

### 1. Upload Assignments
- PDF, DOCX, or TXT files
- Get AI-powered analysis

### 2. Search Academic Sources
- RAG-powered similarity search
- Find relevant research papers

### 3. Plagiarism Detection
- Automatic similarity checking
- Identifies potential matches

### 4. Research Suggestions
- AI-generated improvement ideas
- Citation recommendations

---

## 📊 View Your Data

### Database GUI
```
http://localhost:5050
```
Login: admin@admin.com / admin123

Connect to database:
- Host: `postgres`
- Database: `academic_helper`
- User: `student`
- Password: `secure_password`

---

## 🛑 Stop Everything

```bash
docker-compose down
```

Restart later:
```bash
docker-compose up -d
```

---

## ❓ Something Wrong?

### Run the checker:
```bash
python check_setup.py
```

### Check logs:
```bash
docker-compose logs backend
```

### Restart everything:
```bash
docker-compose down
docker-compose up -d
```

Wait 30 seconds and try again!

---

## 📖 Need More Help?

- **Beginner?** Read `BEGINNER_GUIDE.md`
- **Details?** Read `SETUP_INSTRUCTIONS.md`
- **Technical?** Read `TECHNICAL_DOCUMENTATION.md`

---

## ✨ You're Done!

Your backend is running at: **http://localhost:8000**

Try the API at: **http://localhost:8000/docs**

---

**Total setup time: ~5 minutes** ⚡
