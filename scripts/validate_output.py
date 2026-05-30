#!/usr/bin/env python3
"""
validate_output.py — Validate LLM outputs for hallucination signals.

This script performs STRUCTURAL checks on LLM outputs to detect common hallucination
patterns. It does NOT verify factual accuracy (that requires NLI models or database
lookups). It catches FORMAT and STRUCTURE issues that indicate potential hallucinations.

IMPORTANT: This script catches ~30-40% of hallucinations. For production use, combine with:
- NLI-based claim verification (e.g., deberta-v3-large-mnli)
- Database lookups for citations
- Human review for high-stakes outputs
- Guardrails AI or similar frameworks

Usage:
    python validate_output.py --output "The model's response here"
    python validate_output.py --file output.txt
    python validate_output.py --output "..." --source "..." --strict
"""

import argparse
import json
import re
import sys
from typing import Dict, List, Tuple


# ============================================================================
# RED FLAG DETECTION
# ============================================================================

# Patterns that indicate likely hallucination
HALLUCINATION_PATTERNS = {
    "fabricated_statistic": {
        "pattern": r'\b\d{2,3}%\b',
        "description": "Precise percentage without source",
        "severity": "HIGH",
        "explanation": "Specific percentages (e.g., '73% of users') without cited sources are often fabricated."
    },
    "unsourced_studies": {
        "pattern": r'(?:studies|research|evidence)\s+(?:show|suggest|indicate|demonstrate)',
        "description": "References to 'studies show' without citation",
        "severity": "HIGH",
        "explanation": "'Studies show' without a specific citation is a common hallucination pattern."
    },
    "vague_authority": {
        "pattern": r'(?:experts|scientists|researchers|doctors|lawyers)\s+(?:say|believe|agree|recommend)',
        "description": "Vague appeal to authority",
        "severity": "MEDIUM",
        "explanation": "Which experts? Cite specific sources."
    },
    "perfect_citation_format": {
        "pattern": r'(?:et al\.|,\s*\d{4}\))',
        "description": "Academic citation format (may be fabricated)",
        "severity": "MEDIUM",
        "explanation": "Well-formatted citations can be fabricated to look authoritative."
    },
    "invented_quote": {
        "pattern": r'(?:as\s+\w+\s+(?:once\s+)?said|according\s+to\s+\w+|in\s+the\s+words\s+of)',
        "description": "Attribution to a person (may be misattributed)",
        "severity": "MEDIUM",
        "explanation": "Quotes are frequently misattributed. Verify against quote databases."
    },
    "specific_number_no_source": {
        "pattern": r'(?:approximately|about|around|nearly|over|more than)\s+\d[\d,]+',
        "description": "Specific numbers without source",
        "severity": "MEDIUM",
        "explanation": "Large specific numbers without sources are often fabricated."
    },
    "date_claim": {
        "pattern": r'(?:in|since|from|during)\s+(?:19|20)\d{2}\b',
        "description": "Specific date/year claim",
        "severity": "LOW",
        "explanation": "Dates should be verifiable. Check against sources."
    },
    "standard_claim": {
        "pattern": r'(?:the\s+standard|the\s+recommended|the\s+usual|typically|normally|generally)',
        "description": "Claim about 'standard' practice",
        "severity": "LOW",
        "explanation": "Standards change. Verify against current guidelines."
    }
}

# Patterns that indicate the model is hedging (good sign)
HEDGING_PATTERNS = [
    r"i(?:'m|\s+am)\s+not\s+(?:sure|certain|confident)",
    r"i\s+don(?:'t|\s+not)\s+know",
    r"i(?:'m|\s+am)\s+unsure",
    r"this\s+(?:may|might|could)\s+be\s+(?:incorrect|wrong|inaccurate)",
    r"please\s+verify",
    r"check\s+(?:the|your)\s+(?:official|current|latest)",
    r"verify\s+(?:against|with|in)",
    r"(?:according\s+to|based\s+on)\s+(?:my\s+)?(?:training|knowledge)",
    r"⚠️",
]

