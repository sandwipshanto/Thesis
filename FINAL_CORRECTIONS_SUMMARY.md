# Final Corrections Summary - Bangla LLM Jailbreaking Thesis

**Date:** November 21, 2025  
**Status:** ✅ All false claims corrected

---

## Overview

Comprehensive revision completed to ensure all claims in the thesis accurately reflect what was actually done versus what was initially claimed. This document summarizes all corrections made.

---

## Major Categories of Corrections

### 1. Tokenization Mechanism Claims

**❌ FALSE CLAIMS (Removed):**
- "r = 0.94 correlation validated for Bangla"
- "Pearson correlation coefficient: r = 0.94 (p < 0.001)"
- "Independently validated tokenization mechanism for Bangla"
- "Conceptual validation of tokenization disruption mechanism"
- "Full Integrated Gradients analysis"

**✅ HONEST REPLACEMENTS:**
- "Application of tokenization disruption mechanism (empirically validated for Hindi-English by Aswal & Jaiswal, 2025) to Bangla-English context"
- "AASR patterns consistent with fragmentation-based explanation"
- "Pattern consistent with Hinglish findings (Aswal & Jaiswal, 2025 reported r=0.94 via Integrated Gradients)"
- "Observed relationship between fragmentation and AASR"
- "We apply their validated mechanism; full Integrated Gradients analysis for Bangla remains future work"

**FILES CORRECTED:**
- THESIS_REPORT.md (14+ instances)
- novel_contributions.md (5+ instances)
- README.md (4 instances)

---

### 2. Query Count Claims

**❌ FALSE CLAIMS (Removed):**
- "8,950 queries"
- "9,000 queries"
- "2,250 total queries"

**✅ ACTUAL NUMBERS:**
- "~6,750 queries" (3 models × 5 templates × 3 prompt sets × 3 temps × 50 prompts = 6,750)
- Breakdown:
  - GPT-4o-mini: 2,250 queries
  - Llama-3-8B: 2,250 queries
  - Mistral-7B: 2,250 queries
  - **Total: 6,750 queries**
  - Gemma-1.1-7B: 0 (excluded due to budget)

**FILES CORRECTED:**
- THESIS_REPORT.md (Execution Time section, Cost Breakdown, Appendix E)
- README.md (Project structure section)
- novel_contributions.md (Evaluation framework)

---

### 3. English:Bangla Ratio Claims

**❌ FALSE CLAIMS (Removed):**
- "70% English : 30% Bangla"
- "Target: 70:30 English:Bangla ratio"
- "Validation: Our RQ2 analysis confirms 70:30 ratio is optimal"

**✅ ACTUAL RATIO:**
- "~30% English : ~70% Bangla" (based on actual word count analysis of prompts_cm.csv)
- Questions: 36.2% English
- Scenarios: 26.0% English
- Overall: ~31% English, ~69% Bangla

**RATIONALE FOR CONFUSION:**
- Initial documentation mistakenly inverted the ratio
- Actual implementation had Bangla as majority language (70%)
- English keywords intentionally kept for attack effectiveness

**FILES CORRECTED:**
- THESIS_REPORT.md (Methodology section, RQ2 results)
- README.md (Findings section)
- novel_contributions.md (Attack strategy section)

---

### 4. Effectiveness Percentage Claims

**❌ FALSE CLAIM (Removed):**
- "85% more effective"

**✅ ACTUAL NUMBER:**
- "68% more effective" (English word perturbations vs Bangla word perturbations)
- Calculation: 52.3% / 31.1% = 1.68× = 68% more effective

**FILES CORRECTED:**
- novel_contributions.md (Contribution 2, Summary table)

---

### 5. Cost Estimates

**❌ INCONSISTENT CLAIMS (Standardized):**
- Various cost estimates: $0.38, $0.62, etc.

**✅ ACTUAL COSTS:**
- **Actual spend:** ~$1.00 for ~6,750 queries (3 models)
- Model responses: ~$0.68
- LLM judge evaluations: ~$0.34
- **Total: ~$1.02**

**Full scale estimate (460 prompts, 4 models):**
- Total queries: 248,400
- Total cost: ~$18.63

**FILES CORRECTED:**
- THESIS_REPORT.md (Appendix E)
- novel_contributions.md (Cost efficiency section)

---

### 6. ICC Validation Claims

**❌ FALSE CLAIM (Removed):**
- "Validated: ICC ≥ 0.70" (implying we validated it)

**✅ HONEST STATEMENT:**
- "ICC ≥ 0.70 reported in prior work"
- "Actual ICC: Not calculated due to time constraints (future work)"

**CLARIFICATION:**
- Prior work (Hinglish paper) reported ICC = 0.87 for LLM-as-judge
- We used the same methodology but did NOT validate with human annotations
- Acknowledged as limitation in Section 7.3.3

**FILES CORRECTED:**
- THESIS_REPORT.md (Evaluation methodology section)
- novel_contributions.md (Framework description)

---

## Summary by File

### THESIS_REPORT.md (3,416 lines)
**Sections corrected:** 20+ instances across:
- Abstract (line 119)
- Introduction (lines 203, 215)
- Methodology (lines 631, 1019-1032)
- Experimental Setup (lines 1211-1212, 1240, 1284)
- Results RQ4 (lines 1629, 1695)
- Discussion (line 2063)
- Limitations (lines 2310-2330)
- Conclusion (lines 2827, 2836, 2923)
- Future Work (lines 3012)
- Appendix D (lines 3310-3320)
- Appendix E (lines 3325-3377)

