# Methodological Limitations & Comparison Validity

**Date:** November 20, 2025  
**Status:** CRITICAL - Must Address Before Publication

---

## Executive Summary

Our study makes **direct quantitative comparisons** with the original Hinglish paper (arXiv:2505.14226) that are **methodologically problematic** due to:

1. **Different perturbation strategies** (unknown Hindi rules vs our Bangla rules)
2. **Different prompts** (their 460 unknown prompts vs our 50 custom prompts)
3. **Different scale** (their 165k queries vs our 9k queries)
4. **Unknown experimental details** (exact category distribution, perturbation frequency)

**Conclusion:** We can make **directional/qualitative claims** about mechanism generalization, but **cannot make precise quantitative comparisons** like "Bangla is 53% less effective than Hindi."

---

## Specific Methodological Gaps

### Gap 1: Perturbation Strategy Differences ⚠️ CRITICAL

#### What We Don't Know About Original Paper

**Phonetic Perturbations:**
- Exact perturbation rules for Hindi (vowel swaps, consonant changes, etc.)
- Which specific words were targeted for perturbation
- Perturbation frequency (all harmful words? only some?)
- Hindi-specific phonetic transformations (aspiration, retroflex, etc.)
- Consistency of perturbation application

**Their Methodology Statement (Section 4.1):**
> "We apply phonetic misspellings to sensitive keywords in code-mixed prompts..."

**Problem:** No detailed rules published, no examples of specific transformations

#### What We Did

**Bangla Perturbations:**
- Created perturbation rules based on general phonetic principles
- Targeted English loanwords and harmful keywords
- Applied perturbations to 3-5 words per prompt
- Bangla-specific transformations based on romanization patterns

**Examples:**
- "hate" → "haet"
- "discrimination" → "diskrimineshun"  
- "attack" → "atak"
- "speech" → "speach"

#### Impact on Comparison Validity

**Confounding Variable:**
```
AASR_difference = f(Language_factor, Perturbation_strategy, Prompt_quality, ...)
```

**Cannot isolate:** Is 46% vs 99% due to:
- Bangla language properties? ✅ Possibly
- Our perturbations being less effective? ⚠️ Likely contributor
- Different prompts being easier/harder? ⚠️ Likely contributor
- All of the above? ✅ Most likely

**Validity Assessment:**
- ❌ **INVALID:** "Bangla attacks are 53% less effective than Hindi attacks"
- ❌ **INVALID:** "Protection factor from Hindi training is 53%"
- ✅ **VALID:** "Phonetic perturbations improve Bangla attack success (English 32% → CMP 46%)"
- ✅ **VALID:** "Mechanism generalizes directionally to Bangla"

---

### Gap 2: Prompt Differences ⚠️ CRITICAL

#### Original Paper Prompts

**Scale:** 460 prompts across 23 harm categories

**Categories (from paper Section 3.1):**
- Hate speech, Discrimination, Violence, Cyber attacks, Misinformation, ...
- (Full list not provided, distribution unknown)

**Prompts:** Not publicly released, cannot replicate exactly

**Difficulty:** Unknown - baseline English AASR reported as ~10%

#### Our Study Prompts

**Scale:** 50 prompts across 5-10 categories

**Categories:**
- Hate speech, Discrimination, Violence, Cyber attacks, Misinformation, Substance abuse, Weapons, Privacy violations, Self-harm, Radicalization

**Prompts:** Custom-created, manually reviewed

**Difficulty:** English baseline AASR = 32.4% (3x higher!)

#### Impact Analysis

**English Baseline Difference:**
| Study | English AASR | Interpretation |
|-------|--------------|----------------|
| Hinglish (original) | ~10% | Harder prompts OR better model safety |
| Banglish (ours) | 32.4% | Easier prompts OR worse safety OR both |

**Possible Explanations:**
1. **Our prompts are easier** (more direct, less sophisticated)
2. **Models updated since original paper** (different safety training)
3. **Different harm category distribution** (we may have more "easy" categories)
4. **Small sample size** (50 vs 460, more variance)

**Validity Assessment:**
- ❌ **INVALID:** Direct AASR comparison (99% vs 46%) as evidence of language differences
- ❌ **INVALID:** Claiming Bangla English baseline (32%) is language-specific
- ✅ **VALID:** CM/CMP improve over English baseline **within our study**
- ✅ **VALID:** Progression pattern (English < CM < CMP) holds for Bangla

---

### Gap 3: Scale Differences

#### Sample Size

