"""Cost tracking for PR review operations."""

from dataclasses import dataclass
from typing import ClassVar, Dict, Optional

from .config import LLMProvider


@dataclass
class CostBreakdown:
    """Breakdown of costs for a PR review."""

    llm_input_tokens: int = 0
    llm_output_tokens: int = 0
    llm_cost_usd: float = 0.0
    model_used: str = ""
    pricing_date: str = "2025-05-22"

    def __str__(self) -> str:
        """Human-readable cost summary."""
        return f"""
💰 Cost Breakdown:
   LLM Usage: ${self.llm_cost_usd:.4f} ({self.llm_input_tokens:,} input + {self.llm_output_tokens:,} output tokens)
   Model: {self.model_used}
"""


class CostTracker:
    """Tracks costs for PR review operations."""

    # Default pricing (as of May 2025) - can be overridden in config
    DEFAULT_PRICING: ClassVar[Dict] = {
        LLMProvider.ANTHROPIC: {
            "claude-opus-4-20250514": {
                "input_per_million": 15.00,  # $15.00 per million input tokens
                "output_per_million": 75.00,  # $75.00 per million output tokens
            },
            "claude-sonnet-4-20250514": {
                "input_per_million": 3.00,  # $3.00 per million input tokens
                "output_per_million": 15.00,  # $15.00 per million output tokens
            },
            "claude-3-5-sonnet-20241022": {
                "input_per_million": 3.00,  # $3.00 per million input tokens
                "output_per_million": 15.00,  # $15.00 per million output tokens
            },
            "claude-3-5-sonnet-latest": {
                "input_per_million": 3.00,  # $3.00 per million input tokens
                "output_per_million": 15.00,  # $15.00 per million output tokens
            },
            "claude-3-5-haiku-20241022": {
                "input_per_million": 0.80,  # $0.80 per million input tokens
                "output_per_million": 4.00,  # $4.00 per million output tokens
            },
            "claude-3-5-haiku-latest": {
                "input_per_million": 0.80,  # $0.80 per million input tokens
                "output_per_million": 4.00,  # $4.00 per million output tokens
            },
        },
        LLMProvider.OPENAI: {
            "gpt-4.1": {
                "input_per_million": 2.00,  # $2.00 per million input tokens
                "output_per_million": 8.00,  # $8.00 per million output tokens
            },
            "gpt-4.1-mini": {
                "input_per_million": 0.40,  # $0.40 per million input tokens
                "output_per_million": 1.60,  # $1.60 per million output tokens
            },
            "gpt-4.1-nano": {
                "input_per_million": 0.10,  # $0.10 per million input tokens
                "output_per_million": 0.40,  # $0.40 per million output tokens
            },
            "gpt-4o": {
                "input_per_million": 2.50,  # $2.50 per million input tokens
                "output_per_million": 10.00,  # $10.00 per million output tokens
            },
            "gpt-4o-mini": {
                "input_per_million": 0.15,  # $0.15 per million input tokens
                "output_per_million": 0.60,  # $0.60 per million output tokens
            },
            "gpt-4-turbo": {
                "input_per_million": 10.00,  # $10.00 per million input tokens
                "output_per_million": 30.00,  # $30.00 per million output tokens
            },
        },
        LLMProvider.GOOGLE: {
            # Gemini pricing from https://ai.google.dev/gemini-api/docs/pricing
            "gemini-2.5-flash": {
                "input_per_million": 0.15,  # $0.15 per million input tokens
                "output_per_million": 0.60,  # $0.60 per million output tokens (non-thinking)
            },
            "gemini-2.5-flash-preview": {
                "input_per_million": 0.15,  # $0.15 per million input tokens
                "output_per_million": 0.60,  # $0.60 per million output tokens (non-thinking)
            },
            "gemini-2.5-pro": {
                "input_per_million": 2.50,  # $2.50 per million input tokens (>200k tokens)
                "output_per_million": 15.00,  # $15.00 per million output tokens (>200k tokens)
            },
            "gemini-2.5-pro-preview": {
                "input_per_million": 2.50,  # $2.50 per million input tokens (>200k tokens)
                "output_per_million": 15.00,  # $15.00 per million output tokens (>200k tokens)
            },
            "gemini-2.0-flash": {
                "input_per_million": 0.15,  # Estimated based on Flash pricing pattern
                "output_per_million": 0.60,  # Estimated based on Flash pricing pattern
            },
            "gemini-2.0-flash-lite": {
                "input_per_million": 0.075,  # Estimated - lite version should be cheaper
                "output_per_million": 0.30,  # Estimated - lite version should be cheaper
            },
            "gemini-1.5-flash": {
                "input_per_million": 0.15,  # $0.15 per million input tokens (>128k tokens)
                "output_per_million": 0.60,  # $0.60 per million output tokens (>128k tokens)
            },
            "gemini-1.5-flash-8b": {
                "input_per_million": 0.075,  # $0.075 per million input tokens (>128k tokens)
                "output_per_million": 0.30,  # $0.30 per million output tokens (>128k tokens)
            },
            "gemini-1.5-pro": {
                "input_per_million": 2.50,  # $2.50 per million input tokens (>128k tokens)
                "output_per_million": 10.00,  # $10.00 per million output tokens (>128k tokens)
            },
            # Legacy naming patterns
            "gemini-1.5-pro-latest": {
                "input_per_million": 2.50,  # Same as gemini-1.5-pro
                "output_per_million": 10.00,  # Same as gemini-1.5-pro
            },
            "gemini-1.5-flash-latest": {
                "input_per_million": 0.15,  # Same as gemini-1.5-flash
                "output_per_million": 0.60,  # Same as gemini-1.5-flash
            },
        },
        LLMProvider.OLLAMA: {
            # Ollama is completely free - all models cost $0
            # Latest popular models from ollama.com/library
            "qwen2.5-coder:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "deepseek-r1:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "codellama:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "llama3.3:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "devstral:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "gemma3:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "qwen3:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "phi4:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            # Legacy popular models
            "llama3.2:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "llama3.1:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "llama3:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "mistral:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "deepseek-coder:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "qwen2.5:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            "gemma2:latest": {"input_per_million": 0.00, "output_per_million": 0.00},
            # Default fallback for any Ollama model
            "_default": {"input_per_million": 0.00, "output_per_million": 0.00},
        },
    }

    def __init__(self, custom_pricing: Optional[Dict] = None):
        """Initialize cost tracker with optional custom pricing."""
        self.pricing = custom_pricing or self.DEFAULT_PRICING
        self.reset()

    def reset(self):
        """Reset cost tracking for a new review."""
        self.breakdown = CostBreakdown()

    def track_llm_usage(self, provider: LLMProvider, model: str, input_tokens: int, output_tokens: int):
        """Track LLM API usage and calculate costs."""
        self.breakdown.llm_input_tokens += input_tokens
        self.breakdown.llm_output_tokens += output_tokens

        # Strip prefix from model name for pricing lookup
        stripped_model = self._strip_model_prefix(model)

        # Get pricing for this provider/model
        if provider in self.pricing and stripped_model in self.pricing[provider]:
            pricing = self.pricing[provider][stripped_model]
            input_cost = (input_tokens / 1_000_000) * pricing["input_per_million"]
            output_cost = (output_tokens / 1_000_000) * pricing["output_per_million"]

            self.breakdown.llm_cost_usd += input_cost + output_cost
        elif provider == LLMProvider.OLLAMA:
            # All Ollama models are free - use default $0.00 pricing
            if provider in self.pricing and "_default" in self.pricing[provider]:
                pricing = self.pricing[provider]["_default"]
                self.breakdown.llm_cost_usd += 0.00  # Always free
            else:
                self.breakdown.llm_cost_usd += 0.00  # Fallback - still free
        else:
            # Unknown model - use a reasonable estimate and warn
            print(f"⚠️  Unknown pricing for {provider.value}/{stripped_model}, using estimates")
            print("   Update pricing in ~/.kit/review-config.yaml or check current rates")
            self.breakdown.llm_cost_usd += (input_tokens / 1_000_000) * 3.0
            self.breakdown.llm_cost_usd += (output_tokens / 1_000_000) * 15.0

        # Store the original model name with prefix for reference
        self.breakdown.model_used = model
        self._update_total()

    def _update_total(self):
        """Update total cost."""
        self.breakdown.total_cost_usd = self.breakdown.llm_cost_usd

    def get_cost_summary(self) -> str:
        """Get human-readable cost summary."""
        return str(self.breakdown)

    def get_total_cost(self) -> float:
        """Get total cost in USD for the current review."""
        return self.breakdown.llm_cost_usd

    def extract_anthropic_usage(self, response) -> tuple[int, int]:
        """Extract token usage from Anthropic response."""
        try:
            usage = response.usage
            return usage.input_tokens, usage.output_tokens
        except AttributeError:
            # Fallback if usage info not available
            return 0, 0

    def extract_openai_usage(self, response) -> tuple[int, int]:
        """Extract token usage from OpenAI response."""
        try:
            usage = response.usage
            return usage.prompt_tokens, usage.completion_tokens
        except AttributeError:
            # Fallback if usage info not available
            return 0, 0

    @classmethod
    def get_available_models(cls) -> Dict[str, list[str]]:
        """Get all available models organized by provider."""
        available = {}
        for provider, models in cls.DEFAULT_PRICING.items():
            available[provider.value] = list(models.keys())
        return available

    @classmethod
    def get_all_model_names(cls) -> list[str]:
        """Get a flat list of all available model names."""
        all_models = []
        for provider_models in cls.DEFAULT_PRICING.values():
            all_models.extend(provider_models.keys())
        return sorted(all_models)

    @classmethod
    def _strip_model_prefix(cls, model_name: str) -> str:
        """Strip provider prefixes from model names.

        Examples:
        - vertex_ai/claude-sonnet-4-20250514 -> claude-sonnet-4-20250514
        - openrouter/meta-llama/llama-3.3-70b -> meta-llama/llama-3.3-70b
        - gpt-4o -> gpt-4o (unchanged)
        """
        # Remove anything before the first "/"
        if "/" in model_name:
            return model_name.split("/", 1)[1]

        return model_name

    @classmethod
    def is_valid_model(cls, model_name: str) -> bool:
        """Check if a model name is valid/supported.

        Supports prefixed model names like 'vertex_ai/claude-sonnet-4-20250514'.
        """
        # Try exact match first
        if model_name in cls.get_all_model_names():
            return True

        # Try with prefix stripped
        stripped_model = cls._strip_model_prefix(model_name)
        if stripped_model in cls.get_all_model_names():
            return True

        # Special case for Ollama - any model is valid since it's local
        if ":" in model_name and not model_name.startswith("http"):
            # Looks like an Ollama model (e.g., "llama3:latest", "qwen2.5-coder:7b")
            return True

        return False

    @classmethod
    def get_model_suggestions(cls, invalid_model: str) -> list[str]:
        """Get model suggestions for an invalid model name."""
        all_models = cls.get_all_model_names()
        suggestions = []

        # Strip prefix for comparison
        stripped_invalid = cls._strip_model_prefix(invalid_model).lower()

        # Check for models that start similarly or contain common parts
        for model in all_models:
            lower_model = model.lower()
            # Check if models start similarly
            starts_similar = lower_model.startswith(stripped_invalid[:4]) or stripped_invalid.startswith(
                lower_model[:4]
            )
            # Check if any significant parts match
            parts_match = any(part in lower_model for part in stripped_invalid.split("-")[:2] if len(part) > 2)

            if starts_similar or parts_match:
                suggestions.append(model)

        # If no good matches, return a few popular ones
        if not suggestions:
            popular_models = ["gpt-4.1-nano", "gpt-4o-mini", "claude-3-5-sonnet-20241022"]
            suggestions = popular_models

        return suggestions[:5]  # Limit to 5 suggestions