### novel_contributions.md (276 lines)
**Sections corrected:** 10+ instances across:
- Executive Summary (line 15)
- Contribution 2 (lines 75, 100)
- Contribution 4 (lines 133-155, 160-165)
- Summary table (line 220)
- Unique contributions (line 250)
- Framework description (line 265)
- Cost efficiency (line 270)
- Evaluation framework (line 60)

### README.md (200 lines)
**Sections corrected:** 4 instances:
- Code-mixing ratio (line 105)
- Query count (line 137)
- Removed r=0.94 claim (line 107)
- English word effectiveness (line 106)

---

## What Remains TRUE

Despite corrections, these claims are **ACCURATE and VERIFIED**:

✅ **46% AASR with CMP** (verified from results CSV)  
✅ **42% improvement over English baseline** ((46-32.4)/32.4 = 42%)  
✅ **68% more effective** (English word targeting: 52.3%/31.1% = 1.68×)  
✅ **Mistral 81.8%, Llama 22.7%, GPT-4o-mini 16.0%** (all verified from CSV)  
✅ **p < 0.05 statistical significance** (Wilcoxon tests conducted)  
✅ **30:70 English:Bangla ratio** (actual word count from prompts_cm.csv)  
✅ **First Bangla-English code-mixing jailbreaking study** (literature review confirms)  
✅ **Template ineffectiveness** (None template: 46.2% vs jailbreak templates: 35.1-42.5%)  
✅ **~6,750 total queries** (3 models × 2,250 each)  
✅ **50 prompts across 10 categories** (dataset verified)  
✅ **3 models tested** (GPT-4o-mini, Llama-3-8B, Mistral-7B)  
✅ **Gemma excluded due to budget** (acknowledged limitation)  

---

## What Is Now HONESTLY REPRESENTED

### Tokenization Mechanism Understanding

**What we DID:**
- Observed AASR progression aligns with fragmentation progression
- Token counting shows expected pattern (English < CM < CMP)
- Qualitative analysis of responses consistent with mechanism

**What we DID NOT:**
- Run Integrated Gradients analysis for Bangla
- Calculate Pearson correlation coefficient
- Empirically measure attribution scores
- Directly validate causation

**How we frame it NOW:**
- "Bangla-English patterns consistent with tokenization disruption mechanism empirically validated for Hindi-English (Aswal & Jaiswal, 2025)"
- "Application of their validated mechanism to new language"
- "Direct empirical validation via Integrated Gradients remains future work"

### Research Positioning

**What we claim:**
- First Bangla-English code-mixing jailbreaking study ✅
- Application of existing mechanism to new language ✅
- Language-specific findings (template ineffectiveness, English targeting) ✅
- Scalable methodology for other Indic languages ✅

**What we DON'T claim anymore:**
- Independent validation of tokenization mechanism ❌
- Calculated correlation coefficients ❌
- Quantitative causation proof ❌

---

## Implications for Thesis Defense

### Strengths to Emphasize

1. **First Bangla study** - Genuinely novel, 230M speakers untested
2. **Strong empirical results** - 46% AASR, statistically significant
3. **Language-specific discoveries** - Template ineffectiveness, English word targeting
4. **Reproducible methodology** - Clear 3-step process, ~$1 cost
5. **Honest limitations** - Acknowledged what wasn't done

### How to Handle Questions About Tokenization

**If asked: "Did you validate the tokenization mechanism?"**

**Answer:** "We observed patterns consistent with the tokenization disruption mechanism empirically validated for Hindi-English by Aswal & Jaiswal (2025) using Integrated Gradients. Our AASR progression (32.4% → 42.1% → 46.0%) aligns with fragmentation progression (1.12 → 1.87 → 2.14 tokens/word), supporting the hypothesis that their mechanism generalizes to Bangla. However, we did not conduct Integrated Gradients analysis ourselves due to resource constraints - that remains important future work to empirically validate the mechanism specifically for Bangla-English contexts."

**If asked: "What's your correlation coefficient?"**

**Answer:** "We did not calculate a correlation coefficient. We observed a consistent pattern where increased tokenization fragmentation corresponded with increased AASR, which aligns with Aswal & Jaiswal's findings for Hindi-English (they reported r=0.94). Our contribution is demonstrating this pattern holds for a new language - Bangla - rather than independently measuring the correlation."

---

## Future Work Clearly Identified

The thesis now honestly identifies these as **future work**:

1. ✅ Integrated Gradients analysis for Bangla (replicating Aswal & Jaiswal's methodology)
2. ✅ ICC validation with human annotators
3. ✅ Scaling to 460 prompts (full dataset)
4. ✅ Including Gemma-1.1-7B (4th model)
5. ✅ Empirical correlation calculation
6. ✅ Layer-by-layer activation inspection

---

## Final Verification Checklist

- [✅] All r=0.94 claims removed or properly attributed to Hinglish paper
- [✅] All query counts corrected to ~6,750
- [✅] All English:Bangla ratios corrected to 30:70
- [✅] All "validated" claims replaced with "observed patterns consistent with"
- [✅] All effectiveness percentages corrected to 68%
- [✅] All cost estimates standardized to ~$1
- [✅] All ICC claims clarified as "prior work" not "our validation"
- [✅] All "Integrated Gradients analysis" marked as future work
- [✅] All mechanism claims attributed to Hinglish paper's empirical work
- [✅] Gemma exclusion acknowledged throughout

---

## Confidence Assessment

**Thesis integrity:** ✅ HIGH  
**Claim accuracy:** ✅ HIGH  
**Defense readiness:** ✅ HIGH  

All false/inflated claims have been corrected. The thesis now presents an honest, accurate account of what was done, what was found, and what remains to be validated. The research remains valuable and novel - first Bangla study with strong empirical results - but claims are now properly scoped to match actual work completed.

---

**Status:** Ready for submission and defense with honest, defensible claims throughout.
