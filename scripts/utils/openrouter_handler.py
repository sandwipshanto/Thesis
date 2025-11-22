"""
OpenRouter API Handler

This module provides a unified interface for accessing multiple LLMs through OpenRouter API.
Supports ChatGPT, Llama, Gemma, and Mistral models with cost tracking and error handling.

Author: Research Team
Date: November 2025
"""

import os
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import openai
from dotenv import load_dotenv
from tqdm import tqdm


@dataclass
class ModelResponse:
    """Response from a model query."""
    model: str
    prompt: str
    response: str
    temperature: float
    tokens_used: int
    cost: float
    timestamp: str
    success: bool
    error: Optional[str] = None
    metadata: Dict = field(default_factory=dict)


@dataclass
class QueryStats:
    """Statistics for a batch of queries."""
    total_queries: int
    successful_queries: int
    failed_queries: int
    total_tokens: int
    total_cost: float
    average_response_time: float
    models_used: Dict[str, int]


class OpenRouterHandler:
    """
    Handler for OpenRouter API to access multiple LLMs.
    
    This class provides a unified interface for querying different models
    through OpenRouter, with features like:
    - Automatic retry on failure
    - Cost tracking
    - Rate limiting
    - Batch processing
    - Progress tracking
    """
    
    # Model pricing (per 1M tokens) - approximate OpenRouter rates
    MODEL_PRICING = {
        'openai/gpt-4o-mini': {'input': 0.15, 'output': 0.60},
        'meta-llama/llama-3-8b-instruct': {'input': 0.05, 'output': 0.08},
        'google/gemma-1.1-7b-it': {'input': 0.05, 'output': 0.05},
        'mistralai/mistral-7b-instruct-v0.3': {'input': 0.06, 'output': 0.06}
    }
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        timeout: int = 60
    ):
        """
        Initialize OpenRouter handler.
        
        Args:
            api_key: OpenRouter API key (loads from .env if not provided)
            max_retries: Maximum number of retry attempts on failure
            retry_delay: Delay between retries in seconds
            timeout: Request timeout in seconds
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.api_key = api_key or os.getenv('OPENROUTER_API_KEY')
        if not self.api_key:
            raise ValueError("OpenRouter API key not found. Set OPENROUTER_API_KEY in .env file.")
        
        # Get optional settings
        self.base_url = os.getenv('OPENROUTER_BASE_URL', 'https://openrouter.ai/api/v1')
        self.app_name = os.getenv('YOUR_APP_NAME', 'Bangla-English-LLM-Red-Teaming')
        self.site_url = os.getenv('YOUR_SITE_URL', 'https://github.com/sandwipshanto/Thesis')
        
        # Configuration
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.timeout = timeout
        
        # Initialize OpenAI client with OpenRouter
        self.client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            default_headers={
                "HTTP-Referer": self.site_url,
                "X-Title": self.app_name
            }
        )
        
        # Statistics tracking
        self.query_count = 0
        self.total_cost = 0.0
        self.total_tokens = 0
        self.model_usage = {}
    
    def _calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate cost for a query."""
        if model not in self.MODEL_PRICING:
            # Default pricing if model not in list
            return (prompt_tokens + completion_tokens) * 0.0001 / 1000
        
        pricing = self.MODEL_PRICING[model]
        input_cost = (prompt_tokens / 1_000_000) * pricing['input']
        output_cost = (completion_tokens / 1_000_000) * pricing['output']
        
        return input_cost + output_cost
    
    def query_model(
        self,
        prompt: str,
        model: str,
        temperature: float = 0.6,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> ModelResponse:
        """
        Query a single model through OpenRouter.
        
        Args:
            prompt: User prompt
            model: Model identifier (e.g., 'openai/gpt-4o-mini')
            temperature: Sampling temperature (0.0-1.0)
            max_tokens: Maximum tokens in response
            system_prompt: Optional system prompt
            **kwargs: Additional parameters for the API
        
        Returns:
            ModelResponse object with results
        """
        messages = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        # Add user prompt
        messages.append({"role": "user", "content": prompt})
        
        # Attempt query with retries
        for attempt in range(self.max_retries):
            try:
                start_time = time.time()
                
                # Make API call with timeout
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    timeout=self.timeout,
                    **kwargs
                )
                
                # Extract response
                response_text = response.choices[0].message.content
                prompt_tokens = response.usage.prompt_tokens
                completion_tokens = response.usage.completion_tokens
                total_tokens = response.usage.total_tokens
                
                # Calculate cost
                cost = self._calculate_cost(model, prompt_tokens, completion_tokens)
                
                # Update statistics
                self.query_count += 1
                self.total_cost += cost
                self.total_tokens += total_tokens
                self.model_usage[model] = self.model_usage.get(model, 0) + 1
                
                # Create response object
                return ModelResponse(
                    model=model,
                    prompt=prompt,
                    response=response_text,
                    temperature=temperature,
                    tokens_used=total_tokens,
                    cost=cost,
                    timestamp=datetime.now().isoformat(),
                    success=True,
                    metadata={
                        'prompt_tokens': prompt_tokens,
                        'completion_tokens': completion_tokens,
                        'response_time': time.time() - start_time,
                        'attempt': attempt + 1
                    }
                )
            
            except Exception as e:
                error_msg = str(e)
                
                # If last attempt, return error response
                if attempt == self.max_retries - 1:
                    return ModelResponse(
                        model=model,
                        prompt=prompt,
                        response="",
                        temperature=temperature,
                        tokens_used=0,
                        cost=0.0,
                        timestamp=datetime.now().isoformat(),
                        success=False,
                        error=error_msg
                    )
                
                # Wait before retry
                time.sleep(self.retry_delay * (attempt + 1))
    
    def query_batch(
        self,
        prompts: List[str],
        model: str,
        temperature: float = 0.6,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        show_progress: bool = True,
        **kwargs
    ) -> List[ModelResponse]:
        """
        Query multiple prompts with the same model.
        
        Args:
            prompts: List of prompts
            model: Model identifier
            temperature: Sampling temperature
            max_tokens: Maximum tokens in response
            system_prompt: Optional system prompt
            show_progress: Show progress bar
            **kwargs: Additional API parameters
        
        Returns:
            List of ModelResponse objects
        """
        responses = []
        
        iterator = tqdm(prompts, desc=f"Querying {model}") if show_progress else prompts
        
        for prompt in iterator:
            response = self.query_model(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt,
                **kwargs
            )
            responses.append(response)
        
        return responses
    
    def query_multi_model(
        self,
        prompt: str,
        models: List[str],
        temperature: float = 0.6,
        max_tokens: int = 1000,
        system_prompt: Optional[str] = None,
        show_progress: bool = True,
        **kwargs
    ) -> Dict[str, ModelResponse]:
        """
        Query the same prompt across multiple models.
        
        Args:
            prompt: User prompt
            models: List of model identifiers
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            system_prompt: Optional system prompt
            show_progress: Show progress bar
            **kwargs: Additional API parameters
        
        Returns:
            Dictionary mapping model names to responses
        """
        responses = {}
        
        iterator = tqdm(models, desc="Querying models") if show_progress else models
        
        for model in iterator:
            response = self.query_model(
                prompt=prompt,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt,
                **kwargs
            )
            responses[model] = response
        
        return responses
    
    def test_connectivity(self, models: Optional[List[str]] = None) -> Dict[str, bool]:
        """
        Test connectivity to models.
        
        Args:
            models: List of models to test (tests all if None)
        
        Returns:
            Dictionary mapping model names to success status
        """
        if models is None:
            models = list(self.MODEL_PRICING.keys())
        
        results = {}
        test_prompt = "Hello, this is a test message. Please respond with 'OK'."
        
        print("Testing model connectivity...\n")
        
        for model in models:
            print(f"Testing {model}...", end=" ")
            response = self.query_model(
                prompt=test_prompt,
                model=model,
                temperature=0.0,
                max_tokens=10
            )
            
            if response.success:
                print(f"✓ SUCCESS (cost: ${response.cost:.6f})")
                results[model] = True
            else:
                print(f"✗ FAILED ({response.error})")
                results[model] = False
        
        return results
    
    def get_statistics(self) -> QueryStats:
        """Get query statistics."""
        successful = sum(1 for count in self.model_usage.values())
        
        return QueryStats(
            total_queries=self.query_count,
            successful_queries=successful,
            failed_queries=self.query_count - successful,
            total_tokens=self.total_tokens,
            total_cost=self.total_cost,
            average_response_time=0.0,  # Would need to track this
            models_used=self.model_usage.copy()
        )
    
    def save_responses(
        self,
        responses: List[ModelResponse],
        output_path: Union[str, Path],
        format: str = 'jsonl'
    ):
        """
        Save responses to file.
        
        Args:
            responses: List of ModelResponse objects
            output_path: Output file path
            format: Output format ('jsonl' or 'json')
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'jsonl':
            with open(output_path, 'w', encoding='utf-8') as f:
                for response in responses:
                    json.dump({
                        'model': response.model,
                        'prompt': response.prompt,
                        'response': response.response,
                        'temperature': response.temperature,
                        'tokens_used': response.tokens_used,
                        'cost': response.cost,
                        'timestamp': response.timestamp,
                        'success': response.success,
                        'error': response.error,
                        'metadata': response.metadata
                    }, f, ensure_ascii=False)
                    f.write('\n')
        
        elif format == 'json':
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump([{
                    'model': r.model,
                    'prompt': r.prompt,
                    'response': r.response,
                    'temperature': r.temperature,
                    'tokens_used': r.tokens_used,
                    'cost': r.cost,
                    'timestamp': r.timestamp,
                    'success': r.success,
                    'error': r.error,
                    'metadata': r.metadata
                } for r in responses], f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(responses)} responses to {output_path}")


def main():
    """Demo usage of OpenRouter handler."""
    print("=" * 70)
    print("OPENROUTER API HANDLER - CONNECTIVITY TEST")
    print("=" * 70)
    print()
    
    # Initialize handler
    try:
        handler = OpenRouterHandler()
        print(f"✓ OpenRouter handler initialized")
        print(f"  Base URL: {handler.base_url}")
        print(f"  App Name: {handler.app_name}\n")
    except ValueError as e:
        print(f"✗ Error: {e}")
        return
    
    # Test connectivity
    models = [
        'openai/gpt-4o-mini',
        'meta-llama/llama-3-8b-instruct',
        'google/gemma-1.1-7b-it',
        'mistralai/mistral-7b-instruct-v0.3'
    ]
    
    results = handler.test_connectivity(models)
    
    # Print summary
    print("\n" + "=" * 70)
    print("CONNECTIVITY TEST SUMMARY")
    print("=" * 70)
    successful = sum(1 for success in results.values() if success)
    print(f"Models tested: {len(models)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(models) - successful}")
    
    # Get statistics
    stats = handler.get_statistics()
    print(f"\nTotal cost: ${stats.total_cost:.6f}")
    print(f"Total tokens: {stats.total_tokens}")
    
    if successful == len(models):
        print("\n✓ ALL MODELS ACCESSIBLE - Ready for experiments!")
    else:
        print("\n⚠ Some models failed - check API key and funding")


if __name__ == "__main__":
    main()
