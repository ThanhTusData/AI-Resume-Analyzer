"""
LLM Client Wrapper
Unified interface for OpenAI, Google Gemini, and other LLM providers
"""

from typing import Optional, List, Dict
from enum import Enum
import openai
import google.generativeai as genai
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class LLMProvider(Enum):
    """Supported LLM providers"""
    OPENAI = "openai"
    GOOGLE = "google"
    ANTHROPIC = "anthropic"


class LLMClient:
    """Universal LLM client for multiple providers"""
    
    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ):
        """
        Initialize LLM client
        
        Args:
            provider: LLM provider name (openai, google, anthropic)
            api_key: API key for the provider
            model: Model name (optional, uses default if not provided)
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
        """
        self.provider = LLMProvider(provider.lower())
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Set default models
        self.model = model or self._get_default_model()
        
        # Initialize provider-specific clients
        self._initialize_client()
        
        logger.info(f"LLM Client initialized: {self.provider.value} - {self.model}")
    
    def _get_default_model(self) -> str:
        """Get default model for provider"""
        defaults = {
            LLMProvider.OPENAI: "gpt-4-turbo-preview",
            LLMProvider.GOOGLE: "gemini-pro",
            LLMProvider.ANTHROPIC: "claude-3-opus-20240229"
        }
        return defaults.get(self.provider, "gpt-4-turbo-preview")
    
    def _initialize_client(self):
        """Initialize provider-specific client"""
        if self.provider == LLMProvider.OPENAI:
            openai.api_key = self.api_key
            self.client = openai
            
        elif self.provider == LLMProvider.GOOGLE:
            genai.configure(api_key=self.api_key)
            self.client = genai.GenerativeModel(self.model)
            
        elif self.provider == LLMProvider.ANTHROPIC:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                logger.error("Anthropic package not installed")
                raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """
        Generate text using the configured LLM
        
        Args:
            prompt: User prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens
            system_prompt: System/instruction prompt
            
        Returns:
            Generated text response
        """
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        logger.debug(f"Generating with {self.provider.value}: {prompt[:100]}...")
        
        try:
            if self.provider == LLMProvider.OPENAI:
                return self._generate_openai(prompt, temp, tokens, system_prompt)
            
            elif self.provider == LLMProvider.GOOGLE:
                return self._generate_google(prompt, temp, tokens, system_prompt)
            
            elif self.provider == LLMProvider.ANTHROPIC:
                return self._generate_anthropic(prompt, temp, tokens, system_prompt)
            
        except Exception as e:
            logger.error(f"Generation error: {str(e)}")
            raise
    
    def _generate_openai(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str]
    ) -> str:
        """Generate using OpenAI"""
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        
        return response.choices[0].message.content
    
    def _generate_google(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str]
    ) -> str:
        """Generate using Google Gemini"""
        # Combine system prompt with user prompt for Gemini
        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_tokens
        )
        
        response = self.client.generate_content(
            full_prompt,
            generation_config=generation_config
        )
        
        return response.text
    
    def _generate_anthropic(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int,
        system_prompt: Optional[str]
    ) -> str:
        """Generate using Anthropic Claude"""
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt if system_prompt else "",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    def generate_batch(
        self,
        prompts: List[str],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        system_prompt: Optional[str] = None
    ) -> List[str]:
        """
        Generate responses for multiple prompts
        
        Args:
            prompts: List of prompts
            temperature: Sampling temperature
            max_tokens: Maximum tokens per response
            system_prompt: System prompt for all requests
            
        Returns:
            List of generated responses
        """
        responses = []
        
        for idx, prompt in enumerate(prompts):
            logger.info(f"Processing prompt {idx + 1}/{len(prompts)}")
            response = self.generate(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                system_prompt=system_prompt
            )
            responses.append(response)
        
        return responses
    
    def generate_structured(
        self,
        prompt: str,
        schema: Dict,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Generate structured output matching a schema
        
        Args:
            prompt: User prompt
            schema: JSON schema for output
            temperature: Sampling temperature
            max_tokens: Maximum tokens
            
        Returns:
            Parsed structured response
        """
        import json
        
        # Append schema instruction to prompt
        schema_prompt = f"{prompt}\n\nPlease provide the response in the following JSON format:\n{json.dumps(schema, indent=2)}"
        
        response = self.generate(
            prompt=schema_prompt,
            temperature=temperature or 0.3,  # Lower temp for structured output
            max_tokens=max_tokens
        )
        
        # Try to extract and parse JSON
        try:
            # Find JSON in response
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in response")
                return {}
                
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return {}
    
    def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text
        
        Args:
            text: Text to count tokens for
            
        Returns:
            Estimated token count
        """
        # Simple estimation: ~4 characters per token
        return len(text) // 4
    
    def get_embedding(self, text: str) -> List[float]:
        """
        Get embedding vector for text
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding vector
        """
        if self.provider == LLMProvider.OPENAI:
            response = openai.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        
        else:
            logger.warning(f"Embeddings not implemented for {self.provider.value}")
            return []
    
    def get_cost_estimate(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Estimate cost for API call
        
        Args:
            prompt_tokens: Number of prompt tokens
            completion_tokens: Number of completion tokens
            
        Returns:
            Estimated cost in USD
        """
        # Pricing as of 2024 (approximate)
        pricing = {
            "gpt-4-turbo-preview": {"prompt": 0.01, "completion": 0.03},
            "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
            "gemini-pro": {"prompt": 0.00025, "completion": 0.0005},
            "claude-3-opus-20240229": {"prompt": 0.015, "completion": 0.075}
        }
        
        model_pricing = pricing.get(self.model, {"prompt": 0.01, "completion": 0.03})
        
        prompt_cost = (prompt_tokens / 1000) * model_pricing["prompt"]
        completion_cost = (completion_tokens / 1000) * model_pricing["completion"]
        
        return prompt_cost + completion_cost