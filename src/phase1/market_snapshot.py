"""
Step 1.2: Overall Market Snapshot
Menganalisis kinerja pasar secara keseluruhan
"""

import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime


class MarketSnapshot:
    """Analyze overall market performance"""
    
    def __init__(self, integrated_df: pd.DataFrame):
        """
        Initialize MarketSnapshot
        
        Args:
            integrated_df: Integrated sales and product data
        """
        self.df = integrated_df
        self.results = {}
    
    def execute(self) -> Dict:
        """
        Execute market snapshot analysis
        
        Returns:
            Dictionary with market metrics
        """
        print("="*80)
        print("PHASE 1.2: OVERALL MARKET SNAPSHOT")
        print("="*80)
        
        # Calculate market size
        self.results['total_market_size'] = self._calculate_market_size()
        
        # Calculate company market share
        self.results['market_share'] = self._calculate_market_share()
        
        # Calculate category growth
        self.results['category_growth'] = self._calculate_category_growth()
        
        # Channel analysis
        self.results['channel_analysis'] = self._analyze_channels()
        
        # Regional analysis
        self.results['regional_analysis'] = self._analyze_regions()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Market Snapshot Analysis Completed!")
        
        return self.results
    
    def _calculate_market_size(self) -> Dict:
        """Calculate total market size"""
        total_revenue = self.df['revenue'].sum()
        total_units = self.df['units_sold'].sum()
        total_transactions = self.df['transaction_id'].nunique()
        
        # Year-over-year comparison
        current_year = self.df['year'].max()
        prev_year = current_year - 1
        
        current_year_revenue = self.df[self.df['year'] == current_year]['revenue'].sum()
        prev_year_revenue = self.df[self.df['year'] == prev_year]['revenue'].sum()
        
        yoy_growth = ((current_year_revenue - prev_year_revenue) / prev_year_revenue * 100) if prev_year_revenue > 0 else 0
        
        return {
            'total_revenue': total_revenue,
            'total_units': total_units,
            'total_transactions': total_transactions,
            'current_year_revenue': current_year_revenue,
            'prev_year_revenue': prev_year_revenue,
            'yoy_growth_pct': yoy_growth
        }
    
    def _calculate_market_share(self) -> pd.DataFrame:
        """Calculate market share by product/category"""
        # By product
        product_share = self.df.groupby('product_id').agg({
            'revenue': 'sum',
            'product_name': 'first',
            'brand': 'first',
            'type': 'first'
        }).reset_index()
        
        total_revenue = product_share['revenue'].sum()
        product_share['market_share_pct'] = (product_share['revenue'] / total_revenue * 100).round(2)
        product_share = product_share.sort_values('market_share_pct', ascending=False)
        
        # By category
        category_share = self.df.groupby('type').agg({
            'revenue': 'sum'
        }).reset_index()
        category_share['market_share_pct'] = (category_share['revenue'] / total_revenue * 100).round(2)
        category_share = category_share.sort_values('market_share_pct', ascending=False)
        
        # By brand
        brand_share = self.df.groupby('brand').agg({
            'revenue': 'sum'
        }).reset_index()
        brand_share['market_share_pct'] = (brand_share['revenue'] / total_revenue * 100).round(2)
        brand_share = brand_share.sort_values('market_share_pct', ascending=False)
        
        return {
            'by_product': product_share,
            'by_category': category_share,
            'by_brand': brand_share
        }
    
    def _calculate_category_growth(self) -> pd.DataFrame:
        """Calculate category growth YoY and QoQ"""
        # Year-over-year growth
        current_year = self.df['year'].max()
        prev_year = current_year - 1
        
        current_year_category = self.df[self.df['year'] == current_year].groupby('type')['revenue'].sum()
        prev_year_category = self.df[self.df['year'] == prev_year].groupby('type')['revenue'].sum()
        
        yoy_growth = ((current_year_category - prev_year_category) / prev_year_category * 100).round(2)
        
        # Quarter-over-quarter growth
        latest_quarter = self.df['quarter'].max()
        latest_year = self.df['year'].max()
        
        current_quarter = self.df[
            (self.df['year'] == latest_year) & (self.df['quarter'] == latest_quarter)
        ].groupby('type')['revenue'].sum()
        
        prev_quarter = latest_quarter - 1
        if prev_quarter == 0:
            prev_quarter = 4
            prev_year_quarter = latest_year - 1
        else:
            prev_year_quarter = latest_year
        
        previous_quarter = self.df[
            (self.df['year'] == prev_year_quarter) & (self.df['quarter'] == prev_quarter)
        ].groupby('type')['revenue'].sum()
        
        qoq_growth = ((current_quarter - previous_quarter) / previous_quarter * 100).round(2)
        
        growth_df = pd.DataFrame({
            'category': yoy_growth.index,
            'yoy_growth_pct': yoy_growth.values,
            'qoq_growth_pct': qoq_growth.values if len(qoq_growth) > 0 else [0] * len(yoy_growth)
        })
        
        return growth_df
    
    def _analyze_channels(self) -> pd.DataFrame:
        """Analyze channel performance"""
        channel_metrics = self.df.groupby('channel').agg({
            'revenue': ['sum', 'mean'],
            'units_sold': 'sum',
            'transaction_id': 'count',
            'discount_pct': 'mean'
        }).round(2)
        
        channel_metrics.columns = ['_'.join(col).strip() for col in channel_metrics.columns.values]
        channel_metrics = channel_metrics.reset_index()
        channel_metrics = channel_metrics.rename(columns={
            'revenue_sum': 'total_revenue',
            'revenue_mean': 'avg_revenue_per_transaction',
            'units_sold_sum': 'total_units',
            'transaction_id_count': 'total_transactions',
            'discount_pct_mean': 'avg_discount_pct'
        })
        
        total_revenue = channel_metrics['total_revenue'].sum()
        channel_metrics['revenue_share_pct'] = (channel_metrics['total_revenue'] / total_revenue * 100).round(2)
        channel_metrics = channel_metrics.sort_values('total_revenue', ascending=False)
        
        return channel_metrics
    
    def _analyze_regions(self) -> pd.DataFrame:
        """Analyze regional performance"""
        region_metrics = self.df.groupby('region').agg({
            'revenue': 'sum',
            'units_sold': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        region_metrics = region_metrics.rename(columns={
            'revenue': 'total_revenue',
            'units_sold': 'total_units',
            'transaction_id': 'total_transactions'
        })
        
        total_revenue = region_metrics['total_revenue'].sum()
        region_metrics['revenue_share_pct'] = (region_metrics['total_revenue'] / total_revenue * 100).round(2)
        region_metrics = region_metrics.sort_values('total_revenue', ascending=False)
        
        return region_metrics
    
    def _print_summary(self):
        """Print summary of market snapshot"""
        print("\n📊 Market Snapshot Summary:")
        print(f"   Total Market Revenue: Rp {self.results['total_market_size']['total_revenue']:,.0f}")
        print(f"   Total Units Sold: {self.results['total_market_size']['total_units']:,.0f}")
        print(f"   Total Transactions: {self.results['total_market_size']['total_transactions']:,}")
        print(f"   YoY Growth: {self.results['total_market_size']['yoy_growth_pct']:.2f}%")
        
        print("\n🏆 Top 5 Products by Market Share:")
        top_products = self.results['market_share']['by_product'].head(5)
        for _, row in top_products.iterrows():
            print(f"   • {row['product_name']}: {row['market_share_pct']:.2f}%")
        
        print("\n📈 Top Growing Categories (YoY):")
        top_categories = self.results['category_growth'].nlargest(5, 'yoy_growth_pct')
        for _, row in top_categories.iterrows():
            print(f"   • {row['category']}: {row['yoy_growth_pct']:.2f}%")

