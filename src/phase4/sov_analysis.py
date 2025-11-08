"""
Step 4.2: Source of Volume (SOV) Analysis
Menganalisis dari mana penjualan produk baru berasal
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta
from scipy import stats


class SOVAnalyzer:
    """Analyze source of volume for new product launches"""
    
    def __init__(self, integrated_df: pd.DataFrame, new_launches: pd.DataFrame):
        """
        Initialize SOVAnalyzer
        
        Args:
            integrated_df: Integrated sales data
            new_launches: New launch information from Phase 4.1
        """
        self.df = integrated_df
        self.new_launches = new_launches
        self.results = {}
    
    def execute(self, window_months: int = 6) -> Dict:
        """
        Execute SOV analysis
        
        Args:
            window_months: Months before/after launch to analyze
        
        Returns:
            Dictionary with SOV analysis results
        """
        print("="*80)
        print("PHASE 4.2: SOURCE OF VOLUME (SOV) ANALYSIS")
        print("="*80)
        
        # Check if we have launches to analyze
        if len(self.new_launches) == 0 or 'product_id' not in self.new_launches.columns:
            print("⚠️ No new launches available for SOV analysis")
            return {
                'sov_by_launch': {},
                'sov_breakdown': pd.DataFrame(),
                'significance_tests': {}
            }
        
        # Analyze SOV for each new launch
        self.results['sov_by_launch'] = self._analyze_sov_by_launch(window_months)
        
        # Calculate SOV breakdown
        if len(self.results['sov_by_launch']) > 0:
            self.results['sov_breakdown'] = self._calculate_sov_breakdown()
            
            # Statistical significance testing
            self.results['significance_tests'] = self._perform_significance_tests()
            
            # Print summary
            self._print_summary()
        else:
            print("⚠️ No SOV data calculated (no valid launches found)")
            self.results['sov_breakdown'] = pd.DataFrame()
            self.results['significance_tests'] = {}
        
        print("\n✅ SOV Analysis Completed!")
        
        return self.results
    
    def _analyze_sov_by_launch(self, window_months: int) -> Dict:
        """Analyze SOV for each new launch"""
        sov_results = {}
        
        for _, launch in self.new_launches.iterrows():
            new_product_id = launch['product_id']
            launch_date = launch['launch_date']
            product_type = launch['type']
            product_brand = launch['brand']
            
            # Define periods
            pre_start = launch_date - pd.DateOffset(months=window_months)
            pre_end = launch_date
            post_start = launch_date
            post_end = launch_date + pd.DateOffset(months=window_months)
            
            # New product sales
            new_product_sales = self.df[
                (self.df['product_id'] == new_product_id) &
                (self.df['date'] >= post_start) &
                (self.df['date'] < post_end)
            ]
            new_product_revenue = new_product_sales['revenue'].sum()
            new_product_units = new_product_sales['units_sold'].sum()
            
            # Existing products (same category, same brand)
            existing_products = self.df[
                (self.df['type'] == product_type) &
                (self.df['brand'] == product_brand) &
                (self.df['product_id'] != new_product_id)
            ]
            
            # Pre-launch period
            pre_launch_existing = existing_products[
                (existing_products['date'] >= pre_start) &
                (existing_products['date'] < pre_end)
            ]
            pre_revenue = pre_launch_existing.groupby('product_id')['revenue'].sum()
            
            # Post-launch period
            post_launch_existing = existing_products[
                (existing_products['date'] >= post_start) &
                (existing_products['date'] < post_end)
            ]
            post_revenue = post_launch_existing.groupby('product_id')['revenue'].sum()
            
            # Calculate cannibalization
            cannibalized_revenue = 0
            cannibalized_products = []
            
            for product_id in pre_revenue.index:
                if product_id in post_revenue.index:
                    revenue_change = post_revenue[product_id] - pre_revenue[product_id]
                    if revenue_change < 0:
                        cannibalized_revenue += abs(revenue_change)
                        cannibalized_products.append({
                            'product_id': product_id,
                            'revenue_loss': abs(revenue_change),
                            'pct_change': (revenue_change / pre_revenue[product_id] * 100) if pre_revenue[product_id] > 0 else 0
                        })
            
            # Competitor products (same category, different brand)
            competitor_products = self.df[
                (self.df['type'] == product_type) &
                (self.df['brand'] != product_brand)
            ]
            
            pre_competitor = competitor_products[
                (competitor_products['date'] >= pre_start) &
                (competitor_products['date'] < pre_end)
            ]['revenue'].sum()
            
            post_competitor = competitor_products[
                (competitor_products['date'] >= post_start) &
                (competitor_products['date'] < post_end)
            ]['revenue'].sum()
            
            competitor_loss = pre_competitor - post_competitor if pre_competitor > post_competitor else 0
            
            # Market expansion (total market growth)
            pre_market_total = self.df[
                (self.df['date'] >= pre_start) &
                (self.df['date'] < pre_end) &
                (self.df['type'] == product_type)
            ]['revenue'].sum()
            
            post_market_total = self.df[
                (self.df['date'] >= post_start) &
                (self.df['date'] < post_end) &
                (self.df['type'] == product_type)
            ]['revenue'].sum()
            
            market_expansion = post_market_total - pre_market_total - new_product_revenue
            
            # Calculate SOV breakdown
            total_sov = new_product_revenue
            cannibalization_pct = (cannibalized_revenue / total_sov * 100) if total_sov > 0 else 0
            competitor_pct = (competitor_loss / total_sov * 100) if total_sov > 0 else 0
            expansion_pct = (market_expansion / total_sov * 100) if total_sov > 0 else 0
            
            sov_results[new_product_id] = {
                'new_product_id': new_product_id,
                'new_product_name': launch['product_name'],
                'launch_date': launch_date,
                'new_product_revenue': new_product_revenue,
                'new_product_units': new_product_units,
                'cannibalized_revenue': cannibalized_revenue,
                'cannibalized_products': cannibalized_products,
                'competitor_loss': competitor_loss,
                'market_expansion': market_expansion,
                'sov_breakdown': {
                    'cannibalization_pct': cannibalization_pct,
                    'competitor_pct': competitor_pct,
                    'expansion_pct': expansion_pct
                }
            }
        
        return sov_results
    
    def _calculate_sov_breakdown(self) -> pd.DataFrame:
        """Calculate overall SOV breakdown"""
        breakdowns = []
        
        for product_id, sov_data in self.results['sov_by_launch'].items():
            breakdowns.append({
                'product_id': product_id,
                'product_name': sov_data['new_product_name'],
                'total_revenue': sov_data['new_product_revenue'],
                'cannibalization_pct': sov_data['sov_breakdown']['cannibalization_pct'],
                'competitor_pct': sov_data['sov_breakdown']['competitor_pct'],
                'expansion_pct': sov_data['sov_breakdown']['expansion_pct'],
                'cannibalization_revenue': sov_data['cannibalized_revenue'],
                'competitor_revenue': sov_data['competitor_loss'],
                'expansion_revenue': sov_data['market_expansion']
            })
        
        breakdown_df = pd.DataFrame(breakdowns)
        
        return breakdown_df
    
    def _perform_significance_tests(self) -> Dict:
        """Perform statistical significance tests for cannibalization"""
        significance_results = {}
        
        for product_id, sov_data in self.results['sov_by_launch'].items():
            launch_date = sov_data['launch_date']
            window_months = 6
            
            pre_start = launch_date - pd.DateOffset(months=window_months)
            pre_end = launch_date
            post_start = launch_date
            post_end = launch_date + pd.DateOffset(months=window_months)
            
            # Test for each cannibalized product
            test_results = []
            
            for target in sov_data['cannibalized_products']:
                target_id = target['product_id']
                
                # Get monthly revenue data
                target_sales = self.df[self.df['product_id'] == target_id]
                
                pre_period = target_sales[
                    (target_sales['date'] >= pre_start) &
                    (target_sales['date'] < pre_end)
                ].groupby(target_sales['date'].dt.to_period('M'))['revenue'].sum()
                
                post_period = target_sales[
                    (target_sales['date'] >= post_start) &
                    (target_sales['date'] < post_end)
                ].groupby(target_sales['date'].dt.to_period('M'))['revenue'].sum()
                
                if len(pre_period) > 1 and len(post_period) > 1:
                    # T-test
                    t_stat, p_value = stats.ttest_ind(pre_period, post_period)
                    
                    test_results.append({
                        'target_product_id': target_id,
                        'revenue_loss': target['revenue_loss'],
                        'pct_change': target['pct_change'],
                        't_statistic': t_stat,
                        'p_value': p_value,
                        'is_significant': p_value < 0.05
                    })
            
            significance_results[product_id] = test_results
        
        return significance_results
    
    def _print_summary(self):
        """Print summary of SOV analysis"""
        print("\n📊 SOV Analysis Summary:")
        
        if len(self.results['sov_breakdown']) > 0:
            print("\n   Source of Volume Breakdown:")
            for _, row in self.results['sov_breakdown'].iterrows():
                print(f"\n   {row['product_name']}:")
                print(f"      • Total Revenue: Rp {row['total_revenue']:,.0f}")
                print(f"      • From Cannibalization: {row['cannibalization_pct']:.1f}% "
                      f"(Rp {row['cannibalization_revenue']:,.0f})")
                print(f"      • From Competitors: {row['competitor_pct']:.1f}% "
                      f"(Rp {row['competitor_revenue']:,.0f})")
                print(f"      • From Market Expansion: {row['expansion_pct']:.1f}% "
                      f"(Rp {row['expansion_revenue']:,.0f})")