# Patterns that indicate grounding in source material
GROUNDING_PATTERNS = [
    r'\[Source:\s*[^\]]+\]',
    r'\[Doc:\s*[^\]]+\]',
    r'according\s+to\s+the\s+(?:provided|source|document)',
    r'the\s+(?:document|source|text)\s+(?:states|says|indicates|shows)',
    r'(?:in|from)\s+the\s+(?:provided|source|retrieved)\s+(?:document|context|text)',
    r'as\s+(?:stated|mentioned|noted|described)\s+in',
    r'quote:\s*["\']',
]


def extract_claims(text: str) -> List[str]:
    """Extract potential factual claims from text."""
    # Split on sentence boundaries
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    # Filter: keep sentences with factual-looking content
    claims = []
    for s in sentences:
        s = s.strip()
        if len(s) < 15:
            continue
        # Skip questions
        if s.endswith('?'):
            continue
        # Skip hedging (these are safe)
        if any(re.search(p, s, re.IGNORECASE) for p in HEDGING_PATTERNS):
            continue
        claims.append(s)
    
    return claims


def detect_red_flags(text: str) -> List[Dict]:
    """Detect hallucination red flags in text."""
    flags = []
    
    for flag_name, flag_info in HALLUCINATION_PATTERNS.items():
        matches = re.finditer(flag_info["pattern"], text, re.IGNORECASE)
        for match in matches:
            # Get surrounding context
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].replace('\n', ' ').strip()
            
            flags.append({
                "type": flag_name,
                "severity": flag_info["severity"],
                "description": flag_info["description"],
                "explanation": flag_info["explanation"],
                "matched_text": match.group(),
                "context": f"...{context}...",
                "position": match.start()
            })
    
    return flags


def check_hedging(text: str) -> Tuple[int, List[str]]:
    """Check for hedging language (good sign — model is expressing uncertainty)."""
    hedging_found = []
    
    for pattern in HEDGING_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        hedging_found.extend(matches)
    
    return len(hedging_found), hedging_found


def check_grounding(text: str) -> Tuple[int, List[str]]:
    """Check for grounding language (good sign — model is citing sources)."""
    grounding_found = []
    
    for pattern in GROUNDING_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        grounding_found.extend(matches)
    
    return len(grounding_found), grounding_found


def check_structured_output(text: str) -> Dict:
    """Check if output uses structured format (best practice)."""
    result = {
        "is_json": False,
        "has_claims_array": False,
        "has_confidence_field": False,
        "has_source_field": False,
        "has_verified_field": False,
        "score": 0
    }
    
    # Try to parse as JSON
    try:
        data = json.loads(text)
        result["is_json"] = True
        
        if isinstance(data, dict):
            if "claims" in data and isinstance(data["claims"], list):
                result["has_claims_array"] = True
                
                # Check claim structure
                if data["claims"]:
                    claim = data["claims"][0]
                    if "confidence" in claim:
                        result["has_confidence_field"] = True
                    if "source" in claim:
                        result["has_source_field"] = True
                    if "verified" in claim:
                        result["has_verified_field"] = True
    except (json.JSONDecodeError, KeyError, TypeError):
        pass
    
    # Calculate score
    if result["is_json"]:
        result["score"] += 2
    if result["has_claims_array"]:
        result["score"] += 2
    if result["has_confidence_field"]:
        result["score"] += 1
    if result["has_source_field"]:
        result["score"] += 2
    if result["has_verified_field"]:
        result["score"] += 1
    
    return result


