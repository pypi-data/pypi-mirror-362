"""
Configuration management for Claude chat application.
"""

class Config:
    """Application configuration settings."""
    
    def __init__(self):
        # Provider selection (ollama, openrouter, google)
        self.provider = "google"  # Default to google
        
        # Legacy settings (for backward compatibility)
        self.host = None  # None means localhost:11434
        self.model = "gemini-2.5-flash"
        self.num_ctx = 2048
        self.thinking_enabled = False  # Default to thinking disabled
        
        # Provider-specific configurations
        self.providers = {
            "ollama": {
                "host": "http://localhost:11434/v1",
                "model": "qwen3:4b",
                "num_ctx": 2048,
                "temperature": 0.7
            },
            "openrouter": {
                "api_key": "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",
                "model": "gemini-2.5-flash-lite-preview-06-17", #"gemini-2.5-flash",
                "num_ctx": 4096,
                "temperature": 0.7
            },
            "google": {
                "api_key": "AIzaSyBb8wTvVw9e25aX8XK-eBuu1JzDEPCdqUE",
                "model": "gemini-2.5-flash",
                "num_ctx": 4096,
                "temperature": 0.7,
                "thinking_budget": 0  # Disable thinking for speed
            },
            "vllm": {
                "base_url": "http://localhost:8000/v1",
                "model": None,  # Auto-detected
                "num_ctx": 4096,
                "temperature": 0.7
            }
        }
    
    def set_provider(self, provider: str) -> None:
        """Set the LLM provider."""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}. Available: {list(self.providers.keys())}")
        self.provider = provider
        
        # Update legacy settings for backward compatibility
        provider_config = self.providers[provider]
        if provider == "ollama":
            self.host = provider_config["host"] if provider_config["host"] != "http://localhost:11434" else None
            self.model = provider_config["model"]
            self.num_ctx = provider_config["num_ctx"]
        elif provider == "openrouter":
            # self.host = "https://openrouter.ai/api/v1"
            self.host = "https://generativelanguage.googleapis.com/v1beta/openai/"
            self.model = provider_config["model"]
            self.num_ctx = provider_config["num_ctx"]
        elif provider == "google":
            self.host = "https://generativelanguage.googleapis.com"
            self.model = provider_config["model"]
            self.num_ctx = provider_config["num_ctx"]
        elif provider == "vllm":
            self.host = provider_config.get("base_url", "http://localhost:8000/v1")
            self.model = provider_config.get("model", "auto-detected")
            self.num_ctx = provider_config["num_ctx"]
    
    def get_provider_config(self, provider: str = None) -> dict:
        """Get configuration for specific provider."""
        provider = provider or self.provider
        return self.providers.get(provider, {})
    
    def get_current_config(self) -> dict:
        """Get current provider configuration."""
        return self.get_provider_config(self.provider)
    
    def set_provider_option(self, provider: str, key: str, value) -> None:
        """Set a specific option for a provider."""
        if provider not in self.providers:
            raise ValueError(f"Unknown provider: {provider}")
        self.providers[provider][key] = value
        
        # Update legacy settings if current provider
        if provider == self.provider:
            self.set_provider(provider)
    
    def set_host(self, host: str) -> None:
        """Set the LLM host URL (legacy compatibility)."""
        if self.provider == "ollama":
            self.providers["ollama"]["host"] = host
            self.host = host if host != "http://localhost:11434" else None
    
    def set_model(self, model: str) -> None:
        """Set the LLM model (legacy compatibility)."""
        self.providers[self.provider]["model"] = model
        self.model = model
    
    def get_host_display(self) -> str:
        """Get host for display purposes."""
        current_config = self.get_current_config()
        if self.provider == "ollama":
            host = current_config.get("host", "http://localhost:11434")
            return host
        elif self.provider == "openrouter":
            return "https://openrouter.ai/api/v1"
        elif self.provider == "google":
            return "https://generativelanguage.googleapis.com"
        elif self.provider == "vllm":
            return current_config.get("base_url", "http://localhost:8000/v1")
        return self.host if self.host else "http://localhost:11434"
    
    def get_provider_display(self) -> str:
        """Get current provider for display."""
        return f"{self.provider.upper()}"

# Global config instance
config = Config()
