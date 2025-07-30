"""Configuration management for AI Commit Generator."""

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Configuration-related errors."""

    pass


class Config:
    """Configuration manager for AI Commit Generator."""

    # Default configuration values
    DEFAULT_CONFIG = {
        "api": {
            "provider": "groq",
            "models": {
                "groq": {
                    "default": "llama3-70b-8192",
                    "alternatives": ["llama3-8b-8192", "mixtral-8x7b-32768"],
                },
                "openrouter": {
                    "default": "meta-llama/llama-3.1-70b-instruct",
                    "alternatives": [
                        "anthropic/claude-3.5-sonnet",
                        "google/gemini-pro-1.5",
                    ],
                },
                "cohere": {
                    "default": "command-r-plus",
                    "alternatives": ["command-r", "command-light"],
                },
            },
        },
        "commit": {
            "max_chars": 72,
            "types": [
                "feat",
                "fix",
                "docs",
                "style",
                "refactor",
                "perf",
                "test",
                "build",
                "ci",
                "chore",
                "revert",
            ],
            "scopes": [
                "api",
                "auth",
                "ui",
                "db",
                "config",
                "deps",
                "security",
                "performance",
                "i18n",
                "tests",
            ],
        },
        "processing": {
            "max_diff_size": 8000,
            "exclude_patterns": [
                "*.lock",
                "*.log",
                "node_modules/*",
                ".git/*",
                "dist/*",
                "build/*",
                "*.min.js",
                "*.min.css",
            ],
            "truncate_files": True,
            "max_file_lines": 100,
        },
        "fallback": {
            "default_message": "chore: update files",
            "max_retries": 3,
            "retry_delay": 1,
        },
        "debug": {
            "enabled": False,
            "log_file": ".commitgen.log",
            "save_requests": False,
        },
    }

    def __init__(self, repo_root: Optional[Path] = None):
        """Initialize configuration.

        Args:
            repo_root: Root directory of the Git repository. If None, will try to detect.
        """
        self.repo_root = repo_root or self._find_repo_root()
        self.config_file = self.repo_root / ".commitgen.yml"
        self.env_file = self.repo_root / ".env"

        # Load configuration
        self._config = self._load_config()
        self._load_env()

    def _find_repo_root(self) -> Path:
        """Find the Git repository root directory."""
        current = Path.cwd()
        while current != current.parent:
            if (current / ".git").exists():
                return current
            current = current.parent
        raise ConfigError("Not in a Git repository")

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from .commitgen.yml file."""
        config = self.DEFAULT_CONFIG.copy()

        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f) or {}
                config = self._merge_config(config, user_config)
                logger.debug(f"Loaded configuration from {self.config_file}")
            except yaml.YAMLError as e:
                raise ConfigError(f"Invalid YAML in {self.config_file}: {e}")
            except Exception as e:
                raise ConfigError(f"Error reading {self.config_file}: {e}")
        else:
            logger.debug("No configuration file found, using defaults")

        return config

    def _merge_config(
        self, base: Dict[str, Any], override: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Recursively merge configuration dictionaries."""
        result = base.copy()
        for key, value in override.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result

    def _load_env(self) -> None:
        """Load environment variables from .env file."""
        if self.env_file.exists():
            load_dotenv(self.env_file)
            logger.debug(f"Loaded environment from {self.env_file}")

    @property
    def provider(self) -> str:
        """Get the configured AI provider."""
        return self._config["api"]["provider"]

    @property
    def model(self) -> str:
        """Get the model for the current provider."""
        provider = self.provider
        models = self._config["api"]["models"].get(provider, {})

        # Check for environment variable override
        env_var = f"{provider.upper()}_MODEL"
        env_model = os.getenv(env_var)
        if env_model:
            return env_model

        return models.get("default", "llama3-70b-8192")

    @property
    def api_key(self) -> str:
        """Get the API key for the current provider."""
        provider = self.provider
        env_var = f"{provider.upper()}_API_KEY"
        api_key = os.getenv(env_var)

        if not api_key:
            raise ConfigError(
                f"API key not found. Please set {env_var} in your .env file"
            )

        return api_key

    @property
    def max_chars(self) -> int:
        """Get maximum characters for commit message."""
        return self._config["commit"]["max_chars"]

    @property
    def commit_types(self) -> List[str]:
        """Get allowed commit types."""
        return self._config["commit"]["types"]

    @property
    def commit_scopes(self) -> List[str]:
        """Get allowed commit scopes."""
        return self._config["commit"]["scopes"]

    @property
    def max_diff_size(self) -> int:
        """Get maximum diff size to send to AI."""
        return self._config["processing"]["max_diff_size"]

    @property
    def exclude_patterns(self) -> List[str]:
        """Get file patterns to exclude from diff."""
        return self._config["processing"]["exclude_patterns"]

    @property
    def max_retries(self) -> int:
        """Get maximum number of API retries."""
        return self._config["fallback"]["max_retries"]

    @property
    def retry_delay(self) -> int:
        """Get delay between retries in seconds."""
        return self._config["fallback"]["retry_delay"]

    @property
    def default_message(self) -> str:
        """Get default fallback commit message."""
        return self._config["fallback"]["default_message"]

    @property
    def debug_enabled(self) -> bool:
        """Check if debug mode is enabled."""
        return (
            self._config["debug"]["enabled"]
            or os.getenv("DEBUG_ENABLED", "").lower() == "true"
        )

    @property
    def log_file(self) -> Path:
        """Get debug log file path."""
        return self.repo_root / self._config["debug"]["log_file"]

    def get_prompt_template(self) -> str:
        """Get the prompt template for AI generation."""
        template = self._config.get("prompt", {}).get("template")
        if not template:
            # Default template
            template = """Generate a conventional commit message under {max_chars} characters for the following git diff.

Use one of these types: {types}

If applicable, include a scope in parentheses after the type.

Format: type(scope): description

Be concise and descriptive. Focus on WHAT changed, not HOW.

Git diff:
{diff}

Respond with ONLY the commit message, no explanations or additional text."""

        return template

    def validate(self) -> None:
        """Validate the configuration."""
        # Validate provider
        valid_providers = ["groq", "openrouter", "cohere"]
        if self.provider not in valid_providers:
            raise ConfigError(
                f"Invalid provider '{self.provider}'. Must be one of: {valid_providers}"
            )

        # Validate API key exists
        try:
            self.api_key
        except ConfigError:
            raise ConfigError(f"API key not configured for provider '{self.provider}'")

        # Validate numeric values
        if self.max_chars <= 0:
            raise ConfigError("max_chars must be positive")
        if self.max_diff_size <= 0:
            raise ConfigError("max_diff_size must be positive")
        if self.max_retries < 0:
            raise ConfigError("max_retries must be non-negative")
        if self.retry_delay < 0:
            raise ConfigError("retry_delay must be non-negative")
