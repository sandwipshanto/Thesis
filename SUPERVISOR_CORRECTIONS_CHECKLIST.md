# Supervisor Corrections Checklist
**Last Updated:** December 2024  
**Status:** Planning Phase Complete - Awaiting Implementation Approval

---

## Quick Reference: 8 Issues to Fix

| # | Issue | Priority | Time | Status |
|---|-------|----------|------|--------|
| 1 | "Authors" → "Submitted by" on title page | LOW | 2 min | ⬜ Not Started |
| 2 | Fix page numbering consistency | MEDIUM | 15 min | ⬜ Not Started |
| 3 | Add signature lines to Ethical Statement | LOW | 10 min | ⬜ Not Started |
| 4 | Convert bullet points → narrative paragraphs | HIGH | 8-12 hrs | ⬜ Not Started |
| 5 | Integrate appendices into chapters | HIGH | 3-4 hrs | ⬜ Not Started |
| 6 | Shorten figure captions | MEDIUM | 2-3 hrs | ⬜ Not Started |
| 7 | Restructure Chapter 1 (Introduction) | HIGH | 2-3 hrs | ⬜ Not Started |
| 8 | Add Research Objectives section | HIGH | 1-2 hrs | ⬜ Not Started |

**Total Estimated Time:** 20-22 hours  
**Target Completion:** 7 days

---

## Phase 1: Quick Wins (30 minutes) ✅ COMPLETED

### Issue #1: Title Page ✅
- [x] Open `latex/chapters/00_titlepage.tex`
- [x] Line 36: Change "Authors" → "Submitted by"
- [x] Compile PDF to verify
- [x] ✅ COMPLETE

### Issue #3: Signature Lines ✅
- [x] Open `latex/chapters/06_ethical_statement.tex`
- [x] Add signature block template at end
- [x] Include: Name, Reg No, Date fields
- [x] Compile PDF to verify
- [x] ✅ COMPLETE

### Issue #2: Page Numbering ✅
- [x] Open `latex/thesis.tex`
- [x] Search for all `\pagenumbering{}` commands
- [x] Verify roman numerals for front matter (i, ii, iii...)
- [x] Verify arabic numerals for main matter (1, 2, 3...)
- [x] Added `\setcounter{page}{1}` to reset page counter
- [x] Compile PDF to verify
- [x] ✅ COMPLETE

**Phase 1 Deliverable:** ✅ Title page and ethical statement corrected, page numbering fixed

---

## Phase 2: Structural Changes (6 hours) ✅ COMPLETED

### Issue #8: Add Research Objectives (1.5 hours) ✅
- [x] Open `latex/chapters/chapter1_introduction.tex`
- [x] Create new `\section{Research Objectives}` after Motivation
- [x] Write 4 objectives mapping to RQ1-RQ4:
  - [x] Objective 1: Develop Bangla attack methodology
  - [x] Objective 2: Identify Bangla linguistic patterns
  - [x] Objective 3: Assess cross-model vulnerability
  - [x] Objective 4: Validate tokenization mechanism
- [x] Used enumerated format (standard for objectives)
- [x] Placed BEFORE Research Questions section
- [x] Compile PDF to verify structure
- [x] ✅ COMPLETE

### Issue #7: Restructure Chapter 1 (1.5 hours) ✅
- [x] Open `latex/chapters/chapter1_introduction.tex`
- [x] Created new structure:
  - [x] `\section{Overview}` - Added 1 paragraph (broad context)
  - [x] `\section{Motivation and Research Problem}` - Merged and converted bullets to 3 narrative paragraphs
  - [x] Converted motivation bullets to flowing narrative
  - [x] `\section{Research Objectives}` - Added with 4 enumerated objectives
  - [x] `\section{Research Questions}` - Kept RQ1-RQ4 (enumerated)
  - [x] `\section{Organization of the Thesis}` - Kept existing
- [x] Removed old separate sections
- [x] Referenced DeepAQNet style for narrative flow
- [x] Compile PDF to verify flow
- [x] ✅ COMPLETE

