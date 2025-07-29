"""
Pyhtelasso: A Python package for detecting treatment effect heterogeneity using debiased lasso.

This package implements a novel approach for detecting treatment effect heterogeneity:
1. Transform outcome: y* = y * (t - p) / (p * (1 - p))
2. Run debiased lasso on y* ~ X to identify significant moderators

Author: [Your Name]
License: MIT
"""

from .pyhtelasso import (
    HTELasso
)

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

__all__ = [
    "HTELasso",
]
