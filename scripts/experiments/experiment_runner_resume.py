"""
Resume Experiment Runner - Continue from Configuration 131

This script resumes the experiment from where it stopped due to disk space.
It will run configurations 131-180 (last 50 configurations).
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from scripts.experiments.experiment_runner import ExperimentRunner
import yaml

def main():
    print("=" * 70)
    print("RESUMING EXPERIMENT FROM CONFIGURATION 131")
    print("=" * 70)
    print()
    
    # Load config
    config_path = "config/run_config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Get all configurations
    models = config['experiment']['enabled_models']
    templates = config['experiment']['enabled_templates']
    prompt_sets = config['experiment']['enabled_prompt_sets']
    temperatures = config['experiment']['temperatures']
    
    # Calculate which configurations to run
    # Configurations 131-180 (last 50)
    total_configs = len(models) * len(templates) * len(prompt_sets) * len(temperatures)
    start_config = 130  # 0-indexed, so this is configuration 131
    
    print(f"Total configurations: {total_configs}")
    print(f"Resuming from configuration: {start_config + 1}")
    print(f"Remaining configurations: {total_configs - start_config}")
    print()
    
    # Calculate which specific configurations to run
    all_configs = []
    config_id = 0
    for model in models:
        for template in templates:
            for prompt_set in prompt_sets:
                for temp in temperatures:
                    if config_id >= start_config:
                        all_configs.append({
                            'model': model,
                            'template': template,
                            'prompt_set': prompt_set,
                            'temperature': temp,
                            'config_id': config_id + 1
                        })
                    config_id += 1
    
    print("Configurations to run:")
    for cfg in all_configs[:5]:
        print(f"  Config {cfg['config_id']}: {cfg['model']} + {cfg['template']} + {cfg['prompt_set']} + T={cfg['temperature']}")
    print(f"  ... ({len(all_configs)} total)")
    print()
    
    # Modify config to run only the remaining configurations
    # We'll do this by temporarily modifying the config
    resume_config = config.copy()
    
    # Calculate which model/template/set/temp combinations are left
    # Based on configuration 131-180
    
    # Configuration pattern: Model(4) × Template(5) × PromptSet(3) × Temp(3)
    # Total: 180 configurations
    # Completed: 130 configurations
    # Remaining: 50 configurations
    
    # Configuration 131 would be:
    # config_id = 130 (0-indexed)
    # model_idx = 130 // (5*3*3) = 130 // 45 = 2 (3rd model = gemma-7b)
    # template_idx = (130 % 45) // (3*3) = 40 // 9 = 4 (5th template = Sandbox)
    # prompt_set_idx = (130 % 9) // 3 = 4 // 3 = 1 (2nd set = CM)
    # temp_idx = 130 % 3 = 1 (2nd temp = 0.6)
    
    # So we need: gemma-7b, Sandbox, CM, 0.6 onwards
    
    # Simpler approach: Just filter the enabled options
    start_model_idx = 2  # gemma-7b (3rd model)
    start_template_idx = 4  # Sandbox (5th template)
    start_prompt_idx = 1  # CM (2nd prompt set)
    start_temp_idx = 1  # 0.6 (2nd temperature)
    
    # For the last 50 configs, we need gemma-7b (all remaining) + mistral-7b (all)
    # Let's just run from where we left off
    
    print("Estimated remaining time: 0.1 hours (with 20 parallel workers)")
    print("Estimated remaining cost: $12.50")
    print()
    print("Auto-proceeding with resume...")
    print()
    
    # Initialize runner
    runner = ExperimentRunner(config_path)
    
    # Load prompts
    prompts = runner.load_prompts()
    
    # Manually run configurations 131-180
    config_counter = 0
    total_configs_to_run = len(all_configs)
    
    for model in models:
        for template in templates:
            for prompt_set in prompt_sets:
                for temp in temperatures:
                    config_id = config_counter
                    config_counter += 1
                    
                    # Skip completed configurations (0-129)
                    if config_id < start_config:
                        continue
                    
                    print()
                    print(f"Configuration {config_id + 1}/{total_configs}")
                    print(f"  Model: {model}")
                    print(f"  Template: {template}")
                    print(f"  Prompt Set: {prompt_set}")
                    print(f"  Temperature: {temp}")
                    print()
                    
                    # Get model ID
                    model_id = runner.get_model_openrouter_id(model)
                    if not model_id:
                        print(f"  [X] Unknown model: {model}")
                        continue
                    
                    # Get prompt dataframe
                    prompt_df = prompts.get(prompt_set)
                    if prompt_df is None:
                        print(f"  [X] Prompt set not found: {prompt_set}")
                        continue
                    
                    # Run this configuration
                    runner._run_single_configuration(
                        model_name=model,
                        model_id=model_id,
                        template_name=template,
                        prompt_set_name=prompt_set,
                        prompt_df=prompt_df,
                        temperature=temp,
                        batch_size=10
                    )
                    
                    # Save intermediate results every 50 queries
                    if runner.total_queries % 50 == 0:
                        runner._save_intermediate_results()
    
    # Save final results
    runner._save_final_results()
    
    print()
    print("=" * 70)
    print("RESUME COMPLETE!")
    print("=" * 70)
    print(f"Total queries completed: {runner.total_queries}")
    print(f"Total cost: ${runner.total_cost:.2f}")
    print()

if __name__ == "__main__":
    main()
