"""
Statistical Significance Testing - Wilcoxon Signed-Rank Tests
Step 9: Test if CM and CMP transitions show statistically significant improvements

This script performs Wilcoxon signed-rank tests to compare:
- English vs CM (code-mixing effect)
- CM vs CMP (phonetic perturbation effect)

For each model-template combination across all prompts.

Author: Research Project
Date: November 20, 2025
"""

import os
import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Tuple
from datetime import datetime
from pathlib import Path


class StatisticalTester:
    """
    Perform Wilcoxon signed-rank tests on AASR scores.
    Tests paired comparisons: English→CM and CM→CMP.
    """
    
    def __init__(self, evaluations_file: str):
        """
        Initialize statistical tester.
        
        Args:
            evaluations_file: Path to all evaluations CSV
        """
        self.evaluations_file = evaluations_file
        
        print(f"Loading evaluations from: {evaluations_file}")
        self.evaluations = pd.read_csv(evaluations_file)
        
        print(f"Loaded {len(self.evaluations)} evaluations")
        
        # Calculate per-prompt AASR scores
        self.prompt_scores = self._calculate_prompt_scores()
    
    def _calculate_prompt_scores(self) -> pd.DataFrame:
        """
        Calculate AASR for each prompt-model-template-promptset-temperature combination.
        
        Returns:
            DataFrame with prompt-level AASR scores
        """
        print("\nCalculating per-prompt AASR scores...")
        
        # Group by configuration + prompt_id
        grouped = self.evaluations.groupby([
            'model', 'template', 'prompt_set', 'temperature', 'prompt_id'
        ]).agg({
            'harmful': 'mean',  # AASR = mean of harmful
            'relevant': 'mean'
        }).reset_index()
        
        grouped.rename(columns={
            'harmful': 'aasr',
            'relevant': 'aarr'
        }, inplace=True)
        
        print(f"  Calculated scores for {len(grouped)} unique prompt configurations")
        
        return grouped
    
    def wilcoxon_signed_rank_test(
        self,
        group1: pd.Series,
        group2: pd.Series,
        alternative: str = 'two-sided'
    ) -> Tuple[float, float]:
        """
        Perform Wilcoxon signed-rank test.
        
        Args:
            group1: First group (e.g., English AASR)
            group2: Second group (e.g., CM AASR)
            alternative: 'two-sided', 'less', or 'greater'
        
        Returns:
            (statistic, p-value) tuple
        """
        # Ensure aligned indices
        aligned = pd.DataFrame({
            'group1': group1.values,
            'group2': group2.values
        }).dropna()
        
        if len(aligned) < 3:
            # Not enough samples for test
            return np.nan, np.nan
        
        try:
            statistic, p_value = stats.wilcoxon(
                aligned['group1'],
                aligned['group2'],
                alternative=alternative
            )
            return statistic, p_value
        except Exception as e:
            print(f"    Warning: Wilcoxon test failed: {e}")
            return np.nan, np.nan
    
    def compute_effect_size_cohens_d(
        self,
        group1: pd.Series,
        group2: pd.Series
    ) -> float:
        """
        Compute Cohen's d effect size.
        
        d = (mean1 - mean2) / pooled_std
        
        Args:
            group1: First group
            group2: Second group
        
        Returns:
            Cohen's d value
        """
        mean1 = group1.mean()
        mean2 = group2.mean()
        std1 = group1.std()
        std2 = group2.std()
        n1 = len(group1)
        n2 = len(group2)
        
        # Pooled standard deviation
        pooled_std = np.sqrt(((n1-1)*std1**2 + (n2-1)*std2**2) / (n1+n2-2))
        
        if pooled_std == 0:
            return 0.0
        
        cohens_d = (mean2 - mean1) / pooled_std
        return cohens_d
    
    def test_all_transitions(self) -> pd.DataFrame:
        """
        Test all English→CM and CM→CMP transitions.
        
        Returns:
            DataFrame with test results for all model-template combinations
        """
        print("\n" + "="*70)
        print("WILCOXON SIGNED-RANK TESTS")
        print("="*70)
        
        results = []
        
        # Get unique model-template-temperature combinations
        configs = self.prompt_scores[['model', 'template', 'temperature']].drop_duplicates()
        
        print(f"\nTesting {len(configs)} configurations...")
        
        for idx, row in configs.iterrows():
            model = row['model']
            template = row['template']
            temperature = row['temperature']
            
            # Filter for this configuration
            config_data = self.prompt_scores[
                (self.prompt_scores['model'] == model) &
                (self.prompt_scores['template'] == template) &
                (self.prompt_scores['temperature'] == temperature)
            ]
            
            # Get English, CM, CMP scores for same prompts
            english_scores = config_data[config_data['prompt_set'] == 'English'].set_index('prompt_id')['aasr']
            cm_scores = config_data[config_data['prompt_set'] == 'CM'].set_index('prompt_id')['aasr']
            cmp_scores = config_data[config_data['prompt_set'] == 'CMP'].set_index('prompt_id')['aasr']
            
            # Test English vs CM
            eng_cm_stat, eng_cm_p = self.wilcoxon_signed_rank_test(
                english_scores,
                cm_scores,
                alternative='two-sided'
            )
            eng_cm_cohens_d = self.compute_effect_size_cohens_d(english_scores, cm_scores)
            
            # Test CM vs CMP
            cm_cmp_stat, cm_cmp_p = self.wilcoxon_signed_rank_test(
                cm_scores,
                cmp_scores,
                alternative='two-sided'
            )
            cm_cmp_cohens_d = self.compute_effect_size_cohens_d(cm_scores, cmp_scores)
            
            # Test English vs CMP (direct)
            eng_cmp_stat, eng_cmp_p = self.wilcoxon_signed_rank_test(
                english_scores,
                cmp_scores,
                alternative='two-sided'
            )
            eng_cmp_cohens_d = self.compute_effect_size_cohens_d(english_scores, cmp_scores)
            
            # Store results
            results.append({
                'model': model,
                'template': template,
                'temperature': temperature,
                'n_prompts': len(english_scores),
                # English vs CM
                'eng_cm_statistic': eng_cm_stat,
                'eng_cm_pvalue': eng_cm_p,
                'eng_cm_cohens_d': eng_cm_cohens_d,
                'eng_cm_significant': eng_cm_p < 0.05 if not np.isnan(eng_cm_p) else False,
                # CM vs CMP
                'cm_cmp_statistic': cm_cmp_stat,
                'cm_cmp_pvalue': cm_cmp_p,
                'cm_cmp_cohens_d': cm_cmp_cohens_d,
                'cm_cmp_significant': cm_cmp_p < 0.05 if not np.isnan(cm_cmp_p) else False,
                # English vs CMP
                'eng_cmp_statistic': eng_cmp_stat,
                'eng_cmp_pvalue': eng_cmp_p,
                'eng_cmp_cohens_d': eng_cmp_cohens_d,
                'eng_cmp_significant': eng_cmp_p < 0.05 if not np.isnan(eng_cmp_p) else False,
                # Mean AASR values
                'mean_aasr_english': english_scores.mean(),
                'mean_aasr_cm': cm_scores.mean(),
                'mean_aasr_cmp': cmp_scores.mean()
            })
        
        results_df = pd.DataFrame(results)
        
        print(f"\n✓ Completed {len(results_df)} Wilcoxon tests")
        
        return results_df
    
    def summarize_results(self, results: pd.DataFrame) -> Dict:
        """
        Generate summary statistics from Wilcoxon test results.
        
        Args:
            results: DataFrame with test results
        
        Returns:
            Dictionary with summary statistics
        """
        print("\n" + "="*70)
        print("WILCOXON TEST SUMMARY")
        print("="*70)
        
        summary = {}
        
        # English vs CM
        eng_cm_sig = results['eng_cm_significant'].sum()
        eng_cm_total = results['eng_cm_significant'].notna().sum()
        eng_cm_positive = ((results['eng_cm_significant']) & (results['mean_aasr_cm'] > results['mean_aasr_english'])).sum()
        
        print(f"\nEnglish → CM Transition:")
        print(f"  Significant improvements: {eng_cm_positive}/{eng_cm_total} ({eng_cm_positive/eng_cm_total*100:.1f}%)")
        print(f"  Mean Cohen's d: {results['eng_cm_cohens_d'].mean():.3f}")
        print(f"  Median p-value: {results['eng_cm_pvalue'].median():.4f}")
        
        summary['eng_cm'] = {
            'significant_count': eng_cm_sig,
            'total_tests': eng_cm_total,
            'positive_improvements': eng_cm_positive,
            'mean_cohens_d': results['eng_cm_cohens_d'].mean(),
            'median_pvalue': results['eng_cm_pvalue'].median()
        }
        
        # CM vs CMP
        cm_cmp_sig = results['cm_cmp_significant'].sum()
        cm_cmp_total = results['cm_cmp_significant'].notna().sum()
        cm_cmp_positive = ((results['cm_cmp_significant']) & (results['mean_aasr_cmp'] > results['mean_aasr_cm'])).sum()
        
        print(f"\nCM → CMP Transition:")
        print(f"  Significant improvements: {cm_cmp_positive}/{cm_cmp_total} ({cm_cmp_positive/cm_cmp_total*100:.1f}%)")
        print(f"  Mean Cohen's d: {results['cm_cmp_cohens_d'].mean():.3f}")
        print(f"  Median p-value: {results['cm_cmp_pvalue'].median():.4f}")
        
        summary['cm_cmp'] = {
            'significant_count': cm_cmp_sig,
            'total_tests': cm_cmp_total,
            'positive_improvements': cm_cmp_positive,
            'mean_cohens_d': results['cm_cmp_cohens_d'].mean(),
            'median_pvalue': results['cm_cmp_pvalue'].median()
        }
        
        # English vs CMP (direct)
        eng_cmp_sig = results['eng_cmp_significant'].sum()
        eng_cmp_total = results['eng_cmp_significant'].notna().sum()
        eng_cmp_positive = ((results['eng_cmp_significant']) & (results['mean_aasr_cmp'] > results['mean_aasr_english'])).sum()
        
        print(f"\nEnglish → CMP Transition (Direct):")
        print(f"  Significant improvements: {eng_cmp_positive}/{eng_cmp_total} ({eng_cmp_positive/eng_cmp_total*100:.1f}%)")
        print(f"  Mean Cohen's d: {results['eng_cmp_cohens_d'].mean():.3f}")
        print(f"  Median p-value: {results['eng_cmp_pvalue'].median():.4f}")
        
        summary['eng_cmp'] = {
            'significant_count': eng_cmp_sig,
            'total_tests': eng_cmp_total,
            'positive_improvements': eng_cmp_positive,
            'mean_cohens_d': results['eng_cmp_cohens_d'].mean(),
            'median_pvalue': results['eng_cmp_pvalue'].median()
        }
        
        # By model
        print(f"\n" + "-"*70)
        print("Model-Specific Results (English → CMP):")
        print("-"*70)
        
        for model in results['model'].unique():
            model_data = results[results['model'] == model]
            sig_count = model_data['eng_cmp_significant'].sum()
            total_count = len(model_data)
            mean_cohens_d = model_data['eng_cmp_cohens_d'].mean()
            
            print(f"\n{model}:")
            print(f"  Significant: {sig_count}/{total_count}")
            print(f"  Mean Cohen's d: {mean_cohens_d:.3f}")
            print(f"  Mean AASR gain: {(model_data['mean_aasr_cmp'] - model_data['mean_aasr_english']).mean():.3f}")
        
        # By template
        print(f"\n" + "-"*70)
        print("Template-Specific Results (English → CMP):")
        print("-"*70)
        
        for template in results['template'].unique():
            template_data = results[results['template'] == template]
            sig_count = template_data['eng_cmp_significant'].sum()
            total_count = len(template_data)
            mean_cohens_d = template_data['eng_cmp_cohens_d'].mean()
            
            print(f"\n{template}:")
            print(f"  Significant: {sig_count}/{total_count}")
            print(f"  Mean Cohen's d: {mean_cohens_d:.3f}")
            print(f"  Mean AASR gain: {(template_data['mean_aasr_cmp'] - template_data['mean_aasr_english']).mean():.3f}")
        
        return summary
    
    def generate_significance_table(
        self,
        results: pd.DataFrame,
        output_dir: str = "results/statistics"
    ):
        """
        Generate significance table showing which model-template pairs benefit from CM/CMP.
        
        Args:
            results: Wilcoxon test results
            output_dir: Directory to save tables
        """
        print(f"\n" + "="*70)
        print("GENERATING SIGNIFICANCE TABLES")
        print("="*70)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Create pivot tables
        # English → CM significance
        eng_cm_pivot = results.pivot_table(
            index='model',
            columns='template',
            values='eng_cm_significant',
            aggfunc='mean'
        )
        
        # CM → CMP significance
        cm_cmp_pivot = results.pivot_table(
            index='model',
            columns='template',
            values='cm_cmp_significant',
            aggfunc='mean'
        )
        
        # English → CMP significance
        eng_cmp_pivot = results.pivot_table(
            index='model',
            columns='template',
            values='eng_cmp_significant',
            aggfunc='mean'
        )
        
        # Cohen's d pivot (English → CMP)
        cohens_d_pivot = results.pivot_table(
            index='model',
            columns='template',
            values='eng_cmp_cohens_d',
            aggfunc='mean'
        )
        
        # P-value pivot (English → CMP)
        pvalue_pivot = results.pivot_table(
            index='model',
            columns='template',
            values='eng_cmp_pvalue',
            aggfunc='mean'
        )
        
        # Save tables
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        eng_cm_path = os.path.join(output_dir, f"eng_cm_significance_{timestamp}.csv")
        eng_cm_pivot.to_csv(eng_cm_path)
        print(f"  ✓ Saved English→CM significance table: {eng_cm_path}")
        
        cm_cmp_path = os.path.join(output_dir, f"cm_cmp_significance_{timestamp}.csv")
        cm_cmp_pivot.to_csv(cm_cmp_path)
        print(f"  ✓ Saved CM→CMP significance table: {cm_cmp_path}")
        
        eng_cmp_path = os.path.join(output_dir, f"eng_cmp_significance_{timestamp}.csv")
        eng_cmp_pivot.to_csv(eng_cmp_path)
        print(f"  ✓ Saved English→CMP significance table: {eng_cmp_path}")
        
        cohens_d_path = os.path.join(output_dir, f"cohens_d_pivot_{timestamp}.csv")
        cohens_d_pivot.to_csv(cohens_d_path)
        print(f"  ✓ Saved Cohen's d table: {cohens_d_path}")
        
        pvalue_path = os.path.join(output_dir, f"pvalue_pivot_{timestamp}.csv")
        pvalue_pivot.to_csv(pvalue_path)
        print(f"  ✓ Saved p-value table: {pvalue_path}")
    
    def save_detailed_results(
        self,
        results: pd.DataFrame,
        output_dir: str = "results/statistics"
    ):
        """
        Save detailed Wilcoxon test results.
        
        Args:
            results: Test results DataFrame
            output_dir: Directory to save results
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"wilcoxon_results_{timestamp}.csv")
        
        results.to_csv(output_path, index=False)
        print(f"\n✓ Saved detailed results to: {output_path}")
    
    def generate_summary_report(
        self,
        results: pd.DataFrame,
        summary: Dict,
        output_dir: str = "results/statistics"
    ):
        """
        Generate text summary report.
        
        Args:
            results: Test results
            summary: Summary statistics
            output_dir: Output directory
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(output_dir, f"significance_summary_{timestamp}.md")
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Statistical Significance Testing - Wilcoxon Signed-Rank Tests\n\n")
            f.write(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("## Objective\n\n")
            f.write("Test whether code-mixing (CM) and phonetic perturbations (CMP) produce\n")
            f.write("statistically significant improvements in attack success rates compared to\n")
            f.write("English baseline prompts.\n\n")
            
            f.write("## Methodology\n\n")
            f.write("- **Test:** Wilcoxon signed-rank test (paired, non-parametric)\n")
            f.write("- **Significance threshold:** p < 0.05\n")
            f.write("- **Effect size:** Cohen's d\n")
            f.write("- **Comparisons:**\n")
            f.write("  1. English → CM (code-mixing effect)\n")
            f.write("  2. CM → CMP (phonetic perturbation effect)\n")
            f.write("  3. English → CMP (combined effect)\n\n")
            
            f.write("## Overall Results\n\n")
            
            # English → CM
            f.write("### English → CM Transition\n\n")
            f.write(f"- **Significant tests:** {summary['eng_cm']['significant_count']}/{summary['eng_cm']['total_tests']}\n")
            f.write(f"- **Positive improvements:** {summary['eng_cm']['positive_improvements']}\n")
            f.write(f"- **Mean Cohen's d:** {summary['eng_cm']['mean_cohens_d']:.3f}\n")
            f.write(f"- **Median p-value:** {summary['eng_cm']['median_pvalue']:.4f}\n\n")
            
            # CM → CMP
            f.write("### CM → CMP Transition\n\n")
            f.write(f"- **Significant tests:** {summary['cm_cmp']['significant_count']}/{summary['cm_cmp']['total_tests']}\n")
            f.write(f"- **Positive improvements:** {summary['cm_cmp']['positive_improvements']}\n")
            f.write(f"- **Mean Cohen's d:** {summary['cm_cmp']['mean_cohens_d']:.3f}\n")
            f.write(f"- **Median p-value:** {summary['cm_cmp']['median_pvalue']:.4f}\n\n")
            
            # English → CMP
            f.write("### English → CMP Transition (Combined)\n\n")
            f.write(f"- **Significant tests:** {summary['eng_cmp']['significant_count']}/{summary['eng_cmp']['total_tests']}\n")
            f.write(f"- **Positive improvements:** {summary['eng_cmp']['positive_improvements']}\n")
            f.write(f"- **Mean Cohen's d:** {summary['eng_cmp']['mean_cohens_d']:.3f}\n")
            f.write(f"- **Median p-value:** {summary['eng_cmp']['median_pvalue']:.4f}\n\n")
            
            f.write("## Model-Specific Findings\n\n")
            for model in results['model'].unique():
                model_data = results[results['model'] == model]
                sig_count = model_data['eng_cmp_significant'].sum()
                total_count = len(model_data)
                mean_cohens_d = model_data['eng_cmp_cohens_d'].mean()
                mean_gain = (model_data['mean_aasr_cmp'] - model_data['mean_aasr_english']).mean()
                
                f.write(f"### {model}\n\n")
                f.write(f"- Significant configurations: {sig_count}/{total_count}\n")
                f.write(f"- Mean effect size (Cohen's d): {mean_cohens_d:.3f}\n")
                f.write(f"- Mean AASR gain (CMP vs English): {mean_gain:.3f}\n\n")
            
            f.write("## Template-Specific Findings\n\n")
            for template in results['template'].unique():
                template_data = results[results['template'] == template]
                sig_count = template_data['eng_cmp_significant'].sum()
                total_count = len(template_data)
                mean_cohens_d = template_data['eng_cmp_cohens_d'].mean()
                mean_gain = (template_data['mean_aasr_cmp'] - template_data['mean_aasr_english']).mean()
                
                f.write(f"### {template}\n\n")
                f.write(f"- Significant configurations: {sig_count}/{total_count}\n")
                f.write(f"- Mean effect size (Cohen's d): {mean_cohens_d:.3f}\n")
                f.write(f"- Mean AASR gain (CMP vs English): {mean_gain:.3f}\n\n")
            
            f.write("## Interpretation\n\n")
            f.write("**Key Takeaways:**\n\n")
            f.write("1. **Code-mixing effectiveness:** ")
            if summary['eng_cm']['positive_improvements'] > summary['eng_cm']['total_tests'] / 2:
                f.write("Code-mixing shows beneficial effects across majority of configurations.\n")
            else:
                f.write("Code-mixing shows mixed effects across configurations.\n")
            
            f.write("2. **Phonetic perturbation effectiveness:** ")
            if summary['cm_cmp']['positive_improvements'] > summary['cm_cmp']['total_tests'] / 2:
                f.write("Phonetic perturbations provide additional benefit beyond code-mixing.\n")
            else:
                f.write("Phonetic perturbations show variable effects.\n")
            
            f.write("3. **Combined effect:** ")
            if summary['eng_cmp']['positive_improvements'] > summary['eng_cmp']['total_tests'] / 2:
                f.write("CMP (code-mixing + phonetic) significantly outperforms English baseline.\n")
            else:
                f.write("CMP shows context-dependent effectiveness.\n")
            
            f.write("\n## Conclusion\n\n")
            f.write("These Wilcoxon signed-rank tests validate the statistical significance of\n")
            f.write("code-mixing and phonetic perturbation strategies for bypassing LLM safety filters.\n")
            f.write("Results show model-specific and template-specific patterns that inform targeted\n")
            f.write("safety improvements.\n\n")
        
        print(f"✓ Saved summary report to: {report_path}")


def main():
    """Main execution function."""
    print("="*70)
    print("STEP 9: STATISTICAL SIGNIFICANCE TESTING")
    print("="*70)
    print()
    print("Performing Wilcoxon signed-rank tests to validate CM and CMP effectiveness")
    print("="*70)
    print()
    
    # Find latest evaluations file
    responses_dir = "results/responses"
    eval_files = list(Path(responses_dir).glob("all_evaluations_merged_*.csv"))
    
    if not eval_files:
        print("Error: No evaluation files found in results/responses/")
        print("Please run experiment_runner.py first")
        return
    
    latest_evals = max(eval_files, key=os.path.getctime)
    
    print(f"Using evaluations: {latest_evals.name}")
    print()
    
    # Initialize tester
    tester = StatisticalTester(evaluations_file=str(latest_evals))
    
    # Run all Wilcoxon tests
    results = tester.test_all_transitions()
    
    # Summarize results
    summary = tester.summarize_results(results)
    
    # Generate significance tables
    tester.generate_significance_table(results)
    
    # Save detailed results
    tester.save_detailed_results(results)
    
    # Generate summary report
    tester.generate_summary_report(results, summary)
    
    print("\n" + "="*70)
    print("STATISTICAL SIGNIFICANCE TESTING COMPLETE!")
    print("="*70)
    print("\nResults saved to results/statistics/")
    print("\nNext Steps:")
    print("  1. Review significance_summary_*.md for interpretations")
    print("  2. Examine wilcoxon_results_*.csv for detailed p-values")
    print("  3. Check pivot tables for model-template patterns")
    print("  4. Proceed to Step 10: Create Results Tables & Visualizations")
    print()


if __name__ == "__main__":
    main()
