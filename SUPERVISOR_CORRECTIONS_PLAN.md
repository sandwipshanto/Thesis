# Supervisor Corrections Implementation Plan
**Thesis:** Bangla-English Code-Mixed LLM Jailbreaking Research  
**Date Created:** December 2024  
**Deadline:** December 20, 2025  
**Status:** Planning Phase - Awaiting Approval

---

## Overview

This document provides a systematic plan to address 8 major structural and formatting issues identified by the thesis supervisor. The corrections are categorized by complexity and required effort, with a recommended implementation order.

**Reference Standard:** DeepAQNet thesis (Md Sadman Hafiz) - demonstrates proper academic thesis writing with narrative paragraphs, minimal bullet points, and appropriate structure.

---

## Issue Summary & Priority Classification

### HIGH PRIORITY (Structural/Content Changes - 80% of work)
- **Issue #4:** Convert bullet points to narrative paragraphs throughout thesis
- **Issue #5:** Integrate appendices A/B/C into chapters 1-9
- **Issue #8:** Add Research Objectives section
- **Issue #7:** Restructure Chapter 1 (Introduction)

### MEDIUM PRIORITY (Quality Improvements - 15% of work)
- **Issue #6:** Shorten figure captions (move details to main text)
- **Issue #2:** Fix inconsistent page numbering in front matter

### LOW PRIORITY (Simple Fixes - 5% of work)
- **Issue #1:** Change "Authors" to "Submitted by" on title page
- **Issue #3:** Add signature lines to Ethical Statement

---

## Detailed Issue Breakdown

### Issue #1: Title Page Label Change
**Complexity:** ⭐ (Very Simple)  
**Estimated Time:** 2 minutes  
**Files Affected:** `latex/chapters/00_titlepage.tex`

**Current State:**
```latex
Line 36: {\fontsize{13}{16}\selectfont\bfseries Authors\par}
```

**Required Change:**
```latex
Line 36: {\fontsize{13}{16}\selectfont\bfseries Submitted by\par}
```

**Implementation:**
- Single string replacement in line 36
- No dependencies

**Reference:** DeepAQNet uses "Authors:" label (line ~20) - supervisor prefers "Submitted by"

---

### Issue #2: Page Numbering Consistency
**Complexity:** ⭐⭐ (Simple - LaTeX Technical)  
**Estimated Time:** 15 minutes  
**Files Affected:** `latex/thesis.tex`, potentially front matter chapter files

**Problem:**
- Duplicate or inconsistent page numbering in front matter sections
- Front matter should use lowercase roman numerals (i, ii, iii, iv...)
- Main matter should use arabic numerals (1, 2, 3...)
- Issue: Multiple `\pagenumbering{roman}` commands or missing `\setcounter{page}{1}`

**Investigation Required:**
1. Examine `latex/thesis.tex` for all `\pagenumbering{}` commands
2. Check which front matter files manually set page numbers
3. Verify TOC, LOF, LOT page references

**Expected Solution:**
```latex
% Front matter section in thesis.tex
\pagenumbering{roman}
\setcounter{page}{1}
\include{chapters/00_titlepage}    % Page i
\include{chapters/01_declaration}  % Page ii
% ... etc

% Main matter section
\mainmatter
\pagenumbering{arabic}
\setcounter{page}{1}
\include{chapters/chapter1_introduction}  % Page 1
```

**Reference:** DeepAQNet shows proper numbering: Roman (i-xv) → Arabic (1-54)

---

### Issue #3: Signature Lines in Ethical Statement
**Complexity:** ⭐⭐ (Simple - LaTeX Formatting)  
**Estimated Time:** 10 minutes  
**Files Affected:** `latex/chapters/06_ethical_statement.tex`

**Current State:**
- Text-only ethical statement without signature spaces
- Needs space for author signatures and dates

**Required Addition:**
```latex
% At end of ethical statement content
\vspace{2cm}

\noindent
\begin{minipage}{0.45\textwidth}
\rule{0.8\textwidth}{0.4pt}\\
\textbf{Your Name}\\
Registration No: XXXXXXX\\
Date: \underline{\hspace{3cm}}
\end{minipage}
\hfill
\begin{minipage}{0.45\textwidth}
\rule{0.8\textwidth}{0.4pt}\\
\textbf{Co-author Name (if applicable)}\\
Registration No: XXXXXXX\\
Date: \underline{\hspace{3cm}}
\end{minipage}
```

