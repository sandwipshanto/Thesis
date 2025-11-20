"""
Installation Verification Script
Checks all packages are correctly installed for the Bangla-English LLM Red-Teaming project
"""

import sys
print("="*70)
print("INSTALLATION VERIFICATION")
print("="*70)
print(f"Python Version: {sys.version}")
print("="*70)

# Core packages
packages_to_check = [
    ("torch", "PyTorch (CPU)"),
    ("transformers", "HuggingFace Transformers"),
    ("pandas", "Pandas"),
    ("numpy", "NumPy"),
    ("openai", "OpenAI SDK (for OpenRouter)"),
    ("httpx", "HTTPX"),
    ("captum", "Captum (Interpretability)"),
    ("scipy", "SciPy"),
    ("sklearn", "Scikit-learn"),
    ("matplotlib", "Matplotlib"),
    ("seaborn", "Seaborn"),
    ("plotly", "Plotly"),
    ("pingouin", "Pingouin (Statistics)"),
    ("yaml", "PyYAML"),
    ("tqdm", "TQDM (Progress bars)"),
    ("dotenv", "Python-dotenv"),
]

print("\n📦 INSTALLED PACKAGES:")
print("-"*70)

failed = []
for module_name, display_name in packages_to_check:
    try:
        module = __import__(module_name)
        version = getattr(module, "__version__", "✓ installed")
        print(f"✓ {display_name:40} {version}")
    except ImportError as e:
        print(f"✗ {display_name:40} MISSING")
        failed.append(display_name)

print("="*70)

if failed:
    print(f"\n❌ {len(failed)} packages are missing:")
    for pkg in failed:
        print(f"   - {pkg}")
    sys.exit(1)
else:
    print("\n✅ All packages installed successfully!")

# OpenRouter configuration check
print("\n"+"="*70)
print("OPENROUTER API CONFIGURATION")
print("="*70)

import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if api_key and api_key != "your_openrouter_api_key_here":
    print("✓ OpenRouter API key found in .env")
    print(f"  Key preview: {api_key[:8]}...{api_key[-4:]}")
else:
    print("⚠ OpenRouter API key not configured")
    print("  Please add your key to .env file:")
    print("  OPENROUTER_API_KEY=your_actual_key_here")

print("\n" + "="*70)
print("HOW OPENROUTER WORKS")
print("="*70)
print("""
OpenRouter provides a unified API to access multiple LLM providers.
You use the OpenAI Python SDK, but configure it to use OpenRouter's endpoint:

Example:
    from openai import OpenAI
    
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY")
    )
    
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",  # or "meta-llama/llama-3-8b-instruct"
        messages=[{"role": "user", "content": "Hello!"}]
    )

This gives you access to:
  - OpenAI models (gpt-4o-mini)
  - Meta models (llama-3-8b-instruct)
  - Google models (gemma-1.1-7b-it)
  - Mistral models (mistral-7b-instruct-v0.3)
  
All with a single API key and unified billing!
""")

print("="*70)
print("✅ SETUP COMPLETE!")
print("="*70)
print("\nNext steps:")
print("1. Add your OpenRouter API key to .env file")
print("2. Fund your OpenRouter account at https://openrouter.ai/")
print("3. Review config/run_config.yaml for experiment settings")
print("4. Proceed to Step 2: Create base dataset")
print("="*70)
