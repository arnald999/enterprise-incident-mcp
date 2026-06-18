# AI Models, Embeddings, and OpenRouter Strategy

## Embedding Model vs LLM

An embedding model and an LLM solve different problems.

## Embedding Model

An embedding model converts text into a numeric vector.

Example:

```text
"checkout latency spike"
        ↓
[0.12, -0.08, 0.44, ...]
```

These vectors represent semantic meaning.

Similar text produces nearby vectors.

Examples:

```text
"checkout latency spike"
"payment flow slowdown"
"checkout API degraded"
```

may be close in vector space even if the exact words differ.

Embedding models are used for:

* Semantic search
* Similarity matching
* RAG retrieval
* Clustering
* Recommendation
* Classification

In this project, embeddings are used to find similar incidents.

Current local model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Current vector dimension:

```text
384
```

Stored in:

```text
incident_embeddings.embedding
```

using:

```text
pgvector
```

---

## LLM / Chat Model

An LLM generates or reasons over text.

Example:

Input:

```text
Analyze these incident timelines and suggest likely root causes.
```

Output:

```text
The likely root cause appears to be downstream checkout dependency saturation...
```

LLMs are used for:

* Summarization
* RCA generation
* Postmortem writing
* Reasoning
* Explanation
* Decision support
* Natural language responses

Examples:

```text
GPT
Claude
Gemini
Llama
Mistral
Qwen
```

In this project, we currently use deterministic generation for:

* postmortem generation
* RCA draft generation
* investigator report generation

Later, these can be replaced with LLM-backed generation.

---

## Key Difference

| Capability              | Embedding Model | LLM                  |
| ----------------------- | --------------- | -------------------- |
| Converts text to vector | Yes             | No                   |
| Generates text          | No              | Yes                  |
| Used for retrieval      | Yes             | Sometimes indirectly |
| Used for reasoning      | No              | Yes                  |
| Used in semantic search | Yes             | No                   |
| Used in RCA writing     | No              | Yes                  |
| Stored in pgvector      | Yes             | No                   |

---

## How RAG Uses Both

RAG means Retrieval-Augmented Generation.

In this project:

```text
User Query
   ↓
Embedding Model
   ↓
Vector Search
   ↓
Similar Incidents
   ↓
Timeline Context
   ↓
LLM or Deterministic Generator
   ↓
RCA / Investigation Report
```

Embedding model:

```text
Finds relevant incident context.
```

LLM:

```text
Generates the final explanation or recommendation.
```

---

## Current Local Architecture

```text
User Query
   ↓
EmbeddingService
   ↓
SentenceTransformer all-MiniLM-L6-v2
   ↓
384-dimensional vector
   ↓
PostgreSQL + pgvector
   ↓
Semantic Search
   ↓
Incident Context
   ↓
Investigation Report
```

This works well locally because the machine has enough memory to load:

```text
sentence-transformers
transformers
torch
model weights
```

---

## Render Free Tier Issue

Render free tier has limited memory.

The local embedding stack loads:

```text
sentence-transformers
torch
transformers
all-MiniLM-L6-v2
```

This can exceed available memory.

Observed error:

```text
Out of memory
```

This does not mean the architecture is wrong.

It means local embedding inference is too heavy for a constrained deployment environment.

---

## Short-Term Deployment Strategy

For Render free tier:

```text
DISABLE_EMBEDDINGS=true
```

This allows:

```text
/health works publicly
/mcp connects publicly
CRUD tools work
Jira/GitHub mock integrations work
Timeline tools work
Postmortem tools work
```

Semantic tools remain available locally.

This proves public deployment without paying for larger infrastructure.

---

## Long-Term Production Strategy

Replace local embedding inference with an external embedding provider.

Recommended future direction:

```text
OpenRouter Embeddings API
```

New flow:

```text
User Query
   ↓
EmbeddingService
   ↓
OpenRouter Embeddings API
   ↓
Vector
   ↓
PostgreSQL + pgvector
   ↓
Semantic Search
```

Benefits:

* No torch dependency in production container
* Lower memory usage
* Faster startup
* Works on smaller deployment instances
* Provider can be switched through configuration
* Production architecture is closer to real enterprise systems

---

## Future Environment Variables

```env
EMBEDDING_PROVIDER=openrouter
OPENROUTER_API_KEY=...
OPENROUTER_EMBEDDING_MODEL=openai/text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
```

For local development:

```env
EMBEDDING_PROVIDER=local
LOCAL_EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSIONS=384
```

For Render free tier:

```env
DISABLE_EMBEDDINGS=true
```

---

## Important Migration Note

The current database column is:

```python
Vector(384)
```

because `all-MiniLM-L6-v2` returns 384-dimensional vectors.

If using OpenRouter with `text-embedding-3-small`, the vector dimension may be different.

For example:

```text
text-embedding-3-small -> commonly 1536 dimensions
```

So production migration may require changing:

```python
Vector(384)
```

to:

```python
Vector(1536)
```

or another dimension depending on the chosen provider/model.

---

## Recommended Provider Abstraction

Create a provider-based embedding service:

```text
EmbeddingService
   ↓
LocalEmbeddingProvider
   ↓
OpenRouterEmbeddingProvider
```

Interface:

```python
class EmbeddingProvider:
    def embed(self, text: str) -> list[float]:
        ...
```

This keeps the rest of the system unchanged.

The following services should not care whether embeddings come from local inference or OpenRouter:

* EmbeddingRepository
* semantic_search
* index_incident
* investigate_incident
* RAGService

Only the provider changes.

---

## Interview Answer

If asked:

"Why did you separate embedding models from LLMs?"

Answer:

Embedding models and LLMs solve different parts of the RAG pipeline. The embedding model converts incident text into vectors so the system can retrieve semantically similar incidents from pgvector. The LLM is responsible for reasoning and natural language generation, such as writing RCA summaries or investigation reports. Separating these concerns lets us swap local embeddings for OpenRouter embeddings without changing the incident investigator workflow.

---

## Future Roadmap

Phase 1:

```text
Local semantic search using all-MiniLM-L6-v2
```

Phase 2:

```text
Render deployment with embeddings disabled
```

Phase 3:

```text
OpenRouter embeddings provider
```

Phase 4:

```text
OpenRouter or other LLM provider for RCA generation
```

Phase 5:

```text
Fully deployed AI incident investigator
```
