# RAG Setup Guide for Hallucination Prevention

A comprehensive guide to building RAG systems that minimize hallucinations.

---

## Architecture Overview

The optimal RAG pipeline for hallucination prevention has 8 stages:

```
1. INGESTION → 2. SOURCE SELECTION → 3. RETRIEVAL → 4. RERANKING → 
5. EVIDENCE EXTRACTION → 6. CONSTRAINED GENERATION → 7. ATTRIBUTION → 
8. POST-GENERATION GUARDRAILS
```

**Critical rule:** Never glue retrieval directly to generation in production.

---

## Stage 1: Document Ingestion

### Chunking Strategy

| Strategy | Best For | Chunk Size | Overlap |
|---|---|---|---|
| Semantic (by paragraph/section) | Most documents | 500-1000 chars | 75 tokens |
| Fixed-token | Simple texts | 512 tokens | 64 tokens |
| Document-aware | PDFs, legal docs | Clause/section boundaries | Varies |

**Best practices:**
- Semantic chunking beats fixed-token chunking by 40%
- Always snap to sentence boundaries
- Preserve table integrity (don't split tables mid-row)
- For regulatory PDFs, respect clause boundaries
- Store metadata with each chunk (source, page, section)

### Embedding Models

| Model | Dimensions | Best For |
|---|---|---|
| text-embedding-3-small | 1536 | General purpose |
| text-embedding-3-large | 3072 | High accuracy |
| BGE-M3 | 1024 | Multilingual |
| E5-mistral-7b | 4096 | Maximum quality |

---

## Stage 2: Source Selection

Not all sources are equal. Prioritize:
1. Official documentation (highest trust)
2. Peer-reviewed research
3. Verified databases
4. Community documentation (lower trust)
5. Blog posts / forums (lowest trust)

Store trust scores with sources and use them in ranking.

---

## Stage 3: Retrieval

### Hybrid Search (Recommended)

Combine vector similarity with keyword search:

```python
# Pseudo-code
vector_score = cosine_similarity(query_embedding, chunk_embedding)
keyword_score = bm25_score(query, chunk_text)
final_score = 0.7 * vector_score + 0.3 * keyword_score
```

Hybrid search provides 23% improvement on domain-specific queries.

### Parameters

| Parameter | Recommended Value | Notes |
|---|---|---|
| Top-K | 5-10 | More isn't always better |
| Similarity threshold | ≥ 0.7 | Below this → route to refusal |
| Vector weight | 0.7 | In hybrid search |
| BM25 weight | 0.3 | In hybrid search |

### Confidence Threshold

If the top retrieval score is below threshold, route to refusal:

```python
if top_score < CONFIDENCE_THRESHOLD:
    return {
        "answer": None,
        "refusal_reason": "insufficient_evidence",
        "suggestion": "Please refine your query or add more context."
    }
```

---

## Stage 4: Reranking

After initial retrieval, rerank using a cross-encoder:

| Reranker | Type | Best For |
|---|---|---|
| BGE-Reranker-v2-m3 | Cross-encoder | Multilingual |
| Cohere Rerank | API | Easy integration |
| ColBERT | Late interaction | Speed + quality |

Reranking typically improves relevance by 10-20%.

---

## Stage 5: Evidence Extraction

Before generation, extract key evidence from retrieved chunks:

```
For each retrieved chunk:
1. Identify claims relevant to the query
2. Extract direct quotes
3. Note the source and location
4. Rate relevance (HIGH/MEDIUM/LOW)
```

---

## Stage 6: Constrained Generation

Use strict prompting to force grounded generation:

```
Answer ONLY using the evidence provided below.
For each factual claim, include a citation: [Source: <name>, Page: <n>]
If the evidence doesn't contain the answer, say:
"The provided documents do not contain sufficient information."

EVIDENCE:
[insert extracted evidence here]

QUESTION: [insert user query here]
```

---

## Stage 7: Attribution

Every claim in the output must trace back to a source:

```
Claim: "The algorithm achieves 95% accuracy"
Attribution: [Source: paper.pdf, Section 4.2, Page 7]
```

**Citation resolvability check:** Every `[Source: ...]` marker must resolve to an actual document.
Unresolvable citations are bugs — block release.

---

## Stage 8: Post-Generation Guardrails

### Per-Claim NLI Verification

Run Natural Language Inference on each (claim, cited_span) pair:

```python
for claim in extracted_claims:
    nli_result = nli_model(claim, cited_span)
    if nli_result == "contradiction":
        remove_claim(claim)
    elif nli_result == "neutral":
        flag_for_review(claim)
```

### Hallucination Score

Compute a groundedness score:

```python
hallucination_score = contradicted_claims / total_claims
if hallucination_score > THRESHOLD:
    regenerate_or_refuse()
```

---

## Agentic RAG

For complex queries, use an autonomous reasoning loop:

```
1. PLAN: Break query into sub-questions
2. RETRIEVE: Fetch evidence for each sub-question
3. EVALUATE: Check if evidence is sufficient
4. RETRY: If not, reformulate and re-retrieve
5. SYNTHESIZE: Combine verified answers
```

This handles multi-hop queries where single-pass RAG fails.

---

## Monitoring & Metrics

Track these metrics in production:

| Metric | Target | Action if Below |
|---|---|---|
| Retrieval precision | >85% | Improve chunking/embeddings |
| Context utilization | >60% | Check prompt engineering |
| Hallucination rate | <5% | Add more guardrails |
| Citation accuracy | >95% | Fix attribution pipeline |
| Refusal rate | 5-15% | Too low = missing hallucinations; too high = bad retrieval |

---

## Common Pitfalls

1. **Too many chunks:** More context ≠ better answers. Noise increases hallucination.
2. **No refusal path:** Always have a structured refusal when retrieval fails.
3. **Trusting raw similarity:** Cosine similarity doesn't guarantee relevance.
4. **No reranking:** First-pass retrieval is noisy; always rerank.
5. **Stale index:** Re-index when documents update.
6. **No monitoring:** You can't fix what you don't measure.
