"""
Regenerate all analysis summary files with correct 200-prompt data including None template
"""
import pandas as pd
import numpy as np
from datetime import datetime

# Load the regenerated AASR data with None template
print("Loading aasr_aarr_27000.csv...")
df = pd.read_csv('results/metrics/aasr_aarr_27000.csv')

print(f"Total rows: {len(df)}")
print(f"Templates: {sorted(df['template'].unique())}")
print(f"Models: {sorted(df['model'].unique())}")
print(f"Prompt sets: {sorted(df['prompt_set'].unique())}")

# === 1. Prompt Set Comparison ===
print("\n=== Generating prompt_set_comparison.csv ===")
prompt_set_stats = df.groupby('prompt_set').agg({
    'aasr': ['mean', 'std', 'min', 'max'],
    'aarr': ['mean', 'std'],
    'refusal_rate': 'mean'
}).round(4)

prompt_set_stats.columns = ['_'.join(col).strip() for col in prompt_set_stats.columns.values]
prompt_set_stats = prompt_set_stats.reset_index()
prompt_set_stats.to_csv('results/analysis/prompt_set_comparison.csv', index=False)
print(prompt_set_stats)

# === 2. Template Effectiveness ===
print("\n=== Generating template_effectiveness.csv ===")
template_stats = df.groupby('template').agg({
    'aasr': ['mean', 'std', 'min', 'max'],
    'aarr': ['mean', 'std'],
    'refusal_rate': 'mean'
}).round(4)

template_stats.columns = ['_'.join(col).strip() for col in template_stats.columns.values]
template_stats = template_stats.reset_index()
template_stats = template_stats.sort_values('aasr_mean', ascending=False)  # Sort by AASR descending
template_stats.to_csv('results/analysis/template_effectiveness.csv', index=False)
print(template_stats)

# === 3. Model Vulnerability ===
print("\n=== Generating model_vulnerability.csv ===")
model_stats = df.groupby('model').agg({
    'aasr': ['mean', 'std', 'min', 'max'],
    'aarr': ['mean', 'std'],
    'refusal_rate': 'mean'
}).round(4)

model_stats.columns = ['_'.join(col).strip() for col in model_stats.columns.values]
model_stats = model_stats.reset_index()
model_stats = model_stats.sort_values('aasr_mean', ascending=False)  # Sort by AASR descending
model_stats.to_csv('results/analysis/model_vulnerability.csv', index=False)
print(model_stats)

# === 4. Model x Prompt Set Interaction ===
print("\n=== Generating model_promptset_interaction.csv ===")
model_ps_stats = df.groupby(['model', 'prompt_set']).agg({
    'aasr': 'mean',
    'aarr': 'mean',
    'refusal_rate': 'mean'
}).round(4).reset_index()
model_ps_stats.to_csv('results/analysis/model_promptset_interaction.csv', index=False)
print(model_ps_stats)

# === 5. Model x Template Interaction ===
print("\n=== Generating model_template_interaction.csv ===")
model_temp_stats = df.groupby(['model', 'template']).agg({
    'aasr': 'mean',
    'aarr': 'mean',
    'refusal_rate': 'mean'
}).round(4).reset_index()
model_temp_stats.to_csv('results/analysis/model_template_interaction.csv', index=False)
print(model_temp_stats)

# === 6. Temperature Sensitivity ===
print("\n=== Generating temperature_sensitivity.csv ===")
temp_stats = df.groupby('temperature').agg({
    'aasr': ['mean', 'std'],
    'aarr': ['mean', 'std'],
    'refusal_rate': 'mean'
}).round(4)

temp_stats.columns = ['_'.join(col).strip() for col in temp_stats.columns.values]
temp_stats = temp_stats.reset_index()
temp_stats.to_csv('results/analysis/temperature_sensitivity.csv', index=False)
print(temp_stats)

