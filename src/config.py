"""Configuration for CityFlow frontend."""

from pathlib import Path

# Frontend display settings
TITLE = "CityFlow"
SUBTITLE = "AI-Powered Permit Navigator"
DESCRIPTION = "Understand government permits in plain English."

EXAMPLE_QUESTIONS = [
    "I want to open a restaurant. What permits do I need?",
    "What documents are required for hotel registration?",
    "How do I register a food business in Punjab?",
    "What's the process to get a food handling license?",
]

# RAG settings
RAG_TOP_K = 5

# UI states
EMPTY_STATE_MESSAGE = "Ask a permit-related question to get started."
LOADING_MESSAGES = [
    "Analyzing your request...",
    "Searching official documents...",
    "Preparing your permit information...",
]

FALLBACK_MESSAGE = (
    "I couldn't find enough reliable information in the available official sources "
    "to answer this confidently. Please verify with the relevant government authority."
)

DISCLAIMER = (
    "CityFlow provides guidance based on the available official sources. "
    "Requirements may change, so verify important information with the relevant authority."
)

# Paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
STORAGE_DIR = PROJECT_ROOT / "storage"
