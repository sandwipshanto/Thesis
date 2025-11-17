"""
Dataset Validation and Analysis Script
Validates the harmful prompts dataset and generates a distribution report
"""

import pandas as pd
from collections import Counter
import sys

# Load the dataset
print("="*70)
print("DATASET VALIDATION - Harmful Prompts (English)")
print("="*70)

try:
    df = pd.read_csv('data/raw/harmful_prompts_english.csv')
    print(f"\n✓ Successfully loaded dataset")
    print(f"  Total prompts: {len(df)}")
except Exception as e:
    print(f"\n✗ Error loading dataset: {e}")
    sys.exit(1)

# Validate structure
print("\n" + "="*70)
print("DATASET STRUCTURE")
print("="*70)

required_columns = ['id', 'dataset_source', 'category', 'original_question', 
                   'hypothetical_scenario', 'severity']
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    print(f"✗ Missing columns: {', '.join(missing_cols)}")
    sys.exit(1)
else:
    print("✓ All required columns present")
    print(f"  Columns: {', '.join(df.columns.tolist())}")

# Check for missing values
print("\n" + "-"*70)
print("Missing Values:")
missing = df.isnull().sum()
if missing.sum() == 0:
    print("✓ No missing values")
else:
    print("⚠ Missing values found:")
    for col, count in missing[missing > 0].items():
        print(f"  {col}: {count}")

# Category distribution
print("\n" + "="*70)
print("CATEGORY DISTRIBUTION")
print("="*70)

category_counts = df['category'].value_counts()
print(f"\nTotal categories: {len(category_counts)}")
print("\nPrompts per category:")
for category, count in category_counts.items():
    percentage = (count / len(df)) * 100
    print(f"  {category:25} {count:2} prompts ({percentage:5.1f}%)")

# Severity distribution
print("\n" + "="*70)
print("SEVERITY DISTRIBUTION")
print("="*70)

severity_counts = df['severity'].value_counts()
print(f"\nSeverity levels:")
for severity, count in severity_counts.items():
    percentage = (count / len(df)) * 100
    print(f"  {severity:10} {count:2} prompts ({percentage:5.1f}%)")

# Validate hypothetical scenario transformation
print("\n" + "="*70)
print("HYPOTHETICAL SCENARIO VALIDATION")
print("="*70)

# Check if scenarios follow the pattern
hypothetical_keywords = ["let's say", "suppose", "imagine", "what if"]
valid_scenarios = df['hypothetical_scenario'].str.lower().str.contains('|'.join(hypothetical_keywords))
valid_count = valid_scenarios.sum()
invalid_count = len(df) - valid_count

print(f"\nScenarios with hypothetical framing:")
print(f"  ✓ Valid: {valid_count}/{len(df)} ({(valid_count/len(df)*100):.1f}%)")
if invalid_count > 0:
    print(f"  ⚠ Potentially invalid: {invalid_count}")
    print("\n  Examples of potentially invalid scenarios:")
    for idx, row in df[~valid_scenarios].head(3).iterrows():
        print(f"    ID {row['id']}: {row['hypothetical_scenario'][:80]}...")

# Sample prompts
print("\n" + "="*70)
print("SAMPLE PROMPTS (Random 5)")
print("="*70)

sample = df.sample(min(5, len(df)))
for _, row in sample.iterrows():
    print(f"\nID: {row['id']} | Category: {row['category']} | Severity: {row['severity']}")
    print(f"Original: {row['original_question']}")
    print(f"Scenario: {row['hypothetical_scenario']}")

# Balance assessment
print("\n" + "="*70)
print("DATASET BALANCE ASSESSMENT")
print("="*70)

# Category balance
max_cat = category_counts.max()
min_cat = category_counts.min()
balance_ratio = min_cat / max_cat if max_cat > 0 else 0

print(f"\nCategory balance:")
print(f"  Max prompts per category: {max_cat}")
print(f"  Min prompts per category: {min_cat}")
print(f"  Balance ratio: {balance_ratio:.2f}")

if balance_ratio >= 0.8:
    print("  ✓ Good balance (ratio ≥ 0.8)")
elif balance_ratio >= 0.6:
    print("  ⚠ Acceptable balance (ratio ≥ 0.6)")
else:
    print("  ✗ Poor balance (ratio < 0.6)")

# Severity balance
severity_order = ['low', 'medium', 'high', 'critical']
print(f"\nSeverity distribution balance:")
for sev in severity_order:
    count = severity_counts.get(sev, 0)
    print(f"  {sev:10} {count:2} prompts")

# Final summary
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

print(f"""
Dataset Statistics:
  Total Prompts: {len(df)}
  Categories: {len(category_counts)}
  Prompts per category: {min_cat}-{max_cat}
  Severity levels: {', '.join(severity_counts.index.tolist())}
  
Dataset Quality:
  ✓ Structure: Valid
  ✓ Completeness: {100 - (missing.sum() / (len(df) * len(df.columns)) * 100):.1f}%
  ✓ Hypothetical framing: {(valid_count/len(df)*100):.1f}%
  ✓ Category balance: {'Good' if balance_ratio >= 0.8 else 'Acceptable' if balance_ratio >= 0.6 else 'Needs improvement'}

Dataset is ready for Step 3: Prompt transformation (CM and CMP)
""")

print("="*70)

# Save distribution report
report = {
    'total_prompts': len(df),
    'categories': len(category_counts),
    'category_distribution': category_counts.to_dict(),
    'severity_distribution': severity_counts.to_dict(),
    'balance_ratio': float(balance_ratio),
    'hypothetical_framing_rate': float(valid_count / len(df))
}

import json
with open('data/raw/dataset_distribution_report.json', 'w') as f:
    json.dump(report, f, indent=2)

print("\n✓ Distribution report saved to: data/raw/dataset_distribution_report.json")
print("="*70)
