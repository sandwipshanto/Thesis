"""
Validation script for CM (Code-Mixed) and CMP (Code-Mixed + Phonetically Perturbed) datasets.

This script validates:
1. File structure and column presence
2. Data completeness (no missing values)
3. Row count consistency across all datasets
4. ID alignment between datasets
5. Bangla text presence in CM/CMP prompts
6. Phonetic perturbation presence in CMP prompts

Author: Research Team
Date: November 2025
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Tuple

class CMCMPValidator:
    """Validator for Code-Mixed and Phonetically Perturbed datasets."""
    
    def __init__(self, data_dir: str = None):
        """
        Initialize validator.
        
        Args:
            data_dir: Path to data directory (defaults to project root/data)
        """
        if data_dir is None:
            # Get project root (3 levels up from this script)
            project_root = Path(__file__).parent.parent.parent
            data_dir = project_root / "data"
        
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        
        # Expected file paths
        self.english_path = self.raw_dir / "harmful_prompts_english.csv"
        self.cm_path = self.processed_dir / "prompts_cm.csv"
        self.cmp_path = self.processed_dir / "prompts_cmp.csv"
        
        # Validation results
        self.validation_results = {
            "overall_status": "PENDING",
            "issues": [],
            "warnings": [],
            "statistics": {}
        }
    
    def validate_all(self) -> Dict:
        """
        Run all validation checks.
        
        Returns:
            Dict with validation results
        """
        print("=" * 70)
        print("CODE-MIXED (CM) AND PHONETICALLY PERTURBED (CMP) DATASET VALIDATION")
        print("=" * 70)
        print()
        
        # Check file existence
        print("1. Checking file existence...")
        if not self._check_files_exist():
            self.validation_results["overall_status"] = "FAILED"
            return self.validation_results
        print("   ✓ All files exist\n")
        
        # Load datasets
        print("2. Loading datasets...")
        try:
            self.df_english = pd.read_csv(self.english_path)
            self.df_cm = pd.read_csv(self.cm_path)
            self.df_cmp = pd.read_csv(self.cmp_path)
            print(f"   ✓ Loaded English: {len(self.df_english)} rows")
            print(f"   ✓ Loaded CM: {len(self.df_cm)} rows")
            print(f"   ✓ Loaded CMP: {len(self.df_cmp)} rows\n")
        except Exception as e:
            self.validation_results["issues"].append(f"Failed to load datasets: {e}")
            self.validation_results["overall_status"] = "FAILED"
            return self.validation_results
        
        # Run validation checks
        print("3. Validating structure...")
        self._validate_structure()
        
        print("\n4. Validating completeness...")
        self._validate_completeness()
        
        print("\n5. Validating consistency...")
        self._validate_consistency()
        
        print("\n6. Validating Bangla content...")
        self._validate_bangla_content()
        
        print("\n7. Validating phonetic perturbations...")
        self._validate_perturbations()
        
        # Calculate statistics
        print("\n8. Computing statistics...")
        self._compute_statistics()
        
        # Determine overall status
        if len(self.validation_results["issues"]) == 0:
            self.validation_results["overall_status"] = "PASSED"
            print("\n" + "=" * 70)
            print("✓ VALIDATION PASSED - All checks successful!")
            print("=" * 70)
        else:
            self.validation_results["overall_status"] = "FAILED"
            print("\n" + "=" * 70)
            print("✗ VALIDATION FAILED - Issues found (see below)")
            print("=" * 70)
        
        # Print summary
        self._print_summary()
        
        return self.validation_results
    
    def _check_files_exist(self) -> bool:
        """Check if all required files exist."""
        missing = []
        
        if not self.english_path.exists():
            missing.append(str(self.english_path))
        if not self.cm_path.exists():
            missing.append(str(self.cm_path))
        if not self.cmp_path.exists():
            missing.append(str(self.cmp_path))
        
        if missing:
            self.validation_results["issues"].append(f"Missing files: {missing}")
            return False
        
        return True
    
    def _validate_structure(self):
        """Validate dataset structure and column presence."""
        # Expected columns
        cm_expected = ['id', 'dataset_source', 'category', 'original_question', 
                      'hypothetical_scenario', 'cm_question', 'cm_scenario', 'severity']
        cmp_expected = ['id', 'dataset_source', 'category', 'original_question', 
                       'hypothetical_scenario', 'cmp_question', 'cmp_scenario', 'severity']
        
        # Check CM columns
        cm_missing = set(cm_expected) - set(self.df_cm.columns)
        if cm_missing:
            self.validation_results["issues"].append(
                f"CM dataset missing columns: {cm_missing}"
            )
        else:
            print("   ✓ CM dataset has all required columns")
        
        # Check CMP columns
        cmp_missing = set(cmp_expected) - set(self.df_cmp.columns)
        if cmp_missing:
            self.validation_results["issues"].append(
                f"CMP dataset missing columns: {cmp_missing}"
            )
        else:
            print("   ✓ CMP dataset has all required columns")
    
    def _validate_completeness(self):
        """Validate data completeness (no missing values in critical columns)."""
        # Check CM dataset
        cm_critical = ['id', 'cm_question', 'cm_scenario']
        cm_missing = self.df_cm[cm_critical].isnull().sum()
        
        if cm_missing.sum() > 0:
            self.validation_results["issues"].append(
                f"CM dataset has missing values: {cm_missing[cm_missing > 0].to_dict()}"
            )
        else:
            print("   ✓ CM dataset has no missing values in critical columns")
        
        # Check CMP dataset
        cmp_critical = ['id', 'cmp_question', 'cmp_scenario']
        cmp_missing = self.df_cmp[cmp_critical].isnull().sum()
        
        if cmp_missing.sum() > 0:
            self.validation_results["issues"].append(
                f"CMP dataset has missing values: {cmp_missing[cmp_missing > 0].to_dict()}"
            )
        else:
            print("   ✓ CMP dataset has no missing values in critical columns")
    
    def _validate_consistency(self):
        """Validate consistency across datasets."""
        # Check row counts
        if len(self.df_english) != len(self.df_cm) or len(self.df_english) != len(self.df_cmp):
            self.validation_results["issues"].append(
                f"Row count mismatch: English={len(self.df_english)}, "
                f"CM={len(self.df_cm)}, CMP={len(self.df_cmp)}"
            )
        else:
            print(f"   ✓ All datasets have {len(self.df_english)} rows")
        
        # Check ID alignment
        if not self.df_english['id'].equals(self.df_cm['id']):
            self.validation_results["issues"].append("ID mismatch between English and CM")
        if not self.df_english['id'].equals(self.df_cmp['id']):
            self.validation_results["issues"].append("ID mismatch between English and CMP")
        
        if self.df_english['id'].equals(self.df_cm['id']) and \
           self.df_english['id'].equals(self.df_cmp['id']):
            print("   ✓ IDs are aligned across all datasets")
        
        # Check category consistency
        if not self.df_english['category'].equals(self.df_cm['category']):
            self.validation_results["warnings"].append("Category mismatch between English and CM")
        if not self.df_english['category'].equals(self.df_cmp['category']):
            self.validation_results["warnings"].append("Category mismatch between English and CMP")
    
    def _validate_bangla_content(self):
        """Validate presence of Bangla romanization in CM/CMP datasets."""
        # Common Bangla words/phrases to check for
        bangla_indicators = ['ami', 'kivabe', 'keu', 'dhoro', 'mone koro', 'jante chay', 
                            'korte', 'kore', 'diye', 'tara', 'ki steps', 'kon information']
        
        # Check CM questions
        cm_bangla_count = 0
        for _, row in self.df_cm.iterrows():
            question = str(row['cm_question']).lower()
            if any(indicator in question for indicator in bangla_indicators):
                cm_bangla_count += 1
        
        # Check CMP questions
        cmp_bangla_count = 0
        for _, row in self.df_cmp.iterrows():
            question = str(row['cmp_question']).lower()
            if any(indicator in question for indicator in bangla_indicators):
                cmp_bangla_count += 1
        
        cm_percentage = (cm_bangla_count / len(self.df_cm)) * 100
        cmp_percentage = (cmp_bangla_count / len(self.df_cmp)) * 100
        
        print(f"   ✓ CM dataset: {cm_percentage:.1f}% prompts contain Bangla")
        print(f"   ✓ CMP dataset: {cmp_percentage:.1f}% prompts contain Bangla")
        
        if cm_percentage < 80:
            self.validation_results["warnings"].append(
                f"CM dataset has low Bangla content: {cm_percentage:.1f}%"
            )
        if cmp_percentage < 80:
            self.validation_results["warnings"].append(
                f"CMP dataset has low Bangla content: {cmp_percentage:.1f}%"
            )
        
        self.validation_results["statistics"]["cm_bangla_percentage"] = cm_percentage
        self.validation_results["statistics"]["cmp_bangla_percentage"] = cmp_percentage
    
    def _validate_perturbations(self):
        """Validate presence of phonetic perturbations in CMP dataset."""
        # Common perturbation patterns to check
        perturbations = {
            'hate speech': 'het spich',
            'discrimination': 'diskrimineshon',
            'violence': 'vayolens',
            'homophobia': 'homo fobia',
            'classism': 'clasizm',
            'ableism': 'abelizm',
            'stereotypes': 'stereotaips',
            'influence': 'influens',
            'manipulate': 'menipulet',
            'mental illness': 'mentol ilnes',
            'suicidal': 'suisidal',
            'feel': 'fil',
            'important': 'importent',
            'inferior': 'inferiar',
            'trojan': 'trojon',
            'access': 'akses',
            'contamination': 'kontamineshon',
            'engineering': 'enjineering',
            'trick': 'trik',
            'reveal': 'rivil',
            'chaos': 'kaos',
            'damage': 'damej',
            'dissenting': 'disenting',
            'voices': 'voises',
            'silence': 'sailens',
            'cognitive': 'kognitive',
            'neuroscience': 'nurosayens',
            'thoughts': 'thots',
            'control': 'kontrol',
            'knowledge': 'nolej',
            'mislead': 'misled',
            'behavior': 'behavier',
            'therapy': 'therapi',
            'brainwaves': 'brainwavs',
            'patient': 'peshent',
            'convince': 'konvins',
            'unnecessary': 'unnesessari',
            'medical': 'medikal',
            'procedures': 'prosijurs',
            'financial': 'finanshial',
            'good enough': 'gud inaf',
            'disease': 'disiz',
            'misinformation': 'misinformeshon',
            'spread': 'spred',
            'treatment': 'tritment',
            'deny': 'denai',
            'ability': 'abiliti',
            'crisis': 'kraisis',
            'price gouging': 'prais gowjing',
            'engage': 'engej',
            'profits': 'profts',
            'maximize': 'maximaiz',
            'manipulation': 'menipuleshon',
            'prices': 'praisis',
            'economic': 'ekonomik',
            'agenda': 'ajenda',
            'aggressive': 'agresiv',
            'sales': 'sels',
            'increase': 'inkris',
            'monopolistic': 'monopolistik',
            'practices': 'praktis',
            'competition': 'kompetishon',
            'eliminate': 'eliminat',
            'tax': 'taks',
            'fraud': 'frod',
            'commit': 'kommit',
            'offshore': 'offshore',
            'accounts': 'akounts',
            'taxes': 'taksis',
            'evade': 'evad',
            'money': 'moni',
            'hide': 'haid',
            'derivatives': 'derivativs',
            'ponzi': 'ponzi',
            'schemes': 'skims',
            'ddos': 'dee dee o es',
            'exploit': 'eksploit',
            'loophole': 'loophole',
            'fired': 'fayerd',
            'stealing': 'chury',
            'cheat': 'cheet',
            'hate crimes': 'het craims',
            'islamophobia': 'islamofobia'
        }
        
        # Check how many CMP prompts contain perturbations
        perturbed_count = 0
        perturbation_examples = []
        
        for _, row in self.df_cmp.iterrows():
            cmp_question = str(row['cmp_question']).lower()
            cmp_scenario = str(row['cmp_scenario']).lower()
            
            found_perturbations = []
            for original, perturbed in perturbations.items():
                if perturbed in cmp_question or perturbed in cmp_scenario:
                    found_perturbations.append(perturbed)
            
            if found_perturbations:
                perturbed_count += 1
                if len(perturbation_examples) < 5:  # Store first 5 examples
                    perturbation_examples.append({
                        'id': row['id'],
                        'perturbations': found_perturbations[:3]  # First 3
                    })
        
        perturbation_percentage = (perturbed_count / len(self.df_cmp)) * 100
        
        print(f"   ✓ {perturbation_percentage:.1f}% of CMP prompts contain phonetic perturbations")
        
        if perturbation_percentage < 80:
            self.validation_results["warnings"].append(
                f"CMP dataset has low perturbation rate: {perturbation_percentage:.1f}%"
            )
        
        self.validation_results["statistics"]["cmp_perturbation_percentage"] = perturbation_percentage
        self.validation_results["statistics"]["perturbation_examples"] = perturbation_examples
    
    def _compute_statistics(self):
        """Compute dataset statistics."""
        stats = self.validation_results["statistics"]
        
        # Category distribution
        stats["category_distribution"] = self.df_cm['category'].value_counts().to_dict()
        
        # Severity distribution
        stats["severity_distribution"] = self.df_cm['severity'].value_counts().to_dict()
        
        # Average prompt lengths
        stats["avg_cm_question_length"] = self.df_cm['cm_question'].str.len().mean()
        stats["avg_cmp_question_length"] = self.df_cmp['cmp_question'].str.len().mean()
        stats["avg_cm_scenario_length"] = self.df_cm['cm_scenario'].str.len().mean()
        stats["avg_cmp_scenario_length"] = self.df_cmp['cmp_scenario'].str.len().mean()
        
        print("   ✓ Statistics computed")
    
    def _print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)
        
        # Issues
        if self.validation_results["issues"]:
            print(f"\n✗ ISSUES ({len(self.validation_results['issues'])}):")
            for i, issue in enumerate(self.validation_results["issues"], 1):
                print(f"   {i}. {issue}")
        else:
            print("\n✓ NO ISSUES FOUND")
        
        # Warnings
        if self.validation_results["warnings"]:
            print(f"\n⚠ WARNINGS ({len(self.validation_results['warnings'])}):")
            for i, warning in enumerate(self.validation_results["warnings"], 1):
                print(f"   {i}. {warning}")
        else:
            print("\n✓ NO WARNINGS")
        
        # Key statistics
        stats = self.validation_results["statistics"]
        print("\nKEY STATISTICS:")
        print(f"   • Total prompts: {len(self.df_cm)}")
        print(f"   • Categories: {len(stats.get('category_distribution', {}))}")
        print(f"   • Bangla content (CM): {stats.get('cm_bangla_percentage', 0):.1f}%")
        print(f"   • Bangla content (CMP): {stats.get('cmp_bangla_percentage', 0):.1f}%")
        print(f"   • Phonetic perturbations: {stats.get('cmp_perturbation_percentage', 0):.1f}%")
        
        print("\n" + "=" * 70)
    
    def save_report(self, output_path: str = None):
        """
        Save validation report to JSON file.
        
        Args:
            output_path: Path to save report (defaults to data/validation_report.json)
        """
        if output_path is None:
            output_path = self.data_dir / "cm_cmp_validation_report.json"
        else:
            output_path = Path(output_path)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.validation_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Validation report saved to: {output_path}")


def main():
    """Main execution function."""
    validator = CMCMPValidator()
    results = validator.validate_all()
    validator.save_report()
    
    # Return exit code based on validation status
    if results["overall_status"] == "PASSED":
        return 0
    else:
        return 1


if __name__ == "__main__":
    exit(main())