**Reference:** DeepAQNet Ethical Statement has signature blocks for both authors (page vii)

---

### Issue #4: Convert Bullet Points to Narrative Paragraphs
**Complexity:** ⭐⭐⭐⭐⭐ (Very Complex - Major Rewriting)  
**Estimated Time:** 8-12 hours  
**Files Affected:** All chapter files (chapter1-9 + abstract)

**Problem Analysis:**
Current thesis extensively uses:
- `\begin{itemize}...\end{itemize}` - Unordered bullet lists
- `\begin{enumerate}...\end{enumerate}` - Numbered lists

**Examples from reconnaissance:**

**Chapter 1 (Introduction):**
```latex
Lines 12-16: \begin{itemize} with 4 bullet points about motivation
Lines 30-35: \begin{enumerate} with 4 numbered research questions
Lines 46-51: More \begin{itemize} for contributions
```

**Abstract:**
```latex
Lines 11-19: \begin{enumerate} with 6 "Key Contributions"
```

**Acceptable vs Unacceptable Bullet Usage:**

✅ **KEEP bullets for:**
- Research Questions (RQ1-RQ4) - standard academic format
- Novel Contributions list (acceptable in intro/conclusion)
- Code listings in appendices/methodology

❌ **CONVERT to paragraphs:**
- Motivation sections
- Background explanations
- Methodology descriptions
- Results discussions
- Literature review summaries
- Abstract content (CRITICAL - abstracts should NEVER have bullet points)

**Conversion Strategy:**

1. **Abstract (HIGHEST PRIORITY):**
   ```latex
   BEFORE:
   \subsection*{Key Contributions}
   \begin{enumerate}
       \item First Bangla-specific study...
       \item Custom phonetic perturbations...
       \item Tokenization mechanism validation...
   \end{enumerate}
   
   AFTER:
   This research makes several novel contributions to LLM security research. 
   First, it presents the first systematic investigation of Bangla-English 
   code-mixed jailbreaking attacks, addressing a vulnerability affecting 230 
   million speakers. Second, it develops custom phonetic perturbation strategies 
   tailored to Bangla romanization patterns... [continue flowing narrative]
   ```

2. **Chapter 1 - Motivation:**
   - Current: 4 bullet points listing motivation factors
   - Convert to: 1-2 flowing paragraphs explaining the research gap
   - Model after DeepAQNet's "Motivation and Research Problem" section (lines 201-240)

3. **Systematic Approach (per chapter):**
   - Identify all `\begin{itemize}` and `\begin{enumerate}` blocks
   - Categorize: Keep (RQs/contributions) vs Convert (everything else)
   - Rewrite using transition words: "First,", "Additionally,", "Furthermore,", "Moreover,"
   - Use topic sentences to introduce each idea
   - Maintain logical flow between paragraphs

**Chapter-by-Chapter Breakdown:**

| Chapter | Current Bullet Blocks (Estimate) | Conversion Priority |
|---------|----------------------------------|---------------------|
| Abstract | 1 enumerate (6 items) | CRITICAL - Do first |
| Chapter 1 | 5+ blocks (~20 items) | HIGH - Introduction |
| Chapter 2 | 3-4 blocks (~15 items) | HIGH - Background |
| Chapter 3 | 2-3 blocks (~10 items) | MEDIUM - Methodology |
| Chapter 4 | 2-3 blocks (~10 items) | MEDIUM - Experiments |
| Chapter 5 | 3-4 blocks (~15 items) | HIGH - Results |
| Chapter 6-9 | 2-3 blocks each (~30 total) | MEDIUM-LOW |

**Quality Checklist (Per Conversion):**
- [ ] Maintains original technical accuracy
- [ ] Uses proper academic transition words
- [ ] Each paragraph has clear topic sentence
- [ ] Ideas flow logically without abrupt jumps
- [ ] Removes redundant "firstly, secondly, thirdly" if not needed
- [ ] Preserves all citations and technical details

**Reference Example (DeepAQNet Abstract - Lines 93-115):**
Notice how it describes 6+ contributions as flowing narrative paragraphs, NOT bullet points:
```
"Although smartphones have emerged as... Our study focuses on Dhaka... 
we've developed a Deep Convolutional Neural Network... The model's ability 
to operate... Tests show it outperforms... We utilised LIME and GRAD-CAM..."
```

---

