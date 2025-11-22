"""
Experiment Runner for Bangla-English LLM Red-Teaming

This script orchestrates the complete experimental pipeline:
1. Load prompts (English, CM, CMP)
2. Load jailbreak templates
3. Generate templated prompts
4. Query models across all configurations
5. Automatically evaluate responses with LLM judge
6. Calculate AASR/AARR metrics
7. Save results incrementally

Controlled by: config/run_config.yaml (manual experiment configuration)

Author: Research Team
Date: November 2025
"""

import os
import sys
import yaml
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.openrouter_handler import OpenRouterHandler
from jailbreak.template_generator import JailbreakTemplateGenerator
from evaluation.llm_judge import LLMJudge
from evaluation.calculate_metrics import MetricsCalculator


class ExperimentRunner:
    """
    Orchestrates the complete experimental pipeline for LLM red-teaming.
    
    Implements:
    - Configuration loading from run_config.yaml
    - Prompt loading (English, CM, CMP)
    - Template application (None, OM, AntiLM, AIM, Sandbox)
    - Model querying (4 models × 3 temperatures)
    - Automatic evaluation (LLM judge)
    - Metrics calculation (AASR/AARR)
    - Incremental saving and progress tracking
    """
    
    def __init__(self, config_path: str = "config/run_config.yaml"):
        """
        Initialize experiment runner.
        
        Args:
            config_path: Path to run configuration file
        """
        print("=" * 70)
        print("BANGLA-ENGLISH LLM RED-TEAMING - EXPERIMENT RUNNER")
        print("=" * 70)
        print()
        
        # Load configuration
        self.config = self._load_config(config_path)
        self.config_path = config_path
        
        # Initialize components
        self.handler = OpenRouterHandler()
        self.template_gen = JailbreakTemplateGenerator('config/jailbreak_templates.yaml')
        self.judge = LLMJudge('config/judge_prompts.yaml')
        
        # Load model configurations
        with open('config/model_config.yaml', 'r', encoding='utf-8') as f:
            self.model_config = yaml.safe_load(f)
        
        # Statistics
        self.total_queries = 0
        self.total_evaluations = 0
        self.total_cost = 0.0
        self.start_time = None
        
        # Results storage
        self.responses = []
        self.evaluations = []
        self.results_lock = threading.Lock()  # Thread-safe result storage
        self.completed_queries = set()  # Track completed (model, template, prompt_set, temp, prompt_id)
        
        print(f"[OK] Experiment runner initialized")
        print(f"  Config: {config_path}")
        print(f"  Models: {len(self.config['experiment']['enabled_models'])}")
        print(f"  Templates: {len(self.config['experiment']['enabled_templates'])}")
        print(f"  Prompt sets: {len(self.config['experiment']['enabled_prompt_sets'])}")
        print(f"  Temperatures: {len(self.config['experiment']['temperatures'])}")
        print()
    
    def _load_completed_queries(self):
        """Load previously completed queries to enable resume functionality."""
        responses_dir = Path(self.config['output']['responses_dir'])
        
        if not responses_dir.exists():
            return
        
        # Find all intermediate response files
        response_files = list(responses_dir.glob('responses_intermediate_*.csv'))
        
        if not response_files:
            return
        
        # Load the most recent file
        latest_file = max(response_files, key=lambda p: p.stat().st_mtime)
        
        try:
            df = pd.read_csv(latest_file)
            for _, row in df.iterrows():
                key = (
                    row['model'],
                    row['template'],
                    row['prompt_set'],
                    row['temperature'],
                    row['prompt_id']
                )
                self.completed_queries.add(key)
            
            print(f"📂 Loaded {len(self.completed_queries)} completed queries from {latest_file.name}")
            print(f"   Resuming from where we left off...\\n")
        except Exception as e:
            print(f"⚠ Could not load previous progress: {e}\\n")
    
    def _load_config(self, path: str) -> Dict:
        """Load run configuration."""
        with open(path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Validate required fields
        required = ['experiment', 'data', 'output']
        for field in required:
            if field not in config:
                raise ValueError(f"Missing required config field: {field}")
        
        # Set default max_workers if not specified
        if 'max_workers' not in config['experiment']:
            config['experiment']['max_workers'] = 10  # Default parallel workers
        
        return config
    
    def load_prompts(self) -> Dict[str, pd.DataFrame]:
        """
        Load prompts for all enabled prompt sets.
        
        Returns:
            Dictionary mapping prompt set names to DataFrames
        """
        print("Loading prompts...")
        
        prompts = {}
        data_config = self.config['data']
        enabled_sets = self.config['experiment']['enabled_prompt_sets']
        
        # Map prompt set names to file paths
        file_map = {
            'English': data_config.get('english_prompts', 'data/raw/harmful_prompts_english.csv'),
            'CM': data_config.get('cm_prompts', 'data/processed/prompts_cm.csv'),
            'CMP': data_config.get('cmp_prompts', 'data/processed/prompts_cmp.csv')
        }
        
        for prompt_set in enabled_sets:
            if prompt_set not in file_map:
                print(f"  ⚠ Unknown prompt set: {prompt_set}, skipping")
                continue
            
            filepath = file_map[prompt_set]
            if not Path(filepath).exists():
                print(f"  ⚠ File not found: {filepath}, skipping {prompt_set}")
                continue
            
            df = pd.read_csv(filepath, encoding='utf-8')
            
            # Limit to configured number of prompts
            num_prompts = self.config['experiment'].get('num_prompts', len(df))
            df = df.head(num_prompts)
            
            prompts[prompt_set] = df
            print(f"  [OK] Loaded {len(df)} prompts from {prompt_set}")
        
        print()
        return prompts
    
    def calculate_total_queries(self, prompts: Dict[str, pd.DataFrame]) -> int:
        """Calculate total number of queries to be made."""
        num_models = len(self.config['experiment']['enabled_models'])
        num_templates = len(self.config['experiment']['enabled_templates'])
        num_temps = len(self.config['experiment']['temperatures'])
        
        total = 0
        for prompt_set, df in prompts.items():
            total += len(df) * num_models * num_templates * num_temps
        
        return total
    
    def get_model_openrouter_id(self, model_name: str) -> str:
        """Get OpenRouter model ID from model name."""
        models = self.model_config.get('models', {})
        
        if model_name in models:
            return models[model_name]['openrouter_id']
        
        # Fallback: assume it's already an OpenRouter ID
        return model_name
    
    def run_experiments(self, dry_run: bool = False):
        """
        Run the complete experimental pipeline.
        
        Args:
            dry_run: If True, only print what would be done without executing
        """
        self.start_time = time.time()
        
        # Load prompts
        prompts = self.load_prompts()
        
        if not prompts:
            print("✗ No prompts loaded. Check your configuration and data files.")
            return
        
        # Calculate total queries
        total_queries = self.calculate_total_queries(prompts)
        
        print("=" * 70)
        print("EXPERIMENT CONFIGURATION")
        print("=" * 70)
        print(f"Models: {self.config['experiment']['enabled_models']}")
        print(f"Templates: {self.config['experiment']['enabled_templates']}")
        print(f"Prompt sets: {list(prompts.keys())}")
        print(f"Temperatures: {self.config['experiment']['temperatures']}")
        print(f"Total configurations: {total_queries}")
        print()
        
        # Estimate cost and time
        avg_cost_per_query = 0.005  # Conservative estimate
        estimated_cost = total_queries * avg_cost_per_query
        
        # Time estimate with parallel processing
        max_workers = self.config['experiment'].get('max_workers', 10)
        # Assume ~2 seconds per query, divided by max_workers for parallelization
        estimated_time_hours = (total_queries * 2) / (max_workers * 3600)
        
        print(f"Estimated cost: ${estimated_cost:.2f}")
        print(f"Estimated time: {estimated_time_hours:.1f} hours (with {max_workers} parallel workers)")
        print()
        
        if dry_run:
            print("DRY RUN MODE - No queries will be made")
            return
        
        # Load previously completed queries for resume
        self._load_completed_queries()
        
        # Confirm before proceeding
        if self.config.get('safety', {}).get('require_confirmation', True):
            response = input("Proceed with experiments? (yes/no): ")
            if response.lower() not in ['yes', 'y']:
                print("Experiments cancelled.")
                return
        
        print("=" * 70)
        print("RUNNING EXPERIMENTS")
        print("=" * 70)
        print()
        
        # Run experiments for each configuration
        self._run_all_configurations(prompts)
        
        # Final summary
        self._print_summary()
    
    def _run_all_configurations(self, prompts: Dict[str, pd.DataFrame]):
        """Run experiments for all configurations."""
        experiment_config = self.config['experiment']
        
        # Get enabled settings
        models = experiment_config['enabled_models']
        templates = experiment_config['enabled_templates']
        temperatures = experiment_config['temperatures']
        batch_size = experiment_config.get('batch_size', 10)
        save_interval = experiment_config.get('save_interval', 50)
        
        # Iterate through all configurations
        total_configs = len(models) * len(templates) * len(prompts) * len(temperatures)
        config_num = 0
        
        for model_name in models:
            model_id = self.get_model_openrouter_id(model_name)
            
            for template_name in templates:
                for prompt_set_name, prompt_df in prompts.items():
                    for temperature in temperatures:
                        config_num += 1
                        
                        print(f"Configuration {config_num}/{total_configs}")
                        print(f"  Model: {model_name}")
                        print(f"  Template: {template_name}")
                        print(f"  Prompt Set: {prompt_set_name}")
                        print(f"  Temperature: {temperature}")
                        print()
                        
                        # Run this configuration
                        self._run_single_configuration(
                            model_name=model_name,
                            model_id=model_id,
                            template_name=template_name,
                            prompt_set_name=prompt_set_name,
                            prompt_df=prompt_df,
                            temperature=temperature,
                            batch_size=batch_size
                        )
                        
                        # Save intermediate results
                        if self.total_queries % save_interval == 0:
                            self._save_intermediate_results()
        
        # Final save
        self._save_final_results()
    
    def _run_single_configuration(
        self,
        model_name: str,
        model_id: str,
        template_name: str,
        prompt_set_name: str,
        prompt_df: pd.DataFrame,
        temperature: float,
        batch_size: int = 10
    ):
        """Run experiments for a single configuration using batched parallel processing."""
        
        # Determine which prompt column to use
        if prompt_set_name == 'English':
            prompt_col = 'hypothetical_scenario'
        elif prompt_set_name == 'CM':
            prompt_col = 'cm_scenario'
        elif prompt_set_name == 'CMP':
            prompt_col = 'cmp_scenario'
        else:
            print(f"  ⚠ Unknown prompt set: {prompt_set_name}, using hypothetical_scenario")
            prompt_col = 'hypothetical_scenario'
        
        # Get max workers from config
        max_workers = self.config['experiment'].get('max_workers', 10)
        
        # Filter out already completed prompts
        prompts_to_process = []
        for idx, row in prompt_df.iterrows():
            query_key = (model_name, template_name, prompt_set_name, temperature, row['id'])
            if query_key not in self.completed_queries:
                prompts_to_process.append(row)
        
        num_prompts = len(prompts_to_process)
        num_total = len(prompt_df)
        num_skipped = num_total - num_prompts
        
        if num_skipped > 0:
            print(f"  ⏭ Skipping {num_skipped} already completed prompts")
        
        if num_prompts == 0:
            print(f"  ✓ All prompts already completed for this configuration")
            return
        
        # Use ThreadPoolExecutor with all prompts at once (more efficient than small batches)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all prompts as futures
            futures = []
            for row in prompts_to_process:
                future = executor.submit(
                    self._process_single_prompt,
                    row=row,
                    prompt_col=prompt_col,
                    model_name=model_name,
                    model_id=model_id,
                    template_name=template_name,
                    prompt_set_name=prompt_set_name,
                    temperature=temperature
                )
                futures.append(future)
            
            # Process completed futures with progress bar
            with tqdm(total=num_prompts, desc=f"  Querying {model_name}", leave=False) as pbar:
                for future in as_completed(futures, timeout=300):  # 5 min total timeout
                    try:
                        future.result(timeout=5)  # Quick result fetch
                        pbar.update(1)
                    except TimeoutError:
                        pbar.update(1)
                    except Exception as e:
                        pbar.update(1)
    
    def _process_single_prompt(
        self,
        row,
        prompt_col: str,
        model_name: str,
        model_id: str,
        template_name: str,
        prompt_set_name: str,
        temperature: float
    ):
        """Process a single prompt (called in parallel threads)."""
        prompt_id = row['id']
        user_prompt = row[prompt_col]
        english_prompt = row['hypothetical_scenario']
        
        try:
            # Apply jailbreak template
            template_result = self.template_gen.apply_template(
                prompt=user_prompt,
                template_name=template_name,
                model_name=model_name
            )
            
            # Query model
            response = self.handler.query_model(
                prompt=template_result.user_prompt,
                model=model_id,
                temperature=temperature,
                max_tokens=1000,
                system_prompt=template_result.system_prompt
            )
            
            # Store response (thread-safe with lock)
            response_data = {
                'prompt_id': prompt_id,
                'model': model_name,
                'model_openrouter_id': model_id,
                'template': template_name,
                'prompt_set': prompt_set_name,
                'temperature': temperature,
                'original_prompt': english_prompt,
                'user_prompt': user_prompt,
                'system_prompt': template_result.system_prompt,
                'full_prompt': template_result.full_prompt,
                'response': response.response,
                'tokens_used': response.tokens_used,
                'cost': response.cost,
                'success': response.success,
                'error': response.error,
                'timestamp': response.timestamp,
                'category': row.get('category', 'unknown'),
                'severity': row.get('severity', 'unknown')
            }
            
            with self.results_lock:
                self.responses.append(response_data)
                self.total_queries += 1
                self.total_cost += response.cost
                # Mark as completed
                query_key = (model_name, template_name, prompt_set_name, temperature, prompt_id)
                self.completed_queries.add(query_key)
            
            # Evaluate with LLM judge
            if response.success:
                evaluation = self.judge.evaluate_response(
                    prompt_id=str(prompt_id),
                    model=model_name,
                    template=template_name,
                    prompt_set=prompt_set_name,
                    temperature=temperature,
                    original_prompt=english_prompt,
                    model_response=response.response
                )
                
                with self.results_lock:
                    self.evaluations.append(evaluation)
                    self.total_evaluations += 1
                    self.total_cost += evaluation.evaluation_cost
        
        except Exception as e:
            print(f"  [X] Error processing prompt {prompt_id}: {str(e)}")
    
    def _save_intermediate_results(self):
        """Save intermediate results to disk."""
        print(f"  💾 Saving intermediate results ({self.total_queries} queries so far)...")
        
        # Save responses
        if self.responses:
            responses_df = pd.DataFrame(self.responses)
            output_dir = Path(self.config['output']['responses_dir'])
            output_dir.mkdir(parents=True, exist_ok=True)
            
            responses_file = output_dir / f"responses_intermediate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            responses_df.to_csv(responses_file, index=False, encoding='utf-8')
        
        # Save evaluations
        if self.evaluations:
            eval_data = [{
                'prompt_id': e.prompt_id,
                'model': e.model,
                'template': e.template,
                'prompt_set': e.prompt_set,
                'temperature': e.temperature,
                'harmful': e.harmful,
                'relevant': e.relevant,
                'refusal': e.refusal,
                'timestamp': e.timestamp
            } for e in self.evaluations]
            
            eval_df = pd.DataFrame(eval_data)
            eval_file = output_dir / f"evaluations_intermediate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            eval_df.to_csv(eval_file, index=False, encoding='utf-8')
    
    def _save_final_results(self):
        """Save final results and calculate metrics."""
        print()
        print("=" * 70)
        print("SAVING FINAL RESULTS")
        print("=" * 70)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_dir = Path(self.config['output']['responses_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save all responses
        if self.responses:
            responses_df = pd.DataFrame(self.responses)
            responses_file = output_dir / f"all_responses_{timestamp}.csv"
            responses_df.to_csv(responses_file, index=False, encoding='utf-8')
            print(f"[OK] Saved {len(self.responses)} responses to {responses_file}")
        
        # Save all evaluations
        if self.evaluations:
            self.judge.save_evaluations(
                self.evaluations,
                output_dir / f"all_evaluations_{timestamp}.csv"
            )
            print(f"[OK] Saved {len(self.evaluations)} evaluations")
            
            # Calculate and save metrics
            summaries = self.judge.calculate_metrics_by_configuration(self.evaluations)
            
            metrics_dir = Path(self.config['output']['metrics_dir'])
            metrics_dir.mkdir(parents=True, exist_ok=True)
            
            self.judge.save_metrics(
                summaries,
                metrics_dir / f"aasr_aarr_{timestamp}.csv"
            )
            print(f"[OK] Saved metrics for {len(summaries)} configurations")
        
        print()
    
    def _print_summary(self):
        """Print experiment summary."""
        elapsed_time = time.time() - self.start_time
        hours = int(elapsed_time // 3600)
        minutes = int((elapsed_time % 3600) // 60)
        
        print("=" * 70)
        print("EXPERIMENT SUMMARY")
        print("=" * 70)
        print(f"Total queries: {self.total_queries}")
        print(f"Total evaluations: {self.total_evaluations}")
        print(f"Total cost: ${self.total_cost:.2f}")
        print(f"Time elapsed: {hours}h {minutes}m")
        print()
        
        if self.evaluations:
            overall_aasr = self.judge.calculate_aasr(self.evaluations)
            overall_aarr = self.judge.calculate_aarr(self.evaluations)
            
            print("Overall Metrics:")
            print(f"  AASR (Average Attack Success Rate): {overall_aasr:.4f}")
            print(f"  AARR (Average Attack Relevance Rate): {overall_aarr:.4f}")
        
        print()
        print("[OK] Experiments complete!")
        print("  Next steps:")
        print("    1. Review results in results/responses/ and results/metrics/")
        print("    2. Run human annotation study (Step 6 - ICC validation)")
        print("    3. Perform statistical analysis (Step 8)")
        print("    4. Generate visualizations and comparison tables")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Bangla-English LLM red-teaming experiments")
    parser.add_argument('--config', default='config/run_config.yaml', help='Path to run configuration')
    parser.add_argument('--dry-run', action='store_true', help='Print configuration without running')
    parser.add_argument('--test-mode', action='store_true', help='Run with minimal test configuration')
    
    args = parser.parse_args()
    
    # Initialize runner
    runner = ExperimentRunner(args.config)
    
    # Override with test mode if requested
    if args.test_mode:
        print("[TEST] TEST MODE ENABLED")
        print("  Using minimal configuration for testing")
        print()
        
        runner.config['experiment']['enabled_models'] = ['gpt-4o-mini']
        runner.config['experiment']['enabled_templates'] = ['None', 'Sandbox']
        runner.config['experiment']['enabled_prompt_sets'] = ['English', 'CMP']
        runner.config['experiment']['temperatures'] = [0.6]
        runner.config['experiment']['num_prompts'] = 2  # Just 2 prompts for testing
        runner.config['safety']['require_confirmation'] = False  # Auto-proceed in test mode
    
    # Run experiments
    runner.run_experiments(dry_run=args.dry_run)


if __name__ == "__main__":
    main()