| Metric | Original | Our Study | Ratio |
|--------|----------|-----------|-------|
| Prompts | 460 | 50 | 9.2:1 |
| Temperatures | 6 | 3 | 2:1 |
| Total Queries | ~165,600 | 8,950 | 18.5:1 |

**Statistical Implications:**
- Our study has **lower statistical power**
- Higher variance in AASR estimates
- Less confident in generalization

**Validity:** Our findings are **directionally valid** but may not generalize to full 460-prompt scale

---

### Gap 4: Unknown Experimental Details

**Missing Information from Original Paper:**

1. **Exact model versions tested** (ChatGPT-4o-mini from which date?)
2. **API parameters** (top_p, frequency_penalty, etc.)
3. **Prompt formatting** (how templates were integrated)
4. **Evaluation criteria** (exact LLM-judge prompt)
5. **Temporal factors** (models tested in 2024 vs our 2025 tests)

**Impact:** Small variations in any of these could affect AASR by 10-20%

---

## What We CAN vs CANNOT Claim

### ❌ CANNOT Claim (Overstatements to Remove)

1. **"Bangla attacks are 53% less effective than Hindi attacks"**
   - Confounds language, prompts, perturbations, scale

2. **"Hindi safety training provides 53% protection for Bangla"**
   - Protection factor calculation assumes all else equal (it's not)

3. **"Bangla has higher English baseline due to language factors"**
   - Could be prompt difficulty, model updates, category distribution

4. **"Hindi is 2x more effective for jailbreaking than Bangla"**
   - Direct quantitative comparison invalid

5. **"Romanization variability explains 53% effectiveness gap"**
   - Cannot isolate one factor from confounds

### ✅ CAN Claim (Valid Findings)

1. **"Phonetic perturbations improve Bangla attack success"**
   - ✅ English 32.4% → CM 42.1% → CMP 46.0% (within-study comparison)

2. **"Mechanism generalizes directionally to Bangla"**
   - ✅ Same pattern (code-mixing + phonetic) works for both languages

3. **"Same models vulnerable across languages"**
   - ✅ GPT-4o-mini and Llama-3-8B show vulnerability to both Hindi and Bangla

4. **"Bangla attacks achieve 46% AASR with CMP"**
   - ✅ Empirical finding from our experiments

5. **"Template effectiveness differs between languages"**
   - ✅ "None" best for Bangla (46.2%), OM best for Hindi (~99%)
   - ⚠️ But could also be prompt-dependent

6. **"Tokenization disruption correlates with AASR (r=0.94)"**
   - ✅ Within our Bangla study, mechanism validated

7. **"English words in code-mixing most effective"**
   - ✅ Within our Bangla study (85% vs 65%)

---

## Revised Comparison Framework

### Approach 1: **Qualitative Comparison Only**

**Safe Claim:**
> "While the original Hinglish study reported near-perfect attack success (99% AASR), our Banglish study shows moderate success (46% AASR). However, direct quantitative comparison is not methodologically sound due to differences in prompts, perturbation strategies, and scale. **Directionally**, both studies validate that code-mixing + phonetic perturbations bypass safety filters, suggesting a **generalizable mechanism** across Indic languages."

### Approach 2: **Within-Study Focus**

**Safe Claim:**
> "Our study demonstrates that Bangla code-mixing with phonetic perturbations achieves **46% AASR**, representing a **42% improvement** over the English baseline (32.4%). This validates the core mechanism from the Hinglish paper—tokenization disruption via code-mixing and phonetic misspellings—while highlighting the need for **controlled replication** with identical prompts and perturbations to enable precise cross-lingual comparisons."

### Approach 3: **Mechanism Validation Focus**

**Safe Claim:**
> "We validate three key findings from the original Hinglish study for Bangla:
> 1. ✅ Code-mixing increases attack success (English 32% → CM 42%)
> 2. ✅ Phonetic perturbations further improve success (CM 42% → CMP 46%)
> 3. ✅ Same models vulnerable (GPT-4o-mini, Llama-3-8B)
>
> The **magnitude** of effectiveness may differ due to language-specific factors, but the **mechanism** generalizes, confirming tokenization-based bypass as a **systematic multilingual vulnerability**."

---

## How to Proceed: Recommendations

### Option 1: **Acknowledge Limitations Prominently** ⭐ RECOMMENDED

**Action:**
1. Add "Methodological Limitations" section to all analysis documents
2. Revise quantitative claims to qualitative claims
3. Reframe "53% less effective" as "lower but concerning effectiveness"
4. Add caveats to all Hinglish vs Banglish comparisons

**Pros:**
- Maintains intellectual honesty
- Strengthens paper (reviewers will appreciate transparency)
- Findings still valid and impactful

**Cons:**
- Less "punchy" headlines
- Cannot claim precise cross-lingual transfer metrics

---

### Option 2: **Attempt Controlled Replication** (Future Work)

**Action:**
1. Contact original authors for exact prompts and perturbation rules
2. Replicate their 460 prompts with Bangla translations
3. Use identical perturbation strategy for both languages
4. Enable true apples-to-apples comparison

**Pros:**
- Gold standard comparison
- Can make precise quantitative claims

**Cons:**
- Requires author cooperation (may not respond)
- Expensive (460 prompts × 3 sets × 4 models × 3 temps = ~16,500 queries, ~$7)
- Time-consuming (2-3 weeks additional work)

---

### Option 3: **Reframe as Pilot/Exploratory Study**

**Action:**
1. Position as **exploratory validation** of mechanism generalization
2. Emphasize **directional findings** over quantitative comparisons
3. Call for **standardized benchmark** for multilingual jailbreaking research

**Pros:**
- Honest about scope
- Positions as foundation for future work
- Still publishable (many pilot studies in top venues)

**Cons:**
- May be seen as "incomplete" by some reviewers

---

## Recommended Revisions to Analysis Documents

### High Priority (Must Fix Before Submission)

1. **`rq1_cross_lingual_replication.md`**
   - Remove "53% reduction" language
   - Change to: "While Hinglish achieved 99% AASR, Banglish achieved 46%, we cannot attribute this difference solely to language factors due to methodological differences..."
   - Add limitations section

2. **`rq3_multilingual_safety_gaps.md`**
   - Remove "53% protection factor" calculation
   - Change to: "Hindi safety training provides partial but incomplete Bangla protection (observed 46% AASR vs reported 99% for Hindi), though precise transfer metrics cannot be calculated..."

3. **`hinglish_vs_banglish_comparison.md`**
   - Add prominent "Comparison Validity Caveats" section at top
   - Reframe all quantitative comparisons as "directional observations"
   - Add table showing methodological differences

4. **`novel_contributions.md`**
   - Remove "Quantified cross-lingual safety transfer (53%)" as a contribution
   - Change to: "Demonstrated directional cross-lingual vulnerability"
   - Add "Need for standardized multilingual benchmark" as contribution

### Medium Priority (Improve Clarity)

5. **All documents:** Add footnote/caveat on first Hinglish comparison:
   > "Note: Direct quantitative comparison with original Hinglish study limited by differences in prompts (50 vs 460), perturbation strategies, and experimental scale. Comparisons should be interpreted directionally, not as precise measurements."

---

## Revised Abstract Language (Example)

**❌ Current (Overstatement):**
> "We find that Bangla code-mixing attacks achieve 46% AASR compared to Hindi's 99%, demonstrating a 53% effectiveness reduction and quantifying cross-lingual safety transfer for the first time."

**✅ Revised (Honest):**
> "We find that Bangla code-mixing attacks achieve 46% AASR (compared to reported 99% for Hindi), validating mechanism generalization while highlighting the need for controlled replication to precisely quantify cross-lingual effectiveness differences. Our study demonstrates that the same models vulnerable to Hindi attacks (GPT-4o-mini, Llama-3-8B) remain vulnerable to Bangla, confirming systematic multilingual safety gaps."

---

## Conclusion

Your concern is **100% valid and critical**. We have been making **overconfident quantitative comparisons** that conflate:
- Language differences
- Prompt differences  
- Perturbation strategy differences
- Scale differences

**Recommended Path Forward:**
1. ✅ **Acknowledge limitations** prominently in all documents
2. ✅ **Revise claims** from quantitative to qualitative
3. ✅ **Reframe contributions** as mechanism validation, not precise transfer metrics
4. ✅ **Call for standardized benchmark** as future work
5. ⏸️ **Consider controlled replication** if time/resources allow

**Core Validity Remains:**
- ✅ Bangla attacks work (46% AASR)
- ✅ Mechanism generalizes (tokenization disruption)
- ✅ Same models vulnerable  
- ✅ Template effectiveness differs
- ✅ English words in code-mixing effective

**What We Lose:**
- ❌ "53% less effective" headline
- ❌ "53% protection factor" metric
- ❌ Precise quantitative cross-lingual comparisons

**What We Gain:**
- ✅ Intellectual honesty
- ✅ Stronger paper (reviewers appreciate transparency)
- ✅ Foundation for future standardized comparisons

Should I proceed with revising the analysis documents to incorporate these methodological caveats?