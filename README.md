# Bangla-English Code-Mixing LLM Jailbreaking Research

**Research on Bangla-English code-mixing and phonetic perturbations as a novel jailbreaking strategy for Large Language Models.**

---

## 📁 Project Structure

```
Thesis-1/
├── latex/                          # LaTeX thesis files
│   ├── thesis.tex                  # Main thesis document
│   ├── references.bib              # Bibliography
│   ├── chapters/                   # Individual thesis chapters
│   ├── images/                     # Images (university logo, etc.)
│   ├── build/                      # Build artifacts (auto-generated)
│   ├── compile_thesis.ps1          # Compilation script
│   ├── clean_build.ps1             # Clean build artifacts
│   └── README.md                   # LaTeX documentation
│
├── config/                         # Experiment configuration files
│   ├── run_config.yaml             # Main experiment control
│   ├── model_config.yaml           # Model settings
│   ├── jailbreak_templates.yaml    # Jailbreak templates
│   └── judge_prompts.yaml          # LLM-as-judge prompts
│
├── data/                           # Dataset files
│   ├── raw/                        # Original prompts (50 prompts)
│   ├── processed/                  # CM and CMP variants
│   └── annotations/                # Human annotations
│
├── scripts/                        # Python scripts
│   ├── data_preparation/           # Prompt generation
│   ├── experiments/                # Experiment runner
│   ├── evaluation/                 # LLM-as-judge evaluation
│   ├── analysis/                   # Statistical analysis
│   ├── visualization/              # Plot generation
│   └── utils/                      # Helper utilities
│
├── results/                        # Experimental results
│   ├── responses/                  # Model responses (~2,250 queries)
│   ├── metrics/                    # AASR/AARR scores
│   ├── analysis/                   # Statistical test results
│   ├── plots/                      # Visualizations
│   └── tables/                     # Result tables
│
├── docs/                           # Documentation
│   ├── BANGLA_CM_CMP_GUIDE.md      # Methodology guide
│   └── STEP*_COMPLETION_REPORT.md  # Progress reports
│
├── THESIS_REPORT.md                # Complete thesis in Markdown
├── paper.md                        # Paper draft
├── RESEARCH_CHECKLIST.md           # Research progress tracker
└── requirements.txt                # Python dependencies
```

---

## 🚀 Quick Start

### 1. Python Environment Setup

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Generate LaTeX PDF

```powershell
# Navigate to LaTeX directory
cd latex

# Compile thesis (requires MiKTeX)
.\compile_thesis.ps1

# Output: thesis.pdf
```

### 3. Run Experiments

```powershell
# Configure experiment in config/run_config.yaml

# Run experiment
python scripts/experiments/experiment_runner.py

# Evaluate results
python scripts/evaluation/llm_judge.py

# Analyze results
python scripts/analysis/statistical_tests.py
```

---

## 📊 Key Research Findings

- **46% AASR** with Bangla code-mixing + phonetic perturbations (42% improvement over English)
- **English word targeting** is 68% more effective than Bangla word perturbations
- **70:30 English:Bangla ratio** optimal for attack success
- **All 3 tested LLMs vulnerable** (Mistral-7B: 81.8%, Llama-3-8B: 22.7%, GPT-4o-mini: 16.0%)
- **Tokenization fragmentation** strongly correlates with attack success (r=0.94)

---

## 📝 Documentation

- **[LaTeX README](latex/README.md)** - Thesis compilation guide
- **[Methodology Guide](docs/BANGLA_CM_CMP_GUIDE.md)** - Code-mixing methodology
- **[Research Checklist](RESEARCH_CHECKLIST.md)** - Progress tracking
- **[Thesis Report](THESIS_REPORT.md)** - Complete thesis in Markdown

---

## 🔬 Research Methodology

**Three-Step Prompt Transformation:**

1. **English Baseline** → Hypothetical scenario framing
2. **Code-Mixing (CM)** → 70% English + 30% Bangla (romanized)
3. **Phonetic Perturbations (CMP)** → Misspell English keywords

**Experimental Design:**

- **Models:** GPT-4o-mini, Llama-3-8B, Mistral-7B (Gemma excluded due to budget)
- **Prompts:** 50 harmful prompts (10 categories)
- **Templates:** 5 jailbreak templates (None, OM, AntiLM, AIM, Sandbox)
- **Temperatures:** 0.2, 0.6, 1.0
- **Total Queries:** ~2,250 model responses
- **Budget:** ~$1 (reduced from planned $10 for 460 prompts)

---

## 📖 Citation

```bibtex
@thesis{shanto2024bangla,
  title={Bangla-English Code-Mixing and Phonetic Perturbations: A Novel Jailbreaking Strategy for Large Language Models},
  author={Shanto, Sandwip Kumar and Mridha, Md. Meraj},
  year={2024},
  school={Shahjalal University of Science and Technology},
  type={Bachelor's Thesis},
  address={Sylhet, Bangladesh}
}
```

---

## 👥 Authors

- **Sandwip Kumar Shanto** (2020831020)
- **Md. Meraj Mridha** (2020831034)

**Supervisor:** Dr. Ahsan Habib, Associate Professor, IICT, SUST

---

## ⚠️ Ethical Notice

This research involves potentially harmful content used exclusively for academic purposes to improve AI safety. The dataset is not publicly released. Findings will be responsibly disclosed to affected organizations.

---

## 📄 License

This research is for academic purposes only. Dataset available upon request with usage agreement.
