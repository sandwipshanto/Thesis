"""
Results Tables & Visualizations
Step 10: Create comprehensive tables and plots from experimental results

This script generates:
- Table 1: Overall AASR/AARR for all models
- Heatmaps: Model × Template × Prompt Set
- Bar charts: English vs CM vs CMP comparisons
- LaTeX exports for paper

Author: Research Project
Date: November 20, 2025
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path


class ResultsVisualizer:
    """
    Create tables and visualizations from experimental results.
    """
    
    def __init__(self, metrics_file: str):
        """
        Initialize visualizer.
        
        Args:
            metrics_file: Path to AASR/AARR metrics CSV
        """
        self.metrics_file = metrics_file
        
        print(f"Loading metrics from: {metrics_file}")
        self.metrics = pd.read_csv(metrics_file)
        
        print(f"Loaded {len(self.metrics)} configurations")
        
        # Set visualization style
        sns.set_style("whitegrid")
        plt.rcParams['figure.dpi'] = 300
        plt.rcParams['font.size'] = 10
    
    def create_table1_overall_aasr_aarr(self) -> pd.DataFrame:
        """
        Create Table 1: Overall AASR and AARR for all models.
        
        Format (from paper):
        - Rows: Models
        - Columns: Templates (None, OM, AntiLM, AIM, Sandbox)
        - Sub-columns: Eng, CM, CMP for each template
        - Two separate tables: one for AASR, one for AARR
        
        Returns:
            DataFrame with table structure
        """
        print("\n" + "="*70)
        print("TABLE 1: OVERALL AASR AND AARR")
        print("="*70)
        
        # Average across temperatures
        avg_metrics = self.metrics.groupby([
            'model', 'template', 'prompt_set'
        ]).agg({
            'aasr': 'mean',
            'aarr': 'mean'
        }).reset_index()
        
        # Create AASR table
        aasr_pivot = avg_metrics.pivot_table(
            index='model',
            columns=['template', 'prompt_set'],
            values='aasr',
            aggfunc='mean'
        )
        
        # Create AARR table
        aarr_pivot = avg_metrics.pivot_table(
            index='model',
            columns=['template', 'prompt_set'],
            values='aarr',
            aggfunc='mean'
        )
        
        # Reorder columns: None, OM, AntiLM, AIM, Sandbox
        template_order = ['None', 'OM', 'AntiLM', 'AIM', 'Sandbox']
        prompt_order = ['English', 'CM', 'CMP']
        
        # Reorder multi-index columns
        aasr_pivot = aasr_pivot.reindex(
            columns=[(t, p) for t in template_order for p in prompt_order if (t, p) in aasr_pivot.columns]
        )
        
        aarr_pivot = aarr_pivot.reindex(
            columns=[(t, p) for t in template_order for p in prompt_order if (t, p) in aarr_pivot.columns]
        )
        
        print("\nAASR Table:")
        print(aasr_pivot.round(3))
        
        print("\nAARR Table:")
        print(aarr_pivot.round(3))
        
        return aasr_pivot, aarr_pivot
    
    def plot_aasr_heatmap(
        self,
        output_dir: str = "results/plots"
    ):
        """
        Create heatmap showing AASR across Model × Template × Prompt Set.
        
        Args:
            output_dir: Directory to save plot
        """
        print("\nCreating AASR heatmap...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Average across temperatures
        avg_metrics = self.metrics.groupby([
            'model', 'template', 'prompt_set'
        ])['aasr'].mean().reset_index()
        
        # Create separate heatmaps for each prompt set
        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        
        prompt_sets = ['English', 'CM', 'CMP']
        
        for idx, prompt_set in enumerate(prompt_sets):
            data = avg_metrics[avg_metrics['prompt_set'] == prompt_set]
            
            # Pivot for heatmap
            heatmap_data = data.pivot(
                index='model',
                columns='template',
                values='aasr'
            )
            
            # Reorder
            template_order = ['None', 'OM', 'AntiLM', 'AIM', 'Sandbox']
            heatmap_data = heatmap_data.reindex(
                columns=[t for t in template_order if t in heatmap_data.columns]
            )
            
            # Plot
            ax = axes[idx]
            sns.heatmap(
                heatmap_data,
                annot=True,
                fmt='.3f',
                cmap='YlOrRd',
                vmin=0,
                vmax=1,
                cbar_kws={'label': 'AASR'},
                ax=ax
            )
            ax.set_title(f'{prompt_set} Prompt Set', fontsize=14, fontweight='bold')
            ax.set_xlabel('Jailbreak Template', fontsize=12)
            ax.set_ylabel('Model', fontsize=12)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"aasr_heatmap_{timestamp}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved heatmap to: {output_path}")
        
        plt.close()
    
    def plot_model_comparison(
        self,
        output_dir: str = "results/plots"
    ):
        """
        Create bar chart comparing AASR across models for each prompt set.
        
        Args:
            output_dir: Directory to save plot
        """
        print("\nCreating model comparison plot...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Average across templates and temperatures
        model_avg = self.metrics.groupby([
            'model', 'prompt_set'
        ])['aasr'].mean().reset_index()
        
        # Pivot for plotting
        model_pivot = model_avg.pivot(
            index='model',
            columns='prompt_set',
            values='aasr'
        )
        
        # Reorder columns
        model_pivot = model_pivot[['English', 'CM', 'CMP']]
        
        # Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x = np.arange(len(model_pivot.index))
        width = 0.25
        
        bars1 = ax.bar(x - width, model_pivot['English'], width, 
                       label='English', color='steelblue', alpha=0.8)
        bars2 = ax.bar(x, model_pivot['CM'], width, 
                       label='CM', color='orange', alpha=0.8)
        bars3 = ax.bar(x + width, model_pivot['CMP'], width, 
                       label='CMP', color='crimson', alpha=0.8)
        
        ax.set_xlabel('Model', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average AASR', fontsize=12, fontweight='bold')
        ax.set_title('Model Vulnerability: English vs CM vs CMP', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(model_pivot.index, rotation=15, ha='right')
        ax.legend(loc='upper left', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, 1)
        
        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"model_comparison_{timestamp}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved model comparison to: {output_path}")
        
        plt.close()
    
    def plot_template_comparison(
        self,
        output_dir: str = "results/plots"
    ):
        """
        Create bar chart comparing AASR across templates for each prompt set.
        
        Args:
            output_dir: Directory to save plot
        """
        print("\nCreating template comparison plot...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Average across models and temperatures
        template_avg = self.metrics.groupby([
            'template', 'prompt_set'
        ])['aasr'].mean().reset_index()
        
        # Pivot for plotting
        template_pivot = template_avg.pivot(
            index='template',
            columns='prompt_set',
            values='aasr'
        )
        
        # Reorder
        template_order = ['None', 'OM', 'AntiLM', 'AIM', 'Sandbox']
        template_pivot = template_pivot.reindex(
            index=[t for t in template_order if t in template_pivot.index]
        )
        template_pivot = template_pivot[['English', 'CM', 'CMP']]
        
        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = np.arange(len(template_pivot.index))
        width = 0.25
        
        bars1 = ax.bar(x - width, template_pivot['English'], width, 
                       label='English', color='steelblue', alpha=0.8)
        bars2 = ax.bar(x, template_pivot['CM'], width, 
                       label='CM', color='orange', alpha=0.8)
        bars3 = ax.bar(x + width, template_pivot['CMP'], width, 
                       label='CMP', color='crimson', alpha=0.8)
        
        ax.set_xlabel('Jailbreak Template', fontsize=12, fontweight='bold')
        ax.set_ylabel('Average AASR', fontsize=12, fontweight='bold')
        ax.set_title('Template Effectiveness: English vs CM vs CMP', 
                     fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(template_pivot.index)
        ax.legend(loc='upper right', fontsize=11)
        ax.grid(axis='y', alpha=0.3)
        ax.set_ylim(0, 1)
        
        # Add value labels on bars
        for bars in [bars1, bars2, bars3]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.3f}',
                       ha='center', va='bottom', fontsize=8)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"template_comparison_{timestamp}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved template comparison to: {output_path}")
        
        plt.close()
    
    def plot_transition_effects(
        self,
        output_dir: str = "results/plots"
    ):
        """
        Create visualization showing English→CM→CMP transitions.
        
        Args:
            output_dir: Directory to save plot
        """
        print("\nCreating transition effects plot...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Overall averages
        overall_avg = self.metrics.groupby('prompt_set')['aasr'].mean()
        
        # By model
        model_avg = self.metrics.groupby(['model', 'prompt_set'])['aasr'].mean().unstack()
        
        # Create subplots
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Plot 1: Overall transition
        ax1 = axes[0]
        prompt_sets = ['English', 'CM', 'CMP']
        values = [overall_avg[ps] for ps in prompt_sets]
        
        ax1.plot(prompt_sets, values, marker='o', linewidth=2.5, 
                markersize=10, color='crimson')
        ax1.fill_between(range(len(prompt_sets)), values, alpha=0.3, color='crimson')
        
        for i, (ps, val) in enumerate(zip(prompt_sets, values)):
            ax1.text(i, val + 0.02, f'{val:.3f}', ha='center', 
                    fontweight='bold', fontsize=11)
        
        ax1.set_xlabel('Prompt Type', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Average AASR', fontsize=12, fontweight='bold')
        ax1.set_title('Overall Attack Success Rate Progression', 
                     fontsize=13, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_ylim(0, max(values) * 1.15)
        
        # Plot 2: By model
        ax2 = axes[1]
        
        for model in model_avg.index:
            values = [model_avg.loc[model, ps] for ps in prompt_sets]
            ax2.plot(prompt_sets, values, marker='o', linewidth=2, 
                    markersize=8, label=model, alpha=0.8)
        
        ax2.set_xlabel('Prompt Type', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Average AASR', fontsize=12, fontweight='bold')
        ax2.set_title('Model-Specific Transition Effects', 
                     fontsize=13, fontweight='bold')
        ax2.legend(loc='best', fontsize=10)
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"transition_effects_{timestamp}.png")
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"  ✓ Saved transition effects to: {output_path}")
        
        plt.close()
    
    def export_table_to_latex(
        self,
        table: pd.DataFrame,
        table_name: str,
        output_dir: str = "results/tables"
    ):
        """
        Export table to LaTeX format.
        
        Args:
            table: DataFrame to export
            table_name: Name for the output file
            output_dir: Directory to save file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{table_name}_{timestamp}.tex")
        
        # Generate LaTeX
        latex_str = table.to_latex(
            float_format="%.3f",
            multicolumn=True,
            multicolumn_format='c',
            caption=f"{table_name.replace('_', ' ').title()}",
            label=f"tab:{table_name}"
        )
        
        with open(output_path, 'w') as f:
            f.write(latex_str)
        
        print(f"  ✓ Saved LaTeX table to: {output_path}")
    
    def export_table_to_markdown(
        self,
        table: pd.DataFrame,
        table_name: str,
        output_dir: str = "results/tables"
    ):
        """
        Export table to Markdown format.
        
        Args:
            table: DataFrame to export
            table_name: Name for the output file
            output_dir: Directory to save file
        """
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(output_dir, f"{table_name}_{timestamp}.md")
        
        with open(output_path, 'w') as f:
            f.write(f"# {table_name.replace('_', ' ').title()}\n\n")
            f.write(table.round(3).to_markdown())
            f.write(f"\n\n*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n")
        
        print(f"  ✓ Saved Markdown table to: {output_path}")
    
    def generate_all_visualizations(self):
        """Generate all tables and plots."""
        print("\n" + "="*70)
        print("GENERATING ALL VISUALIZATIONS")
        print("="*70)
        
        # Table 1
        aasr_table, aarr_table = self.create_table1_overall_aasr_aarr()
        
        # Save Table 1
        print("\nExporting Table 1...")
        aasr_table.to_csv("results/tables/table1_aasr.csv")
        aarr_table.to_csv("results/tables/table1_aarr.csv")
        self.export_table_to_latex(aasr_table, "table1_aasr")
        self.export_table_to_latex(aarr_table, "table1_aarr")
        self.export_table_to_markdown(aasr_table, "table1_aasr")
        self.export_table_to_markdown(aarr_table, "table1_aarr")
        
        # Plots
        self.plot_aasr_heatmap()
        self.plot_model_comparison()
        self.plot_template_comparison()
        self.plot_transition_effects()
        
        print("\n" + "="*70)
        print("ALL VISUALIZATIONS COMPLETE!")
        print("="*70)
        print("\nGenerated files:")
        print("  Tables:")
        print("    - results/tables/table1_aasr.csv")
        print("    - results/tables/table1_aarr.csv")
        print("    - results/tables/table1_*.tex (LaTeX)")
        print("    - results/tables/table1_*.md (Markdown)")
        print("\n  Plots:")
        print("    - results/plots/aasr_heatmap_*.png")
        print("    - results/plots/model_comparison_*.png")
        print("    - results/plots/template_comparison_*.png")
        print("    - results/plots/transition_effects_*.png")


