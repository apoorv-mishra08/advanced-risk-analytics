"""
Risk Visualization - Advanced plotting capabilities
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

class RiskVisualizer:
    """Advanced visualization suite for risk analytics"""
    
    def __init__(self):
        self.color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
    
    def plot_var_distribution(self, results: dict) -> go.Figure:
        """Create VaR comparison chart"""
        
        methods = ['Historical', 'Parametric', 'Monte Carlo']
        values = [results['historical'], results['parametric'], results['monte_carlo']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=methods,
                y=values,
                marker_color=self.color_palette[:3],
                text=[f'${v:,.0f}' for v in values],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title='Value-at-Risk Comparison',
            xaxis_title='VaR Method',
            yaxis_title='VaR Value ($)',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_risk_decomposition(self, portfolio) -> go.Figure:
        """Create risk decomposition pie chart"""
        
        returns = portfolio.get_returns()
        weights = portfolio.get_weights()
        
        # Calculate individual asset volatilities
        asset_vols = returns.std() * np.sqrt(252)
        risk_contributions = weights * asset_vols
        risk_contributions = risk_contributions / risk_contributions.sum()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=portfolio.assets,
                values=risk_contributions,
                hole=0.4,
                marker_colors=self.color_palette[:len(portfolio.assets)]
            )
        ])
        
        fig.update_layout(
            title='Portfolio Risk Decomposition',
            template='plotly_white',
            height=400
        )
        
        return fig
    
    def plot_time_series(self, portfolio) -> go.Figure:
        """Create time series analysis chart"""
        
        returns = portfolio.get_portfolio_returns()
        cumulative_returns = (1 + returns).cumprod()
        
        # Calculate rolling volatility
        rolling_vol = returns.rolling(window=30).std() * np.sqrt(252)
        
        fig = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Cumulative Returns', 'Rolling Volatility'),
            vertical_spacing=0.1
        )
        
        # Cumulative returns
        fig.add_trace(
            go.Scatter(
                x=cumulative_returns.index,
                y=cumulative_returns.values,
                mode='lines',
                name='Cumulative Returns',
                line=dict(color=self.color_palette[0])
            ),
            row=1, col=1
        )
        
        # Rolling volatility
        fig.add_trace(
            go.Scatter(
                x=rolling_vol.index,
                y=rolling_vol.values,
                mode='lines',
                name='30-Day Rolling Volatility',
                line=dict(color=self.color_palette[1])
            ),
            row=2, col=1
        )
        
        fig.update_layout(
            height=600,
            template='plotly_white',
            title_text="Portfolio Performance Analysis"
        )
        
        return fig
    
    def plot_correlation_heatmap(self, portfolio) -> go.Figure:
        """Create correlation heatmap"""
        
        corr_matrix = portfolio.get_correlation_matrix()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=np.round(corr_matrix.values, 2),
            texttemplate="%{text}",
            textfont={"size": 10}
        ))
        
        fig.update_layout(
            title='Asset Correlation Matrix',
            template='plotly_white',
            height=500
        )
        
        return fig
