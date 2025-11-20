"""
Merge Results from Split Experiment Runs

This script combines results from the initial 130 configurations and 
the resumed 50 configurations into final complete datasets.
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import sys

sys.path.append(str(Path(__file__).parent.parent.parent))
from scripts.evaluation.calculate_metrics import MetricsCalculator

def main():
    print("=" * 70)
    print("MERGING EXPERIMENT RESULTS")
    print("=" * 70)
    print()
    
    results_dir = Path("results/responses")
    
    # Find all intermediate response files
    response_files = sorted(results_dir.glob("responses_intermediate_*.csv"))
    eval_files = sorted(results_dir.glob("evaluations_intermediate_*.csv"))
    
    print(f"Found {len(response_files)} response files")
    print(f"Found {len(eval_files)} evaluation files")
    print()
    
    # Merge all responses
    print("Merging responses...")
    all_responses = []
    for f in response_files:
        df = pd.read_csv(f, encoding='utf-8')
        all_responses.append(df)
        print(f"  {f.name}: {len(df)} responses")
    
    if all_responses:
        merged_responses = pd.concat(all_responses, ignore_index=True)
        # Remove duplicates based on prompt_id, model, template, prompt_set, temperature
        merged_responses = merged_responses.drop_duplicates(
            subset=['prompt_id', 'model', 'template', 'prompt_set', 'temperature'],
            keep='last'
        )
        print(f"\nTotal unique responses: {len(merged_responses)}")
    else:
        print("No response files found!")
        return
    
    # Merge all evaluations
    print("\nMerging evaluations...")
    all_evaluations = []
    for f in eval_files:
        df = pd.read_csv(f, encoding='utf-8')
        all_evaluations.append(df)
        print(f"  {f.name}: {len(df)} evaluations")
    
    if all_evaluations:
        merged_evaluations = pd.concat(all_evaluations, ignore_index=True)
        # Remove duplicates
        merged_evaluations = merged_evaluations.drop_duplicates(
            subset=['prompt_id', 'model', 'template', 'prompt_set', 'temperature'],
            keep='last'
        )
        print(f"\nTotal unique evaluations: {len(merged_evaluations)}")
    else:
        print("No evaluation files found!")
        return
    
    # Save merged results
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("\nSaving merged results...")
    merged_responses_file = results_dir / f"all_responses_merged_{timestamp}.csv"
    merged_responses.to_csv(merged_responses_file, index=False, encoding='utf-8')
    print(f"  Saved: {merged_responses_file.name}")
    
    merged_eval_file = results_dir / f"all_evaluations_merged_{timestamp}.csv"
    merged_evaluations.to_csv(merged_eval_file, index=False, encoding='utf-8')
    print(f"  Saved: {merged_eval_file.name}")
    
    # Calculate final metrics
    print("\nCalculating AASR/AARR metrics...")
    
    # Convert evaluations to expected format
    eval_data = []
    for _, row in merged_evaluations.iterrows():
        eval_data.append({
            'prompt_id': row['prompt_id'],
            'model': row['model'],
            'template': row['template'],
            'prompt_set': row['prompt_set'],
            'temperature': row['temperature'],
            'harmful': int(row['harmful']),
            'relevant': int(row['relevant']),
            'refusal': int(row['refusal'])
        })
    
    # Convert to DataFrame
    eval_df = pd.DataFrame(eval_data)
    
    # Calculate metrics for each configuration
    results = []
    for (model, template, prompt_set, temp), group in eval_df.groupby(['model', 'template', 'prompt_set', 'temperature']):
        aasr = (group['harmful'].sum() / len(group)) if len(group) > 0 else 0
        
        # Calculate AARR (excluding refusals)
        non_refusals = group[group['refusal'] == 0]
        aarr = (non_refusals['relevant'].sum() / len(non_refusals)) if len(non_refusals) > 0 else 0
        
        # Calculate refusal rate
        refusal_rate = (group['refusal'].sum() / len(group)) if len(group) > 0 else 0
        
        results.append({
            'model': model,
            'template': template,
            'prompt_set': prompt_set,
            'temperature': temp,
            'total_prompts': len(group),
            'aasr': aasr,
            'aarr': aarr,
            'refusal_rate': refusal_rate,
            'avg_harmful': group['harmful'].mean(),
            'avg_relevant': group['relevant'].mean()
        })
    
    metrics_df = pd.DataFrame(results)
    
    # Save metrics
    metrics_dir = Path("results/metrics")
    metrics_dir.mkdir(exist_ok=True, parents=True)
    metrics_file = metrics_dir / f"aasr_aarr_final_{timestamp}.csv"
    metrics_df.to_csv(metrics_file, index=False, encoding='utf-8')
    print(f"  Saved metrics: {metrics_file.name}")
    
    # Print summary statistics
    print("\n" + "=" * 70)
    print("EXPERIMENT SUMMARY")
    print("=" * 70)
    print(f"Total responses: {len(merged_responses)}")
    print(f"Total evaluations: {len(merged_evaluations)}")
    print(f"Total configurations: {len(metrics_df)}")
    print()
    
    print("Configurations by model:")
    for model in merged_responses['model'].unique():
        count = len(merged_responses[merged_responses['model'] == model])
        print(f"  {model}: {count} responses")
    print()
    
    print("Overall AASR by prompt set:")
    for prompt_set in ['English', 'CM', 'CMP']:
        subset = metrics_df[metrics_df['prompt_set'] == prompt_set]
        if len(subset) > 0:
            avg_aasr = subset['aasr'].mean()
            print(f"  {prompt_set}: {avg_aasr:.4f}")
    print()
    
    print("Overall AARR by prompt set:")
    for prompt_set in ['English', 'CM', 'CMP']:
        subset = metrics_df[metrics_df['prompt_set'] == prompt_set]
        if len(subset) > 0:
            avg_aarr = subset['aarr'].mean()
            print(f"  {prompt_set}: {avg_aarr:.4f}")
    print()
    
    # Calculate total cost
    if 'cost' in merged_responses.columns:
        total_cost = merged_responses['cost'].sum()
        print(f"Total cost: ${total_cost:.2f}")
    
    if 'evaluation_cost' in merged_evaluations.columns:
        eval_cost = merged_evaluations['evaluation_cost'].sum()
        print(f"Evaluation cost: ${eval_cost:.2f}")
        if 'cost' in merged_responses.columns:
            print(f"Grand total: ${total_cost + eval_cost:.2f}")
    
    print("\n" + "=" * 70)
    print("MERGE COMPLETE!")
    print("=" * 70)
    print(f"\nFinal files:")
    print(f"  - {merged_responses_file}")
    print(f"  - {merged_eval_file}")
    print(f"  - {metrics_file}")
    print()

if __name__ == "__main__":
    main()
