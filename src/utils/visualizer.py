"""
Visualization utilities
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path


class Visualizer:
    """Create visualizations for analysis"""
    
    def __init__(self, output_dir: str = None):
        """
        Initialize Visualizer
        
        Args:
            output_dir: Directory to save visualizations. If None, uses default.
        """
        if output_dir is None:
            base_path = Path(__file__).parent.parent.parent
            self.output_dir = base_path / 'outputs' / 'dashboards'
        else:
            self.output_dir = Path(output_dir)
        
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_figure(self, fig, filename: str):
        """Save figure to file"""
        filepath = self.output_dir / filename
        fig.write_html(str(filepath))
        print(f"💾 Saved: {filepath}")
        return filepath
    
    def create_market_snapshot(self, market_data: pd.DataFrame):
        """Create market snapshot visualization"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Total Market Size', 'Company Market Share', 
                          'Category Growth YoY', 'Channel Distribution'),
            specs=[[{'type': 'bar'}, {'type': 'pie'}],
                   [{'type': 'bar'}, {'type': 'bar'}]]
        )
        
        # Add visualizations based on market_data structure
        # This is a template - adjust based on actual data structure
        
        fig.update_layout(height=800, title_text='Market Snapshot Dashboard')
        return fig
    
    def create_product_portfolio_dashboard(self, product_metrics: pd.DataFrame):
        """Create product portfolio dashboard"""
        # Product performance heatmap
        fig = px.imshow(
            product_metrics.select_dtypes(include=[np.number]).T,
            labels=dict(x="Product", y="Metric", color="Value"),
            title='Product Performance Dashboard',
            color_continuous_scale='RdYlGn',
            aspect="auto"
        )
        return fig
    
    def create_bcg_matrix(self, bcg_data: pd.DataFrame):
        """Create BCG Matrix visualization"""
        fig = px.scatter(
            bcg_data,
            x='relative_market_share',
            y='market_growth_rate',
            size='total_revenue',
            color='bcg_category',
            hover_data=['product_name', 'brand', 'market_share_pct'],
            title='BCG Matrix: Innovation Radar',
            labels={
                'relative_market_share': 'Relative Market Share',
                'market_growth_rate': 'Market Growth Rate (%)'
            }
        )
        return fig
    
    def create_forecast_plot(self, historical: pd.Series, forecast: pd.Series, 
                            confidence_interval: tuple = None):
        """Create forecast visualization"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical.index,
            y=historical.values,
            name='Historical',
            line=dict(color='blue')
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast.index,
            y=forecast.values,
            name='Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        # Confidence interval
        if confidence_interval:
            lower, upper = confidence_interval
            fig.add_trace(go.Scatter(
                x=forecast.index,
                y=lower,
                fill=None,
                mode='lines',
                line_color='rgba(255,0,0,0.2)',
                showlegend=False
            ))
            fig.add_trace(go.Scatter(
                x=forecast.index,
                y=upper,
                fill='tonexty',
                mode='lines',
                line_color='rgba(255,0,0,0.2)',
                name='Confidence Interval'
            ))
        
        fig.update_layout(
            title='Sales Forecast',
            xaxis_title='Date',
            yaxis_title='Revenue (IDR)',
            height=500
        )
        
        return fig
    
    def create_cannibalization_chart(self, cannib_data: pd.DataFrame):
        """Create cannibalization analysis visualization"""
        fig = px.bar(
            cannib_data,
            x='pct_change',
            y='old_product',
            color='cannibalization_detected',
            title='Product Cannibalization Impact',
            labels={'pct_change': 'Revenue Change (%)', 'old_product': 'Existing Product'},
            orientation='h'
        )
        fig.add_vline(x=-10, line_dash="dash", line_color="red", 
                     annotation_text="Cannibalization Threshold (-10%)")
        return fig

