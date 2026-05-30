# 🛡️ Anti-Hallucination Skill

> A comprehensive skill for preventing, detecting, and reducing AI hallucinations in LLM outputs.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
<!-- Replace Tlkh201313 with your actual GitHub username -->
[![GitHub stars](https://img.shields.io/github/stars/Tlkh201313/Stop-hallucinating-skill.svg?style=social&label=Star&maxAge=2592000)](https://github.com/Tlkh201313/Stop-hallucinating-skill)

---

## 📖 Overview

AI hallucinations — outputs that are syntactically fluent but factually incorrect — are one of the biggest challenges in deploying LLMs reliably. This skill provides a comprehensive toolkit of techniques, prompt templates, and architectural patterns to minimize hallucinations across all domains.

### Key Features

- **12 prompt templates** — copy-paste ready for any use case
- **6 architecture patterns** — from simple RAG to advanced Self-RAG
- **5 detection methods** — from basic citation checks to token-level verification
- **Domain-specific guidance** — legal, medical, code, financial, scientific
- **Production checklists** — ready for enterprise deployment
- **Tools & libraries guide** — curated list of the best anti-hallucination tools

### What Makes This Different

Most anti-hallucination guides are **reference documents** — they tell you what to do but don't enforce it. This skill is an **enforcement system**:

- **Structured output enforcement** — JSON schemas with required fields prevent hallucinations from hiding in prose
- **Concrete examples** — 8 real hallucination patterns with detection and correction guidance
- **Incident response protocol** — What to do when hallucinations escape
- **Measurement framework** — How to know if your guardrails are working
- **Anti-injection defenses** — Prevents prompt attacks from bypassing guardrails
- **Multi-turn rules** — Prevents hallucination compounding across conversation turns

### Research-Backed

All techniques are based on:
- 2024-2026 academic research (Nature, ICLR, arXiv)
- Production experience from companies like Anthropic, NVIDIA, Meta
- Industrial studies (Trane Technologies, Stanford, MIT)
- Open-source tools (Guardrails AI, NeMo Guardrails, styxx)

---

## 📦 Installation

### Option 1: npx (Recommended)

```bash
npx Stop-hallucinating-skill install
```

This installs the skill to your OpenCode skills directory. No cloning required.

### Option 2: Manual Clone

```bash
git clone https://github.com/Tlkh201313/Stop-hallucinating-skill.git
cd Stop-hallucinating-skill
```

### Option 3: Direct Use

Copy the prompt templates from `prompt-templates.md` directly into your system prompts.

---

## 🚀 Quick Start

### 0. Install via npx (Recommended)

No cloning required. Works on Windows, Mac, and Linux:

```bash
# Install the skill to OpenCode
npx Stop-hallucinating-skill install

# Or use the short alias
npx anti-hall install
```

**Other commands:**

```bash
# Validate text for hallucination signals
npx Stop-hallucinating-skill validate --text "Studies show 73% of users prefer..."

# Show prompt templates
npx Stop-hallucinating-skill prompt structured

# Show quick guide
npx Stop-hallucinating-skill guide

# Check version
npx Stop-hallucinating-skill version
```

**Without installing (one-time use):**

```bash
# Run directly without installing
npx Stop-hallucinating-skill validate --text "Your text here"
```

---

### 1. Immediate Use (No Code Changes)

Add this to your system prompt:

```
If you are uncertain or do not have sufficient information to answer accurately,
say "I don't know" or "I'm not confident about this." Do not guess or fabricate.

For every factual claim, include a citation. If you cannot find a supporting source,
retract the claim.
```

This single change can dramatically reduce hallucinations.

### 2. Choose Your Template

| Use Case | Template | File |
|---|---|---|
| General factual tasks | Template 1 (Minimal) | `prompt-templates.md` |
| Document Q&A / RAG | Template 2 (Document-Grounded) | `prompt-templates.md` |
| High-stakes research | Template 3 (Research Mode) | `prompt-templates.md` |
| Code generation | Template 4 (Technical) | `prompt-templates.md` |
| Post-generation audit | Template 5 (Verification Pass) | `prompt-templates.md` |
| Long documents | Template 6 (Quotes-First) | `prompt-templates.md` |
| Advanced verification | Template 8 (Chain-of-Verification) | `prompt-templates.md` |

### 3. Domain-Specific Guidance

| Domain | Key Risks | Guidance |
|---|---|---|
| Legal | Invented case citations | `domain-specific.md` |
| Medical | Wrong dosages, interactions | `domain-specific.md` |
| Code | Invented APIs, packages | `domain-specific.md` |
| Financial | Fabricated statistics | `domain-specific.md` |
| Scientific | Fake paper citations | `domain-specific.md` |

### 4. Validate Your Outputs

Run the validation script to check for hallucination signals:

```bash
# Basic check
python scripts/validate_output.py --output "Your model's response here"

# Strict mode (fails on any HIGH severity flag)
python scripts/validate_output.py --output "..." --strict

# Verbose output (shows details)
python scripts/validate_output.py --output "..." --verbose

# JSON output (for programmatic use)
python scripts/validate_output.py --output "..." --json
```

The script detects:
- Fabricated statistics (precise percentages without source)
- Unsourced "studies show" claims
- Vague authority appeals
- Misattributed quotes
- Missing grounding references

---

## 📁 Project Structure

```
Stop-hallucinating-skill/
├── SKILL.md                    # Main skill documentation
├── prompt-templates.md         # 12 copy-paste prompt templates
├── domain-specific.md          # Domain-specific guidance
├── references/
│   ├── rag-setup.md           # RAG pipeline setup guide
│   ├── theory.md              # Hallucination theory & taxonomy
│   ├── tools-and-libraries.md # Curated tools list
│   ├── examples.md            # 8 real hallucination examples with detection
│   └── measurement.md         # How to measure if guardrails are working
├── scripts/
│   └── validate_output.py     # Output validation script
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
└── LICENSE                    # MIT License
```

---

## 🎯 Techniques Overview

### Prompt-Level (Zero Infrastructure Changes)

| Technique | Effectiveness | Complexity |
|---|---|---|
| Allow "I don't know" | High | Low |
| Require citations | High | Low |
| Context restriction | High | Low |
| Chain-of-Thought | Medium-High | Low |
| Chain-of-Verification | Very High (+23% F1) | Medium |
| Decomposed prompting | High (34%→80%) | Medium |
| Domain glossary | High (77% improvement) | Low |
| Temperature control | Medium | Low |
| Anti-sycophancy | Medium | Low |

### Architecture-Level (For Production Systems)

| Technique | Effectiveness | Complexity |
|---|---|---|
| RAG (proper implementation) | Very High (3-5x reduction) | High |
| Agentic RAG | Very High | High |
| Multi-model validation | High | Medium |
| Iterative refinement | High | Medium |
| Human-in-the-loop | Very High | High |
| Self-RAG | State-of-the-art | High |

### Detection & Verification

| Technique | Effectiveness | Complexity |
|---|---|---|
| Best-of-N (Self-Consistency) | High (+17.9%) | Low |
| Citation audit | High | Medium |
| Uncertainty quantification | Medium-High | Low |
| Semantic groundedness | High | Medium |
| Token-level detection | Very High | High |

---

## 🛠️ Tools & Libraries

### Production Frameworks
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) — Python framework with validators
- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails) — Enterprise guardrails
- [DeepTeam](https://github.com/confident-ai/deepteam) — Red-teaming framework

### Detection Libraries
- [styxx](https://github.com/fathom-lab/styxx) — 0.998 AUC, CPU-only, no LLM needed
- [Director AI](https://github.com/anulum/director-ai) — Real-time streaming halt
- [HalluciGuard](https://github.com/Hermes-Lekkas/HalluciGuard) — Claim extraction + verification

### RAG Evaluation
- [RAGAS](https://github.com/explodinggradients/ragas) — RAG assessment framework
- [Open RAG Eval](https://github.com/vectara/open-rag-eval) — Vectara's evaluation tools

See `references/tools-and-libraries.md` for the complete list.
See `references/examples.md` for concrete hallucination patterns to test against.

---

## 📊 Effectiveness by Technique

Based on research and industrial studies:

| Technique | Hallucination Reduction | Source |
|---|---|---|
| Multi-layered approach | Up to 96% | Stanford 2024 |
| Chain-of-Verification | +23% F1 | Meta 2024 |
| Self-Consistency | +17.9% accuracy | Wang et al. 2022 |
| Decomposed Prompting | 34% → 80% | Trane Technologies 2026 |
| Domain Glossary | 77% improvement | Trane Technologies 2026 |
| RAG (proper setup) | 3-5x reduction | Industry consensus |
| Behavioral Trust Clustering | 52% reduction | snc-core |
| Token-Guard | State-of-the-art | ICLR 2026 |

---

## 🔧 Installation

This is a skill, not a library. To use it:

### For OpenCode Users
1. Clone this repository to your skills directory
2. The skill will be automatically available

### For General Use
1. Copy the prompt templates from `prompt-templates.md`
2. Follow the architecture guidance in `SKILL.md`
3. Apply domain-specific rules from `domain-specific.md`

---

## 📝 Usage Examples

### Example 1: Simple Factual Q&A

```python
system_prompt = """
You are a factual assistant. Follow these rules:
- If uncertain, say "I'm not confident about this"
- If you don't know, say "I don't know"
- Never fabricate citations or statistics
- Distinguish between facts and inferences
"""
```

### Example 2: RAG Pipeline

```python
system_prompt = """
Answer ONLY using the provided documents.
For each claim, cite: [Doc: <name>, Section: <section>]
If the documents don't contain the answer, say so.
Do not use your training knowledge.
"""
```

### Example 3: High-Stakes Verification

```python
# First pass: generate answer
answer = llm.generate(query, system_prompt=research_mode_prompt)

# Second pass: verify
verification = llm.generate(
    f"Review this answer. For each claim, verify it against the source. "
    f"Remove any [UNVERIFIED] claims.\n\n{answer}",
    system_prompt=verification_prompt
)
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### What to Contribute

- New prompt templates
- Domain-specific guidance
- Tool integrations
- Research findings
- Bug fixes and improvements

---

## 📚 References

- [A Survey on Hallucination in LLMs](https://www.mdpi.com/2078-2489/16/5/559) — MDPI 2025
- [Semantic Entropy](https://www.nature.com/articles/s41586-024-07421-0) — Nature 2024
- [Chain-of-Verification](https://arxiv.org/abs/2309.11495) — Meta 2024
- [Self-RAG](https://arxiv.org/abs/2310.11511) — 2023
- [Token-Guard](https://openreview.net/forum?id=token-guard) — ICLR 2026
- [Guardrails AI Documentation](https://docs.guardrailsai.com/)
- [NVIDIA NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Anthropic for research on hallucination prevention
- NVIDIA for NeMo Guardrails framework
- The open-source community for tools and libraries
- Researchers publishing on hallucination detection and prevention

---

## 📧 Contact

If you have questions or feedback, please open an issue on GitHub.

---

**Remember:** No technique eliminates hallucinations entirely. Always validate critical information in high-stakes domains (legal, medical, financial) regardless of how many guardrails are in place.
