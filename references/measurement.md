# Hallucination Measurement & Evaluation Framework

How to measure if your anti-hallucination system is actually working.

---

## Why Measure?

You cannot fix what you do not measure. Without metrics:
- You don't know if guardrails are working
- You can't compare different approaches
- You can't detect regressions
- You can't justify the cost of anti-hallucination measures

---

## Key Metrics

### 1. Hallucination Rate

**Definition:** Percentage of outputs containing at least one hallucinated claim.

```
Hallucination Rate = (Outputs with hallucinations / Total outputs) × 100
```

**Target:** <5% for production systems, <1% for high-stakes domains.

**How to measure:**
1. Sample 100-500 outputs from your system
2. Have human reviewers or NLI models verify each claim
3. Count outputs with at least one unverified/false claim

### 2. Factual Precision

**Definition:** Percentage of claims that are verifiably true.

```
Factual Precision = (Verified true claims / Total claims) × 100
```

**Target:** >95% for factual systems.

### 3. Citation Accuracy

**Definition:** Percentage of citations that are real and support the claim.

```
Citation Accuracy = (Valid citations / Total citations) × 100
```

**Target:** >95%. Any fabricated citation is a critical failure.

### 4. Refusal Rate

**Definition:** Percentage of queries where the model says "I don't know."

```
Refusal Rate = (Refused queries / Total queries) × 100
```

**Target:** 5-15%. 
- Too low (<5%): Model is probably hallucinating instead of refusing
- Too high (>15%): Retrieval or prompts may be too restrictive

### 5. Grounding Score

**Definition:** Average semantic similarity between claims and source documents.

```
Grounding Score = mean(cosine_similarity(claim_embedding, source_embedding))
```

**Target:** >0.7 average.

### 6. Confidence Calibration

**Definition:** How well the model's expressed confidence matches actual accuracy.

```
Calibration Error = |Stated confidence - Actual accuracy|
```

**Target:** <0.1 average calibration error.

A well-calibrated model that says "HIGH confidence" should be right >90% of the time.

---

## Evaluation Datasets

### Standard Benchmarks

| Dataset | Size | Domain | What It Tests |
|---|---|---|---|
| HaluEval | 35K samples | General | General hallucination detection |
| TruthfulQA | 817 questions | General | Truthfulness vs. misconceptions |
| FActScore | Varies | Biography | Atomic fact checking |
| RAGAS | Varies | RAG | Faithfulness, relevance, precision |
| HaluEval-Wild | Varies | Multi-domain | Real-world hallucinations |

### Building Your Own Dataset

1. **Collect real failures:** Every hallucination caught in production goes in the dataset
2. **Include edge cases:** Ambiguous questions, recent events, niche topics
3. **Include adversarial cases:** Prompt injections, misleading questions
4. **Balance:** Include both hallucinated and grounded examples
5. **Label carefully:** Each claim needs ground-truth verification

### Dataset Structure

```json
{
  "id": "test_001",
  "query": "What is the recommended dosage of metformin?",
  "context": "Source document text here...",
  "expected_behavior": "Should provide dosage WITH source citation, or refuse if not in context",
  "hallucination_indicators": [
    "Specific dosage without citation",
    "Claim about ADA guidelines without verification"
  ],
  "correct_response": "Per the provided prescribing information, the starting dose is...",
  "severity": "CRITICAL"
}
```

---

## A/B Testing Framework

### Comparing Guardrail Configurations

```
GROUP A (Control):   No anti-hallucination guardrails
GROUP B (Treatment): With anti-hallucination guardrails

Measure:
- Hallucination rate (primary metric)
- Factual precision
- Refusal rate
- User satisfaction
- Response latency
```

### Statistical Significance

- Minimum sample size: 100 outputs per group
- Use chi-squared test for hallucination rate comparison
- Require p < 0.05 for significance
- Report confidence intervals

### Example Test Plan

