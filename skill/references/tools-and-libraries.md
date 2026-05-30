# Tools & Libraries for Hallucination Prevention

A curated list of tools, libraries, and frameworks for preventing, detecting, and measuring
LLM hallucinations.

---

## Production Frameworks

### Guardrails AI
- **GitHub:** guardrails-ai/guardrails (6,900+ stars)
- **License:** Apache-2.0
- **What it does:** Python framework with validators from Guarduards Hub; RAIL spec + Pydantic schemas; structured output + hallucination checks
- **Best for:** Production guardrails with structured output validation
- **Key features:**
  - Validators for hallucination, toxicity, bias
  - Pydantic-style schema enforcement
  - Hub of pre-built validators
  - Integration with all major LLM providers

### NVIDIA NeMo Guardrails
- **License:** Apache-2.0
- **What it does:** Colang-based state machines for input/output/retrieval/dialog rails
- **Best for:** Enterprise guardrails with complex conversation flows
- **Key features:**
  - GPU-accelerated parallel rails
  - Integrates Guardrails AI validators
  - Custom Colang programming language
  - Topical, moderation, and execution rails

### DeepTeam (Confident AI)
- **GitHub:** confident-ai/deepteam (1,800+ stars)
- **License:** Apache-2.0
- **What it does:** Red-teaming framework with production guardrails
- **Best for:** Testing and validating LLM outputs
- **Key features:**
  - HallucinationGuard
  - OWASP/NIST/MITRE frameworks
  - 7 production guardrails
  - Vulnerability scanning

---

## Detection Libraries

### styxx
- **GitHub:** fathom-lab/styxx
- **License:** MIT
- **What it does:** 9 calibrated cognometric instruments for hallucination detection
- **Best for:** Lightweight, CPU-only detection without LLM calls
- **Key features:**
  - 0.998 AUC on HaluEval benchmark
  - Pure Python, CPU-only, no LLM required
  - `@trust` decorator for easy integration
  - 9 signals: text, entity, grounding, probe, novelty, NLI, etc.

### LettuceDetect
- **GitHub:** KRLabsOrg/LettuceDetect
- **License:** MIT
- **What it does:** Token-classifier or LLM-based hallucination detection facade
- **Best for:** Flexible detection with multiple backends
- **Key features:**
  - Unified API for different detection methods
  - Supports both classifier and LLM-based approaches
  - Easy to extend

### Dingo
- **GitHub:** MigoXLab/dingo
- **License:** Apache-2.0
- **What it does:** Uses HHEM-2.1-Open model for hallucination scoring
- **Best for:** Quick hallucination scoring of text
- **Key features:**
  - Pre-trained hallucination detection model
  - Easy API
  - Batch processing support

### Director AI
- **GitHub:** anulum/director-ai
- **License:** AGPL-3.0
- **What it does:** Real-time NLI + RAG fact-checking with token-level streaming halt
- **Best for:** Real-time hallucination prevention during generation
- **Key features:**
  - 5-tier scoring (rules→embeddings→NLI)
  - Rust-accelerated for speed
  - Streaming halt when coherence drops
  - Dual-entropy scoring

### HalluciGuard
- **GitHub:** Hermes-Lekkas/HalluciGuard
- **License:** AGPL-3.0
- **What it does:** Claim extraction + confidence scoring + web verification
- **Best for:** Multi-step verification with external fact-checking
- **Key features:**
  - LangChain callback integration
  - Provider-agnostic
  - Web verification capability

---

## RAG Evaluation

### Open RAG Eval (Vectara)
- **GitHub:** vectara/open-rag-eval
- **License:** Apache-2.0
- **What it does:** RAG evaluation with BERTScore, ROUGE, hallucination scoring
- **Best for:** Evaluating RAG pipeline quality
- **Key features:**
  - Multiple evaluation metrics
  - Hallucination-specific scoring
  - Comparison across RAG configurations

### RAGAS
- **What it does:** RAG Assessment framework
- **Best for:** Evaluating faithfulness, answer relevance, context precision
- **Key metrics:**
  - Faithfulness: Are claims supported by context?
  - Answer relevance: Does answer address the question?
  - Context precision: Is retrieved context relevant?

### LlamaIndex Evaluators
- **What it does:** Built-in evaluation for LlamaIndex RAG pipelines
- **Best for:** LlamaIndex users
- **Key features:**
  - Faithfulness evaluator
  - Relevancy evaluator
  - Correctness evaluator

---

## Observability & Monitoring

### Opik (Comet ML)
- **GitHub:** comet-ml/opik
- **License:** Apache-2.0
- **What it does:** LLM observability with hallucination metrics
- **Best for:** Production monitoring and debugging
- **Key features:**
  - Hallucination() metric for programmatic scoring
  - Trace logging
  - Experiment tracking

