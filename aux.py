"""
Module to hold auxiliary fuctions
"""

import pandas as pd

def convert_nan_to_none(value):
    """Convert pandas NaN to None."""
    return value if not pd.isna(value) else None
