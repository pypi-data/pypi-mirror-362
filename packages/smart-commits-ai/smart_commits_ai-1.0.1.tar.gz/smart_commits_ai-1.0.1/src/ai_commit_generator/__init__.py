"""
AI Commit Generator - Automatically generate conventional commit messages using AI.

This package provides an AI-powered Git commit message generator that analyzes
staged changes and creates professional, conventional commit messages using
various AI providers (Groq, OpenRouter, Cohere).
"""

__version__ = "1.0.0"
__author__ = "AI Commit Generator Team"
__email__ = "team@ai-commit-generator.dev"

from .core import CommitGenerator
from .config import Config
from .api_clients import APIClient, GroqClient, OpenRouterClient, CohereClient

__all__ = [
    "CommitGenerator",
    "Config", 
    "APIClient",
    "GroqClient",
    "OpenRouterClient", 
    "CohereClient",
    "__version__",
]
