# Runbook Addendum - Embeddings, OpenRouter, and Render Deployment

## Local Embedding Mode

Use this mode for full local development.

Environment:

```env
EMBEDDING_PROVIDER=local
DISABLE_EMBEDDINGS=false
```

Run server:

```powershell
$env:PYTHONPATH="src"
python -m enterprise_incident_mcp.server
```

Run HTTP server:

```powershell
$env:PYTHONPATH="src"
python -m enterprise_incident_mcp.web_server
```

Test health:

```text
http://localhost:8000/health
```

Test MCP:

```text
http://localhost:8000/mcp
```

Use MCP Inspector with:

```text
Transport: Streamable HTTP
URL: http://localhost:8000/mcp
```

---

## Render Free-Tier Deployment Mode

Use this mode when Render memory is limited.

Environment:

```env
DISABLE_EMBEDDINGS=true
PYTHONPATH=/app/src
DATABASE_URL=postgresql+asyncpg://...
```

Expected behavior:

```text
/health works
/mcp connects
CRUD tools work
timeline tools work
Jira mock works
GitHub mock works
semantic tools return disabled message
```

This is useful to prove public deployment.

---

## Render Production Mode With OpenRouter

Use this mode when moving semantic search to API-based embeddings.

Environment:

```env
EMBEDDING_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_EMBEDDING_MODEL=openai/text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
PYTHONPATH=/app/src
DATABASE_URL=postgresql+asyncpg://...
```

Expected behavior:

```text
/health works
/mcp connects
index_incident works
semantic_search works
investigate_incident works
```

---

## Important Dimension Warning

If switching from local embeddings to OpenRouter embeddings, check vector dimension.

Current local setup:

```text
all-MiniLM-L6-v2 -> 384 dimensions
```

Current database:

```python
Vector(384)
```

If using a provider that returns 1536 dimensions, create a migration:

```powershell
alembic revision --autogenerate -m "update embedding dimension"
```

or manually alter the vector column.

Example target:

```python
Vector(1536)
```

Do not mix embeddings of different dimensions in the same column.

---

## Recommended Future EmbeddingService Design

```python
class EmbeddingService:
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def embed(self, text: str) -> list[float]:
        return self.provider.embed(text)
```

Providers:

```python
class LocalEmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        ...

class OpenRouterEmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        ...
```

Factory:

```python
def get_embedding_provider():
    provider = os.getenv("EMBEDDING_PROVIDER", "local")

    if provider == "openrouter":
        return OpenRouterEmbeddingProvider()

    if os.getenv("DISABLE_EMBEDDINGS") == "true":
        return DisabledEmbeddingProvider()

    return LocalEmbeddingProvider()
```

---

## Semantic Tool Fallback

When embeddings are disabled, semantic tools should not crash.

They should return:

```json
{
  "error": "embeddings_disabled",
  "message": "Semantic search is disabled in this deployment. Enable an embedding provider to use this tool."
}
```

Apply this to:

```text
index_incident
semantic_search
investigate_incident
generate_incident_rca
```

---

## Render Deployment Checklist

1. Create Render PostgreSQL.
2. Copy External Database URL.
3. Run migrations from local machine.
4. Copy Internal Database URL.
5. Create Render Web Service.
6. Set environment variables.
7. Deploy.
8. Test `/health`.
9. Test `/mcp` with Inspector.
10. Validate CRUD tools.
11. Validate timeline tools.
12. Validate semantic tools depending on embedding mode.

---

## Deployment Modes Summary

| Mode                | Embeddings  | Semantic Search | Cost            | Use Case                    |
| ------------------- | ----------- | --------------- | --------------- | --------------------------- |
| Local               | Local model | Enabled         | Free            | Development                 |
| Render Free         | Disabled    | Disabled        | Free            | Public health/MCP demo      |
| Render Paid         | Local model | Enabled         | Paid            | Full demo                   |
| Render + OpenRouter | API-based   | Enabled         | Low/usage-based | Recommended production path |

---

## Recommended Commit Messages

Disable local embeddings for Render:

```bash
git commit -m "fix: disable embeddings in constrained deployment environments"
```

Add provider abstraction:

```bash
git commit -m "feat: add configurable embedding provider architecture"
```

Add OpenRouter embeddings:

```bash
git commit -m "feat: add OpenRouter embeddings provider"
```

Update docs:

```bash
git commit -m "docs: document embedding architecture and deployment strategy"
```