### Issue #5: Integrate Appendices into Chapters
**Complexity:** ⭐⭐⭐⭐ (Complex - Structural Reorganization)  
**Estimated Time:** 3-4 hours  
**Files Affected:** 
- `latex/chapters/appendix_a.tex` (Prompts)
- `latex/chapters/appendix_b.tex` (Statistical Tables)
- `latex/chapters/appendix_c.tex` (Code Samples)
- `latex/chapters/chapter3_methodology.tex`
- `latex/chapters/chapter4_experimental_setup.tex`
- `latex/chapters/chapter5_results.tex`
- `latex/thesis.tex` (remove appendix includes)

**Current Structure:**
```
Thesis.tex includes:
- Chapters 1-9 (main content)
- Appendix A: Prompt Examples
- Appendix B: Statistical Tables
- Appendix C: Code Implementations
```

**Recommended Integration:**

**Appendix A (Prompts) → Chapter 4 (Experimental Setup):**
- Move to new subsection: "4.X Sample Prompt Examples"
- Location: After methodology description, before results
- Rationale: Prompts are part of experimental design

**Appendix B (Statistical Tables) → Chapter 5 (Results):**
- Distribute tables to relevant results sections
- Example: AASR/AARR detailed tables → "5.X Detailed Model Performance Metrics"
- Keep only essential tables in main text
- Consider: Create supplementary materials document for extensive tables (if university allows)

**Appendix C (Code Samples) → Multiple Locations:**
- Critical code snippets → Chapter 3 (Methodology) subsection "3.X Implementation Details"
- Data processing code → Chapter 4 (Experimental Setup)
- Evaluation code → Chapter 5 (Results)
- Alternative: If code is extensive, keep as appendix but justify in text why it's separated

**Implementation Steps:**

1. **Phase 1: Content Audit (30 mins)**
   - Read all three appendix files completely
   - Categorize each section by logical chapter placement
   - Identify redundant content (already mentioned in chapters)

2. **Phase 2: Chapter Integration (2 hours)**
   - Create new subsections in target chapters
   - Copy-paste content from appendices
   - Add transition text to integrate smoothly
   - Update cross-references (e.g., "See Appendix A" → "As shown in Section 4.3")

3. **Phase 3: Cleanup (1 hour)**
   - Remove appendix includes from `thesis.tex`
   - Update Table of Contents structure
   - Verify all figure/table references still work
   - Check for orphaned citations

4. **Phase 4: Justification (30 mins)**
   - If keeping any appendix, add justification in relevant chapter
   - Example: "Due to space constraints, complete code implementations are provided in Appendix C"

**Verification Checklist:**
- [ ] No orphaned references to "Appendix A/B/C"
- [ ] All tables/figures have proper captions in new locations
- [ ] Chapter subsections remain logically ordered
- [ ] Page count doesn't balloon excessively (if it does, condense)
- [ ] All code snippets have proper syntax highlighting

**Reference:** DeepAQNet has NO separate appendices - all content integrated into 8 chapters

---

### Issue #6: Shorten Figure Captions
**Complexity:** ⭐⭐⭐ (Medium - Requires Judgment)  
**Estimated Time:** 2-3 hours  
**Files Affected:** All chapter files with figures

**Problem:**
- Current captions are overly verbose (multiple sentences, detailed explanations)
- Proper format: Caption = concise label, Details = main text discussion

**Current Style (Example):**
```latex
\caption{AASR and AARR scores across all 180 experimental configurations showing 
that code-mixed prompts (CM) achieved 68\% effectiveness while code-mixed with 
phonetic perturbations (CMP) reached 72\% effectiveness, demonstrating that 
Bangla-specific romanization patterns significantly improve jailbreak success 
rates compared to English baseline (12\%) when tested on GPT-4o-mini, 
Llama-3-8B, Gemma-1.1-7B, and Mistral-7B models.}
```

**Proper Style (What Supervisor Wants):**
```latex
\caption{AASR and AARR scores across 180 experimental configurations}

% Then in main text BEFORE the figure:
Figure~\ref{fig:aasr_comparison} presents the AASR and AARR scores across all 
180 experimental configurations. Code-mixed prompts (CM) achieved 68\% 
effectiveness, while code-mixed with phonetic perturbations (CMP) reached 72\% 
effectiveness. This demonstrates that Bangla-specific romanization patterns 
significantly improve jailbreak success rates compared to the English 
baseline (12\%) across GPT-4o-mini, Llama-3-8B, Gemma-1.1-7B, and Mistral-7B.
```

