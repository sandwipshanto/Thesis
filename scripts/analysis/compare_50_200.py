"""
Compare 50-prompt vs 200-prompt experiment results
"""

import pandas as pd
import numpy as np

# Load both datasets
old_50 = pd.read_csv('results/metrics/aasr_aarr_final_20251120_095257.csv')
new_200 = pd.read_csv('results/metrics/aasr_aarr_27000.csv')

print("=" * 70)
print("50-PROMPT vs 200-PROMPT COMPARISON")
print("=" * 70)

# Overall AASR by prompt set
print("\n### OVERALL AASR BY PROMPT SET ###")
old_summary = old_50.groupby('prompt_set')['aasr'].mean()
new_summary = new_200.groupby('prompt_set')['aasr'].mean()

comparison_df = pd.DataFrame({
    '50 Prompts': old_summary,
    '200 Prompts': new_summary,
    'Change (%)': ((new_summary - old_summary) / old_summary * 100).round(2)
})

print(comparison_df)

# Model-specific comparison
print("\n### MODEL-SPECIFIC COMPARISON (CMP variant) ###")
models = ['gpt-4o-mini', 'llama-3-8b', 'mistral-7b']

model_comparison = []
for model in models:
    old_aasr = old_50[(old_50['model'] == model) & (old_50['prompt_set'] == 'CMP')]['aasr'].mean()
    new_aasr = new_200[(new_200['model'] == model) & (new_200['prompt_set'] == 'CMP')]['aasr'].mean()
    change = ((new_aasr - old_aasr) / old_aasr * 100) if old_aasr > 0 else 0
    
    model_comparison.append({
        'Model': model,
        '50 Prompts': f"{old_aasr:.1%}",
        '200 Prompts': f"{new_aasr:.1%}",
        'Change': f"{change:+.1f}%"
    })

model_df = pd.DataFrame(model_comparison)
print(model_df.to_string(index=False))

# Statistical power comparison
print("\n### STATISTICAL SIGNIFICANCE COMPARISON ###")
print("\nFrom Wilcoxon tests:")
print("Transition      | 50 Prompts | 200 Prompts (27k)")
print("----------------|------------|-------------------")
print("English → CM    | ~0.001     | 0.0209")
print("CM → CMP        | ~0.023     | 0.1291")
print("English → CMP   | ~0.001     | 0.0070")

# Variance comparison
print("\n### VARIANCE COMPARISON ###")
old_variance = old_50.groupby('prompt_set')['aasr'].std()
new_variance = new_200.groupby('prompt_set')['aasr'].std()

variance_df = pd.DataFrame({
    '50 Prompts (SD)': old_variance,
    '200 Prompts (SD)': new_variance,
    'Reduction (%)': ((old_variance - new_variance) / old_variance * 100).round(2)
})
print(variance_df)

# Sample size
print("\n### SAMPLE SIZE ###")
print(f"50 prompts:  {len(old_50)} configurations × 50 prompts = ~6,750 queries")
print(f"200 prompts: {len(new_200)} configurations × 200 prompts = 36,000 queries (27,000 collected)")
print(f"Statistical power improvement: 4× larger sample")

# Export comparison table
output_path = 'results/tables/50_vs_200_comparison.csv'
comparison_df.to_csv(output_path)
print(f"\n✓ Saved comparison table to: {output_path}")

print("\n" + "=" * 70)
print("COMPARISON COMPLETE")
print("=" * 70)
