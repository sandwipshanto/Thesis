# Bangla-English Code-Mixing and Phonetic Perturbations: A Novel Jailbreaking Strategy for Large Language Models

Undergraduate thesis (SWE-450), Institute of Information and Communication Technology,
Shahjalal University of Science and Technology, Sylhet. Submitted 20 December 2025.

📄 **[Read the thesis (PDF)](latex/thesis.pdf)** · 🎤 [Defense presentation](presentation/DEFENSE_PRESENTATION.md)

> ⚠️ **Content warning:** this repository contains harmful prompts and LLM outputs produced
> during red-teaming. They are shared for AI-safety research only. See [Data](#data).

---

## Summary

This is the first study of **Bangla-English (Banglish) code-mixing combined with phonetic
perturbations** as a jailbreak strategy. Each harmful prompt goes through three steps:

1. **English**: rewritten as a hypothetical scenario
2. **CM (code-mixed)**: rewritten in romanized Bangla mixed with English
3. **CMP (code-mixed + perturbed)**: sensitive English keywords are phonetically misspelled

**Setup:** 200 harmful prompts (10 categories) × 3 prompt sets × 5 jailbreak templates
(None, OM, AntiLM, AIM, Sandbox) × 3 temperatures (0.2, 0.6, 1.0) × 3 models
(GPT-4o-mini, Llama-3-8B, Mistral-7B) = **27,000 responses**, scored by GPT-4o-mini as an
LLM judge. An earlier 50-prompt run (6,750 queries) served as a validation phase.

## Key results

Average Attack Success Rate (AASR), from [`results/metrics/aasr_aarr_27000.csv`](results/metrics/aasr_aarr_27000.csv):

| Prompt set | AASR |
|---|---|
| English | 35.0% |
| CM | 39.3% |
| **CMP** | **43.9%** (English → CMP, Wilcoxon p = 0.0070) |

| Model | AASR |
|---|---|
| Mistral-7B | 86.6% |
| Llama-3-8B | 21.8% |
| GPT-4o-mini | 9.8% |

- Perturbing **English** words inside Banglish is 68% more effective than perturbing Bangla words.
- Jailbreak templates **reduce** effectiveness for Bangla: plain prompts (no template) reach
  45.9% AASR, the highest of all five templates.
- Non-standard Bangla romanization creates multiple tokenization paths, consistent with a
  token-fragmentation mechanism for bypassing safety filters.

## Repository structure

```
├── latex/                      Thesis source (thesis.tex, chapters/, references.bib) and final thesis.pdf
├── presentation/               Defense presentation and slides
├── config/                     Experiment config: models, templates, judge prompts, run settings
├── data/
│   ├── raw/                    200 English harmful prompts (10 categories)
│   ├── processed/              CM and CMP variants of each prompt
│   └── annotations/            Human annotation guidelines
├── scripts/
│   ├── data_preparation/       Prompt sampling and CM/CMP validation
│   ├── jailbreak/              Jailbreak template generation
│   ├── experiments/            Query runner (via OpenRouter) and result merging
│   ├── evaluation/             LLM-as-judge and metric calculation
│   ├── analysis/               Statistical tests and summary regeneration
│   ├── interpretability/       Integrated-gradients attribution
│   ├── visualization/          Plots and tables
│   └── utils/                  OpenRouter API client
├── results/                    Final 200-prompt run (see below)
│   └── validation_50prompts/   Earlier 50-prompt validation run, same layout
└── docs/
    ├── BANGLA_CM_CMP_GUIDE.md  Code-mixing and perturbation methodology
    ├── writeups/               Markdown version of the thesis, paper draft, summary
    └── progress/               Research checklists and step-by-step progress reports
```

## Data

Everything the reported numbers come from is included:

```
data/raw + data/processed                          input prompts
  └─ scripts/experiments/experiment_runner.py
     results/responses/responses_merged_27000.csv       27,000 model responses
     results/responses/evaluations_merged_27000.csv     judge scores + raw judge output
     results/responses/all_evaluations_merged_27000.csv judge scores (compact)
       └─ scripts/analysis/regenerate_aasr_with_none.py
          results/metrics/aasr_aarr_27000.csv            AASR / AARR per configuration
            ├─ scripts/analysis/statistical_tests.py     → results/statistics/*_20251123_181114.*
            ├─ scripts/analysis/regenerate_analysis_summaries.py → results/analysis/
            └─ scripts/visualization/results_plotter.py  → results/plots/, results/tables/
```

Note: 58 of the 27,000 responses have no judge evaluation, so metrics are computed over 26,942
evaluated responses.

The response files contain real harmful model outputs. Please use them only for safety research
and do not redistribute them outside that context.

## Reproducing

```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Re-run analysis from the included data (no API key needed); run from the repo root
python scripts/analysis/regenerate_aasr_with_none.py
python scripts/analysis/statistical_tests.py
python scripts/analysis/regenerate_analysis_summaries.py
python scripts/visualization/results_plotter.py

# Re-run the experiment itself (needs an OpenRouter API key in .env; costs ~$1.50)
python scripts/experiments/experiment_runner.py --config config/run_config.yaml
python scripts/experiments/merge_results.py
```

To build the thesis PDF, see [latex/README.md](latex/README.md) (pdfLaTeX + BibTeX, e.g.
`latex/compile_thesis.ps1` on Windows).

## Authors

- **Sandwip Kumar Shanto** (2020831020)
- **Md. Meraj Mridha** (2020831034)

**Supervisor:** Dr. Ahsan Habib, Associate Professor, IICT, SUST

## Citation

```bibtex
@thesis{shanto2025bangla,
  title   = {Bangla-English Code-Mixing and Phonetic Perturbations: A Novel Jailbreaking Strategy for Large Language Models},
  author  = {Shanto, Sandwip Kumar and Mridha, Md. Meraj},
  year    = {2025},
  school  = {Shahjalal University of Science and Technology},
  type    = {Bachelor's Thesis},
  address = {Sylhet, Bangladesh}
}
```

## Ethics

This work studies LLM vulnerabilities in order to improve safety for Bangla speakers. The
prompts and responses are released for research and reproducibility; please use them
responsibly.
