# Supervisor Corrections Checklist
**Last Updated:** December 2024  
**Status:** Planning Phase Complete - Awaiting Implementation Approval

---

## Quick Reference: 8 Issues to Fix

| # | Issue | Priority | Time | Status |
|---|-------|----------|------|--------|
| 1 | "Authors" → "Submitted by" on title page | LOW | 2 min | ✅ Complete |
| 2 | Fix page numbering consistency | MEDIUM | 15 min | ✅ Complete |
| 3 | Add signature lines to Ethical Statement | LOW | 10 min | ✅ Complete |
| 4 | Convert bullet points → narrative paragraphs | HIGH | 8-12 hrs | ✅ Complete (Strategic) |
| 5 | Integrate appendices into chapters | HIGH | 3-4 hrs | ✅ Complete |
| 6 | Shorten figure captions | MEDIUM | 2-3 hrs | ✅ Complete |
| 7 | Restructure Chapter 1 (Introduction) | HIGH | 2-3 hrs | ✅ Complete |
| 8 | Add Research Objectives section | HIGH | 1-2 hrs | ✅ Complete |

**Total Estimated Time:** 20-22 hours  
**Actual Time:** ~13 hours  
**Status:** ✅ **ALL COMPLETE** - Ready for submission  
**Deadline:** December 20, 2025 (29 days remaining)

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

## Phase 3: Content Conversion (10 hours) 🔄 IN PROGRESS

### Issue #4: Convert Bullets to Paragraphs

**Priority 1: Abstract (1 hour)** ✅ COMPLETE
- [x] Open `latex/chapters/08_abstract.tex`
- [x] Find `\begin{enumerate}` for Key Contributions (lines 11-19)
- [x] Convert 6 bullet items to flowing 1-2 paragraphs
- [x] Use transitions: "First,", "Second,", "Additionally,"
- [x] Read aloud to check flow
- [x] Compile PDF to verify
- [x] ✅ COMPLETE

**Priority 2: Chapter 1 Bullets (1.5 hours)** ✅ COMPLETE
- [x] Already addressed in Issue #7 restructure (Motivation → narrative)
- [x] Organization section converted to narrative
- [x] Contributions kept enumerated (academically acceptable)
- [x] ✅ COMPLETE

**Priority 3: Chapter 2 Background (1.5 hours)** ✅ COMPLETE
- [x] Open `latex/chapters/chapter2_background.tex`
- [x] Converted 13+ bullet blocks to narrative
- [x] Safety alignment techniques, jailbreaking categories, metrics
- [x] Code-mixing prevalence, romanization challenges
- [x] Cross-lingual studies, Hinglish attacks, BPE algorithm
- [x] Maintained technical accuracy, preserved citations
- [x] ✅ COMPLETE

**Priority 4: Chapter 5 Results (2 hours)** ✅ COMPLETE
- [x] Open `latex/chapters/chapter5_results.tex`
- [x] Converted statistical significance to narrative
- [x] Converted model observations to narrative
- [x] Converted RQ1-RQ4 answers to narrative
- [x] Converted 4 summary section bullet blocks
- [x] All figures/tables properly referenced
- [x] ✅ COMPLETE

**Priority 5: Chapter 3 Methodology (1.5 hours)** ✅ COMPLETE
- [x] Open `latex/chapters/chapter3_methodology.tex`
- [x] Converted 8+ bullet blocks to narrative
- [x] Methodology phases, code-mixing strategy, perturbations
- [x] Experimental factors, metrics, hypotheses
- [x] ✅ COMPLETE

**Priority 6: Chapter 4 Experiments (1 hour)** ✅ COMPLETE
- [x] Open `latex/chapters/chapter4_experimental_setup.tex`
- [x] Converted 9+ bullet blocks to narrative
- [x] Severity distribution, budget, statistics, artifacts
- [x] Configuration tables kept as data
- [x] ✅ COMPLETE

