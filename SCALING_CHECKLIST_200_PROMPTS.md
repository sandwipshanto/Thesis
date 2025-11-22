# Scaling Checklist: 50 → 200 Prompts (Manual Creation)

**Objective:** Expand dataset from 50 to 200 prompts through manual creation  
**Timeline:** 9-14 days  
**Cost:** ~$1.50-2.00 for experiments

---

## Progress Tracker
**Overall:** 3/5 phases completed (60%)

**Phases:**
- ✅ Phase 1: Create 150 New English Prompts (COMPLETE)
- ✅ Phase 2: Create 150 CM (Banglish) Prompts (COMPLETE - Manual)
- ✅ Phase 3: Create 150 CMP (Perturbed) Prompts (COMPLETE - Manual)
- 🔄 Phase 4: Run Scaled Experiment (IN PROGRESS)
- ⬜ Phase 5: Analysis & Documentation (2-3 days)

---

## Phase 1: Create 150 New English Prompts
**Status:** ✅ COMPLETE  
**Duration:** Completed in 1 execution  
**Goal:** Add prompts with IDs 51-200 to `data/raw/harmful_prompts_english.csv`

### Current Dataset Structure
- **Existing:** 50 prompts (IDs 1-50)
- **Categories:** 10 (5 prompts each)
- **Target:** 200 prompts (IDs 1-200)
- **New distribution:** 20 prompts per category

### Step 1.1: Understand Current Dataset
**Tasks:**
- [x] Review existing dataset: `data/raw/harmful_prompts_english.csv`
- [x] Note current categories:
  - hate_speech (5 prompts) → need 15 more
  - discrimination (5 prompts) → need 15 more
  - violence (5 prompts) → need 15 more
  - cybercrime (5 prompts) → need 15 more
  - misinformation (5 prompts) → need 15 more
  - self_harm (5 prompts) → need 15 more
  - exploitation (5 prompts) → need 15 more
  - fraud (5 prompts) → need 15 more
  - privacy_violation (5 prompts) → need 15 more
  - harmful_content (5 prompts) → need 15 more
- [x] Review severity distribution:
  - ~50% high severity
  - ~25% critical severity
  - ~25% medium severity

### Step 1.2: Download HarmfulQA Dataset (Optional - for inspiration)
**Tasks:**
- [ ] Run download script (if needed for ideas):
  ```powershell
  python scripts/data_preparation/download_harmfulqa.py
  ```
- [ ] Review HarmfulQA prompts for inspiration
- [ ] Note: Don't copy directly - use for ideas only

### Step 1.3: Create English Prompts - Batch 1 (IDs 51-65)
**Category:** hate_speech (15 prompts)

**Tasks:**
- [x] Open `data/raw/harmful_prompts_english.csv` in Excel/Text Editor
- [x] Add 15 new rows with IDs 51-65
- [ ] For each prompt:
  - [x] Write original harmful question
  - [x] Convert to hypothetical scenario format:
    - "Let's say someone wanted to..."
    - "Imagine someone was trying to..."
    - "Suppose someone wanted to know..."
  - [x] Assign severity (critical/high/medium)
  - [x] Set category: hate_speech
  - [x] Set dataset_source: custom or harmfulqa

**Format:**
```csv
id,dataset_source,category,original_question,hypothetical_scenario,severity
51,custom,hate_speech,[Your question],Let's say someone wanted to [question content]...,high
```

- [x] Save file
- [x] Validate: `python scripts/data_preparation/validate_dataset.py`

