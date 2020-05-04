"""Twilight for GitHub is a machine learning-based utility to analyze commit history on Github."""
from .cli import main
from .analysis import create_dataset, analyze_dataset
from .repo import GHRepositoryWeeksum

__version__ = '0.1.0'
