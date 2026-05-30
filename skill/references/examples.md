# Hallucination Examples & Detection Patterns

Concrete examples of hallucinations, why they slip past guardrails, and how to catch them.

---

## Example 1: Fabricated Academic Citation

### The Hallucination
> "According to Smith et al. (2024) in Nature Machine Intelligence, transformer models 
> exhibit a 47% reduction in hallucination when using chain-of-thought prompting."

### Why It Slips Past Guardrails
- Looks perfectly formatted (author, year, journal)
- The statistic (47%) sounds plausible
- The journal exists and is prestigious
- CoT does reduce hallucinations, so the claim seems reasonable

### How to Catch It
1. **Citation verification:** Search Google Scholar for "Smith et al. 2024 Nature Machine Intelligence hallucination chain-of-thought" — this paper does not exist
2. **Statistical red flag:** Precise percentages (47%) without a source are suspicious
3. **Structured output check:** If using JSON format, the "source" field would be null or fabricated

### Correct Response
> "Chain-of-thought prompting has been shown to reduce hallucinations in several studies. 
> A 2023 study by Wei et al. at Google Research found significant improvements. 
> However, I cannot provide an exact percentage without verifying the specific paper. 
> Please search Google Scholar for the latest results."

---

## Example 2: Confident Medical Misinformation

### The Hallucination
> "The recommended dosage of metformin for Type 2 diabetes is 500mg twice daily, 
> taken with meals. This is the standard first-line treatment per the 2024 ADA guidelines."

### Why It Slips Past Guardrails
- Metformin IS a first-line treatment for Type 2 diabetes (true)
- 500mg is a real dosage (but not the only one)
- ADA guidelines do exist and are authoritative
- The statement sounds medically accurate

### How to Catch It
1. **Dosage verification:** The standard starting dose is actually 500mg once or twice daily, 
   but the maximum dose is 2550mg/day. The statement is oversimplified and potentially dangerous.
2. **Guideline verification:** Check the actual 2024 ADA Standards of Care — the specific 
   dosage recommendation may differ.
3. **Safety check:** Medical dosages MUST be verified against the actual source document, 
   not the model's memory.

### Correct Response
> "Metformin is commonly used as a first-line treatment for Type 2 diabetes. 
> Per the ADA Standards of Care, typical starting doses range from 500mg to 1000mg daily. 
> However, dosing is individualized based on kidney function, tolerance, and other factors. 
> ⚠️ Please verify the specific dosage with a qualified clinician or the current ADA guidelines."

---

## Example 3: Plausible But Wrong Technical API

### The Hallucination
> "To read a specific sheet from an Excel file in pandas, use:
> `df = pd.read_excel('file.xlsx', sheet_number=2)`"