### PromptShield
- **GitHub:** Neeraj-Ch0udhary/promptshield
- **What it does:** 3-layer protection: input guard + output guard + memory layer
- **Best for:** Comprehensive guardrails with monitoring
- **Key features:**
  - Input injection detection
  - Output hallucination detection
  - Memory layer for context

### PromptProof
- **GitHub:** MindfulwareDev/PromptProof
- **License:** GPL-3.0
- **What it does:** 60+ guardrail prompts with CLI tools
- **Best for:** Quick setup with many pre-built prompts
- **Key features:**
  - Adversarial test suite
  - OpenAI/Anthropic/Ollama integrations
  - LangChain/LlamaIndex support

---

## Specialized Tools

### Token-Guard
- **GitHub:** RongHuiQiang/Token-Guard
- **License:** Apache-2.0
- **What it does:** Token-level hallucination control via self-checking decoding
- **Best for:** Research and advanced applications
- **Key features:**
  - ICLR 2026 paper
  - Prunes hallucinated tokens mid-generation
  - Works at inference time

### SNC-Core (Behavioral Trust Clustering)
- **GitHub:** Dan23RR/snc-core
- **License:** MIT
- **What it does:** Thermodynamic governance layer for LLM outputs
- **Best for:** Model-agnostic hallucination reduction
- **Key features:**
  - 52% hallucination reduction on HumanEval
  - Samples K=5 candidates, clusters by equivalence
  - Computes trust score
  - Abstains when uncertain

### LLM Guardrails (TypeScript)
- **GitHub:** llm-guardrails/llm-guardrails
- **License:** MIT
- **What it does:** TypeScript-native content guards
- **Best for:** Node.js/TypeScript applications
- **Key features:**
  - 12μs latency, 80K checks/sec
  - 10 content guards
  - Zero dependencies

---

## Embedding & Vector Libraries

### Sentence Transformers
- **What it does:** Compute embeddings for semantic similarity
- **Best for:** Computing groundedness scores
- **Key models:**
  - all-MiniLM-L6-v2 (fast, general)
  - BGE-M3 (multilingual)
  - E5-mistral-7b (highest quality)

### FAISS (Facebook AI)
- **What it does:** Efficient vector similarity search
- **Best for:** Large-scale vector retrieval
- **Key features:**
  - GPU acceleration
  - Multiple index types
  - Billion-scale support

### Chroma
- **What it does:** AI-native open-source vector database
- **Best for:** Simple RAG setups
- **Key features:**
  - Easy API
  - Persistent storage
  - Metadata filtering

### Weaviate
- **What it does:** Vector search engine with modules
- **Best for:** Production RAG with hybrid search
- **Key features:**
  - Built-in vectorization
  - Hybrid search (vector + BM25)
  - GraphQL API

---

## NLI Models

For claim verification, use these NLI models:

| Model | Type | Best For |
|---|---|---|
| deberta-v3-large-mnli | Cross-encoder | High accuracy |
| deberta-v3-base-mnli | Cross-encoder | Speed + quality |
| BGE-Reranker-v2-m3 | Cross-encoder | Multilingual |
| bart-large-mnli | Seq2seq | Zero-shot |

---

## Quick Comparison

| Tool | Language | LLM Required | Latency | Best For |
|---|---|---|---|---|
| Guardrails AI | Python | No | Low | Production guardrails |
| NeMo Guardrails | Python | No | Medium | Enterprise flows |
| styxx | Python | No | Very Low | Lightweight detection |
| Director AI | Rust/Python | No | Very Low | Real-time prevention |
| DeepTeam | Python | No | Medium | Red-teaming |
| RAGAS | Python | Yes | High | RAG evaluation |
| Token-Guard | Python | No | Low | Research |

---

## Installation Examples

### Guardrails AI
```bash
pip install guardrails-ai
guardrails hub install hub://guardrails/contains_llm hallucination
```

### styxx
```bash
pip install styxx
```

### RAGAS
```bash
pip install ragas
```

### Sentence Transformers
```bash
pip install sentence-transformers
```

---

## Choosing the Right Tool

| Need | Recommended Tool |
|---|---|
| Production guardrails | Guardrails AI or NeMo Guardrails |
| Lightweight detection | styxx |
| Real-time prevention | Director AI |
| RAG evaluation | RAGAS or Open RAG Eval |
| Red-teaming/testing | DeepTeam |
| TypeScript/Node.js | LLM Guardrails |
| Research | Token-Guard or SNC-Core |
