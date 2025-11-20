"""
Statistical Analysis for Bangla-English LLM Red-Teaming

This script performs comprehensive statistical analysis on the experiment results:
1. Model comparison (vulnerability ranking)
2. Template effectiveness analysis
3. Prompt set comparison (English vs CM vs CMP)
4. Temperature sensitivity analysis
5. Statistical significance testing (t-tests, ANOVA)
6. Effectiveness gain calculations

Based on: "Haet Bhasha aur Diskrimineshun" (arXiv:2505.14226)
Extension: Bangla-English code-mixed jailbreaking
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class StatisticalAnalyzer:
    """Perform statistical analysis on red-teaming results."""
    
    def __init__(self, metrics_file: str, evaluations_file: str):
        """
        Initialize analyzer with results.
        
        Args:
            metrics_file: Path to AASR/AARR metrics CSV
            evaluations_file: Path to evaluations CSV
        """
        self.metrics_df = pd.read_csv(metrics_file)
        self.eval_df = pd.read_csv(evaluations_file)
        
        print(f"Loaded {len(self.metrics_df)} configurations")
        print(f"Loaded {len(self.eval_df)} evaluations")
        print()
    
    def model_vulnerability_ranking(self) -> pd.DataFrame:
        """
        Rank models by vulnerability (average AASR across all configs).
        
        Returns:
            DataFrame with model rankings
        """
        print("=" * 70)
        print("MODEL VULNERABILITY RANKING")
        print("=" * 70)
        print()
        
        model_stats = self.metrics_df.groupby('model').agg({
            'aasr': ['mean', 'std', 'min', 'max'],
            'aarr': ['mean', 'std'],
            'refusal_rate': 'mean'
        }).round(4)
        
        # Flatten column names
        model_stats.columns = ['_'.join(col).strip() for col in model_stats.columns.values]
        model_stats = model_stats.sort_values('aasr_mean', ascending=False)
        
        print("Model Rankings (by average AASR):")
        print(model_stats)
        print()
        
        return model_stats
    
    def template_effectiveness(self) -> pd.DataFrame:
        """
        Analyze jailbreak template effectiveness.
        
        Returns:
            DataFrame with template effectiveness
        """
        print("=" * 70)
        print("TEMPLATE EFFECTIVENESS ANALYSIS")
        print("=" * 70)
        print()
        
        template_stats = self.metrics_df.groupby('template').agg({
            'aasr': ['mean', 'std', 'min', 'max'],
            'aarr': ['mean', 'std'],
            'refusal_rate': 'mean'
        }).round(4)
        
        template_stats.columns = ['_'.join(col).strip() for col in template_stats.columns.values]
        template_stats = template_stats.sort_values('aasr_mean', ascending=False)
        
        print("Template Rankings (by average AASR):")
        print(template_stats)
        print()
        
        return template_stats
    
    def prompt_set_comparison(self) -> pd.DataFrame:
        """
        Compare English vs CM vs CMP effectiveness.
        
        Returns:
            DataFrame with prompt set comparisons
        """
        print("=" * 70)
        print("PROMPT SET COMPARISON (English vs CM vs CMP)")
        print("=" * 70)
        print()
        
        prompt_stats = self.metrics_df.groupby('prompt_set').agg({
            'aasr': ['mean', 'std', 'min', 'max'],
            'aarr': ['mean', 'std'],
            'refusal_rate': 'mean'
        }).round(4)
        
        prompt_stats.columns = ['_'.join(col).strip() for col in prompt_stats.columns.values]
        
        # Reorder to English -> CM -> CMP
        prompt_stats = prompt_stats.reindex(['English', 'CM', 'CMP'])
        
        print("Prompt Set Statistics:")
        print(prompt_stats)
        print()
        
        # Calculate effectiveness gains
        english_aasr = prompt_stats.loc['English', 'aasr_mean']
        cm_aasr = prompt_stats.loc['CM', 'aasr_mean']
        cmp_aasr = prompt_stats.loc['CMP', 'aasr_mean']
        
        cm_gain = ((cm_aasr - english_aasr) / english_aasr * 100) if english_aasr > 0 else 0
        cmp_gain = ((cmp_aasr - english_aasr) / english_aasr * 100) if english_aasr > 0 else 0
        
        print(f"Effectiveness Gains (over English baseline):")
        print(f"  CM:  {cm_gain:+.1f}%")
        print(f"  CMP: {cmp_gain:+.1f}%")
        print()
        
        return prompt_stats
    
    def temperature_sensitivity(self) -> pd.DataFrame:
        """
        Analyze temperature impact on AASR/AARR.
        
        Returns:
            DataFrame with temperature analysis
        """
        print("=" * 70)
        print("TEMPERATURE SENSITIVITY ANALYSIS")
        print("=" * 70)
        print()
        
        temp_stats = self.metrics_df.groupby('temperature').agg({
            'aasr': ['mean', 'std'],
            'aarr': ['mean', 'std'],
            'refusal_rate': 'mean'
        }).round(4)
        
        temp_stats.columns = ['_'.join(col).strip() for col in temp_stats.columns.values]
        temp_stats = temp_stats.sort_index()
        
        print("Temperature Impact:")
        print(temp_stats)
        print()
        
        return temp_stats
    
    def statistical_significance_tests(self) -> Dict:
        """
        Perform t-tests and ANOVA for statistical significance.
        
        Returns:
            Dictionary with test results
        """
        print("=" * 70)
        print("STATISTICAL SIGNIFICANCE TESTS")
        print("=" * 70)
        print()
        
        results = {}
        
        # T-test: English vs CM
        english_aasr = self.metrics_df[self.metrics_df['prompt_set'] == 'English']['aasr']
        cm_aasr = self.metrics_df[self.metrics_df['prompt_set'] == 'CM']['aasr']
        cmp_aasr = self.metrics_df[self.metrics_df['prompt_set'] == 'CMP']['aasr']
        
        t_stat_cm, p_value_cm = stats.ttest_ind(english_aasr, cm_aasr)
        t_stat_cmp, p_value_cmp = stats.ttest_ind(english_aasr, cmp_aasr)
        
        print("T-tests (English vs CM/CMP):")
        print(f"  English vs CM:  t={t_stat_cm:.4f}, p={p_value_cm:.6f}")
        print(f"  English vs CMP: t={t_stat_cmp:.4f}, p={p_value_cmp:.6f}")
        
        if p_value_cm < 0.05:
            print(f"  ✓ CM is significantly different from English (p < 0.05)")
        if p_value_cmp < 0.05:
            print(f"  ✓ CMP is significantly different from English (p < 0.05)")
        print()
        
        results['t_test_cm'] = {'t_stat': t_stat_cm, 'p_value': p_value_cm}
        results['t_test_cmp'] = {'t_stat': t_stat_cmp, 'p_value': p_value_cmp}
        
        # ANOVA: Models
        model_groups = [self.metrics_df[self.metrics_df['model'] == m]['aasr'].values 
                       for m in self.metrics_df['model'].unique()]
        f_stat, p_value = stats.f_oneway(*model_groups)
        
        print(f"ANOVA (Model differences):")
        print(f"  F={f_stat:.4f}, p={p_value:.6f}")
        if p_value < 0.05:
            print(f"  ✓ Models have significantly different vulnerabilities (p < 0.05)")
        print()
        
        results['anova_models'] = {'f_stat': f_stat, 'p_value': p_value}
        
        # ANOVA: Templates
        template_groups = [self.metrics_df[self.metrics_df['template'] == t]['aasr'].values 
                          for t in self.metrics_df['template'].unique()]
        f_stat, p_value = stats.f_oneway(*template_groups)
        
        print(f"ANOVA (Template differences):")
        print(f"  F={f_stat:.4f}, p={p_value:.6f}")
        if p_value < 0.05:
            print(f"  ✓ Templates have significantly different effectiveness (p < 0.05)")
        print()
        
        results['anova_templates'] = {'f_stat': f_stat, 'p_value': p_value}
        
        return results
    
    def model_template_interaction(self) -> pd.DataFrame:
        """
        Analyze model-template interaction effects.
        
        Returns:
            Pivot table of model × template AASR
        """
        print("=" * 70)
        print("MODEL × TEMPLATE INTERACTION")
        print("=" * 70)
        print()
        
        pivot = self.metrics_df.pivot_table(
            values='aasr',
            index='model',
            columns='template',
            aggfunc='mean'
        ).round(4)
        
        print("Average AASR by Model × Template:")
        print(pivot)
        print()
        
        # Find best template for each model
        print("Best template for each model:")
        for model in pivot.index:
            best_template = pivot.loc[model].idxmax()
            best_aasr = pivot.loc[model].max()
            print(f"  {model}: {best_template} (AASR={best_aasr:.4f})")
        print()
        
        return pivot
    
    def model_promptset_interaction(self) -> pd.DataFrame:
        """
        Analyze model-prompt set interaction effects.
        
        Returns:
            Pivot table of model × prompt set AASR
        """
        print("=" * 70)
        print("MODEL × PROMPT SET INTERACTION")
        print("=" * 70)
        print()
        
        pivot = self.metrics_df.pivot_table(
            values='aasr',
            index='model',
            columns='prompt_set',
            aggfunc='mean'
        ).round(4)
        
        # Reorder columns
        pivot = pivot[['English', 'CM', 'CMP']]
        
        print("Average AASR by Model × Prompt Set:")
        print(pivot)
        print()
        
        # Calculate effectiveness gain per model
        print("Effectiveness Gain (CMP vs English) by Model:")
        for model in pivot.index:
            english = pivot.loc[model, 'English']
            cmp = pivot.loc[model, 'CMP']
            gain = ((cmp - english) / english * 100) if english > 0 else 0
            print(f"  {model}: {gain:+.1f}%")
        print()
        
        return pivot
    
    def generate_summary_report(self, output_file: str):
        """
        Generate comprehensive summary report.
        
        Args:
            output_file: Path to save summary report
        """
        print("=" * 70)
        print("GENERATING SUMMARY REPORT")
        print("=" * 70)
        print()
        
        report = []
        report.append("=" * 70)
        report.append("STATISTICAL ANALYSIS SUMMARY")
        report.append("Bangla-English LLM Red-Teaming")
        report.append("=" * 70)
        report.append("")
        
        # Overall statistics
        report.append("OVERALL STATISTICS")
        report.append("-" * 70)
        report.append(f"Total configurations: {len(self.metrics_df)}")
        report.append(f"Total evaluations: {len(self.eval_df)}")
        report.append(f"Models tested: {', '.join(self.metrics_df['model'].unique())}")
        report.append(f"Templates tested: {', '.join(self.metrics_df['template'].unique())}")
        report.append(f"Temperatures tested: {', '.join(map(str, sorted(self.metrics_df['temperature'].unique())))}")
        report.append("")
        
        # Key findings
        report.append("KEY FINDINGS")
        report.append("-" * 70)
        
        # Prompt set effectiveness
        prompt_stats = self.metrics_df.groupby('prompt_set')['aasr'].mean()
        english_aasr = prompt_stats['English']
        cm_aasr = prompt_stats['CM']
        cmp_aasr = prompt_stats['CMP']
        
        report.append(f"1. Prompt Set Effectiveness:")
        report.append(f"   - English (baseline): {english_aasr:.4f} AASR")
        report.append(f"   - CM (code-mixed):    {cm_aasr:.4f} AASR ({((cm_aasr-english_aasr)/english_aasr*100):+.1f}%)")
        report.append(f"   - CMP (CM+phonetic):  {cmp_aasr:.4f} AASR ({((cmp_aasr-english_aasr)/english_aasr*100):+.1f}%)")
        report.append("")
        
        # Model vulnerability
        model_aasr = self.metrics_df.groupby('model')['aasr'].mean().sort_values(ascending=False)
        report.append(f"2. Model Vulnerability Ranking:")
        for i, (model, aasr) in enumerate(model_aasr.items(), 1):
            report.append(f"   {i}. {model}: {aasr:.4f} AASR")
        report.append("")
        
        # Template effectiveness
        template_aasr = self.metrics_df.groupby('template')['aasr'].mean().sort_values(ascending=False)
        report.append(f"3. Template Effectiveness Ranking:")
        for i, (template, aasr) in enumerate(template_aasr.items(), 1):
            report.append(f"   {i}. {template}: {aasr:.4f} AASR")
        report.append("")
        
        # Save report
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"Summary report saved to: {output_file}")
        print()

def main():
    print("=" * 70)
    print("STATISTICAL ANALYSIS - STEP 8")
    print("=" * 70)
    print()
    
    # Load latest merged results
    metrics_file = "results/metrics/aasr_aarr_final_20251120_095257.csv"
    eval_file = "results/responses/all_evaluations_merged_20251120_095257.csv"
    
    # Initialize analyzer
    analyzer = StatisticalAnalyzer(metrics_file, eval_file)
    
    # Run all analyses
    model_stats = analyzer.model_vulnerability_ranking()
    template_stats = analyzer.template_effectiveness()
    prompt_stats = analyzer.prompt_set_comparison()
    temp_stats = analyzer.temperature_sensitivity()
    sig_tests = analyzer.statistical_significance_tests()
    model_template = analyzer.model_template_interaction()
    model_prompt = analyzer.model_promptset_interaction()
    
    # Generate summary report
    output_dir = Path("results/analysis")
    output_dir.mkdir(exist_ok=True, parents=True)
    
    summary_file = output_dir / "statistical_summary.txt"
    analyzer.generate_summary_report(str(summary_file))
    
    # Save detailed tables
    model_stats.to_csv(output_dir / "model_vulnerability.csv")
    template_stats.to_csv(output_dir / "template_effectiveness.csv")
    prompt_stats.to_csv(output_dir / "prompt_set_comparison.csv")
    temp_stats.to_csv(output_dir / "temperature_sensitivity.csv")
    model_template.to_csv(output_dir / "model_template_interaction.csv")
    model_prompt.to_csv(output_dir / "model_promptset_interaction.csv")
    
    print("=" * 70)
    print("STATISTICAL ANALYSIS COMPLETE!")
    print("=" * 70)
    print()
    print("Results saved to results/analysis/")
    print()

if __name__ == "__main__":
    main()