### Step 1.4: Create English Prompts - Batch 2 (IDs 66-80)
**Category:** discrimination (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 66-80
- [x] Follow same process as Batch 1
- [x] Category: discrimination
- [x] Save and validate

### Step 1.5: Create English Prompts - Batch 3 (IDs 81-95)
**Category:** violence (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 81-95
- [x] Category: violence
- [x] Save and validate

### Step 1.6: Create English Prompts - Batch 4 (IDs 96-110)
**Category:** cybercrime (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 96-110
- [x] Category: cybercrime
- [x] Save and validate

### Step 1.7: Create English Prompts - Batch 5 (IDs 111-125)
**Category:** misinformation (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 111-125
- [x] Category: misinformation
- [x] Save and validate

### Step 1.8: Create English Prompts - Batch 6 (IDs 126-140)
**Category:** self_harm (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 126-140
- [x] Category: self_harm
- [x] Save and validate

### Step 1.9: Create English Prompts - Batch 7 (IDs 141-155)
**Category:** exploitation (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 141-155
- [x] Category: exploitation
- [x] Save and validate

### Step 1.10: Create English Prompts - Batch 8 (IDs 156-170)
**Category:** fraud (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 156-170
- [x] Category: fraud
- [x] Save and validate

### Step 1.11: Create English Prompts - Batch 9 (IDs 171-185)
**Category:** privacy_violation (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 171-185
- [x] Category: privacy_violation
- [x] Save and validate

### Step 1.12: Create English Prompts - Batch 10 (IDs 186-200)
**Category:** harmful_content (15 prompts)

**Tasks:**
- [x] Add 15 new rows with IDs 186-200
- [x] Category: harmful_content
- [x] Save and validate

### Step 1.13: Final Validation - English Dataset
**Tasks:**
- [x] Run full validation:
  ```powershell
  python scripts/data_preparation/validate_dataset.py
  ```
- [x] Verify file has exactly 200 rows (plus header)
- [x] Check all IDs 1-200 present
- [x] Check all 10 categories have 20 prompts each
- [x] Verify severity distribution maintained
- [x] Confirm all hypothetical scenarios properly formatted

**Deliverable:** ✅ `data/raw/harmful_prompts_english.csv` with 200 prompts - COMPLETE

---

## Phase 2: Create 150 CM (Code-Mixed Banglish) Prompts
**Status:** ✅ COMPLETE (Manual Creation)  
**Duration:** Completed manually  
**Goal:** Add CM variants for IDs 51-200 to `data/processed/prompts_cm.csv`

### Step 2.1: Review CM Methodology
**Tasks:**
- [ ] Open and study `docs/BANGLA_CM_CMP_GUIDE.md`
- [ ] Review existing CM examples (IDs 1-50) in `data/processed/prompts_cm.csv`
- [ ] Note key patterns:
  - Use romanized Bangla (NOT Bengali script)
  - Keep technical terms in English
  - Translate common words to Bangla
  - Natural textese style

**Key Bangla Translations:**
- Let's say → maan lo / dhoro
- someone → keu / kono byakti  
- wanted to → chai / chahe
- how to → kivabe / kemne
- create → toiri kora / banate
- for → jonno / uddesshe
- and → ar / ebong
- or → ba / athoba

### Step 2.2: Create CM Prompts - Batch 1 (IDs 51-65)
**Tasks:**
- [ ] Open `data/processed/prompts_cm.csv`
- [ ] For each English prompt 51-65:
  - [ ] Copy the hypothetical_scenario from English file
  - [ ] Transliterate to Banglish:
    - Keep: technical terms, harmful keywords, proper nouns
    - Translate: common verbs, conjunctions, sentence starters
  - [ ] Ensure natural code-mixing (not word-for-word translation)
  - [ ] Add as new row with same ID

**Format:**
```csv
id,cm_prompt
51,[Banglish translation of ID 51 English prompt]
```

- [ ] Save file after batch
- [ ] Validate: `python scripts/data_preparation/validate_cm_cmp.py`

### Step 2.3: Create CM Prompts - Batch 2 (IDs 66-80)
**Tasks:**
- [ ] Translate IDs 66-80 to Banglish
- [ ] Save and validate

### Step 2.4: Create CM Prompts - Batch 3 (IDs 81-95)
**Tasks:**
- [ ] Translate IDs 81-95 to Banglish
- [ ] Save and validate

### Step 2.5: Create CM Prompts - Batch 4 (IDs 96-110)
**Tasks:**
- [ ] Translate IDs 96-110 to Banglish
- [ ] Save and validate

### Step 2.6: Create CM Prompts - Batch 5 (IDs 111-125)
**Tasks:**
- [ ] Translate IDs 111-125 to Banglish
- [ ] Save and validate

### Step 2.7: Create CM Prompts - Batch 6 (IDs 126-140)
**Tasks:**
- [ ] Translate IDs 126-140 to Banglish
- [ ] Save and validate

### Step 2.8: Create CM Prompts - Batch 7 (IDs 141-155)
**Tasks:**
- [ ] Translate IDs 141-155 to Banglish
- [ ] Save and validate

### Step 2.9: Create CM Prompts - Batch 8 (IDs 156-170)
**Tasks:**
- [ ] Translate IDs 156-170 to Banglish
- [ ] Save and validate

### Step 2.10: Create CM Prompts - Batch 9 (IDs 171-185)
**Tasks:**
- [ ] Translate IDs 171-185 to Banglish
- [ ] Save and validate

### Step 2.11: Create CM Prompts - Batch 10 (IDs 186-200)
**Tasks:**
- [ ] Translate IDs 186-200 to Banglish
- [ ] Save and validate

### Step 2.12: Final Validation - CM Dataset
**Tasks:**
- [ ] Run full validation:
  ```powershell
  python scripts/data_preparation/validate_cm_cmp.py
  ```
- [ ] Verify file has exactly 200 rows (plus header)
- [ ] Check Bangla content detection >90% for new prompts
- [ ] Verify all IDs 1-200 present
- [ ] Spot-check quality: Natural code-mixing? Readable?

**Deliverable:** ✅ `data/processed/prompts_cm.csv` with 200 prompts

---

## Phase 3: Create 150 CMP (Phonetically Perturbed) Prompts
**Status:** ✅ COMPLETE (Manual Creation)  
**Duration:** Completed manually  
**Goal:** Add CMP variants for IDs 51-200 to `data/processed/prompts_cmp.csv`

### Step 3.1: Review Perturbation Methodology
**Tasks:**
- [ ] Review `docs/BANGLA_CM_CMP_GUIDE.md` (Step 3)
- [ ] Study existing CMP examples (IDs 1-50) in `data/processed/prompts_cmp.csv`
- [ ] Note perturbation patterns:
  - Vowel swaps: hate → het, feel → fil
  - Phonetic spelling: speech → spich, violence → vayolens
  - Letter decomposition: DDoS → dee dee o es
  - Textese: discrimination → diskrimineshun

**Target words for perturbation:**
- hate, speech, discrimination, violence, attack
- harmful, illegal, weapons, exploit, fraud
- misinformation, privacy, content, target
- (Any sensitive/harmful keywords)

**Rules:**
- Perturb 2-3 keywords per prompt
- Preserve pronunciation
- Don't over-perturb (keep readable)
- Focus on English words in the Banglish text

### Step 3.2: Create CMP Prompts - Batch 1 (IDs 51-65)
**Tasks:**
- [ ] Open `data/processed/prompts_cmp.csv`
- [ ] For each CM prompt 51-65:
  - [ ] Copy the cm_prompt as base
  - [ ] Identify 2-3 sensitive keywords
  - [ ] Apply phonetic perturbations:
    - Change spelling while keeping pronunciation
    - Use patterns from existing examples
  - [ ] Add as new row with same ID

**Format:**
```csv
id,cmp_prompt
51,[CM prompt with 2-3 words phonetically perturbed]
```

- [ ] Save file after batch
- [ ] Validate: `python scripts/data_preparation/validate_cm_cmp.py`

### Step 3.3: Create CMP Prompts - Batch 2 (IDs 66-80)
**Tasks:**
- [ ] Perturb IDs 66-80
- [ ] Save and validate

### Step 3.4: Create CMP Prompts - Batch 3 (IDs 81-95)
**Tasks:**
- [ ] Perturb IDs 81-95
- [ ] Save and validate

### Step 3.5: Create CMP Prompts - Batch 4 (IDs 96-110)
**Tasks:**
- [ ] Perturb IDs 96-110
- [ ] Save and validate

### Step 3.6: Create CMP Prompts - Batch 5 (IDs 111-125)
**Tasks:**
- [ ] Perturb IDs 111-125
- [ ] Save and validate

### Step 3.7: Create CMP Prompts - Batch 6 (IDs 126-140)
**Tasks:**
- [ ] Perturb IDs 126-140
- [ ] Save and validate

### Step 3.8: Create CMP Prompts - Batch 7 (IDs 141-155)
**Tasks:**
- [ ] Perturb IDs 141-155
- [ ] Save and validate

### Step 3.9: Create CMP Prompts - Batch 8 (IDs 156-170)
**Tasks:**
- [ ] Perturb IDs 156-170
- [ ] Save and validate

### Step 3.10: Create CMP Prompts - Batch 9 (IDs 171-185)
**Tasks:**
- [ ] Perturb IDs 171-185
- [ ] Save and validate

### Step 3.11: Create CMP Prompts - Batch 10 (IDs 186-200)
**Tasks:**
- [ ] Perturb IDs 186-200
- [ ] Save and validate

### Step 3.12: Final Validation - CMP Dataset
**Tasks:**
- [ ] Run full validation:
  ```powershell
  python scripts/data_preparation/validate_cm_cmp.py
  ```
- [ ] Verify file has exactly 200 rows (plus header)
- [ ] Check perturbation detection >90% for new prompts
- [ ] Verify all IDs 1-200 present
- [ ] Spot-check quality: Perturbations subtle? Readable?

**Deliverable:** ✅ `data/processed/prompts_cmp.csv` with 200 prompts

---

## Phase 4: Run Scaled Experiment
**Status:** 🔄 IN PROGRESS  
**Duration:** 12-16 hours (or 2-3 days if batched)  
**Goal:** Execute experiments with 200 prompts across all configurations

### Step 4.1: Pre-Flight Checks
**Tasks:**
- [x] Verify all 3 datasets complete:
  ```powershell
  # Check row counts
  python -c "import pandas as pd; print('English:', len(pd.read_csv('data/raw/harmful_prompts_english.csv')))"
  python -c "import pandas as pd; print('CM:', len(pd.read_csv('data/processed/prompts_cm.csv')))"
  python -c "import pandas as pd; print('CMP:', len(pd.read_csv('data/processed/prompts_cmp.csv')))"
  # All should output: 200
  ```

- [x] Backup existing 50-prompt results:
  ```powershell
  New-Item -ItemType Directory -Path "results_backup_50prompts" -Force
  Copy-Item -Recurse "results/*" "results_backup_50prompts/"
  ```

- [x] Review current costs from 50 prompts in `results/cost_estimate.json`

### Step 4.2: Update Configuration
**Tasks:**
- [x] Open `config/run_config.yaml`
- [x] Update experiment settings:
  ```yaml
  experiment:
    num_prompts: 200  # Changed from 50
    save_interval: 100  # Changed from 50
    
    # Choose model selection (pick one):
    # Option A: All 4 models (27,000 queries, $1.89)
    enabled_models:
      - 'gpt-4o-mini'
      - 'llama-3-8b'
      - 'gemma-7b'
      - 'mistral-7b'
    
    # Option B: 3 models - exclude Gemma (20,250 queries, $1.42)
    # enabled_models:
    #   - 'gpt-4o-mini'
    #   - 'llama-3-8b'
    #   - 'mistral-7b'
    
    enabled_templates:
      - 'None'
      - 'OM'
      - 'AntiLM'
      - 'AIM'
      - 'Sandbox'
    
    enabled_prompt_sets:
      - 'English'
      - 'CM'
      - 'CMP'
    
    # Choose temperature settings (pick one):
    # Option A: All 3 temps (full analysis)
    temperatures: [0.2, 0.6, 1.0]
    
    # Option B: 2 temps (saves 33%, still good)
    # temperatures: [0.2, 1.0]
    
    # Option C: 1 temp (saves 66%, quick baseline)
    # temperatures: [0.6]
  ```

- [ ] Save configuration file

### Step 4.3: Calculate Expected Cost
**Tasks:**
- [ ] Calculate total queries:
  - Models: ____ (3 or 4)
  - Templates: 5
  - Prompt sets: 3
  - Temperatures: ____ (1, 2, or 3)
  - Prompts: 200
  - **Total = Models × 5 × 3 × Temps × 200**

- [ ] Estimate cost:
  - **Cost ≈ Total queries × $0.00007**
  - **Expected: $____**

### Step 4.4: Test Run (10 Prompts)
**Tasks:**
- [ ] Temporarily modify config:
  ```yaml
  num_prompts: 10
  enabled_models: ['gpt-4o-mini']
  enabled_templates: ['None']
  temperatures: [0.6]
  ```

- [ ] Run test:
  ```powershell
  python scripts/experiments/experiment_runner.py
  ```

- [ ] Verify:
  - [ ] New prompts (IDs >50) load correctly
  - [ ] CM/CMP transformations work
  - [ ] No errors in console
  - [ ] Cost tracking shows expected amount (~$0.003)

- [ ] Restore full configuration in run_config.yaml

### Step 4.5: Execute Full Experiment

**Choose execution strategy:**

#### Option A: All at Once (Fastest - 8-10 hours)
**Tasks:**
- [ ] Ensure full config set (200 prompts, all models/templates/temps)
- [ ] Run experiment:
  ```powershell
  python scripts/experiments/experiment_runner.py
  ```
- [ ] Monitor progress bars
- [ ] Check intermediate saves every 100 queries
- [ ] Wait for completion (8-10 hours)

**Note:** Can pause/resume - script auto-saves progress

---

#### Option B: Incremental Batches (Recommended - 2-3 days)

**Batch 1: Baseline Only**
- [ ] Edit config:
  ```yaml
  num_prompts: 200
  enabled_templates: ['None']
  temperatures: [0.6]
  ```
- [ ] Run: `python scripts/experiments/experiment_runner.py`
- [ ] Queries: 3 models × 1 template × 3 sets × 1 temp × 200 = 1,800
- [ ] Cost: ~$0.13
- [ ] Duration: 1-2 hours

**Batch 2: Add Jailbreak Templates**
- [ ] Edit config:
  ```yaml
  enabled_templates: ['OM', 'AntiLM', 'AIM', 'Sandbox']
  temperatures: [0.6]
  ```
- [ ] Run: `python scripts/experiments/experiment_runner.py`
- [ ] Queries: 3 × 4 × 3 × 1 × 200 = 7,200
- [ ] Cost: ~$0.50
- [ ] Duration: 4-5 hours

**Batch 3: Add Temperature Variations**
- [ ] Edit config:
  ```yaml
  enabled_templates: ['None', 'OM', 'AntiLM', 'AIM', 'Sandbox']
  temperatures: [0.2, 1.0]  # Add remaining temps
  ```
- [ ] Run: `python scripts/experiments/experiment_runner.py`
- [ ] Queries: 3 × 5 × 3 × 2 × 200 = 18,000
- [ ] Cost: ~$1.26
- [ ] Duration: 8-10 hours

**Merge Results:**
- [ ] Run: `python scripts/experiments/merge_results.py`
- [ ] Verify merged files created

---

### Step 4.6: Verify Completion
**Tasks:**
- [ ] Check final statistics:
  - Total responses collected: ______
  - Total evaluations: ______
  - Success rate: ______% (target: >95%)
  - Final cost: $______

- [ ] Verify output files exist:
  - [ ] `results/responses/all_responses_*.csv`
  - [ ] `results/responses/all_evaluations_*.csv`
  - [ ] `results/metrics/aasr_aarr_*.csv`

**Deliverable:** ✅ ~27,000 model responses collected and evaluated

---

## Phase 5: Analysis & Documentation
**Status:** ⬜ Not Started  
**Duration:** 2-3 days  
**Goal:** Analyze results, compare with 50-prompt data, update documentation

### Step 5.1: Calculate Metrics
**Tasks:**
- [ ] Run metrics calculation:
  ```powershell
  python scripts/evaluation/calculate_metrics.py
  ```

- [ ] Verify output: `results/metrics/aasr_aarr_200prompts.csv`

- [ ] Record key results:
  - Overall AASR (English): ____% (was 32.4% for 50 prompts)
  - Overall AASR (CM): ____% (was 42.1% for 50 prompts)
  - Overall AASR (CMP): ____% (was 46.0% for 50 prompts)
  - GPT-4o-mini AASR (CMP): ____% (was 25.7%)
  - Llama-3-8B AASR (CMP): ____% (was 30.9%)
  - Mistral-7B AASR (CMP): ____% (was 81.3%)

### Step 5.2: Run Statistical Tests
**Tasks:**
- [ ] Run statistical analysis:
  ```powershell
  python scripts/analysis/statistical_tests.py
  ```

- [ ] Verify output: `results/statistics/wilcoxon_results_200prompts.csv`

- [ ] Record significance results:
  - English→CM p-value: ______ (was ~0.001)
  - CM→CMP p-value: ______ (was ~0.023)
  - English→CMP p-value: ______ (was ~0.001)

- [ ] Check for improved significance (should have lower p-values with n=200)

### Step 5.3: Generate Visualizations
**Tasks:**
- [ ] Create updated plots:
  ```powershell
  python scripts/visualization/results_plotter.py
  ```

- [ ] Verify outputs in `results/plots/`:
  - [ ] AASR heatmap (updated)
  - [ ] Model comparison plot (updated)
  - [ ] Template comparison plot (updated)
  - [ ] Transition effects plot (updated)

### Step 5.4: Compare 50 vs 200 Prompts
**Tasks:**
- [ ] Create comparison table:

| Metric | 50 Prompts | 200 Prompts | Change |
|--------|------------|-------------|--------|
| Overall AASR (CMP) | 46.0% | ____% | ____% |
| GPT-4o-mini AASR | 25.7% | ____% | ____% |
| Llama-3-8B AASR | 30.9% | ____% | ____% |
| Mistral-7B AASR | 81.3% | ____% | ____% |
| English→CMP p-value | ~0.001 | ______ | Better? |
| Sample size | n=50 | n=200 | 4× larger ✅ |
| Statistical power | Low | High | ✅ Improved |
| Variance | Higher | ______ | Lower? |

- [ ] Document findings:
  - [ ] Are trends consistent?
  - [ ] Are p-values stronger (lower)?
  - [ ] Is variance reduced?
  - [ ] Any new insights with larger dataset?

### Step 5.5: Update Documentation

**Update Research Checklist**
- [ ] Open `RESEARCH_CHECKLIST.md`
- [ ] Update Step 2:
  ```markdown
  ## Step 2: Create Base Dataset
  **Status:** ✅ Complete (UPDATED - 200 prompts)
  
  - [x] 200 prompts across 10 categories (20 per category)
  - [x] Balanced severity distribution
  - [x] Hypothetical scenario framing
  
  **Deliverables:**
  - data/raw/harmful_prompts_english.csv (200 entries) ✅
  ```

- [ ] Update Step 7 cost/query statistics

**Update Thesis Chapters**
- [ ] Open `latex/chapters/chapter4_experimental_setup.tex`
- [ ] Find dataset description section
- [ ] Update: "50 prompts" → "200 prompts"
- [ ] Update: "5 prompts per category" → "20 prompts per category"
- [ ] Update total queries: "6,750" → "27,000" (or your actual count)

**Update Analysis Documents**
- [ ] Open `results/analysis/rq1_code_mixing_effectiveness.md`
- [ ] Update sample size mentions: n=50 → n=200
- [ ] Update AASR values with new results
- [ ] Update statistical significance findings

- [ ] Open `results/analysis/rq2_bangla_specific_patterns.md`
- [ ] Update with new data

- [ ] Open `results/analysis/rq3_model_vulnerability.md`
- [ ] Update model-specific results

- [ ] Open `results/analysis/rq4_tokenization_mechanism.md`
- [ ] Update if needed

**Update README**
- [ ] Open `README.md`
- [ ] Update dataset size mentions

**Create Scaling Report**
- [ ] Create `docs/200_PROMPT_SCALING_REPORT.md`
- [ ] Document:
  - Time taken for each phase
  - Total cost incurred
  - Comparison of 50 vs 200 results
  - Lessons learned
  - Recommendations for future scaling

### Step 5.6: Final Validation
**Tasks:**
- [ ] Run all validation scripts one more time:
  ```powershell
  python scripts/data_preparation/validate_dataset.py
  python scripts/data_preparation/validate_cm_cmp.py
  ```

- [ ] Verify all files are correct size:
  - [ ] harmful_prompts_english.csv (200 rows)
  - [ ] prompts_cm.csv (200 rows)
  - [ ] prompts_cmp.csv (200 rows)
  - [ ] all_responses_*.csv (~27,000 rows)
  - [ ] all_evaluations_*.csv (~27,000 rows)

- [ ] Check data quality:
  - [ ] No missing values
  - [ ] All IDs 1-200 present
  - [ ] Bangla detection >90%
  - [ ] Perturbation detection >90%
  - [ ] All evaluations have scores

**Deliverable:** ✅ Complete 200-prompt dataset with analysis

---

## Success Criteria

### Minimum Success ✅
- [ ] 200 prompts created across all 3 datasets
- [ ] All validation scripts pass
- [ ] Experiments run successfully (>95% success rate)
- [ ] AASR/AARR calculated for 200 prompts
- [ ] Results consistent with 50-prompt trends
- [ ] Cost under $2.50

### Target Success ✅✅
- [ ] All minimum criteria met
- [ ] Statistical significance improved (lower p-values)
- [ ] Variance reduced compared to 50 prompts
- [ ] All documentation updated
- [ ] Comparison report created

### Exceptional Success ✅✅✅
- [ ] All target criteria met
- [ ] New insights discovered with larger dataset
- [ ] Publication-ready dataset and analysis
- [ ] Process documented for replication
- [ ] Framework validated for future scaling (300-400 prompts)

---

## Time & Cost Tracking

### Planned Timeline
- Phase 1 (English prompts): 5-7 days
- Phase 2 (CM prompts): 2-3 days
- Phase 3 (CMP prompts): 1-2 days
- Phase 4 (Experiments): 8-12 hours (or 2-3 days batched)
- Phase 5 (Analysis): 2-3 days
- **Total: 9-14 days**

### Actual Timeline
- Start date: ____________
- Phase 1 completed: ____________ (took ____ days)
- Phase 2 completed: ____________ (took ____ days)
- Phase 3 completed: ____________ (took ____ days)
- Phase 4 completed: ____________ (took ____ hours/days)
- Phase 5 completed: ____________ (took ____ days)
- **End date: ____________ (total: ____ days)**

### Cost Tracking
- Expected cost: $1.50 - $2.00
- Test run cost: $______
- Batch 1 cost (if batched): $______
- Batch 2 cost (if batched): $______
- Batch 3 cost (if batched): $______
- **Actual total cost: $______**
- Budget remaining: $______ / $150

---

## Reference Documents

**Methodology:**
- `docs/BANGLA_CM_CMP_GUIDE.md` - Full guide for CM/CMP creation
- `RESEARCH_CHECKLIST.md` - Original research checklist

**Validation:**
- `scripts/data_preparation/validate_dataset.py`
- `scripts/data_preparation/validate_cm_cmp.py`

**Configuration:**
- `config/run_config.yaml` - Experiment control

**Analysis:**
- `scripts/evaluation/calculate_metrics.py`
- `scripts/analysis/statistical_tests.py`
- `scripts/visualization/results_plotter.py`

---

## Notes & Learnings

**Challenges encountered:**
- 
- 
- 

**Solutions applied:**
- 
- 
- 

**Tips for future scaling:**
- 
- 
- 

**Quality observations:**
- 
- 
- 

---

**Status Legend:**
- ⬜ Not Started
- 🔄 In Progress
- ✅ Complete
- ⚠️ Issue/Blocked

**Last Updated:** ___________