def main():
    """Main execution function."""
    print("="*70)
    print("STEP 10: RESULTS TABLES & VISUALIZATIONS")
    print("="*70)
    print()
    print("Creating comprehensive tables and plots from experimental results")
    print("="*70)
    print()
    
    # Find latest metrics file
    metrics_dir = "results/metrics"
    metrics_files = list(Path(metrics_dir).glob("aasr_aarr_final_*.csv"))
    
    if not metrics_files:
        print("Error: No metrics files found in results/metrics/")
        print("Please run experiment_runner.py first")
        return
    
    latest_metrics = max(metrics_files, key=os.path.getctime)
    
    print(f"Using metrics: {latest_metrics.name}")
    print()
    
    # Initialize visualizer
    visualizer = ResultsVisualizer(metrics_file=str(latest_metrics))
    
    # Generate all visualizations
    visualizer.generate_all_visualizations()
    
    print("\n" + "="*70)
    print("STEP 10 COMPLETE!")
    print("="*70)
    print("\nNext Steps:")
    print("  1. Review tables in results/tables/")
    print("  2. Review plots in results/plots/")
    print("  3. Proceed to Step 11: Human Annotation (optional)")
    print("  4. Or skip to Step 13: Analysis & Discussion")
    print()


if __name__ == "__main__":
    main()
