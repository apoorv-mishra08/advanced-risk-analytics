"""
Portfolio Manager - Handles portfolio construction and data management
"""

import pandas as pd
import numpy as np
import yfinance as yf
from typing import List, Dict
import warnings
warnings.filterwarnings('ignore')

class PortfolioManager:
    """Advanced portfolio management with multiple weighting schemes"""
    
    def __init__(self, assets: List[str], start_date, end_date, portfolio_value: float):
        self.assets = assets
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.value = portfolio_value
        
        # Download and process data
        self.price_data = self._download_data()
        self.returns_data = self._calculate_returns()
        self.weights = self._calculate_weights()
        
    def _download_data(self) -> pd.DataFrame:
        """Download price data with error handling"""
        try:
            data = yf.download(
                self.assets, 
                start=self.start_date, 
                end=self.end_date,
                progress=False
            )
            
            if len(self.assets) == 1:
                return data['Adj Close'].to_frame(self.assets[0])
            else:
                return data['Adj Close']
                
        except Exception as e:
            raise ValueError(f"Error downloading data: {str(e)}")
    
    def _calculate_returns(self) -> pd.DataFrame:
        """Calculate log returns"""
        returns = np.log(self.price_data / self.price_data.shift(1))
        return returns.dropna()
    
    def _calculate_weights(self, method: str = "equal") -> np.array:
        """Calculate portfolio weights using different methods"""
        
        n_assets = len(self.assets)
        
        if method == "equal":
            return np.array([1/n_assets] * n_assets)
        
        elif method == "market_cap":
            # Use market cap weighting (simplified with recent prices)
            recent_prices = self.price_data.iloc[-1]
            market_caps = recent_prices / recent_prices.sum()
            return market_caps.values
        
        elif method == "risk_parity":
            # Simplified risk parity
            returns = self.returns_data
            inv_vol = 1 / returns.std()
            weights = inv_vol / inv_vol.sum()
            return weights.values
        
        else:
            return np.array([1/n_assets] * n_assets)
    
    def get_returns(self) -> pd.DataFrame:
        """Get individual asset returns"""
        return self.returns_data
    
    def get_portfolio_returns(self) -> pd.Series:
        """Calculate weighted portfolio returns"""
        return (self.returns_data * self.weights).sum(axis=1)
    
    def get_weights(self) -> np.array:
        """Get portfolio weights"""
        return self.weights
    
    def get_correlation_matrix(self) -> pd.DataFrame:
        """Calculate correlation matrix"""
        return self.returns_data.corr()
    
    def rebalance_portfolio(self, method: str = "equal"):
        """Rebalance portfolio with new weights"""
        self.weights = self._calculate_weights(method)
    
    def get_performance_metrics(self) -> Dict:
        """Calculate portfolio performance metrics"""
        portfolio_returns = self.get_portfolio_returns()
        
        metrics = {
            'total_return': (1 + portfolio_returns).prod() - 1,
            'annualized_return': portfolio_returns.mean() * 252,
            'annualized_volatility': portfolio_returns.std() * np.sqrt(252),
            'skewness': portfolio_returns.skew(),
            'kurtosis': portfolio_returns.kurtosis()
        }
        
        return metrics
