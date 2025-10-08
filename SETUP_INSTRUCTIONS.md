# Setup Instructions - Academic Assignment Helper

## Prerequisites

Before you begin, ensure you have:
- **Docker** installed (version 20.10+)
- **Docker Compose** installed (version 2.0+)
- **Gemini API Key** from Google AI Studio
- At least **4GB of RAM** available
- Ports **5432, 5678, 6379, 8000, 5050** available

---

## Step 1: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the API key

---

## Step 2: Clone and Configure

```bash
# Clone the repository
git clone <your-repo-url>
cd academic-assignment-helper

# Copy the environment template
cp .env.example .env

# Edit .env and add your Gemini API key
nano .env  # or use your preferred editor
```

**In the `.env` file, replace:**
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**With your actual key:**
```env
GEMINI_API_KEY=AIzaSyABC123...your-actual-key
```

You can also generate a secure JWT secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Replace `JWT_SECRET_KEY` in `.env` with this generated value.

---

## Step 3: Start All Services

```bash
# Build and start all containers
docker-compose up -d

# Check that all services are running
docker-compose ps
```

You should see:
```
NAME                    STATUS    PORTS
academic_backend        Up        0.0.0.0:8000->8000/tcp
academic_postgres       Up        0.0.0.0:5432->5432/tcp
academic_redis          Up        0.0.0.0:6379->6379/tcp
academic_n8n            Up        0.0.0.0:5678->5678/tcp
academic_pgadmin        Up        0.0.0.0:5050->80/tcp
```

---

## Step 4: Wait for Services to Initialize

The PostgreSQL database needs a moment to initialize:

```bash
# Watch the logs until you see "database system is ready"
docker-compose logs -f postgres
```

Press `Ctrl+C` when you see:
```
database system is ready to accept connections
```

Then check the backend:
```bash
# Watch backend logs
docker-compose logs -f backend
```

Wait for:
```
Application startup complete.
Uvicorn running on http://0.0.0.0:8000
```

---

## Step 5: Seed Academic Sources

```bash
# Populate the database with sample academic papers
docker-compose exec backend python /data/seed_sources.py
```

You should see:
```
Loading sample academic sources...
Connecting to database...
Processing 1/10: Deep Learning: Methods and Applications
Processing 2/10: Climate Change and Global Warming
...
Successfully inserted 10 academic sources!
```

**Note:** This step requires your Gemini API key to generate embeddings.

---

## Step 6: Configure n8n Workflow

1. Open n8n in your browser:
   ```
   http://localhost:5678
   ```

2. Login with credentials:
   - Username: `admin`
   - Password: `admin123`

3. Import the workflow:
   - Click "Import from File"
   - Navigate to `workflows/assignment_analysis_workflow.json`
   - Click "Open"

4. Configure PostgreSQL credentials:
   - Click on any PostgreSQL node
   - Click "Credentials" dropdown
   - Click "Create New"
   - Enter:
     - Name: `PostgreSQL Academic DB`
     - Host: `postgres`
     - Database: `academic_helper`
     - User: `student`
     - Password: `secure_password`
     - Port: `5432`
   - Click "Save"

5. Configure Gemini credentials:
   - Click on the "AI Analysis (Gemini)" node
   - Click "Credentials" dropdown
   - Click "Create New"
   - Enter:
     - Name: `Google Gemini API`
     - API Key: `<your-gemini-api-key>`
   - Click "Save"

6. Activate the workflow:
   - Click the toggle switch in the top-right corner
   - It should turn green

---

## Step 7: Test the System

### Option A: Automated Test Script

```bash
python test_api.py
```

This will run through the entire workflow automatically.

### Option B: Manual Testing

#### 1. Check API Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "service": "academic-assignment-helper"}
```

#### 2. Register a Student
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@university.edu",
    "password": "Test123!",
    "full_name": "Test Student",
    "student_id": "TEST001"
  }'
```

#### 3. Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@university.edu",
    "password": "Test123!"
  }'
```

**Save the `access_token` from the response!**

#### 4. Create Test Assignment
```bash
echo "Machine Learning Applications

This paper explores machine learning algorithms and their applications in computer vision and natural language processing. Deep learning techniques have revolutionized the field." > /tmp/test_assignment.txt
```

#### 5. Upload Assignment
```bash
curl -X POST http://localhost:8000/upload \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -F "file=@/tmp/test_assignment.txt"
```

**Save the `assignment_id` from the response!**

#### 6. Wait for Processing
```bash
# Wait 10-15 seconds for the n8n workflow to complete
sleep 15
```

#### 7. Get Analysis
```bash
curl -X GET http://localhost:8000/analysis/<ASSIGNMENT_ID> \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## Step 8: Explore the System