**Guidelines:**
- **Caption length:** 1 line preferred, max 2 lines
- **Caption content:** Figure type + key variables shown
- **Main text:** Full interpretation, comparisons, implications
- **Format:** `\caption{Brief description}` OR `\caption[Short]{Long version for LOF}`

**Implementation Strategy:**

1. **Identify all figures** (use grep_search for `\begin{figure}`)
2. **For each figure:**
   - Extract current caption
   - Write concise version (5-10 words)
   - Move details to paragraph BEFORE `\begin{figure}` environment
   - Ensure main text references figure explicitly: `Figure~\ref{fig:label} shows...`

3. **Template for Main Text Discussion:**
   ```latex
   % Paragraph introducing the figure (BEFORE figure environment)
   We analyze the attack success rates across different prompt types in 
   Figure~\ref{fig:aasr_results}. [Detailed explanation of what reader should 
   observe, trends, comparisons, implications - 3-5 sentences]
   
   \begin{figure}[htbp]
       \centering
       \includegraphics[width=0.8\textwidth]{images/aasr_results.png}
       \caption{Attack success rates by prompt type}
       \label{fig:aasr_results}
   \end{figure}
   
   % Optional: Additional interpretation AFTER figure if needed
   These results confirm our hypothesis that...
   ```

**Quality Checklist (Per Figure):**
- [ ] Caption is ≤2 lines
- [ ] Caption describes WHAT is shown, not WHY it's important
- [ ] Main text paragraph exists BEFORE figure placement
- [ ] Main text explicitly references figure: `Figure~\ref{...}`
- [ ] All interpretation/analysis moved to main text
- [ ] Figure still makes sense if read independently

**Reference Example (DeepAQNet Figure 2.1, Line ~145):**
```latex
\caption{Radiance: The Total Light Captured by a Smartphone Camera [36].}
```
Notice: Concise, descriptive, citation in caption. Details in main text.

---

### Issue #7: Restructure Chapter 1 (Introduction)
**Complexity:** ⭐⭐⭐⭐ (Complex - Content Reorganization)  
**Estimated Time:** 2-3 hours  
**Files Affected:** `latex/chapters/chapter1_introduction.tex`

**Current Structure (INCORRECT):**
```latex
\chapter{Introduction}
\section{Motivation}           % ← PROBLEM: Starts with Motivation
    [4 bullet points]
\section{Background}
    [Multiple bullet lists]
\section{Research Gap}
\section{Research Questions}
    [RQ1-RQ4 enumeration - OK to keep]
\section{Novel Contributions}
    [6 bullet points]
\section{Thesis Organization}
```

**Required Structure (Based on DeepAQNet Standard):**
```latex
\chapter{Introduction}
\section{Overview}                    % ← NEW: Broad context first
    [1-2 paragraphs: What is the general problem domain?]

\section{Motivation and Research Problem}  % ← MERGE: Combine motivation + problem
    [2-3 paragraphs: Why does this problem matter? What are consequences?]
    [Convert current 4 motivation bullets to narrative]

\section{Research Objectives}         % ← NEW: Issue #8 - Add objectives
    [See Issue #8 for details]

\section{Research Questions}          % ← KEEP: But rename if needed
    [RQ1-RQ4 - Can keep enumeration, this is standard]

\section{Organization of the Thesis}  % ← KEEP: Standard closing section
    [1 paragraph describing chapter-by-chapter structure]
```

**Implementation Steps:**

**Step 1: Create "Overview" Section (30 mins)**
- Extract 1-2 sentences from current Introduction that provide broadest context
- Model after DeepAQNet lines 201-208:
  ```
  "Millions of fatalities are attributed to poor air quality... The need for 
  accessible and reliable monitoring... This thesis focuses on developing..."
  ```
- For our thesis:
  ```
  "Large language models (LLMs) have transformed human-computer interaction, 
  yet their safety mechanisms remain vulnerable to adversarial attacks. This 
  research investigates a novel attack vector: Bangla-English code-mixed 
  jailbreaking, affecting 230 million speakers in an underexplored linguistic 
  context."
  ```

**Step 2: Merge Motivation + Research Problem (1 hour)**
- Current "Motivation" section has 4 bullets - convert to 2-3 paragraphs
- Structure:
  - **Paragraph 1:** Global context (LLM safety importance, existing vulnerabilities)
  - **Paragraph 2:** Language-specific gap (Code-mixing attacks, Bangla underrepresented)
  - **Paragraph 3:** Specific problem statement (Tokenization exploitation, safety filter bypass)