```
WEEK 1: Baseline measurement (no guardrails)
  - Measure hallucination rate on 200 outputs
  - Build evaluation dataset from failures

WEEK 2: Deploy guardrails
  - Same 200 queries, with guardrails enabled
  - Measure hallucination rate

WEEK 3: Compare
  - Calculate reduction in hallucination rate
  - Check statistical significance
  - Identify remaining failure modes

WEEK 4: Iterate
  - Add guardrails for remaining failure modes
  - Re-test
```

---

## Monitoring in Production

### Real-Time Metrics to Track

| Metric | Alert Threshold | Action |
|---|---|---|
| Hallucination rate (1hr window) | >10% | Page on-call |
| Citation accuracy (1hr window) | <90% | Investigate |
| Refusal rate (1hr window) | >25% | Check retrieval |
| Refusal rate (1hr window) | <2% | Check if model is hallucinating instead |
| Grounding score (1hr window) | <0.6 | Check retrieval quality |

### Sampling Strategy

- Log 100% of outputs for high-stakes domains
- Sample 10% of outputs for general domains
- Random audit 50 outputs per week (human review)
- Automated audit 500 outputs per week (NLI model)

### Incident Tracking

Every hallucination caught in production should log:
```json
{
  "timestamp": "2026-05-30T10:00:00Z",
  "query": "User's question",
  "output": "Model's response",
  "hallucinated_claim": "The specific false claim",
  "severity": "HIGH|MEDIUM|LOW",
  "guardrail_failed": "Which guardrail should have caught this",
  "root_cause": "Why the guardrail failed",
  "fix_applied": "What was changed to prevent recurrence"
}
```

---

## Evaluation Pipeline

### Automated Evaluation (Run Daily)

```python
# Pseudo-code for automated evaluation
def evaluate_daily():
    # 1. Sample outputs from last 24 hours
    outputs = sample_outputs(n=500)
    
    # 2. Run NLI verification on each claim
    for output in outputs:
        claims = extract_claims(output)
        for claim in claims:
            nli_result = nli_model(claim, source_document)
            if nli_result == "contradiction":
                flag_hallucination(output, claim)
    
    # 3. Compute metrics
    hallucination_rate = flagged / total
    factual_precision = verified_claims / total_claims
    
    # 4. Alert if thresholds exceeded
    if hallucination_rate > ALERT_THRESHOLD:
        send_alert(f"Hallucination rate: {hallucination_rate:.1%}")
    
    # 5. Log to dashboard
    log_metrics({
        "hallucination_rate": hallucination_rate,
        "factual_precision": factual_precision,
        "refusal_rate": refusal_rate,
        "grounding_score": grounding_score
    })
```

### Human Evaluation (Run Weekly)

1. Sample 50 outputs randomly
2. Human reviewer checks each output for:
   - Factual accuracy
   - Citation validity
   - Appropriate hedging/uncertainty
   - Missing information
3. Compare human judgments to automated metrics
4. Update automated thresholds if diverging

---

## Reporting Template

### Weekly Hallucination Report

```
HALLUCINATION REPORT — Week of [DATE]

SUMMARY:
- Outputs evaluated: [N]
- Hallucination rate: [X]% (target: <5%)
- Factual precision: [X]% (target: >95%)
- Citation accuracy: [X]% (target: >95%)
- Refusal rate: [X]% (target: 5-15%)

TRENDS:
- Hallucination rate: [↑↓→] vs. last week
- New failure modes discovered: [N]
- Guardrails updated: [list]

INCIDENTS:
- Critical hallucinations: [N]
- Root causes: [list]
- Fixes applied: [list]

ACTION ITEMS:
- [ ] [Action 1]
- [ ] [Action 2]
```

---

## Common Measurement Mistakes

1. **Measuring only what's easy:** Keyword overlap is easy to measure but doesn't catch hallucinations. Use NLI or human review.

2. **Small sample sizes:** 10 outputs is not enough. Need 100+ for statistical significance.

3. **No baseline:** You need a "before" measurement to know if guardrails are helping.

4. **Ignoring false positives:** If guardrails are too strict, they refuse valid answers. Measure refusal rate too.

5. **Not tracking over time:** A single measurement is a snapshot. Track trends.

6. **Trusting the model to evaluate itself:** A model that hallucinated will often "verify" its own hallucination. Use a different model or human review.
