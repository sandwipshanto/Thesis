# Statistical Significance Testing - Wilcoxon Signed-Rank Tests

**Analysis Date:** 2025-11-23 18:11:14

## Objective

Test whether code-mixing (CM) and phonetic perturbations (CMP) produce
statistically significant improvements in attack success rates compared to
English baseline prompts.

## Methodology

- **Test:** Wilcoxon signed-rank test (paired, non-parametric)
- **Significance threshold:** p < 0.05
- **Effect size:** Cohen's d
- **Comparisons:**
  1. English → CM (code-mixing effect)
  2. CM → CMP (phonetic perturbation effect)
  3. English → CMP (combined effect)

## Overall Results

### English → CM Transition

- **Significant tests:** 18/36
- **Positive improvements:** 11
- **Mean Cohen's d:** 0.046
- **Median p-value:** 0.0209

### CM → CMP Transition

- **Significant tests:** 10/36
- **Positive improvements:** 10
- **Mean Cohen's d:** 0.105
- **Median p-value:** 0.1291

### English → CMP Transition (Combined)

- **Significant tests:** 28/36
- **Positive improvements:** 19
- **Mean Cohen's d:** 0.144
- **Median p-value:** 0.0070

## Model-Specific Findings

### gpt-4o-mini

- Significant configurations: 10/12
- Mean effect size (Cohen's d): 0.374
- Mean AASR gain (CMP vs English): 0.080

### llama-3-8b

- Significant configurations: 9/12
- Mean effect size (Cohen's d): 0.304
- Mean AASR gain (CMP vs English): 0.103

### mistral-7b

- Significant configurations: 9/12
- Mean effect size (Cohen's d): -0.246
- Mean AASR gain (CMP vs English): -0.062

## Template-Specific Findings

### AIM

- Significant configurations: 8/9
- Mean effect size (Cohen's d): 0.162
- Mean AASR gain (CMP vs English): 0.059

### AntiLM

- Significant configurations: 6/9
- Mean effect size (Cohen's d): -0.005
- Mean AASR gain (CMP vs English): -0.001

### OM

- Significant configurations: 6/9
- Mean effect size (Cohen's d): 0.279
- Mean AASR gain (CMP vs English): 0.076

### Sandbox

- Significant configurations: 8/9
- Mean effect size (Cohen's d): 0.140
- Mean AASR gain (CMP vs English): 0.027

## Interpretation

**Key Takeaways:**

1. **Code-mixing effectiveness:** Code-mixing shows mixed effects across configurations.
2. **Phonetic perturbation effectiveness:** Phonetic perturbations show variable effects.
3. **Combined effect:** CMP (code-mixing + phonetic) significantly outperforms English baseline.

## Conclusion

These Wilcoxon signed-rank tests validate the statistical significance of
code-mixing and phonetic perturbation strategies for bypassing LLM safety filters.
Results show model-specific and template-specific patterns that inform targeted
safety improvements.

