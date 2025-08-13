"""
Risk Calculator - Core computation engine for VaR calculations
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class RiskCalculator:
    """Advanced risk calculation engine with multiple VaR methodologies"""
    
    def __init__(self, portfolio, confidence_level: float, time_horizon: int, simulations: int = 10000):
        self.portfolio = portfolio
        self.confidence_level = confidence_level
        self.time_horizon = time_horizon
        self.simulations = simulations
        self.alpha = 1 - confidence_level
        
    def calculate_all_var_methods(self) -> Dict:
        """Calculate VaR using all three methods and additional risk metrics"""
        
        returns = self.portfolio.get_returns()
        portfolio_returns = self.portfolio.get_portfolio_returns()
        
        results = {
            'historical': self._calculate_historical_var(portfolio_returns),
            'parametric': self._calculate_parametric_var(returns),
            'monte_carlo': self._calculate_monte_carlo_var(returns),
            'volatility': self._calculate_volatility(portfolio_returns),
            'sharpe_ratio': self._calculate_sharpe_ratio(portfolio_returns),
            'max_drawdown': self._calculate_max_drawdown(portfolio_returns),
            'var_breakdown': self._calculate_component_var(returns)
        }
        
        return results
    
    def _calculate_historical_var(self, returns: pd.Series) -> float:
        """Historical simulation VaR with bootstrap enhancement"""
        
        # Scale returns to time horizon
        scaled_returns = returns * np.sqrt(self.time_horizon)
        
        # Bootstrap sampling for enhanced accuracy
        bootstrap_samples = []
        for _ in range(1000):
            sample = np.random.choice(scaled_returns, size=len(scaled_returns), replace=True)
            bootstrap_samples.extend(sample)
        
        var_percentile = np.percentile(bootstrap_samples, self.alpha * 100)
        return abs(var_percentile * self.portfolio.value)
    
    def _calculate_parametric_var(self, returns: pd.DataFrame) -> float:
        """Enhanced parametric VaR with EWMA volatility"""
        
        # Calculate EWMA covariance matrix
        cov_matrix = self._calculate_ewma_covariance(returns)
        weights = self.portfolio.get_weights()
        
        # Portfolio variance and volatility
        portfolio_variance = np.dot(weights.T, np.dot(cov_matrix, weights))
        portfolio_vol = np.sqrt(portfolio_variance * self.time_horizon)
        
        # VaR calculation with normal distribution
        z_score = stats.norm.ppf(self.alpha)
        var_value = abs(z_score * portfolio_vol * self.portfolio.value)
        
        return var_value
    
    def _calculate_monte_carlo_var(self, returns: pd.DataFrame) -> float:
        """Advanced Monte Carlo simulation with multiple distributions"""
        
        # Fit distributions to returns
        portfolio_returns = self.portfolio.get_portfolio_returns()
        
        # Use t-distribution for fat tails
        params = stats.t.fit(portfolio_returns)
        
        # Generate scenarios
        scenarios = []
        for _ in range(self.simulations):
            # Random scenario generation
            random_returns = stats.t.rvs(*params, size=self.time_horizon)
            scenario_return = np.sum(random_returns)
            scenarios.append(scenario_return * self.portfolio.value)
        
        var_value = abs(np.percentile(scenarios, self.alpha * 100))
        return var_value
    
    def _calculate_ewma_covariance(self, returns: pd.DataFrame, lambda_param: float = 0.94):
        """Calculate Exponentially Weighted Moving Average covariance matrix"""
        
        returns_clean = returns.dropna()
        n_assets = len(returns_clean.columns)
        n_obs = len(returns_clean)
        
        # Initialize with sample covariance
        cov_matrix = returns_clean.cov().values * 252  # Annualize
        
        # EWMA calculation
        for i in range(1, n_obs):
            return_vec = returns_clean.iloc[i].values.reshape(-1, 1)
            cov_matrix = lambda_param * cov_matrix + (1 - lambda_param) * np.dot(return_vec, return_vec.T)
        
        return cov_matrix
    
    def _calculate_volatility(self, returns: pd.Series) -> float:
        """Calculate portfolio volatility"""
        return returns.std() * np.sqrt(252)
    
    def _calculate_sharpe_ratio(self, returns: pd.Series, risk_free_rate: float = 0.02) -> float:
        """Calculate Sharpe ratio"""
        excess_returns = returns.mean() * 252 - risk_free_rate
        return excess_returns / self._calculate_volatility(returns)
    
    def _calculate_max_drawdown(self, returns: pd.Series) -> float:
        """Calculate maximum drawdown"""
        cumulative_returns = (1 + returns).cumprod()
        rolling_max = cumulative_returns.expanding().max()
        drawdown = (cumulative_returns - rolling_max) / rolling_max
        return abs(drawdown.min())
    
    def _calculate_component_var(self, returns: pd.DataFrame) -> Dict:
        """Calculate component VaR for each asset"""
        weights = self.portfolio.get_weights()
        cov_matrix = returns.cov() * 252
        
        portfolio_var = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        
        component_vars = {}
        for i, asset in enumerate(returns.columns):
            marginal_var = np.dot(cov_matrix.iloc[i], weights) / portfolio_var
            component_var = weights[i] * marginal_var
            component_vars[asset] = component_var * self.portfolio.value
        
        return component_vars