### Why It Slips Past Guardrails
- `pd.read_excel()` is a real function
- It does accept a sheet parameter
- The parameter name `sheet_number` LOOKS correct
- The code will actually run without error (it's silently ignored)

### How to Catch It
1. **API verification:** Check the official pandas documentation — the correct parameter is 
   `sheet_name`, not `sheet_number`
2. **Silent failure:** The code runs but reads the FIRST sheet (default), not sheet 2
3. **Test execution:** Running this code and checking the output would reveal the error

### Correct Response
> "To read a specific sheet from an Excel file in pandas, use:
> `df = pd.read_excel('file.xlsx', sheet_name='Sheet2')` 
> or `sheet_name=1` (0-indexed) for the second sheet.
> Verify against: https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html"

---

## Example 4: Historical Fact Confabulation

### The Hallucination
> "The Treaty of Westphalia was signed in 1648, ending the Thirty Years' War. 
> It established the principle of cuius regio, eius religio, which gave rulers 
> the right to determine the religion of their state."

### Why It Slips Past Guardrails
- The Treaty of Westphalia WAS signed in 1648 (true)
- It DID end the Thirty Years' War (true)
- Cuius regio, eius religio IS a real principle (true)
- BUT: This principle was established by the Peace of Augsburg (1555), NOT Westphalia

### How to Catch It
1. **Fact cross-referencing:** The claim mixes two related but distinct historical events
2. **Source verification:** Check the actual text of the Treaty of Westphalia
3. **Domain knowledge:** A historian would immediately recognize this conflation

### Correct Response
> "The Treaty of Westphalia (1648) ended the Thirty Years' War and established 
> principles of state sovereignty and non-interference. The principle of 
> cuius regio, eius religio was actually established earlier by the Peace of 
> Augsburg (1555). Would you like more details on either treaty?"

---

## Example 5: Statistic From Thin Air

### The Hallucination
> "Studies show that 73% of remote workers report higher productivity compared 
> to office-based workers."

### Why It Slips Past Guardrails
- Sounds like a real statistic
- The topic (remote work productivity) is widely studied
- 73% is specific enough to sound researched
- No citation required by the prompt

### How to Catch It
1. **Source demand:** Ask "Which studies? Provide the source."
2. **Statistical suspicion:** Precise percentages without sources are red flags
3. **Verification:** Search for the actual study — it doesn't exist in this form

### Correct Response
> "Research on remote work productivity shows mixed results. Some studies find 
> increased productivity, while others find no significant difference or decreases. 
> I don't have a specific statistic to cite. Would you like me to summarize the 
> general findings from recent research?"

---

## Example 6: Hallucinated Quote

### The Hallucination
> "As Albert Einstein once said, 'The definition of insanity is doing the same 
> thing over and over and expecting different results.'"

### Why It Slips Past Guardrails
- This quote is widely attributed to Einstein (but he never said it)
- It sounds like something a genius would say
- It's been repeated so often it's become "common knowledge"

### How to Catch It
1. **Quote verification:** Check Quote Investigator or reliable quote databases
2. **Attribution check:** Einstein's actual writings don't contain this quote
3. **Red flag:** "As X once said" is a common hallucination pattern for misattributed quotes

### Correct Response
> "This quote is widely attributed to Albert Einstein, but there is no evidence 
> he actually said or wrote it. The earliest known appearance is from a 1981 
> Narcotics Anonymous pamphlet. Would you like the actual source?"

---

## Example 7: Code With Invented Package

### The Hallucination
> "To validate JSON schemas in Python, install the `jsonschema-validator` package:
> `pip install jsonschema-validator`"

### Why It Slips Past Guardrails
- `jsonschema` IS a real package (but the name is wrong)
- The invented name sounds plausible
- The function described is real

### How to Catch It
1. **Package verification:** Check PyPI — `jsonschema-validator` does not exist
2. **Name similarity:** The real package is `jsonschema` (no `-validator` suffix)
3. **Install test:** Running `pip install jsonschema-validator` will fail

### Correct Response
> "To validate JSON schemas in Python, use the `jsonschema` package:
> `pip install jsonschema`
> Documentation: https://python-jsonschema.readthedocs.io/"

---

## Example 8: The "Almost Right" Hallucination

### The Hallucination
> "The Python `requests` library was created by Kenneth Reitz and first released 
> in 2011. It is licensed under the Apache License 2.0."

### Why It Slips Past Guardrails
- Kenneth Reitz DID create requests (true)
- It WAS first released in 2011 (true)
- But it's licensed under the Apache License 2.0 — FALSE, it's actually MIT licensed

### How to Catch It
1. **License verification:** Check the actual LICENSE file in the requests repository
2. **Red flag:** Most claims are true, making the false one harder to spot
3. **Systematic checking:** Every claim must be verified, not just the suspicious ones

### Correct Response
> "The Python `requests` library was created by Kenneth Reitz and first released 
> in 2011. It is licensed under the MIT License. 
> Source: https://github.com/psf/requests/blob/main/LICENSE"

---

## Detection Patterns (Red Flags)

### Language Red Flags
| Pattern | Risk | Example |
|---|---|---|
| Precise percentages without source | High | "73% of users report..." |
| "Studies show" without citation | High | "Studies show that..." |
| "As X once said" | Medium | Often misattributed |
| "It is well-known that" | Medium | May not be well-known |
| "The standard approach is" | Medium | May be outdated or wrong |
| Very specific numbers | Medium | "The company has 1,247 employees" |

### Structural Red Flags
| Pattern | Risk | Example |
|---|---|---|
| No citations in factual response | High | Claims without sources |
| All claims marked "HIGH" confidence | Medium | Overconfident model |
| No caveats or limitations | Medium | Real answers have nuances |
| Suspiciously complete answer | Medium | Real knowledge has gaps |
| Perfect formatting of citations | Low | May be fabricated to look real |

### Domain-Specific Red Flags
| Domain | Red Flag | Why |
|---|---|---|
| Legal | Case citation in perfect format | Models fabricate these |
| Medical | Specific dosage without source | Dangerous if wrong |
| Code | Parameter name that "looks right" | May be silently wrong |
| Academic | Author + Year + Journal combo | Common fabrication pattern |
| Financial | Specific figures without date | May be outdated or invented |

---

## How to Use These Examples

1. **For testing:** Use these examples to test your guardrails. If your system lets any 
   of these through, your guardrails need strengthening.

2. **For training:** Show these examples to your team so they recognize hallucination patterns.

3. **For prompt engineering:** Use the "Correct Response" examples as few-shot examples 
   in your prompts to teach the model how to handle uncertainty.

4. **For validation:** Use the "How to Catch It" patterns to build automated checks.
