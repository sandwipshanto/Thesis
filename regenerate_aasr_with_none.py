import pandas as pd
import numpy as np

# Load merged evaluations
print("Loading all_evaluations_merged_27000.csv...")
df = pd.read_csv('results/responses/all_evaluations_merged_27000.csv')

print(f"Total rows: {len(df)}")
print(f"Empty template rows: {(df['template'] == '').sum()}")
print(f"Non-empty template rows: {(df['template'] != '').sum()}")

# Replace empty template with 'None'
df['template'] = df['template'].replace('', 'None')
df['template'] = df['template'].fillna('None')

print(f"\nAfter replacement:")
print(f"None template rows: {(df['template'] == 'None').sum()}")

# Check template distribution
print(f"\nTemplate distribution:")
print(df['template'].value_counts().sort_index())

# Calculate AASR and AARR for each configuration
print("\nCalculating AASR metrics...")
results = []
for (model, template, prompt_set, temp), group in df.groupby(['model', 'template', 'prompt_set', 'temperature']):
    aasr = group['harmful'].mean()
    aarr = group['relevant'].mean()
    refusal_rate = group['refusal'].mean()
    total = len(group)
    
    results.append({
        'model': model,
        'template': template,
        'prompt_set': prompt_set,
        'temperature': temp,
        'aasr': aasr,
        'aarr': aarr,
        'refusal_rate': refusal_rate,
        'total_responses': total
    })

# Create results dataframe
results_df = pd.DataFrame(results)

# Sort by model, template, prompt_set, temperature
results_df = results_df.sort_values(['model', 'template', 'prompt_set', 'temperature'])

# Save to new CSV (replacing old one)
output_file = 'results/metrics/aasr_aarr_27000.csv'
results_df.to_csv(output_file, index=False)

print(f'\n✓ Generated {output_file}')
print(f'✓ Total configurations: {len(results_df)}')
print(f'\n=== Template breakdown ===')
print(results_df['template'].value_counts().sort_index())

print(f'\n=== Overall AASR by prompt_set ===')
for ps, aasr in results_df.groupby('prompt_set')['aasr'].mean().items():
    print(f"{ps:10s}: {aasr:.3f} ({aasr*100:.1f}%)")

print(f'\n=== Overall AASR by template (DESCENDING) ===')
for template, aasr in results_df.groupby('template')['aasr'].mean().sort_values(ascending=False).items():
    print(f"{template:10s}: {aasr:.3f} ({aasr*100:.1f}%)")

print(f'\n=== Model-specific AASR by prompt_set ===')
for model in ['gpt-4o-mini', 'llama-3-8b', 'mistral-7b']:
    model_df = results_df[results_df['model'] == model]
    print(f"\n{model}:")
    for ps, aasr in model_df.groupby('prompt_set')['aasr'].mean().items():
        print(f"  {ps:10s}: {aasr:.3f} ({aasr*100:.1f}%)")

print("\n✓ Regeneration complete!")
