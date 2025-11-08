"""
Step 1.3: Detailed Product Portfolio Analysis
Melakukan 'deep dive' pada setiap produk dalam portofolio
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta


class ProductPortfolio:
    """Analyze detailed product portfolio"""
    
    def __init__(self, integrated_df: pd.DataFrame, marketing_df: pd.DataFrame = None, 
                 reviews_df: pd.DataFrame = None):
        """
        Initialize ProductPortfolio
        
        Args:
            integrated_df: Integrated sales and product data
            marketing_df: Marketing campaigns data
            reviews_df: Customer reviews data
        """
        self.df = integrated_df
        self.marketing_df = marketing_df
        self.reviews_df = reviews_df
        self.product_metrics = None
        self.results = {}
    
    def execute(self) -> Dict:
        """
        Execute product portfolio analysis
        
        Returns:
            Dictionary with product metrics and analysis
        """
        print("="*80)
        print("PHASE 1.3: DETAILED PRODUCT PORTFOLIO ANALYSIS")
        print("="*80)
        
        # Sales performance analysis
        self.results['sales_performance'] = self._analyze_sales_performance()
        
        # Distribution analysis
        self.results['distribution_analysis'] = self._analyze_distribution()
        
        # Pricing & promotion analysis
        self.results['pricing_promotion'] = self._analyze_pricing_promotion()
        
        # Consumer profile (if reviews available)
        if self.reviews_df is not None:
            self.results['consumer_profile'] = self._analyze_consumer_profile()
        
        # Create comprehensive product metrics
        self.product_metrics = self._create_product_metrics()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Product Portfolio Analysis Completed!")
        
        return {
            'product_metrics': self.product_metrics,
            'analysis_results': self.results
        }
    
    def _analyze_sales_performance(self) -> Dict:
        """Analyze sales performance per SKU/Category"""
        # Overall performance
        performance = self.df.groupby('product_id').agg({
            'revenue': ['sum', 'mean', 'std'],
            'units_sold': ['sum', 'mean'],
            'transaction_id': 'count',
            'product_name': 'first',
            'brand': 'first',
            'type': 'first'
        }).round(2)
        
        performance.columns = ['_'.join(col).strip() for col in performance.columns.values]
        performance = performance.reset_index()
        performance = performance.rename(columns={
            'revenue_sum': 'total_revenue',
            'revenue_mean': 'avg_revenue_per_transaction',
            'revenue_std': 'revenue_volatility',
            'units_sold_sum': 'total_units',
            'units_sold_mean': 'avg_units_per_transaction',
            'transaction_id_count': 'total_transactions',
            'product_name_first': 'product_name',
            'brand_first': 'brand',
            'type_first': 'type'
        })
        
        # Growth metrics
        latest_date = self.df['date'].max()
        last_3m = self.df[self.df['date'] >= (latest_date - timedelta(days=90))]
        prev_3m = self.df[
            (self.df['date'] >= (latest_date - timedelta(days=180))) &
            (self.df['date'] < (latest_date - timedelta(days=90)))
        ]
        
        last_3m_revenue = last_3m.groupby('product_id')['revenue'].sum()
        prev_3m_revenue = prev_3m.groupby('product_id')['revenue'].sum()
        
        growth_rate = ((last_3m_revenue - prev_3m_revenue) / prev_3m_revenue * 100).fillna(0)
        performance['revenue_growth_3m_pct'] = performance['product_id'].map(growth_rate).fillna(0).round(2)
        
        # Seasonality analysis
        monthly_sales = self.df.groupby(['product_id', 'month'])['revenue'].sum().reset_index()
        seasonality = monthly_sales.groupby('product_id')['revenue'].std() / monthly_sales.groupby('product_id')['revenue'].mean()
        performance['seasonality_index'] = performance['product_id'].map(seasonality).fillna(0).round(3)
        
        return {
            'overall': performance,
            'monthly_trends': monthly_sales
        }
    
    def _analyze_distribution(self) -> Dict:
        """Analyze distribution by channel"""
        # Channel performance
        channel_performance = self.df.groupby(['product_id', 'channel']).agg({
            'revenue': 'sum',
            'units_sold': 'sum',
            'transaction_id': 'count'
        }).reset_index()
        
        # Geographic reach
        geographic_reach = self.df.groupby('product_id')['region'].nunique().reset_index()
        geographic_reach.columns = ['product_id', 'geographic_reach']
        
        # Channel diversity
        channel_diversity = self.df.groupby('product_id')['channel'].nunique().reset_index()
        channel_diversity.columns = ['product_id', 'channel_diversity']
        
        return {
            'channel_performance': channel_performance,
            'geographic_reach': geographic_reach,
            'channel_diversity': channel_diversity
        }
    
    def _analyze_pricing_promotion(self) -> Dict:
        """Analyze pricing and promotion effectiveness"""
        # Pricing analysis
        pricing = self.df.groupby('product_id').agg({
            'avg_price': ['mean', 'std', 'min', 'max'],
            'base_price': 'first',
            'discount_pct': 'mean',
            'is_discounted': 'sum'
        }).round(2)
        
        pricing.columns = ['_'.join(col).strip() for col in pricing.columns.values]
        pricing = pricing.reset_index()
        pricing = pricing.rename(columns={
            'avg_price_mean': 'avg_price',
            'avg_price_std': 'price_volatility',
            'avg_price_min': 'min_price',
            'avg_price_max': 'max_price',
            'base_price_first': 'base_price',
            'discount_pct_mean': 'avg_discount_pct',
            'is_discounted_sum': 'discounted_transactions'
        })
        
        # Price elasticity (simplified - correlation between discount and units)
        elasticity_data = []
        for product_id in self.df['product_id'].unique():
            product_data = self.df[self.df['product_id'] == product_id]
            if len(product_data) > 10:
                correlation = product_data['discount_pct'].corr(product_data['units_sold'])
                elasticity_data.append({
                    'product_id': product_id,
                    'price_elasticity': correlation if not np.isnan(correlation) else 0
                })
        
        elasticity_df = pd.DataFrame(elasticity_data)
        
        return {
            'pricing': pricing,
            'price_elasticity': elasticity_df
        }
    
    def _analyze_consumer_profile(self) -> Dict:
        """Analyze consumer profile from reviews"""
        if self.reviews_df is None or len(self.reviews_df) == 0:
            return {}
        
        # Rating analysis
        rating_analysis = self.reviews_df.groupby('product_id').agg({
            'rating': ['mean', 'std', 'count'],
            'sentiment': lambda x: (x == 'Positive').sum() / len(x) * 100
        }).round(2)
        
        rating_analysis.columns = ['_'.join(col).strip() if col[1] else col[0] 
                                  for col in rating_analysis.columns.values]
        rating_analysis = rating_analysis.reset_index()
        rating_analysis = rating_analysis.rename(columns={
            'rating_mean': 'avg_rating',
            'rating_std': 'rating_volatility',
            'rating_count': 'total_reviews',
            'sentiment_<lambda>': 'positive_sentiment_pct'
        })
        
        # Platform distribution
        platform_dist = self.reviews_df.groupby(['product_id', 'platform']).size().reset_index(name='count')
        
        return {
            'ratings': rating_analysis,
            'platform_distribution': platform_dist
        }
    
    def _create_product_metrics(self) -> pd.DataFrame:
        """Create comprehensive product metrics table"""
        # Start with sales performance
        metrics = self.results['sales_performance']['overall'].copy()
        
        # Add distribution metrics
        metrics = metrics.merge(
            self.results['distribution_analysis']['geographic_reach'],
            on='product_id',
            how='left'
        )
        metrics = metrics.merge(
            self.results['distribution_analysis']['channel_diversity'],
            on='product_id',
            how='left'
        )
        
        # Add pricing metrics
        pricing = self.results['pricing_promotion']['pricing'][
            ['product_id', 'avg_price', 'price_volatility', 'avg_discount_pct']
        ]
        metrics = metrics.merge(pricing, on='product_id', how='left')
        
        # Add elasticity
        if len(self.results['pricing_promotion']['price_elasticity']) > 0:
            metrics = metrics.merge(
                self.results['pricing_promotion']['price_elasticity'],
                on='product_id',
                how='left'
            )
        
        # Add consumer profile if available
        if 'consumer_profile' in self.results and 'ratings' in self.results['consumer_profile']:
            ratings = self.results['consumer_profile']['ratings'][
                ['product_id', 'avg_rating', 'total_reviews', 'positive_sentiment_pct']
            ]
            metrics = metrics.merge(ratings, on='product_id', how='left')
        
        # Calculate market share
        total_revenue = metrics['total_revenue'].sum()
        metrics['market_share_pct'] = (metrics['total_revenue'] / total_revenue * 100).round(2)
        
        # Fill NaN values
        metrics = metrics.fillna(0)
        
        return metrics
    
    def _print_summary(self):
        """Print summary of product portfolio"""
        print("\n📊 Product Portfolio Summary:")
        print(f"   Total Products Analyzed: {len(self.product_metrics)}")
        
        print("\n🏆 Top 5 Products by Revenue:")
        top_products = self.product_metrics.nlargest(5, 'total_revenue')
        for _, row in top_products.iterrows():
            print(f"   • {row['product_name']}: Rp {row['total_revenue']:,.0f} "
                  f"(Growth: {row['revenue_growth_3m_pct']:.1f}%)")
        
        print("\n📈 Top 5 Growing Products (3M):")
        top_growth = self.product_metrics.nlargest(5, 'revenue_growth_3m_pct')
        for _, row in top_growth.iterrows():
            print(f"   • {row['product_name']}: {row['revenue_growth_3m_pct']:.1f}% growth")