### API Documentation (Swagger UI)
```
http://localhost:8000/docs
```

### n8n Workflow Dashboard
```
http://localhost:5678
```
Credentials: `admin` / `admin123`

### Database GUI (PgAdmin)
```
http://localhost:5050
```
Credentials: `admin@admin.com` / `admin123`

To connect to the database in PgAdmin:
- Right-click "Servers" → "Register" → "Server"
- General Tab: Name: `Academic DB`
- Connection Tab:
  - Host: `postgres`
  - Port: `5432`
  - Database: `academic_helper`
  - Username: `student`
  - Password: `secure_password`

---

## Common Issues and Solutions

### Issue: Services won't start

**Solution:**
```bash
# Stop and remove all containers
docker-compose down -v

# Rebuild and start fresh
docker-compose up -d --build
```

### Issue: Backend can't connect to database

**Solution:**
```bash
# Wait for PostgreSQL to fully initialize
sleep 30

# Restart backend
docker-compose restart backend
```

### Issue: n8n webhook returns error

**Causes:**
1. Workflow not activated
2. Wrong PostgreSQL credentials
3. Missing Gemini API key

**Solution:**
- Check workflow is active (green toggle in n8n)
- Verify credentials match `.env` file
- Ensure Gemini API key is valid

### Issue: Seed script fails

**Causes:**
1. Invalid Gemini API key
2. Database not ready
3. Network issues

**Solution:**
```bash
# Check if postgres is ready
docker-compose logs postgres | grep "ready to accept connections"

# Verify API key in .env
cat .env | grep GEMINI_API_KEY

# Try seeding again
docker-compose exec backend python /data/seed_sources.py
```

### Issue: Port already in use

**Solution:**
```bash
# Find what's using the port (example for 8000)
lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Issue: Analysis never completes

**Causes:**
1. n8n workflow not activated
2. Webhook URL incorrect
3. Gemini API rate limit

**Solution:**
```bash
# Check n8n logs
docker-compose logs n8n

# Verify webhook was called
docker-compose logs n8n | grep "Webhook received"

# Check backend logs for errors
docker-compose logs backend
```

---

## Verification Checklist

Before considering your setup complete:

- [ ] All 5 services show "Up" in `docker-compose ps`
- [ ] Backend responds at `http://localhost:8000/health`
- [ ] n8n accessible at `http://localhost:5678`
- [ ] Database seeded with 10 academic sources
- [ ] Can register and login successfully
- [ ] Can upload an assignment
- [ ] n8n workflow is activated
- [ ] Analysis results appear within 30 seconds
- [ ] RAG source search returns relevant papers

---

## Stopping the System

```bash
# Stop all services
docker-compose down

# Stop and remove all data (WARNING: Deletes database)
docker-compose down -v
```

---

## Updating the System

```bash
# Pull latest changes
git pull

# Rebuild containers
docker-compose up -d --build

# Reseed database if schema changed
docker-compose exec backend python /data/seed_sources.py
```

---

## Development Mode

For active development with hot-reloading:

```bash
# Backend changes auto-reload (already configured)
docker-compose logs -f backend

# To modify n8n workflow:
# 1. Make changes in n8n UI
# 2. Export workflow: Settings → Download
# 3. Replace workflows/assignment_analysis_workflow.json
```

---

## Production Deployment

**Important:** This setup is for development. For production:

1. Change all default passwords in `.env`
2. Use strong JWT secret (32+ random characters)
3. Set `allow_origins` in CORS to specific domains
4. Use managed PostgreSQL (AWS RDS, Google Cloud SQL)
5. Enable HTTPS with SSL certificates
6. Set up database backups
7. Implement rate limiting
8. Use environment-specific `.env` files
9. Monitor with Prometheus/Grafana
10. Set up log aggregation (ELK, Loki)

---

## Getting Help

If you encounter issues:

1. **Check logs:**
   ```bash
   docker-compose logs <service-name>
   ```

2. **Restart services:**
   ```bash
   docker-compose restart <service-name>
   ```

3. **Clean slate:**
   ```bash
   docker-compose down -v
   docker-compose up -d --build
   ```

4. **Verify configuration:**
   ```bash
   cat .env
   docker-compose config
   ```

---

## Next Steps

- Read `TECHNICAL_DOCUMENTATION.md` for architecture details
- Review `DEMO_GUIDE.md` for creating your demo video
- Explore the Swagger API docs at `http://localhost:8000/docs`
- Check out the n8n workflow in detail
- Query the database in PgAdmin

---

**You're all set! 🎉**

The Academic Assignment Helper is now ready to analyze assignments with RAG-powered suggestions and plagiarism detection.