- Reference DeepAQNet lines 209-240 for narrative flow

**Step 3: Move Background Content (if needed)**
- If current "Background" is too detailed, consider moving to Chapter 2
- Introduction background should be high-level (2-3 paragraphs max)
- Deep technical background belongs in Literature Review

**Step 4: Convert Contributions Bullets (1 hour)**
- Current: 6 enumerated contributions
- Option A: Keep enumeration (acceptable for contributions - see Issue #4)
- Option B: Convert to 2 paragraphs if supervisor insists
  - Paragraph 1: Methodological contributions (prompt design, perturbations)
  - Paragraph 2: Empirical contributions (findings, tokenization analysis)

**Step 5: Update Thesis Organization (15 mins)**
- Ensure it reflects final chapter structure
- Use present tense: "Chapter 2 presents...", "Chapter 3 describes..."
- Keep to 1 paragraph with 2-sentence descriptions per chapter max

**Verification Checklist:**
- [ ] No section starts with bullet points
- [ ] Overview provides immediate context (what/why)
- [ ] Motivation flows naturally into research gap
- [ ] Objectives clearly stated (see Issue #8)
- [ ] Research questions logically follow objectives
- [ ] Organization section matches actual TOC

**Reference:** DeepAQNet Chapter 1 structure (lines 201-265) - follow this model exactly

---

### Issue #8: Add Research Objectives Section
**Complexity:** ⭐⭐⭐ (Medium - New Content Creation)  
**Estimated Time:** 1-2 hours  
**Files Affected:** `latex/chapters/chapter1_introduction.tex`

**Problem:**
- Current thesis has Research Questions (RQ1-RQ4) but NO explicit Objectives
- Objectives = What you aim to accomplish (action-oriented)
- Research Questions = What you want to answer (inquiry-oriented)
- Both are needed in academic thesis

**Relationship:**
```
Objectives (WHAT you'll do) → Research Questions (WHAT you'll answer) → Methodology (HOW you'll do it)
```

**Recommended Objectives (Based on RQs):**

Since we have RQ1-RQ4, create 4 corresponding objectives:

```latex
\section{Research Objectives}

This research aims to achieve the following objectives:

\textbf{Objective 1: Develop and Validate Bangla-English Code-Mixed Attack Prompts}
This study develops a systematic methodology for creating Bangla-English code-mixed 
and phonetically perturbed prompts targeting LLM safety mechanisms. The objective 
is to establish whether code-mixing strategies, previously validated for Hindi-English, 
can be effectively adapted to Bangla's unique romanization and phonetic patterns.

\textbf{Objective 2: Identify Bangla-Specific Linguistic Patterns}
We aim to characterize the specific phonetic perturbations and romanization conventions 
that enable successful jailbreak attacks in Bangla. This includes analyzing which 
transliteration choices and spelling variations most effectively fragment tokens and 
bypass content filters.

\textbf{Objective 3: Assess Cross-Model Vulnerability Consistency}
This research evaluates the vulnerability of major LLMs (GPT-4o-mini, Llama-3-8B, 
Gemma-1.1-7B, Mistral-7B) to Bangla-English code-mixed attacks across varying 
temperatures and jailbreak templates. The objective is to determine whether 
Bangla-based attacks represent a universal vulnerability or model-specific weakness.

\textbf{Objective 4: Validate Tokenization as Attack Mechanism}
We aim to empirically verify that tokenization fragmentation, as proposed by 
Aswal & Jaiswal (2025) for Hinglish, serves as the underlying mechanism for 
Bangla jailbreak success. This involves analyzing token-level representations 
and their correlation with attack success rates.
```

**Alternative Format (If Supervisor Prefers Numbered List):**

```latex
\section{Research Objectives}

The primary objectives of this research are:

\begin{enumerate}
    \item \textbf{Develop Bangla-English Attack Methodology:} Create systematic 
    prompt transformation pipeline adapting Hindi-English code-mixing strategies 
    to Bangla's linguistic features.
    
    \item \textbf{Characterize Bangla Attack Patterns:} Identify phonetic and 
    romanization features that maximize jailbreak effectiveness.
    
    \item \textbf{Evaluate Cross-Model Vulnerabilities:} Test 4 major LLMs across 
    180 configurations to assess universal vulnerability.
    
    \item \textbf{Validate Tokenization Mechanism:} Confirm token fragmentation 
    as root cause through empirical analysis.
\end{enumerate}
```

**Placement:**
- **Location:** After "Motivation and Research Problem", BEFORE "Research Questions"
- **Rationale:** Objectives state your goals → RQs specify what you'll investigate → Methodology explains how

**Reference:** DeepAQNet Section 1.3 "Research Objective" (lines 245-260)
- Uses bullet points for 3 objectives (shows bullets ARE acceptable here)
- Each objective starts with action verb: "Creation of...", "To develop...", "To clarify..."
- Our thesis should mirror this structure

**Verification Checklist:**
- [ ] 4 objectives map to 4 research questions
- [ ] Each objective uses action-oriented language ("develop", "identify", "assess", "validate")
- [ ] Objectives are specific and measurable
- [ ] Placement: After Motivation, Before RQs
- [ ] Consistent formatting (all bold, all numbered, etc.)

---

## Implementation Timeline

### Phase 1: Quick Wins (Day 1 - 30 mins total)
**Goal:** Complete simple fixes to build momentum

1. ✅ Issue #1: Title page "Submitted by" (2 mins)
2. ✅ Issue #3: Signature lines (10 mins)
3. ✅ Issue #2: Page numbering investigation (15 mins)
   - If simple fix → complete
   - If complex → defer to Phase 4

**Deliverable:** Title page and ethical statement corrected

---

### Phase 2: High-Impact Structural Changes (Days 2-3 - 6 hours total)
**Goal:** Address major structural issues that affect entire thesis

**Day 2 (3 hours):**
4. ✅ Issue #8: Add Research Objectives section (1.5 hours)
   - Draft 4 objectives based on RQs
   - Place in Chapter 1 before RQs
   
5. ✅ Issue #7: Restructure Chapter 1 Introduction (1.5 hours)
   - Create Overview section
   - Merge Motivation + Research Problem
   - Integrate new Objectives section
   - Keep RQs, update Organization

**Day 3 (3 hours):**
6. ✅ Issue #5: Integrate Appendices (3 hours)
   - Audit all three appendices
   - Move Appendix A → Chapter 4
   - Move Appendix B → Chapter 5
   - Distribute Appendix C → Chapters 3-5
   - Update thesis.tex includes
   - Fix cross-references

**Deliverable:** Restructured introduction + integrated appendices

---

### Phase 3: Content Conversion (Days 4-6 - 10 hours total)
**Goal:** Convert bullet points to narrative paragraphs

**Priority Order:**
1. ✅ Abstract (1 hour) - CRITICAL, supervisor will read first
2. ✅ Chapter 1 remaining bullets (1.5 hours)
3. ✅ Chapter 2 Background bullets (1.5 hours)
4. ✅ Chapter 5 Results bullets (2 hours)
5. ✅ Chapter 3 Methodology bullets (1.5 hours)
6. ✅ Chapter 4 Experiments bullets (1 hour)
7. ✅ Chapters 6-9 remaining bullets (1.5 hours)

**Strategy:**
- Convert 2-3 chapters per day
- Use DeepAQNet as reference for academic writing style
- Maintain all technical accuracy
- Read aloud to check flow

**Deliverable:** Fully narrative thesis (except RQs/contributions where bullets acceptable)

---

### Phase 4: Polish & Quality Assurance (Day 7 - 3 hours total)
**Goal:** Refine formatting and ensure consistency

7. ✅ Issue #6: Shorten figure captions (2 hours)
   - Identify all figures (grep search)
   - Shorten captions to 1-2 lines
   - Move details to main text paragraphs
   - Verify all figures referenced in text

8. ✅ Issue #2: Finalize page numbering (if deferred) (30 mins)

9. ✅ Final compilation and review (30 mins)
   - Compile PDF (2 passes for TOC)
   - Check page count (should remain ~100-110 pages)
   - Verify TOC, LOF, LOT correctness
   - Proofread front matter

**Deliverable:** Final corrected PDF ready for supervisor review

---

### Total Estimated Time: 20-22 hours (spread over 7 days)

**Realistic Schedule:**
- **Weekend work:** Phases 1-2 (6.5 hours)
- **Weekday evenings (3 days):** Phase 3 (10 hours @ ~3.5 hrs/day)
- **Final weekend:** Phase 4 polish (3 hours)

**Buffer:** Build in 2-3 extra days for unforeseen issues

---

## Risk Assessment & Mitigation

### Risk 1: Bullet Conversion Changes Meaning
**Likelihood:** Medium  
**Impact:** High  
**Mitigation:**
- Keep original files in backup folder
- Convert in small batches, compile PDF after each chapter
- Read aloud to verify clarity maintained
- Have co-author review converted sections

### Risk 2: Appendix Integration Breaks References
**Likelihood:** Medium  
**Impact:** Medium  
**Mitigation:**
- Search for all "Appendix A/B/C" references before moving content
- Use find-replace carefully
- Compile PDF frequently to catch broken references early
- Keep appendix files temporarily (don't delete until verified)

### Risk 3: Page Count Explosion
**Likelihood:** Low  
**Impact:** Medium  
**Mitigation:**
- Narrative paragraphs may be more concise than bullets
- If page count increases >10%, condense some detailed sections
- Use supplementary materials for extensive tables/code (check university policy)

### Risk 4: Time Underestimation
**Likelihood:** High (common in thesis work)  
**Impact:** High  
**Mitigation:**
- Start with Phase 1 immediately upon plan approval
- Set daily targets (e.g., "Convert 2 chapters today")
- If falling behind, prioritize: Abstract → Chapter 1 → Chapter 5 are most visible
- Communicate with supervisor if timeline needs adjustment

### Risk 5: Inconsistent Academic Voice
**Likelihood:** Medium  
**Impact:** Medium  
**Mitigation:**
- Keep DeepAQNet thesis open while writing for style reference
- Use standard academic transition phrases
- Avoid conversational tone (no "we can see that...", use "Figure X demonstrates...")
- Final proofread specifically for voice consistency

---

## Quality Assurance Checklist

### Pre-Implementation
- [ ] All 8 issues clearly understood
- [ ] DeepAQNet reference thesis reviewed
- [ ] Backup of all LaTeX files created
- [ ] Git commit created (if using version control)
- [ ] Co-author (if any) aware of changes

### During Implementation
- [ ] Compile PDF after each major change
- [ ] Check TOC updates correctly
- [ ] Verify no broken references (??  warnings)
- [ ] Page numbers increment logically
- [ ] Figures/tables still render correctly

### Post-Implementation (Before Supervisor Review)
- [ ] All 8 issues addressed
- [ ] Abstract has ZERO bullet points
- [ ] Chapter 1 structure matches DeepAQNet model
- [ ] Research Objectives section exists
- [ ] No standalone appendices (or justified if kept)
- [ ] Figure captions concise (≤2 lines)
- [ ] Page numbering: Roman (i-xv) → Arabic (1-~100)
- [ ] "Submitted by" on title page
- [ ] Signature lines in ethical statement
- [ ] Total page count 100-120 (not excessive)
- [ ] PDF compiled successfully (no errors)
- [ ] Proofread for typos introduced during changes
- [ ] All citations still correctly formatted

### Final Verification
- [ ] Print first 20 pages, check formatting
- [ ] Read Abstract + Chapter 1 aloud for flow
- [ ] Verify all RQs addressed in thesis
- [ ] Check table/figure numbering consistency
- [ ] Confirm deadline: December 20, 2025

---

## Success Criteria

**Thesis will be considered ready for submission when:**

1. ✅ **Structure:** Matches academic standard (DeepAQNet model)
2. ✅ **Abstract:** Pure narrative, no bullet points
3. ✅ **Introduction:** Overview → Motivation → Objectives → RQs → Organization
4. ✅ **Content:** Narrative paragraphs (except RQs/contributions where acceptable)
5. ✅ **Formatting:** Consistent page numbering, concise captions, proper signatures
6. ✅ **Integration:** All essential appendix content in appropriate chapters
7. ✅ **Compilation:** Generates error-free PDF with correct TOC/LOF/LOT
8. ✅ **Accuracy:** All technical claims from previous corrections preserved

**Supervisor should observe:**
- Professional academic writing style throughout
- Clear logical flow without bullet-point crutches
- Proper thesis structure following departmental norms
- All required front matter elements present and correct

---

## Approval & Next Steps

**Plan Status:** ⏳ Awaiting User Approval

**Questions for User (Before Implementation):**

1. **Objectives Format:** Do you prefer paragraph format or numbered list for Research Objectives? (Both are acceptable - see DeepAQNet uses bullets, we proposed both options)

2. **Appendix Integration:** Should we:
   - A) Integrate ALL appendices into chapters (recommended)
   - B) Keep some appendices if they're supplementary only (e.g., extensive code)
   - C) Create separate "Supplementary Materials" document (check with supervisor/university)