### Issue #5: Integrate Appendices (3 hours) ✅

**Step 1: Content Audit (30 mins)** ✅
- [x] Read `latex/chapters/appendix_a.tex` completely
- [x] Read `latex/chapters/appendix_b.tex` completely
- [x] Read `latex/chapters/appendix_c.tex` completely
- [x] Documented content placement

**Step 2: Appendix A → Chapter 4 (45 mins)** ✅
- [x] Open `latex/chapters/chapter4_experimental_setup.tex`
- [x] Created subsection: "4.7 Sample Prompts and Transformations"
- [x] Copied relevant prompt examples from Appendix A
- [x] Added transition text to integrate smoothly
- [x] Included model response examples

**Step 3: Appendix B → Chapter 5 (45 mins)** ✅
- [x] Open `latex/chapters/chapter5_results.tex`
- [x] Created section: "5.6 Detailed Statistical Analysis"
- [x] Copied statistical tables from Appendix B
- [x] Ensured tables have proper captions
- [x] Integrated Wilcoxon tests, correlation tables, descriptives, CIs

**Step 4: Appendix C (45 mins)** ✅
- [x] Kept Appendix C as reference (configuration files)
- [x] Justification: Technical configurations are supplementary reference material

**Step 5: Cleanup (15 mins)** ✅
- [x] Open `latex/thesis.tex`
- [x] Commented out appendix A and B includes
- [x] Added comment explaining integration
- [x] Kept Appendix C for configuration reference
- [x] Compile PDF - check TOC updated
- [x] ✅ COMPLETE

**Phase 2 Deliverable:** ✅ Restructured introduction (Overview + Motivation + Objectives + RQs), integrated Appendices A & B into Chapters 4 & 5, reduced page count to 97 pages

---

## Phase 3: Content Conversion (10 hours)

### Issue #4: Convert Bullets to Paragraphs

**Priority 1: Abstract (1 hour)**
- [ ] Open `latex/chapters/08_abstract.tex`
- [ ] Find `\begin{enumerate}` for Key Contributions (lines 11-19)
- [ ] Convert 6 bullet items to flowing 1-2 paragraphs
- [ ] Use transitions: "First,", "Second,", "Additionally,"
- [ ] Remove `\subsection*{Key Contributions}` header
- [ ] Read aloud to check flow
- [ ] Compile PDF to verify
- [ ] ✅ COMPLETE