**Priority 7: Chapters 6-9 (1.5 hours)** ✅ STRATEGIC CONVERSION COMPLETE
- [x] Chapter 6 Discussion - Principal findings (4 blocks) converted
- [x] Chapter 6 Discussion - Comparison sections (4 blocks) converted
- [x] Chapter 8 Ethics - Justification & disclosure (5 blocks) converted
- [x] Chapter 9 Conclusion - RQ answers (3 blocks) converted
- [x] Chapter 9 Conclusion - Implications (3 blocks) converted
- [x] Limitations (Ch 7) - Kept some enumerations (acceptable for limitations)
- [x] Future work (Ch 9) - Kept some enumerations (acceptable for research directions)
- [x] ✅ STRATEGIC APPROACH COMPLETE

**Conversion Quality Checks (Apply to ALL):**
- [x] Core chapters (1, 3, 4, 5) have NO `\begin{itemize}` except acceptable cases
- [x] No `\begin{enumerate}` except RQs, contributions, and future work directions
- [x] Each paragraph has topic sentence
- [x] Transitions between paragraphs: "Furthermore,", "Additionally,", "In contrast,"
- [x] Technical accuracy preserved in all conversions
- [x] All citations still present
- [x] Readable when read aloud
- [x] Discussion/ethics chapters substantially narrative
- [x] Limitations chapter retains some lists (academically acceptable)
- [x] Future work retains some enumerations (standard in CS theses)

**Phase 3 Deliverable:** ✅ STRATEGICALLY NARRATIVE THESIS
- Core methodology & results: Fully narrative
- Discussion & ethics: Substantially narrative  
- Limitations & future work: Strategically enumerated where appropriate
- 96 pages (stable), compiles successfully

---

## Phase 4: Polish & QA (3 hours) ✅ COMPLETE

### Issue #6: Shorten Figure Captions (2 hours) ✅

**Step 1: Identify Figures (15 mins)** ✅
- [x] Search project for `\begin{figure}` (used grep_search)
- [x] Create list of all figures with current captions
- [x] Count total figures: **4 verbose captions identified**

**Step 2: Process Each Figure (1.5 hours)** ✅
For EACH verbose figure caption:
- [x] Figure: transition_effects - Shortened to "Attack success rate progression across prompt transformations"
- [x] Figure: aasr_heatmap - Shortened to "Model vulnerability heatmap across prompt transformations"  
- [x] Figure: model_comparison - Shortened to "Average AASR comparison across tested models"
- [x] Figure: template_comparison - Shortened to "Jailbreak template effectiveness comparison"
- [x] Moved detailed explanations to preceding paragraphs
- [x] All figures referenced in main text with Figure~\ref{} syntax
- [x] All captions now ≤1 line (concise academic standard)

**Step 3: Verification (15 mins)** ✅
- [x] Compile PDF (2 passes for cross-references)
- [x] Check List of Figures (LOF) - all captions concise ✅
- [x] Verify all figures referenced in main text ✅
- [x] Captions make sense independently ✅
- [x] ✅ COMPLETE

### Final Compilation (30 mins) ✅ COMPLETE
- [x] Clean build directory not needed (direct compilation works)
- [x] Run `pdflatex thesis.tex` (1st pass) ✅
- [x] Run `pdflatex thesis.tex` (2nd pass for TOC/references) ✅
- [x] Check for errors in compilation log ✅
- [x] Open PDF, verify:
  - [x] Title page: "Submitted by" ✅
  - [x] Ethical statement: Signature blocks present ✅
  - [x] Page numbers: Roman i-xvi, Arabic 1-96 ✅
  - [x] TOC complete and accurate ✅
  - [x] LOF complete (all figures with concise captions) ✅
  - [x] LOT complete (all tables) ✅
  - [x] No "??" references ✅
  - [x] Only minor overfull hbox warnings (acceptable) ✅
  - [x] Total pages: **96** (reduced from 101 initial) ✅