3. **Timeline Preference:**
   - Fast track (7 days intensive work)
   - Moderate pace (10-14 days with breaks)
   - Deadline-driven (work backwards from December 20)

4. **Review Checkpoints:**
   - Should I pause after each Phase for your review?
   - Or proceed through all phases and present final draft?

5. **Contribution Bullets:**
   - Keep enumerated list for Novel Contributions (standard in CS)
   - Or convert to paragraphs (harder to scan, but more "academic")

**Once approved, implementation begins with Phase 1 (Quick Wins).**

---

## Appendix: Example Conversions

### Example A: Abstract Key Contributions (Before/After)

**BEFORE (Current - Lines 11-19 in abstract):**
```latex
\subsection*{Key Contributions}
\begin{enumerate}
    \item First systematic investigation of Bangla-English code-mixed jailbreaking
    \item Custom phonetic perturbation strategies for Bangla romanization
    \item Evaluation across 4 major LLMs with 180 configurations
    \item Tokenization mechanism validation through empirical analysis
    \item Novel Sandbox jailbreak template development
    \item Responsible disclosure framework for Bangla vulnerabilities
\end{enumerate}
```

**AFTER (Supervisor's Expected Format):**
```latex
This research makes several significant contributions to LLM security. First, it 
presents the first systematic investigation of Bangla-English code-mixed jailbreaking 
attacks, addressing a critical vulnerability affecting 230 million speakers who have 
been underrepresented in prior security research. Second, we develop custom phonetic 
perturbation strategies specifically tailored to Bangla romanization patterns, 
demonstrating that language-specific adaptations significantly enhance attack 
effectiveness (68-72\% AASR compared to 12\% English baseline). Third, through 
comprehensive evaluation across four major LLMs (GPT-4o-mini, Llama-3-8B, Gemma-1.1-7B, 
Mistral-7B) spanning 180 experimental configurations, we establish that Bangla 
code-mixing represents a universal vulnerability rather than model-specific weakness. 
Fourth, we empirically validate that tokenization fragmentation serves as the underlying 
attack mechanism, consistent with patterns observed in Hindi-English attacks. Additionally, 
we introduce a novel Sandbox jailbreak template for resilience testing and develop a 
responsible disclosure framework appropriate for low-resource language vulnerabilities.
```

### Example B: Chapter 1 Motivation Section (Before/After)

**BEFORE (Current with bullets):**
```latex
\section{Motivation}
\begin{itemize}
    \item LLM safety mechanisms focus primarily on English, leaving code-mixed languages vulnerable
    \item 230 million Bangla speakers lack representation in adversarial research
    \item Code-mixing enables tokenization exploitation through romanization
    \item Responsible disclosure requires language-specific vulnerability assessment
\end{itemize}
```

**AFTER (Narrative paragraphs):**
```latex
\section{Motivation and Research Problem}

Large language models have transformed natural language processing, yet their safety 
mechanisms exhibit systematic biases toward English-language inputs. Recent research 
by Aswal and Jaiswal (2025) demonstrated that Hindi-English code-mixed prompts achieve 
significantly higher jailbreak success rates through tokenization fragmentation, raising 
critical questions about multilingual vulnerability patterns. However, this research 
focused exclusively on Hindi, leaving other major South Asian languages unexplored.

Bangla represents a particularly critical gap in LLM security research. With 230 million 
speakers globally and widespread use of romanized script in digital communication 
(Banglish), this language community faces potential vulnerabilities that remain 
uncharacterized. The unique phonetic features of Bangla, combined with non-standardized 
romanization conventions, create opportunities for adversarial exploitation distinct 
from Hindi-English patterns. Understanding whether code-mixing attacks generalize across 
Indic languages or require language-specific adaptations has important implications for 
developing robust multilingual safety mechanisms.

This research addresses these gaps by investigating Bangla-English code-mixed jailbreaking 
as an independent attack vector. By developing Bangla-specific phonetic perturbations and 
evaluating their effectiveness across major LLM architectures, we aim to characterize the 
tokenization vulnerabilities affecting this underrepresented linguistic community and 
contribute to more inclusive AI safety research.
```

---

**End of Plan Document**
