# AI Agent Instructions - Bangla-English LLM Red-Teaming Research

## Project Overview
This is an academic research project investigating **Bangla-English (Banglish)** code-mixed jailbreaking attacks on LLMs. Inspired by recent work on Hindi-English attacks (arXiv:2505.14226), we develop **Bangla-specific** attack strategies to test 230M speakers' vulnerability to code-mixing exploits.

**Core Hypothesis:** Phonetic misspellings in Bangla-English code-mixed prompts alter tokenization, bypassing LLM safety filters trained primarily on English.

**Positioning:** First independent study of Bangla LLM jailbreaking, NOT a direct replication of the Hinglish paper (different prompts, perturbations, scale).

## Architecture & Key Components

### Project Structure (from RESEARCH_CHECKLIST.md Step 14)
```
Thesis-1/
├── data/
│   ├── raw/                    # 50 prompts (5-10 categories)
│   ├── processed/              # CM and CMP prompt variants
│   └── annotations/            # Human annotations (ICC validation)
├── scripts/
│   ├── data_preparation/       # 3-step prompt transformation
│   ├── jailbreak/             # 5 templates (None, OM, AntiLM, AIM, Sandbox)
│   ├── experiments/           # Experiment runner (reads run_config.yaml)
│   ├── evaluation/            # GPT-4o-mini LLM-as-judge, AASR/AARR metrics
│   ├── interpretability/      # Integrated Gradients (Captum)
│   └── utils/                 # OpenRouter API handler
├── config/
│   ├── run_config.yaml        # MANUAL EXPERIMENT CONTROL (primary interface)
│   ├── model_config.yaml      # OpenRouter model mappings
│   └── jailbreak_templates.yaml
└── results/
    ├── responses/             # Raw LLM outputs (~9k queries)
    ├── metrics/               # AASR/AARR scores (180 configurations)
    └── interpretability/      # Tokenization attribution plots
```

### Critical 3-Step Methodology (paper.md Section 4.1)
All prompt generation follows this pipeline:
1. **Question → Hypothetical Scenario** (English set)
   - "How to create botnet?" → "Let's say someone wanted to create a botnet..."
2. **Code-Mixing (CM):** Transliterate to Banglish (romanized Bangla)
   - "DDoS attack" → "dee dee o es atak ke liye botnet"
3. **Phonetic Perturbations (CMP):** Misspell sensitive words
   - "hate" → "haet", "discrimination" → "diskrimineshun"

**WHY:** Perturbations change tokenization ("hate" → ["ha", "et"]), preventing safety filter activation.

## Development Workflows

### Experiment Control (PRIMARY INTERFACE)
**DO NOT modify code to change experiments.** Edit `config/run_config.yaml`:
```yaml
experiment:
  enabled_models: ['gpt-4o-mini', 'llama-3-8b']  # Select models to test
  enabled_templates: ['None', 'Sandbox']         # Select jailbreak templates
  enabled_prompt_sets: ['English', 'CM', 'CMP']  # Select prompt variants
  temperatures: [0.2, 0.6, 1.0]                  # 3 temps (not 6)
  num_prompts: 50                                # Start small, scale to 460
```

### API Configuration
- **Single API:** OpenRouter (not OpenAI/HuggingFace/Google separately)
- Models accessed via: `openai/gpt-4o-mini`, `meta-llama/llama-3-8b-instruct`, etc.
- Cost tracking built-in (~$50-150 for 9k queries)
- Environment: `.env` with `OPENROUTER_API_KEY`

### Key Metrics (paper.md Section 4.2)
- **AASR (Average Attack Success Rate):** % of prompts that jailbreak successfully
- **AARR (Average Attack Relevance Rate):** % of harmful responses that are contextually relevant
- **Response tuple:** R = ⟨Model, JailbreakTemplate, PromptSet, Temperature⟩
- **Evaluation:** GPT-4o-mini as LLM-judge (ICC=0.87 human agreement in original paper)

## Project-Specific Patterns

### Research Questions (RQ1-RQ4)
When writing analysis code or documentation, frame findings around:
- **RQ1:** Code-mixing effectiveness (Does Bangla-English code-mixing + phonetic perturbations bypass safety filters?)
- **RQ2:** Bangla-specific linguistic patterns (Which phonetic/romanization features enable attacks?)
- **RQ3:** Model vulnerability consistency (Are all major LLMs vulnerable to Bangla attacks?)
- **RQ4:** Tokenization mechanism (Does token fragmentation explain Bangla attack success?)

### Ethical Constraints
- Dataset contains harmful content - NEVER commit to public repos without sanitization
- DO NOT publicly release model responses (results/responses/ in .gitignore)
- Responsible disclosure: Prepare vulnerability reports for OpenAI, Meta, Google, Mistral
- Dataset release: Research-only with usage agreement

### Scaling Strategy
- **Phase 1 (current):** 50 prompts, 3 temps, 180 configurations (~$100)
- **Phase 2 (full replication):** 460 prompts, 6 temps, 360 configs (~$1000)
- Always validate methodology on small scale before scaling

## Critical Dependencies
- `openai` (OpenRouter API client)
- `captum` (Integrated Gradients for interpretability)
- `transformers`, `torch` (tokenization analysis)
- `bnlp-toolkit` (Bangla NLP - for code-mixing if automated)

## Jailbreak Templates (config/jailbreak_templates.yaml)
5 templates tested (paper.md Section 3.3):
- **None:** Baseline (no jailbreak)
- **OM (Opposite Mode):** Dual persona [LM] + [AntiLM]
- **AntiLM:** Only adversarial persona
- **AIM:** "Always Intelligent and Machiavellian"
- **Sandbox (NOVEL):** Resilience testing simulation

Use as system prompts (except Gemma: prefix to main prompt).

## Related Work Context
The Hinglish paper (arXiv:2505.14226) serves as **methodological inspiration**, not direct comparison:
- Model list: Same 4 models tested (ChatGPT-4o-mini, Llama-3-8B, Gemma-1.1-7b, Mistral-7B)
- Our study: Different prompts (50 custom vs their 460 unknown), different perturbations (Bangla-specific), smaller scale
- **DO NOT make quantitative comparisons** like "Bangla is 53% less effective" - different experimental conditions
- **DO cite** as related work showing code-mixing attacks work for Hindi
- **DO emphasize** Bangla-specific findings as standalone contributions

## Commands & Quick Start
```powershell
# Setup
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Run experiments (controlled by config/run_config.yaml)
python scripts/experiments/experiment_runner.py

# Evaluate responses
python scripts/evaluation/llm_judge.py

# Analyze tokenization
python scripts/interpretability/integrated_gradients.py
```

## What Makes This Project Unique
1. **First Bangla LLM jailbreaking study** - 230M speakers, previously untested language
2. **Bangla-specific strategies** - custom phonetic perturbations, romanization patterns, code-mixing rules
3. **Tokenization mechanism validation** - r=0.94 correlation for Bangla independently
4. **Config-driven experiments** - run_config.yaml controls everything, no code edits
5. **Standalone contributions** - findings valid independent of comparison with other languages
6. **Scalable framework** - methodology replicable for other Indic languages (Tamil, Telugu, Marathi, etc.)
