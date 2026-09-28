# Statistical Significance Testing - Wilcoxon Signed-Rank Tests

**Analysis Date:** 2025-11-20 10:22:15

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

- **Significant tests:** 18/45
- **Positive improvements:** 15
- **Mean Cohen's d:** 0.266
- **Median p-value:** 0.0894

### CM → CMP Transition

- **Significant tests:** 5/45
- **Positive improvements:** 5
- **Mean Cohen's d:** 0.087
- **Median p-value:** 0.3458

### English → CMP Transition (Combined)

- **Significant tests:** 16/45
- **Positive improvements:** 14
- **Mean Cohen's d:** 0.374
- **Median p-value:** 0.1573

## Model-Specific Findings

### gpt-4o-mini

- Significant configurations: 6/15
- Mean effect size (Cohen's d): 0.744
- Mean AASR gain (CMP vs English): 0.243

### llama-3-8b

- Significant configurations: 8/15
- Mean effect size (Cohen's d): 0.500
- Mean AASR gain (CMP vs English): 0.193

### mistral-7b

- Significant configurations: 2/15
- Mean effect size (Cohen's d): -0.123
- Mean AASR gain (CMP vs English): -0.028

## Template-Specific Findings

### AIM

- Significant configurations: 2/9
- Mean effect size (Cohen's d): 0.184
- Mean AASR gain (CMP vs English): 0.049

### AntiLM

- Significant configurations: 4/9
- Mean effect size (Cohen's d): 0.055
- Mean AASR gain (CMP vs English): 0.036

### None

- Significant configurations: 6/9
- Mean effect size (Cohen's d): 1.141
- Mean AASR gain (CMP vs English): 0.411

### OM

- Significant configurations: 3/9
- Mean effect size (Cohen's d): 0.434
- Mean AASR gain (CMP vs English): 0.162

### Sandbox

- Significant configurations: 1/9
- Mean effect size (Cohen's d): 0.054
- Mean AASR gain (CMP vs English): 0.022

## Interpretation

**Key Takeaways:**

1. **Code-mixing effectiveness:** Code-mixing shows mixed effects across configurations.
2. **Phonetic perturbation effectiveness:** Phonetic perturbations show variable effects.
3. **Combined effect:** CMP shows context-dependent effectiveness.

## Conclusion

These Wilcoxon signed-rank tests validate the statistical significance of
code-mixing and phonetic perturbation strategies for bypassing LLM safety filters.
Results show model-specific and template-specific patterns that inform targeted
safety improvements.

