"""
Step 2.1: Growth Outlier Detection
Mengidentifikasi SKU dengan pertumbuhan di atas rata-rata kategori
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from scipy import stats


class GrowthOutlierDetector:
    """Detect growth outliers and rising stars"""
    
    def __init__(self, product_metrics: pd.DataFrame, integrated_df: pd.DataFrame):
        """
        Initialize GrowthOutlierDetector
        
        Args:
            product_metrics: Product performance metrics from Phase 1
            integrated_df: Integrated sales data
        """
        self.product_metrics = product_metrics
        self.df = integrated_df
        self.results = {}
    
    def execute(self) -> Dict:
        """
        Execute growth outlier detection
        
        Returns:
            Dictionary with outlier products and analysis
        """
        print("="*80)
        print("PHASE 2.1: GROWTH OUTLIER DETECTION")
        print("="*80)
        
        # Detect growth outliers by category
        self.results['category_outliers'] = self._detect_category_outliers()
        
        # Detect rising stars (low base, high growth)
        self.results['rising_stars'] = self._detect_rising_stars()
        
        # Calculate growth momentum
        self.results['growth_momentum'] = self._calculate_growth_momentum()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Growth Outlier Detection Completed!")
        
        return self.results
    
    def _detect_category_outliers(self) -> Dict:
        """Detect products with growth above category average"""
        outliers_by_category = {}
        
        for category in self.product_metrics['type'].unique():
            category_products = self.product_metrics[self.product_metrics['type'] == category]
            
            if len(category_products) < 2:
                continue
            
            growth_rates = category_products['revenue_growth_3m_pct'].values
            
            # Use IQR method to detect outliers
            Q1 = np.percentile(growth_rates, 25)
            Q3 = np.percentile(growth_rates, 75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Identify outliers (high growth)
            category_outliers = category_products[
                category_products['revenue_growth_3m_pct'] > upper_bound
            ].copy()
            
            category_outliers['outlier_type'] = 'High Growth'
            category_outliers['category_avg_growth'] = category_products['revenue_growth_3m_pct'].mean()
            category_outliers['growth_deviation'] = (
                category_outliers['revenue_growth_3m_pct'] - 
                category_outliers['category_avg_growth']
            )
            
            outliers_by_category[category] = category_outliers
        
        # Combine all outliers
        all_outliers = pd.concat(outliers_by_category.values(), ignore_index=True) if outliers_by_category else pd.DataFrame()
        
        return {
            'by_category': outliers_by_category,
            'all_outliers': all_outliers
        }
    
    def _detect_rising_stars(self) -> pd.DataFrame:
        """Detect rising stars: products with low base but high growth"""
        # Calculate base size (total revenue percentile)
        revenue_percentiles = self.product_metrics['total_revenue'].quantile([0.25, 0.5, 0.75])
        
        # Low base: bottom 50th percentile
        low_base_threshold = revenue_percentiles[0.5]
        
        # High growth: top 25th percentile
        growth_threshold = self.product_metrics['revenue_growth_3m_pct'].quantile(0.75)
        
        rising_stars = self.product_metrics[
            (self.product_metrics['total_revenue'] < low_base_threshold) &
            (self.product_metrics['revenue_growth_3m_pct'] > growth_threshold)
        ].copy()
        
        rising_stars['growth_score'] = (
            rising_stars['revenue_growth_3m_pct'] * 0.7 +
            (1 - rising_stars['total_revenue'] / self.product_metrics['total_revenue'].max()) * 30
        )
        rising_stars = rising_stars.sort_values('growth_score', ascending=False)
        
        return rising_stars
    
    def _calculate_growth_momentum(self) -> pd.DataFrame:
        """Calculate growth momentum (acceleration)"""
        # Compare recent growth vs historical growth
        latest_date = self.df['date'].max()
        
        # Last 3 months
        last_3m = self.df[self.df['date'] >= (latest_date - pd.Timedelta(days=90))]
        
        # Previous 3 months
        prev_3m = self.df[
            (self.df['date'] >= (latest_date - pd.Timedelta(days=180))) &
            (self.df['date'] < (latest_date - pd.Timedelta(days=90)))
        ]
        
        # 3-6 months ago
        old_3m = self.df[
            (self.df['date'] >= (latest_date - pd.Timedelta(days=270))) &
            (self.df['date'] < (latest_date - pd.Timedelta(days=180)))
        ]
        
        # Calculate growth rates
        last_3m_revenue = last_3m.groupby('product_id')['revenue'].sum()
        prev_3m_revenue = prev_3m.groupby('product_id')['revenue'].sum()
        old_3m_revenue = old_3m.groupby('product_id')['revenue'].sum()
        
        recent_growth = ((last_3m_revenue - prev_3m_revenue) / prev_3m_revenue * 100).fillna(0)
        historical_growth = ((prev_3m_revenue - old_3m_revenue) / old_3m_revenue * 100).fillna(0)
        
        # Momentum = acceleration
        momentum = recent_growth - historical_growth
        
        momentum_df = pd.DataFrame({
            'product_id': momentum.index,
            'recent_growth_pct': recent_growth.values,
            'historical_growth_pct': historical_growth.values,
            'momentum': momentum.values
        })
        
        momentum_df = momentum_df.merge(
            self.product_metrics[['product_id', 'product_name']],
            on='product_id',
            how='left'
        )
        
        momentum_df = momentum_df.sort_values('momentum', ascending=False)
        
        return momentum_df
    
    def _print_summary(self):
        """Print summary of growth outliers"""
        print("\n📊 Growth Outlier Summary:")
        
        if len(self.results['category_outliers']['all_outliers']) > 0:
            print(f"   Total Growth Outliers: {len(self.results['category_outliers']['all_outliers'])}")
            print("\n   Top Growth Outliers:")
            top_outliers = self.results['category_outliers']['all_outliers'].nlargest(5, 'revenue_growth_3m_pct')
            for _, row in top_outliers.iterrows():
                print(f"      • {row['product_name']}: {row['revenue_growth_3m_pct']:.1f}% growth "
                      f"(Category avg: {row['category_avg_growth']:.1f}%)")
        else:
            print("   No significant growth outliers detected")
        
        if len(self.results['rising_stars']) > 0:
            print(f"\n   Rising Stars: {len(self.results['rising_stars'])}")
            print("   Products with low base but high growth potential:")
            for _, row in self.results['rising_stars'].head(3).iterrows():
                print(f"      • {row['product_name']}: {row['revenue_growth_3m_pct']:.1f}% growth, "
                      f"Revenue: Rp {row['total_revenue']:,.0f}")
        
        print("\n   Top Momentum Products:")
        top_momentum = self.results['growth_momentum'].head(5)
        for _, row in top_momentum.iterrows():
            print(f"      • {row['product_name']}: Momentum {row['momentum']:.1f}% "
                  f"(Recent: {row['recent_growth_pct']:.1f}%, Historical: {row['historical_growth_pct']:.1f}%)")