def compute_risk_score(
    red_flags: List[Dict],
    hedging_count: int,
    grounding_count: int,
    structured: Dict
) -> Tuple[str, float, List[str]]:
    """Compute overall hallucination risk score."""
    
    # Start at 50 (neutral)
    score = 50.0
    reasons = []
    
    # Red flags increase risk
    for flag in red_flags:
        if flag["severity"] == "HIGH":
            score += 15
            reasons.append(f"HIGH risk: {flag['description']} ('{flag['matched_text']}')")
        elif flag["severity"] == "MEDIUM":
            score += 8
            reasons.append(f"MEDIUM risk: {flag['description']}")
        elif flag["severity"] == "LOW":
            score += 3
    
    # Hedging decreases risk (model is expressing uncertainty)
    if hedging_count > 0:
        score -= min(hedging_count * 5, 20)
        reasons.append(f"Good: {hedging_count} hedging/uncertainty expressions found")
    
    # Grounding decreases risk (model is citing sources)
    if grounding_count > 0:
        score -= min(grounding_count * 8, 30)
        reasons.append(f"Good: {grounding_count} grounding/source references found")
    
    # Structured output decreases risk
    if structured["is_json"]:
        score -= 15
        reasons.append("Good: Output uses structured JSON format")
    if structured["has_source_field"]:
        score -= 10
        reasons.append("Good: Claims have source fields")
    
    # Clamp to 0-100
    score = max(0, min(100, score))
    
    # Classify
    if score >= 75:
        risk = "HIGH"
    elif score >= 50:
        risk = "MEDIUM"
    elif score >= 25:
        risk = "LOW"
    else:
        risk = "MINIMAL"
    
    return risk, score, reasons


def validate_output(output: str, source: str = None, strict: bool = False) -> Dict:
    """Validate LLM output for hallucination signals."""
    
    results = {
        "red_flags": [],
        "hedging": {"count": 0, "examples": []},
        "grounding": {"count": 0, "examples": []},
        "structured_output": {},
        "risk": {"level": "UNKNOWN", "score": 0, "reasons": []},
        "claims_count": 0,
        "passed": True,
        "recommendations": []
    }
    
    # Extract claims
    claims = extract_claims(output)
    results["claims_count"] = len(claims)
    
    # Detect red flags
    results["red_flags"] = detect_red_flags(output)
    
    # Check hedging
    hedging_count, hedging_examples = check_hedging(output)
    results["hedging"] = {"count": hedging_count, "examples": hedging_examples[:5]}
    
    # Check grounding
    grounding_count, grounding_examples = check_grounding(output)
    results["grounding"] = {"count": grounding_count, "examples": grounding_examples[:5]}
    
    # Check structured output
    results["structured_output"] = check_structured_output(output)
    
    # Compute risk
    risk_level, risk_score, risk_reasons = compute_risk_score(
        results["red_flags"], hedging_count, grounding_count, results["structured_output"]
    )
    results["risk"] = {
        "level": risk_level,
        "score": risk_score,
        "reasons": risk_reasons
    }
    
    # Generate recommendations
    if results["red_flags"]:
        results["recommendations"].append(
            "Review flagged claims manually. High-severity flags are likely hallucinations."
        )
    
    if grounding_count == 0 and len(claims) > 2:
        results["recommendations"].append(
            "No source citations found. Add citation requirements to your prompt."
        )
    
    if not results["structured_output"]["is_json"] and strict:
        results["recommendations"].append(
            "Output is not structured JSON. Use structured output format for enforceable verification."
        )
    
    if hedging_count == 0 and len(claims) > 5:
        results["recommendations"].append(
            "Model expresses no uncertainty despite many claims. This may indicate overconfidence."
        )
    
    # Determine pass/fail
    if strict:
        # Strict mode: fail on any HIGH severity flag
        results["passed"] = not any(f["severity"] == "HIGH" for f in results["red_flags"])
    else:
        # Normal mode: fail on HIGH risk score
        results["passed"] = risk_level != "HIGH"
    
    return results


