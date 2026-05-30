# Hallucination Theory & Taxonomy

Understanding why hallucinations happen helps in preventing them.

---

## What Are Hallucinations?

Hallucinations are outputs that are syntactically fluent but factually incorrect, fabricated,
or inconsistent with the provided context. They occur because LLMs are trained to produce
*likely* continuations — not *true* ones.

**Key insight:** LLMs don't "know" things. They predict the next most probable token based
on patterns in training data. When the pattern is ambiguous or the model's knowledge is
insufficient, it fills gaps with plausible-sounding but incorrect information.

---

## Taxonomy of Hallucinations

### By Type

| Type | Description | Example |
|---|---|---|
| **Factual fabrication** | Invented facts, statistics, or citations | "According to Smith et al. (2022)..." (paper doesn't exist) |
| **Factual contradiction** | Stating the opposite of what's true | "The Earth orbits the Sun in 400 days" |
| **Entity hallucination** | Invented people, places, or organizations | "The Stanford Institute of AI Ethics" (doesn't exist) |
| **Numerical hallucination** | Wrong numbers, dates, or calculations | "The company was founded in 1987" (actually 1997) |
| **Contextual drift** | Gradual departure from source material | Starting grounded, ending with fabrication |
| **Confabulation** | Filling knowledge gaps with plausible fiction | Detailed but invented explanation of a rare event |
| **Source hallucination** | Citing real sources for claims they don't support | Real paper, wrong findings attributed |

### By Severity

| Severity | Impact | Example |
|---|---|---|
| **Critical** | Safety/legal/medical harm | Wrong drug dosage, invented legal precedent |
| **Major** | Significant misinformation | Fabricated statistics in a report |
| **Minor** | Slightly incorrect but not harmful | Wrong founding year of a company |
| **Cosmetic** | Stylistic but technically wrong | Slightly misquoted text |

### By Cause

| Cause | Description | Mitigation |
|---|---|---|
| **Knowledge gaps** | Model lacks training data on topic | RAG, retrieval |
| **Ambiguous prompts** | Model guesses what user wants | Specific prompts, decomposition |
| **Distribution shift** | Input differs from training distribution | Domain-specific fine-tuning |
| **Decoding randomness** | High temperature introduces noise | Lower temperature |
| **Attention failure** | Model attends to wrong context | Better chunking, reranking |
| **Sycophancy** | Model agrees with false premises | Anti-sycophancy prompts |
| **Recency bias** | Preferring recent but incorrect patterns | Context-only restriction |

---

## Why LLMs Hallucinate

### The Training Objective Problem

LLMs are trained to minimize cross-entropy loss — predicting the next token. This means:
- They optimize for *likelihood*, not *truth*
- "The Earth is flat" has a non-zero probability in the distribution
- When uncertain, they produce the most *plausible* continuation, not the most *accurate*

### The Knowledge Boundary Problem

LLMs have a fuzzy knowledge boundary:
- They "know" some things well (common facts, well-represented topics)
- They "know" some things poorly (rare events, recent data)
- They don't know what they don't know

This leads to confident-sounding outputs even when the model is wrong.

### The Context Window Problem

As context gets longer:
- Models attend to less of it (attention dilution)
- Earlier context may be "forgotten"
- Models fill gaps with parametric (training) knowledge

This is why long-document summarization is particularly prone to hallucination.

---

## Hallucination Detection Theory

### Signal-Based Detection

| Signal | What It Measures | Reliability |
|---|---|---|
| **Token probability** | Confidence per token | Moderate — overconfident models |
| **Semantic entropy** | Uncertainty at meaning level | High — Nature 2024 |
| **Self-consistency** | Agreement across samples | High — majority voting |
| **NLI entailment** | Claim follows from source | High — for grounded tasks |
| **Retrieval similarity** | Answer grounded in context | Moderate — false positives |

### Behavioral Detection

| Method | Approach | Effectiveness |
|---|---|---|
| **Best-of-N** | Sample N times, compare | High for factual claims |
| **Chain-of-Verification** | Multi-step self-verification | +23% F1 improvement |
| **Self-RAG** | Reflection tokens during generation | State-of-the-art |
| **Multi-model agreement** | Cross-validate across models | High for critical outputs |

### Mechanistic Detection

| Method | Approach | Status |
|---|---|---|
| **Spectral Editing (SEA)** | Project activations toward truth | Research |
| **TruthX** | Auto-encoder for truthful latent space | Research |
| **Token-Guard** | Token-level pruning mid-generation | ICLR 2026 |
| **ReDeEP + AARF** | Attention head analysis | Research |

---

## The Hallucination-Factuality Trade-off

Stricter anti-hallucination measures reduce:
- Creative generation quality
- Ability to handle ambiguous queries
- Response fluency and naturalness
- Coverage of edge cases

**Best practice:** Use a "research mode" toggle:
- **Factual mode:** All guardrails enabled, citations required
- **Creative mode:** Minimal constraints, allow speculation
- **Hybrid mode:** Route based on query intent

---

## Measurement & Benchmarks

### Standard Benchmarks

| Benchmark | What It Measures | Notes |
|---|---|---|
| **HaluEval** | General hallucination detection | 35K samples |
| **TruthfulQA** | Truthfulness vs. human misconceptions | 817 questions |
| **FActScore** | Factual precision in biography generation | Atomic fact checking |
| **RAGAS** | RAG-specific faithfulness | Multiple metrics |
| **HaluEval-Wild** | Real-world hallucination detection | Diverse domains |

### Key Metrics

| Metric | Formula | Interpretation |
|---|---|---|
| **Hallucination rate** | Hallucinated claims / Total claims | Lower is better |
| **Factual precision** | Correct claims / All claims | Higher is better |
| **Faithfulness** | Claims supported by context / All claims | Higher is better |
| **Refusal rate** | "I don't know" responses / Total | 5-15% ideal |
| **Citation accuracy** | Valid citations / All citations | >95% target |

---

## Research Frontiers (2024-2026)

### Active Research Areas

1. **Token-level control:** Pruning hallucinated tokens before they propagate (Token-Guard)
2. **Mechanistic interpretability:** Understanding which attention heads cause hallucinations
3. **Adaptive verification:** Choosing verification depth based on uncertainty (PCC)
4. **Multi-agent verification:** Swarms of agents checking each other
5. **Truthful latent spaces:** Steering generation toward truth in activation space

### Open Problems

1. **No silver bullet:** No technique eliminates hallucinations entirely
2. **Evaluation gap:** Benchmarks don't cover all real-world scenarios
3. **Cost vs. quality:** More verification = more compute = higher latency
4. **Domain transfer:** Techniques that work in one domain may not transfer
5. **Adversarial robustness:** Guardrails can be bypassed with clever prompts

---

## Key Papers & Surveys

| Paper | Year | Key Contribution |
|---|---|---|
| "A Survey on Hallucination in LLMs" (MDPI) | 2025 | 300+ study comprehensive survey |
| "Semantic Entropy" (Nature) | 2024 | Meaning-level uncertainty quantification |
| "Chain-of-Verification" (Meta) | 2024 | +23% F1 via multi-step verification |
| "Self-RAG" | 2023 | Reflection tokens for adaptive retrieval |
| "Token-Guard" (ICLR) | 2026 | Token-level hallucination pruning |
| "TruthX" | 2025 | Truthful latent space auto-encoder |
| "Trane Technologies Industrial Study" | 2026 | Decomposed prompting: 34% → 80% reduction |