# === 7. Statistical Summary (Text Report) ===
print("\n=== Generating statistical_summary.txt ===")
with open('results/analysis/statistical_summary.txt', 'w', encoding='utf-8') as f:
    f.write("="*80 + "\n")
    f.write("STATISTICAL SUMMARY - 200 Prompt Dataset (with None Template)\n")
    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("="*80 + "\n\n")
    
    # Overall statistics
    f.write("OVERALL STATISTICS\n")
    f.write("-"*80 + "\n")
    f.write(f"Total configurations: {len(df)}\n")
    f.write(f"Average AASR: {df['aasr'].mean():.3f} ({df['aasr'].mean()*100:.1f}%)\n")
    f.write(f"Average AARR: {df['aarr'].mean():.3f} ({df['aarr'].mean()*100:.1f}%)\n")
    f.write(f"Average Refusal Rate: {df['refusal_rate'].mean():.3f} ({df['refusal_rate'].mean()*100:.1f}%)\n\n")
    
    # By Prompt Set
    f.write("BY PROMPT SET\n")
    f.write("-"*80 + "\n")
    for ps in ['English', 'CM', 'CMP']:
        ps_df = df[df['prompt_set'] == ps]
        f.write(f"{ps:10s}: AASR={ps_df['aasr'].mean():.3f} ({ps_df['aasr'].mean()*100:.1f}%), ")
        f.write(f"AARR={ps_df['aarr'].mean():.3f}, ")
        f.write(f"Refusal={ps_df['refusal_rate'].mean():.3f}\n")
    f.write("\n")
    
    # By Template (DESCENDING)
    f.write("BY TEMPLATE (DESCENDING ORDER)\n")
    f.write("-"*80 + "\n")
    for template in template_stats['template']:
        temp_df = df[df['template'] == template]
        f.write(f"{template:10s}: AASR={temp_df['aasr'].mean():.3f} ({temp_df['aasr'].mean()*100:.1f}%), ")
        f.write(f"AARR={temp_df['aarr'].mean():.3f}, ")
        f.write(f"Refusal={temp_df['refusal_rate'].mean():.3f}\n")
    f.write("\n")
    
    # By Model
    f.write("BY MODEL (DESCENDING ORDER)\n")
    f.write("-"*80 + "\n")
    for model in model_stats['model']:
        model_df = df[df['model'] == model]
        f.write(f"{model:15s}: AASR={model_df['aasr'].mean():.3f} ({model_df['aasr'].mean()*100:.1f}%), ")
        f.write(f"AARR={model_df['aarr'].mean():.3f}, ")
        f.write(f"Refusal={model_df['refusal_rate'].mean():.3f}\n")
    f.write("\n")
    
    # Model x Prompt Set Detail
    f.write("MODEL-SPECIFIC AASR BY PROMPT SET\n")
    f.write("-"*80 + "\n")
    for model in ['gpt-4o-mini', 'llama-3-8b', 'mistral-7b']:
        f.write(f"\n{model}:\n")
        for ps in ['English', 'CM', 'CMP']:
            subset = df[(df['model'] == model) & (df['prompt_set'] == ps)]
            f.write(f"  {ps:10s}: {subset['aasr'].mean():.3f} ({subset['aasr'].mean()*100:.1f}%)\n")
    f.write("\n")
    
    # KEY FINDINGS
    f.write("="*80 + "\n")
    f.write("KEY FINDINGS\n")
    f.write("="*80 + "\n")
    f.write("1. CODE-MIXING EFFECTIVENESS:\n")
    f.write(f"   - English baseline: {df[df['prompt_set']=='English']['aasr'].mean()*100:.1f}%\n")
    f.write(f"   - Code-Mixed (CM): {df[df['prompt_set']=='CM']['aasr'].mean()*100:.1f}% (+{(df[df['prompt_set']=='CM']['aasr'].mean() - df[df['prompt_set']=='English']['aasr'].mean())*100:.1f}pp)\n")
    f.write(f"   - CM with Perturbations (CMP): {df[df['prompt_set']=='CMP']['aasr'].mean()*100:.1f}% (+{(df[df['prompt_set']=='CMP']['aasr'].mean() - df[df['prompt_set']=='English']['aasr'].mean())*100:.1f}pp)\n\n")
    
    f.write("2. TEMPLATE EFFECT (SURPRISING FINDING):\n")
    f.write(f"   - None (baseline): {df[df['template']=='None']['aasr'].mean()*100:.1f}% ← HIGHEST\n")
    f.write(f"   - AntiLM: {df[df['template']=='AntiLM']['aasr'].mean()*100:.1f}% ({(df[df['template']=='AntiLM']['aasr'].mean() - df[df['template']=='None']['aasr'].mean())*100:.1f}pp vs None)\n")
    f.write(f"   - AIM: {df[df['template']=='AIM']['aasr'].mean()*100:.1f}% ({(df[df['template']=='AIM']['aasr'].mean() - df[df['template']=='None']['aasr'].mean())*100:.1f}pp vs None)\n")
    f.write(f"   - OM: {df[df['template']=='OM']['aasr'].mean()*100:.1f}% ({(df[df['template']=='OM']['aasr'].mean() - df[df['template']=='None']['aasr'].mean())*100:.1f}pp vs None)\n")
    f.write(f"   - Sandbox: {df[df['template']=='Sandbox']['aasr'].mean()*100:.1f}% ({(df[df['template']=='Sandbox']['aasr'].mean() - df[df['template']=='None']['aasr'].mean())*100:.1f}pp vs None)\n")
    f.write("   → Most jailbreak templates REDUCE attack success!\n\n")
    
    f.write("3. MODEL VULNERABILITY:\n")
    f.write(f"   - Mistral-7B: {df[df['model']=='mistral-7b']['aasr'].mean()*100:.1f}% (CRITICAL)\n")
    f.write(f"   - Llama-3-8B: {df[df['model']=='llama-3-8b']['aasr'].mean()*100:.1f}% (MODERATE)\n")
    f.write(f"   - GPT-4o-mini: {df[df['model']=='gpt-4o-mini']['aasr'].mean()*100:.1f}% (LOW)\n\n")

print("\n✅ All summary files regenerated successfully!")
print("\nFiles updated:")
print("  - results/analysis/prompt_set_comparison.csv")
print("  - results/analysis/template_effectiveness.csv")
print("  - results/analysis/model_vulnerability.csv")
print("  - results/analysis/model_promptset_interaction.csv")
print("  - results/analysis/model_template_interaction.csv")
print("  - results/analysis/temperature_sensitivity.csv")
print("  - results/analysis/statistical_summary.txt")
