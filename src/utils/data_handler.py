"""
Data Handler - Advanced data processing and validation
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

class DataHandler:
    """Advanced data processing and validation utilities"""
    
    @staticmethod
    def validate_data(data: pd.DataFrame, min_observations: int = 100) -> Tuple[bool, str]:
        """Validate data quality and completeness"""
        
        if data.empty:
            return False, "Data is empty"
        
        if len(data) < min_observations:
            return False, f"Insufficient data: {len(data)} observations (minimum: {min_observations})"
        
        # Check for excessive missing values
        missing_pct = data.isnull().sum() / len(data)
        if (missing_pct > 0.1).any():
            return False, "Excessive missing values detected"
        
        # Check for constant values
        if (data.std() == 0).any():
            return False, "Constant values detected in data"
        
        return True, "Data validation passed"
    
    @staticmethod
    def clean_data(data: pd.DataFrame, method: str = "drop") -> pd.DataFrame:
        """Clean data using various methods"""
        
        if method == "drop":
            return data.dropna()
        
        elif method == "forward_fill":
            return data.fillna(method='ffill')
        
        elif method == "interpolate":
            return data.interpolate()
        
        else:
            return data.dropna()
    
    @staticmethod
    def detect_outliers(data: pd.Series, method: str = "iqr", threshold: float = 3.0) -> pd.Series:
        """Detect outliers using various methods"""
        
        if method == "iqr":
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            return (data < lower) | (data > upper)
        
        elif method == "zscore":
            z_scores = np.abs((data - data.mean()) / data.std())
            return z_scores > threshold
        
        else:
            return pd.Series([False] * len(data), index=data.index)
    
    @staticmethod
    def calculate_returns(prices: pd.DataFrame, method: str = "log") -> pd.DataFrame:
        """Calculate returns using different methods"""
        
        if method == "log":
            return np.log(prices / prices.shift(1))
        
        elif method == "simple":
            return prices.pct_change()
        
        elif method == "continuous":
            return np.log(prices / prices.shift(1))
        
        else:
            return np.log(prices / prices.shift(1))
