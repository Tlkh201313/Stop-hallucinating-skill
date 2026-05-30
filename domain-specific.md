# Domain-Specific Hallucination Prevention

Hallucinations carry different risks and require different mitigations depending on the field. These rules are MANDATORY — not suggestions.

---

## Legal

**Primary risks:**
- Invented case citations (e.g., "Smith v. Jones, 2021" that doesn't exist)
- Fabricated statutes or regulatory clauses
- Incorrect legal reasoning based on surface similarities to real cases
- AI fabricating court cases — even citing formatting details that make them look real

### MANDATORY approach:

1. **NEVER trust citations without verification.** ALWAYS check case names against Westlaw,
   LexisNexis, or official court databases before including in any filing or memo.

2. **Use this prompt addition:**
   ```
   LEGAL ACCURACY RULES:
   - MUST NOT cite any case, statute, regulation, or legal principle unless you are
     highly confident it exists and the citation is accurate.
   - If you cite a case, include: case name, jurisdiction, year, and holding.
   - MUST NOT cite any case unless you can provide: exact case name, jurisdiction, year,
     AND a verified source. If you cannot provide ALL four, output: "Case citation
     unavailable — verify against Westlaw/LexisNexis."
   - NEVER output a citation in legal format unless verified — the formatting itself
     creates false authority.
   - NEVER invent a statute number or regulatory clause.
   - If you cannot verify a citation, explicitly state: "Citation unverified —
     check against legal database."
   ```

   **ENFORCEMENT:** Every legal citation MUST be verified against a legal database before
   delivery. Unverified citations MUST be removed. A second model checking hallucinated
   citations is NOT sufficient — use database lookup or human verification.

3. **Post-generation audit:** Have a second model (or a lawyer) verify every citation.
   Run NLI on each claim against the source material.

4. **Preferred architecture:** RAG over a verified legal database (Westlaw export, official
   court record APIs) with strict context-only prompting. Use hybrid search (vector + BM25)
   with cross-encoder reranking.

5. **Confidence threshold:** If retrieval confidence < 0.8, route to human review rather than
   generating a response.

---

## Medical / Healthcare

**Primary risks:**
- Incorrect drug dosages, interactions, or contraindications
- Fabricated clinical trial results
- Outdated guidance presented as current standard of care
- Hallucinated dosage information can directly impact patient safety

### MANDATORY approach:

1. **MUST include disclaimer.** Every medical output MUST contain:
   "⚠️ This is not medical advice. Verify with a qualified clinician before acting
   on this information."
   This disclaimer is NON-NEGOTIABLE.

2. **Use domain-restricted RAG.** Ground responses in:
   - UpToDate, PubMed, or institutional clinical guidelines
   - FDA label database for drug information
   - CDC / WHO official guidance documents
   - Only use documents with verified provenance

3. **Prompt additions:**
   ```
   MEDICAL ACCURACY RULES:
   - Base all clinical information on the provided reference documents only.
   - For any dosage, drug name, or interaction, cite the exact source document.
   - MUST use structured format with explicit source fields.
   - Dosage information MUST include the exact source document. If the source does
     not contain dosage info, output: "Dosage not found in provided materials —
     consult prescribing information." NEVER generate dosage from memory.
   - If you are uncertain about a medical fact, explicitly flag it:
     "⚠️ Please verify this with a qualified clinician or current clinical guidelines."
   - NEVER state a drug interaction or contraindication unless it appears in the
     provided sources.
   - If the source document is older than 2 years, note: "Source may be outdated —
     verify against current guidelines."
   - NEVER guess at dosages. If not in source: "Dosage not found in provided materials."
   ```

   **ENFORCEMENT:** Medical outputs MUST use structured format with explicit source fields.
   Dosage information MUST include the exact source document. If the source does not contain
   dosage info, output: "Dosage not found in provided materials — consult prescribing
   information." NEVER generate dosage from memory.

4. **Use uncertainty quantification.** Flag any claim below HIGH confidence for
   mandatory human review before the output reaches clinical staff.

5. **Multi-model validation:** For any clinical recommendation, run through 2+ models
   and flag disagreements for pharmacist/clinician review.

---

## Code Generation

**Primary risks:**
- Invented function names or method signatures (e.g., `pandas.read_excel(sheet_number=2)`)
- Invented CLI flags or options
- Deprecated APIs presented as current
- Hallucinated package names that don't exist on PyPI/npm
- Security vulnerabilities from incorrect API usage

### MANDATORY approach:

1. **Prompt addition:**
   ```
   CODE ACCURACY RULES:
   - MUST ONLY use APIs verifiable against official documentation.
   - If you cannot verify a parameter name, output: "Parameter name unverified —
     check official docs." NEVER guess parameter names — silent failures are worse
     than errors.
   - NEVER invent package names. If a package name might be wrong, say
     "verify this package name before installing."
   - If you can't recall exact syntax, use clearly labelled pseudocode.
   - Always note your knowledge cutoff when referencing library versions:
     "As of my training data, the API was X — please verify in the current docs."
   - For any security-sensitive code (auth, crypto, input validation), explicitly
     warn: "⚠️ Security-critical code — have this reviewed by a security expert."
   ```

   **ENFORCEMENT:** After generating code, verify all package names against PyPI/npm APIs.
   Check parameter names against official documentation. Flag any unverified API calls
   with ⚠️.

2. **Add a test step:** After generating code, instruct the model to:
   ```
   Review the code above. List every external function, method, and package used.
   For each one, state your confidence that it exists and is used correctly.
   Flag anything you are less than highly confident about with ⚠️.
   ```

3. **Prefer retrieval over memory:** Use tools like GitHub Copilot's workspace context,
   Cursor's codebase indexing, or a custom RAG pipeline over your actual codebase
   rather than relying on the model's parametric knowledge of APIs.

4. **Verify package existence:** After generation, check that all imported packages
   exist on PyPI/npm before presenting code to users.

---

## Financial / Business

**Primary risks:**
- Invented statistics (market size, growth rates, revenue figures)
- Fabricated analyst reports or regulatory filings
- Incorrect interpretation of financial instruments
- Outdated market data presented as current

### MANDATORY approach:

1. **ALWAYS cite publicly verifiable sources** (SEC filings, Bloomberg, Reuters, official
   company investor relations pages).

2. **Prompt addition:**
   ```
   FINANCIAL ACCURACY RULES:
   - MUST NOT state any financial figure, market statistic, or projection without a source.
   - Format citations as: [Source: <organisation>, <document/report>, <date>]
   - MUST include the date of any financial figure: "As of [DATE]". If you cannot
     provide a date, output: "Date unavailable — verify current figures." NEVER
     present outdated data as current.
   - If a figure is an estimate or projection, label it explicitly: (estimate)
   - NEVER fabricate analyst quotes or attribute figures to specific reports
     unless you are certain they exist.
   - If you cannot find a specific number, say "Figure not available" rather than
     providing an approximation.
   ```

3. **Architecture:** RAG over verified financial data feeds (Bloomberg API, SEC EDGAR,
   official earnings transcripts) with strict external-knowledge restriction.

4. **Real-time verification:** For market data, integrate with live APIs rather than
   relying on training data. Note: "As of [date] market close" for any figures.

---

## Scientific / Research

**Primary risks:**
- Fabricated paper citations (e.g., "Smith et al., 2022, Nature" that doesn't exist)
- Incorrect interpretation of study findings
- Overstating certainty of contested results
- Mixing up findings from different studies

### MANDATORY approach:

1. **For any cited paper, verify via:**
   - Google Scholar, Semantic Scholar, PubMed, arXiv
   - Check: authors, journal, year, actual DOI
   - Verify the paper actually says what is claimed

2. **Prompt addition:**
   ```
   RESEARCH ACCURACY RULES:
   - MUST verify paper existence against Google Scholar, Semantic Scholar, or PubMed
     before citing. If you cannot verify, output: "Citation unverified — search
     [database] for the original." NEVER output a paper citation unless you can
     confirm: authors, title, journal, year, AND DOI.
   - If citing a study's findings, quote the abstract or key result directly.
   - Distinguish between: replicated findings, single studies, preprints, and consensus.
   - If a result is contested or preliminary, say so explicitly.
   - Do not state "studies show X" without citing a specific study.
   - If you cannot recall exact details of a paper, say:
     "I recall a study on this topic but cannot verify the exact citation —
     please search [Google Scholar/PubMed] for the original."
   - NEVER mix up findings from different studies.
   ```

3. **Use quotes-first approach** (Template 6 in prompt-templates.md) for summarising
   specific papers — extract quotes first, then synthesise.

4. **Cross-reference claims:** For any major claim, try to find 2+ supporting sources.
   Single-source claims should be flagged as such.

---

## Multi-Domain / General Enterprise

For deployments serving mixed use cases, implement a **tiered guardrail system**:

```
TIER 1 — Always on:
  • "I don't know" permission
  • No fabricated citations
  • Temperature ≤ 0.3
  • Anti-sycophancy rules

TIER 2 — Turn on for factual/research tasks:
  • Citations required
  • Context-only restriction
  • Verification pass
  • Chain-of-Verification (CoVe)
  • Decomposed prompting

TIER 3 — Turn on for high-stakes domains (legal, medical, financial):
  • Human-in-the-loop review
  • Multi-model cross-validation
  • Domain-specific RAG corpus
  • Per-claim NLI verification
  • Confidence threshold routing
```

**DEFAULT TO TIER 3** (highest protection) when uncertain about query type. It is better
to over-protect than under-protect. Only downgrade to TIER 2 or TIER 1 when the query is
clearly non-factual (creative writing, brainstorming).

---

## Cross-Domain Best Practices

Regardless of domain, apply these universal practices:

1. **Layer defenses:** No single technique is sufficient. Combine prompt-level,
   architecture-level, and detection techniques.

2. **Prefer refusal over hallucination:** A structured "I don't know" is always better
   than a confident but incorrect answer.

3. **Log everything:** Track queries, responses, confidence scores, and escalations
   for auditing and improvement.

4. **Test adversarially:** Regularly test with edge cases, ambiguous questions, and
   known hallucination triggers.

5. **Iterate:** Monitor real-world performance and update guardrails based on
   observed failure modes.

---

## Universal Enforcement Rules

These rules apply to ALL domains, NO EXCEPTIONS:

1. **NEVER output a citation you cannot verify.** A fabricated citation is worse than no citation.
2. **NEVER present a guess as a fact.** "I don't know" is always better than a confident wrong answer.
3. **NEVER let hedging language disguise a guess.** "It's possible that X" when you made up X is still a hallucination.
4. **ALWAYS use structured output for high-stakes domains.** Prose allows hallucinations to hide. JSON with required source fields forces accountability.
5. **ALWAYS verify before delivery.** A second model is not sufficient for critical domains. Use database lookup, NLI verification, or human review.
6. **ALWAYS prefer refusal over hallucination.** A structured "I cannot verify this" is better than a confident but incorrect answer.
