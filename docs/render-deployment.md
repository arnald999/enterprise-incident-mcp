# Enterprise Incident MCP - Render Deployment Guide

## Goal

Deploy:

* Enterprise Incident MCP Server
* PostgreSQL Database
* pgvector Support
* Streamable HTTP MCP Endpoint

onto Render.

---

# Prerequisites

Before deployment:

```text
✓ GitHub repository pushed
✓ Dockerfile committed
✓ web_server.py implemented
✓ /health endpoint working locally
✓ MCP endpoint working locally
✓ Alembic migrations created
```

Verify locally:

```powershell
$env:PYTHONPATH="src"
python -m enterprise_incident_mcp.web_server
```

Health check:

```text
http://localhost:8000/health
```

Expected:

```json
{
  "status": "healthy"
}
```

---

# Architecture

```text
Internet
     │
     ▼
Render Web Service
     │
     ▼
Enterprise Incident MCP
     │
     ▼
Render PostgreSQL
```

---

# Step 1 - Create PostgreSQL Database

Render Dashboard:

```text
New
 ↓
PostgreSQL
```

Configuration:

```text
Name: enterprise-incident-db
Database: incident_db
User: incident_user
Region: nearest region
```

Click:

```text
Create Database
```

Wait until provisioning completes.

---

# Step 2 - Collect Database URLs

Render generates:

## External Database URL

Used from local machine.

Example:

```text
postgresql://user:password@host.render.com:5432/incident_db
```

Used for:

* Alembic
* psql
* DBeaver
* Local scripts

---

## Internal Database URL

Used by Render services.

Example:

```text
postgresql://user:password@internal-host:5432/incident_db
```

Used for:

* Render Web Service
* Internal Render networking

---

# Step 3 - Run Migrations

Use the External URL.

Convert:

```text
postgresql://
```

to:

```text
postgresql+asyncpg://
```

PowerShell:

```powershell
$env:DATABASE_URL="postgresql+asyncpg://..."
$env:PYTHONPATH="src"

alembic upgrade head
```

Verify:

```powershell
alembic current
```

Expected:

```text
(head)
```

---

# Step 4 - Verify Database Tables

Connect using DBeaver or psql.

Run:

```sql
SELECT tablename
FROM pg_tables
WHERE schemaname = 'public';
```

Expected:

```text
alembic_version
incidents
incident_events
incident_embeddings
```

---

# Step 5 - Create Render Web Service

Render Dashboard:

```text
New
 ↓
Web Service
```

Connect:

```text
GitHub Repository
```

Configuration:

```text
Name:
enterprise-incident-mcp

Runtime:
Docker

Branch:
main

Health Check Path:
/health
```

---

# Step 6 - Configure Environment Variables

Add:

```text
DATABASE_URL
```

Value:

```text
postgresql+asyncpg://...
```

using the Internal Database URL.

Add:

```text
PYTHONPATH
```

Value:

```text
/app/src
```

Do NOT configure:

```text
PORT
```

Render automatically injects PORT.

---

# Step 7 - Verify Dockerfile

CMD must launch:

```dockerfile
CMD ["uv", "run", "python", "-m", "enterprise_incident_mcp.web_server"]
```

NOT:

```dockerfile
server.py
```

because STDIO transport cannot be publicly exposed.

---

# Step 8 - Deploy

Click:

```text
Create Web Service
```

Render will:

```text
Build Docker Image
 ↓
Start Container
 ↓
Run Health Check
```

Wait until deployment completes.

---

# Step 9 - Verify Health Endpoint

Open:

```text
https://YOUR_APP.onrender.com/health
```

Expected:

```json
{
  "status": "healthy",
  "transport": "streamable-http"
}
```

---

# Step 10 - Verify MCP Endpoint

Do NOT use a browser.

Browser requests:

```text
Accept: text/html
```

MCP expects:

```text
Accept: text/event-stream
```

Therefore browser testing is invalid.

---

# Step 11 - Test with MCP Inspector

Start:

```powershell
npx @modelcontextprotocol/inspector
```

Configuration:

```text
Transport:
Streamable HTTP

URL:
https://YOUR_APP.onrender.com/mcp
```

Connect.

Expected:

```text
Resources discovered
Tools discovered
Prompts discovered
```

---

# Step 12 - Functional Validation

Run:

## Create Incident

```text
create_incident
```

---

## Semantic Search

```text
semantic_search
```

Query:

```text
checkout slowdown
```

---

## Investigator

```text
investigate_incident
```

Query:

```text
checkout slowdown
```

Expected:

```text
Similarity scores
Pattern extraction
Investigation report
```

---

# Common Problems

## Problem

```text
404 Not Found
```

Cause:

Wrong MCP route.

Check:

```text
/mcp
```

vs

```text
/mcp/
```

and FastAPI mount configuration.

---

## Problem

```text
Client must accept text/event-stream
```

Cause:

Testing with browser.

Resolution:

Use MCP Inspector.

This is actually a sign that MCP is working.

---

## Problem

```text
Database connection refused
```

Cause:

Using External URL inside Render.

Resolution:

Use Internal Database URL for Render service.

---

## Problem

```text
Alembic hangs
```

Check:

```powershell
alembic current
```

and verify DATABASE_URL points to the correct Render database.

---

# Deployment Checklist

```text
✓ PostgreSQL created
✓ External URL copied
✓ Internal URL copied
✓ Migrations executed
✓ Tables verified
✓ Web Service created
✓ Environment variables configured
✓ Docker image built
✓ Health endpoint verified
✓ Inspector connected
✓ Investigator tested
```