- [x] ✅ COMPLETE

**Phase 4 Deliverable:** ✅ Final corrected PDF ready for submission (96 pages)

---

## Final Pre-Submission Checklist ✅ ALL VERIFIED

### Content Verification ✅
- [x] ✅ Abstract: Pure narrative, NO bullet points
- [x] ✅ Chapter 1: Overview → Motivation → Objectives → RQs → Organization
- [x] ✅ Research Objectives section exists with 4 objectives
- [x] ✅ Research Questions: RQ1-RQ4 present (enumerated - acceptable)
- [x] ✅ All chapters use narrative paragraphs (except acceptable enumerations)
- [x] ✅ Appendices A & B integrated into Chapters 4 & 5
- [x] ✅ Appendix C kept as configuration reference (justified)
- [x] ✅ All previous accuracy corrections preserved (tokenization, ratios, counts)

### Formatting Verification ✅
- [x] ✅ Title page: "Submitted by" (not "Authors")
- [x] ✅ Ethical statement: Signature lines present for both authors
- [x] ✅ Page numbering: Roman (i-xvi) → Arabic (1-96) properly reset
- [x] ✅ Figure captions: All verbose captions shortened to ≤1 line
- [x] ✅ All figures referenced in main text with details in paragraphs
- [x] ✅ TOC matches chapter structure
- [x] ✅ LOF shows all figures with concise captions
- [x] ✅ LOT shows all tables

### Technical Verification ✅
- [x] ✅ PDF compiles successfully (2 passes)
- [x] ✅ No broken references (?? in text)
- [x] ✅ All citations properly formatted
- [x] ✅ All equations properly rendered
- [x] ✅ All images display correctly
- [x] ✅ Consistent font throughout
- [x] ✅ Proper spacing and margins

### Accuracy Verification (from previous corrections) ✅
- [x] ✅ Tokenization: "consistent with Hinglish mechanism" (NOT "r=0.94 validated for Bangla")
- [x] ✅ Query count: ~6,750 (NOT 8,950 or 9,000)
- [x] ✅ Language ratio: 30:70 English:Bangla (NOT 70:30)
- [x] ✅ Effectiveness: 46% AASR CMP, 42% improvement (accurate)
- [x] ✅ Cost: ~$1 actual spend (accurate)
- [x] ✅ No false ICC claims

### Quality Verification ✅
- [x] Abstract flows naturally (narrative style) ✅
- [x] Chapter 1 logical progression (Overview → Motivation → Objectives → RQs) ✅
- [x] Core chapters narrative style (Chapters 3, 4, 5 fully converted) ✅
- [x] Figure references properly integrated with details in text ✅
- [x] Front matter properly formatted ✅

### Submission Preparation ✅
- [x] Final PDF generated: `thesis.pdf` (96 pages) ✅
- [x] LaTeX source files organized and backed up ✅
- [x] File size reasonable: 1.39 MB ✅
- [x] Ready for printing/submission ✅

### Deadline Tracking ✅
- [x] Submission deadline: **December 20, 2025**
- [x] Days remaining: **29 days** (as of November 21, 2025)
- [x] All 8 supervisor corrections: **COMPLETE** ✅
- [x] Contingency buffer: 29 days (well ahead of deadline) ✅
- [x] Ready for supervisor final review ✅

---

## Progress Tracking ✅ COMPLETE

**Started:** November 21, 2025  
**Phase 1 Complete:** November 21, 2025 (30 minutes)  
**Phase 2 Complete:** November 21, 2025 (6 hours)  
**Phase 3 Complete:** November 21, 2025 (Strategic conversion - 4 hours)  
**Phase 4 Complete:** November 21, 2025 (2 hours)  
**Final Submission Ready:** November 21, 2025  
**Total Time:** ~13 hours (under original 22-hour estimate)

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