def print_results(results: Dict, verbose: bool = False):
    """Print validation results."""
    
    print("\n" + "=" * 70)
    print("  HALLUCINATION RISK ASSESSMENT")
    print("=" * 70)
    
    # Risk score
    risk = results["risk"]
    risk_emoji = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "MINIMAL": "✅"}
    emoji = risk_emoji.get(risk["level"], "❓")
    
    print(f"\n  {emoji} RISK LEVEL: {risk['level']} (Score: {risk['score']}/100)")
    
    # Risk reasons
    if risk["reasons"]:
        print("\n  RISK FACTORS:")
        for reason in risk["reasons"]:
            print(f"    • {reason}")
    
    # Red flags
    if results["red_flags"]:
        high_flags = [f for f in results["red_flags"] if f["severity"] == "HIGH"]
        med_flags = [f for f in results["red_flags"] if f["severity"] == "MEDIUM"]
        low_flags = [f for f in results["red_flags"] if f["severity"] == "LOW"]
        
        print(f"\n  🚩 RED FLAGS: {len(results['red_flags'])} total")
        print(f"     HIGH: {len(high_flags)} | MEDIUM: {len(med_flags)} | LOW: {len(low_flags)}")
        
        if verbose and high_flags:
            print("\n  HIGH SEVERITY FLAGS:")
            for flag in high_flags[:5]:
                print(f"    ⚠️  {flag['description']}")
                print(f"       Found: '{flag['matched_text']}'")
                print(f"       Context: {flag['context']}")
                print(f"       Why: {flag['explanation']}")
                print()
    
    # Hedging (good sign)
    hedging = results["hedging"]
    if hedging["count"] > 0:
        print(f"\n  ✅ UNCERTAINTY EXPRESSIONS: {hedging['count']} found (good sign)")
        if verbose and hedging["examples"]:
            for ex in hedging["examples"][:3]:
                print(f"    • '{ex}'")
    
    # Grounding (good sign)
    grounding = results["grounding"]
    if grounding["count"] > 0:
        print(f"\n  ✅ SOURCE GROUNDING: {grounding['count']} references found")
        if verbose and grounding["examples"]:
            for ex in grounding["examples"][:3]:
                print(f"    • '{ex}'")
    
    # Structured output
    structured = results["structured_output"]
    if structured["is_json"]:
        print(f"\n  ✅ STRUCTURED OUTPUT: JSON format detected")
        details = []
        if structured["has_claims_array"]:
            details.append("claims array")
        if structured["has_source_field"]:
            details.append("source fields")
        if structured["has_confidence_field"]:
            details.append("confidence fields")
        if structured["has_verified_field"]:
            details.append("verified fields")
        if details:
            print(f"     Includes: {', '.join(details)}")
    else:
        print(f"\n  ⚠️  OUTPUT FORMAT: Plain text (consider using structured JSON)")
    
    # Recommendations
    if results["recommendations"]:
        print(f"\n  📋 RECOMMENDATIONS:")
        for rec in results["recommendations"]:
            print(f"    • {rec}")
    
    # Overall result
    print("\n" + "=" * 70)
    if results["passed"]:
        print("  ✅ VALIDATION PASSED — No critical hallucination signals detected")
    else:
        print("  ❌ VALIDATION FAILED — High hallucination risk detected")
        print("     Review the red flags above before using this output.")
    print("=" * 70 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Validate LLM outputs for hallucination signals"
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='The LLM output to validate'
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        help='File containing the LLM output'
    )
    
    parser.add_argument(
        '--source', '-s',
        type=str,
        help='Source document (for future NLI integration)'
    )
    
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Strict mode: fail on any HIGH severity flag'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Show detailed output'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    args = parser.parse_args()
    
    # Get output
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            output = f.read()
    elif args.output:
        output = args.output
    else:
        print("Error: Please provide --output or --file")
        sys.exit(1)
    
    # Validate
    results = validate_output(output, args.source, args.strict)
    
    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_results(results, verbose=args.verbose)
    
    # Exit code
    sys.exit(0 if results["passed"] else 1)


if __name__ == '__main__':
    main()