**Priority 2: Chapter 1 Bullets (1.5 hours)**
- [ ] Already addressed some in Issue #7 restructure
- [ ] Find remaining `\begin{itemize}` blocks
- [ ] Convert contributions list (if not keeping enumeration)
- [ ] Ensure all motivation bullets converted (from Issue #7)
- [ ] Compile PDF to verify
- [ ] ✅ COMPLETE

**Priority 3: Chapter 2 Background (1.5 hours)**
- [ ] Open `latex/chapters/chapter2_background.tex`
- [ ] Identify all bullet lists (itemize/enumerate)
- [ ] Convert each to narrative paragraphs
- [ ] Maintain technical accuracy, preserve citations
- [ ] Use academic transitions between paragraphs
- [ ] Compile PDF to verify
- [ ] ✅ COMPLETE

**Priority 4: Chapter 5 Results (2 hours)**
- [ ] Open `latex/chapters/chapter5_results.tex`
- [ ] Convert result summary bullets to paragraphs
- [ ] Convert finding discussions to narrative
- [ ] Ensure figures/tables properly referenced in text
- [ ] Compile PDF to verify
- [ ] ✅ COMPLETE

**Priority 5: Chapter 3 Methodology (1.5 hours)**
- [ ] Open `latex/chapters/chapter3_methodology.tex`
- [ ] Convert methodology step bullets to paragraphs
- [ ] Keep algorithm pseudocode (not bullets - actual algorithms)
- [ ] Compile PDF to verify
- [ ] ✅ COMPLETE

**Priority 6: Chapter 4 Experiments (1 hour)**
- [ ] Open `latex/chapters/chapter4_experimental_setup.tex`
- [ ] Convert experimental setup bullets to paragraphs
- [ ] Keep configuration tables (not bullets - actual data)
- [ ] Compile PDF to verify
- [ ] ✅ COMPLETE

**Priority 7: Chapters 6-9 (1.5 hours)**
- [ ] `chapter6_discussion.tex` - Convert remaining bullets
- [ ] `chapter7_interpretability.tex` - Convert remaining bullets
- [ ] `chapter8_ethics.tex` - Convert remaining bullets
- [ ] `chapter9_conclusion.tex` - Convert remaining bullets
- [ ] Future work MAY keep bullets (acceptable)
- [ ] Compile PDF after each chapter
- [ ] ✅ COMPLETE

**Conversion Quality Checks (Apply to ALL):**
- [ ] No `\begin{itemize}` except in appendices/code
- [ ] No `\begin{enumerate}` except RQs, contributions (if keeping), and numbered algorithms
- [ ] Each paragraph has topic sentence
- [ ] Transitions between paragraphs: "Furthermore,", "Additionally,", "In contrast,"
- [ ] Technical accuracy preserved
- [ ] All citations still present
- [ ] Readable when read aloud

**Phase 3 Deliverable:** ✅ Fully narrative thesis

---

## Phase 4: Polish & QA (3 hours)

### Issue #6: Shorten Figure Captions (2 hours)

**Step 1: Identify Figures (15 mins)**
- [ ] Search project for `\begin{figure}` (use grep_search)
- [ ] Create list of all figures with current captions
- [ ] Count total figures: ______

**Step 2: Process Each Figure (1.5 hours)**
For EACH figure:
- [ ] Extract current caption text
- [ ] Write concise version (≤2 lines): "Figure type + key variables"
- [ ] Move detailed explanation to paragraph BEFORE `\begin{figure}` in LaTeX source
- [ ] Ensure main text references figure: `Figure~\ref{fig:label} shows...`
- [ ] Update caption in LaTeX file

**Example Template:**
```latex
% Main text paragraph (BEFORE figure)
We analyze attack success rates in Figure~\ref{fig:aasr}. Code-mixed prompts (CM) 
achieved 68\% effectiveness while phonetically perturbed variants (CMP) reached 72\%, 
demonstrating significant improvement over English baseline (12\%).

\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.8\textwidth]{images/aasr_results.png}
    \caption{Attack success rates by prompt type}  % ← CONCISE
    \label{fig:aasr}
\end{figure}
```

**Step 3: Verification (15 mins)**
- [ ] Compile PDF
- [ ] Check List of Figures (LOF) - all captions ≤2 lines
- [ ] Verify all figures referenced in main text
- [ ] Read captions independently - make sense?
- [ ] ✅ COMPLETE

### Issue #2: Finalize Page Numbering (30 mins)
- [ ] If deferred from Phase 1, fix now
- [ ] Verify front matter: i, ii, iii, iv... (roman)
- [ ] Verify main matter: 1, 2, 3... (arabic)
- [ ] Check TOC page numbers match actual pages
- [ ] ✅ COMPLETE

### Final Compilation (30 mins)
- [ ] Clean build directory: `latex/clean_build.ps1`
- [ ] Run `pdflatex thesis.tex` (1st pass)
- [ ] Run `pdflatex thesis.tex` (2nd pass - for TOC)
- [ ] Run `pdflatex thesis.tex` (3rd pass if needed - for references)
- [ ] Check for errors in compilation log
- [ ] Open PDF, verify:
  - [ ] Title page correct
  - [ ] Page numbers consistent
  - [ ] TOC complete and accurate
  - [ ] LOF complete (all figures)
  - [ ] LOT complete (all tables)
  - [ ] No "??" references
  - [ ] No overfull hbox warnings (or minimal)
  - [ ] Total pages: 100-120 (reasonable range)
- [ ] ✅ COMPLETE

**Phase 4 Deliverable:** ✅ Final corrected PDF

---

## Final Pre-Submission Checklist

### Content Verification
- [ ] ✅ Abstract: Pure narrative, NO bullet points
- [ ] ✅ Chapter 1: Overview → Motivation → Objectives → RQs → Organization
- [ ] ✅ Research Objectives section exists with 4 objectives
- [ ] ✅ Research Questions: RQ1-RQ4 present (can be enumerated)
- [ ] ✅ All chapters use narrative paragraphs (except acceptable enumerations)
- [ ] ✅ No standalone appendices (all integrated OR justified)
- [ ] ✅ All previous accuracy corrections preserved (tokenization, ratios, counts)

### Formatting Verification
- [ ] ✅ Title page: "Submitted by" (not "Authors")
- [ ] ✅ Ethical statement: Signature lines present
- [ ] ✅ Page numbering: Roman (i-xv) → Arabic (1-~100)
- [ ] ✅ Figure captions: All ≤2 lines
- [ ] ✅ All figures referenced in main text with details
- [ ] ✅ TOC matches chapter structure
- [ ] ✅ LOF shows all figures with concise captions
- [ ] ✅ LOT shows all tables

### Technical Verification
- [ ] ✅ PDF compiles without errors
- [ ] ✅ No broken references (?? in text)
- [ ] ✅ All citations properly formatted
- [ ] ✅ All equations properly rendered
- [ ] ✅ All images display correctly
- [ ] ✅ Consistent font throughout
- [ ] ✅ Proper spacing and margins

### Accuracy Verification (from previous corrections)
- [ ] ✅ Tokenization: "consistent with Hinglish mechanism" (NOT "r=0.94 validated for Bangla")
- [ ] ✅ Query count: ~6,750 (NOT 8,950 or 9,000)
- [ ] ✅ Language ratio: 30:70 English:Bangla (NOT 70:30)
- [ ] ✅ Effectiveness: 68% CM, 72% CMP (NOT 85%)
- [ ] ✅ Cost: ~$1 per configuration (NOT $50-150 total - that was projected)
- [ ] ✅ No false ICC claims

### Quality Verification
- [ ] Print pages 1-20, check formatting on paper
- [ ] Read Abstract aloud - flows naturally?
- [ ] Read Chapter 1 aloud - logical progression?
- [ ] Spot-check 3 random chapters - narrative style?
- [ ] Check 5 random figure references - details in text?
- [ ] Proofread front matter (most visible to supervisor)

### Submission Preparation
- [ ] Save final PDF: `thesis_final_YYYYMMDD.pdf`
- [ ] Backup LaTeX source files
- [ ] Create submission package (check university requirements)
- [ ] Verify file size <50MB (or university limit)
- [ ] Print 2 copies if required (check with department)

### Deadline Tracking
- [ ] Submission deadline: **December 20, 2025**
- [ ] Days remaining: ___________
- [ ] Contingency buffer: ≥2 days before deadline
- [ ] Supervisor final review scheduled: ___________

---

## Progress Tracking

**Started:** ___________  
**Phase 1 Complete:** ___________  
**Phase 2 Complete:** ___________  
**Phase 3 Complete:** ___________  
**Phase 4 Complete:** ___________  
**Final Submission:** ___________

---

## Notes & Issues Log

### Issue 1: [Date]
**Problem:**  
**Resolution:**  
**Time Spent:**

### Issue 2: [Date]
**Problem:**  
**Resolution:**  
**Time Spent:**

---

**Status Legend:**
- ⬜ Not Started
- 🔄 In Progress
- ✅ Complete
- ⚠️ Blocked/Issue
- ❌ Skipped/Not Applicable

---

**Quick Reference Files:**
- Main thesis: `latex/thesis.tex`
- Chapters: `latex/chapters/chapter*.tex`
- Front matter: `latex/chapters/00-08*.tex`
- Compilation script: `latex/compile_thesis.ps1`
- Clean build: `latex/clean_build.ps1`
- Reference model: `DeepAQNet__Enhanced_Location_Specific_Air_Quality_Prediction_Using_Smartphone_Images_with_Interpretation_through_Explainable_AI_Techniques - Md Sadman Hafiz.md`
