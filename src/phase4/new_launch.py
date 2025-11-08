"""
Step 4.1: New Launch Identification
Memilih 3-5 peluncuran produk baru terbesar dalam 12 bulan terakhir
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta


class NewLaunchIdentifier:
    """Identify new product launches for cannibalization analysis"""
    
    def __init__(self, products_df: pd.DataFrame, integrated_df: pd.DataFrame):
        """
        Initialize NewLaunchIdentifier
        
        Args:
            products_df: Product master data
            integrated_df: Integrated sales data
        """
        self.products_df = products_df
        self.df = integrated_df
        self.results = {}
    
    def execute(self, months: int = 12, top_n: int = 5) -> Dict:
        """
        Execute new launch identification
        
        Args:
            months: Number of months to look back for new launches
            top_n: Number of top launches to select
        
        Returns:
            Dictionary with new launch information
        """
        print("="*80)
        print("PHASE 4.1: NEW LAUNCH IDENTIFICATION")
        print("="*80)
        
        # Identify new launches
        self.results['new_launches'] = self._identify_new_launches(months)
        
        # Calculate launch performance
        self.results['launch_performance'] = self._calculate_launch_performance()
        
        # Select top launches
        self.results['top_launches'] = self._select_top_launches(top_n)
        
        # Identify potential cannibalization targets
        self.results['cannibalization_targets'] = self._identify_cannibalization_targets()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ New Launch Identification Completed!")
        
        return self.results
    
    def _identify_new_launches(self, months: int) -> pd.DataFrame:
        """Identify new product launches within specified period"""
        latest_date = self.df['date'].max()
        cutoff_date = latest_date - pd.DateOffset(months=months)
        
        # Filter products launched in the period
        new_launches = self.products_df[
            self.products_df['launch_date'] >= cutoff_date
        ].copy()
        
        new_launches = new_launches.sort_values('launch_date', ascending=False)
        
        return new_launches
    
    def _calculate_launch_performance(self) -> pd.DataFrame:
        """Calculate performance metrics for new launches"""
        launch_performance = []
        
        for _, product in self.results['new_launches'].iterrows():
            product_id = product['product_id']
            launch_date = product['launch_date']
            
            # Sales after launch
            product_sales = self.df[self.df['product_id'] == product_id]
            post_launch_sales = product_sales[product_sales['date'] >= launch_date]
            
            if len(post_launch_sales) == 0:
                continue
            
            # Calculate metrics
            total_revenue = post_launch_sales['revenue'].sum()
            total_units = post_launch_sales['units_sold'].sum()
            total_transactions = post_launch_sales['transaction_id'].nunique()
            
            # Growth rate (comparing first 3 months vs next 3 months)
            first_3m_end = launch_date + pd.DateOffset(months=3)
            next_3m_end = launch_date + pd.DateOffset(months=6)
            
            first_3m_revenue = post_launch_sales[
                (post_launch_sales['date'] >= launch_date) &
                (post_launch_sales['date'] < first_3m_end)
            ]['revenue'].sum()
            
            next_3m_revenue = post_launch_sales[
                (post_launch_sales['date'] >= first_3m_end) &
                (post_launch_sales['date'] < next_3m_end)
            ]['revenue'].sum()
            
            growth_rate = ((next_3m_revenue - first_3m_revenue) / first_3m_revenue * 100) if first_3m_revenue > 0 else 0
            
            # Market penetration
            total_market_revenue = self.df[self.df['date'] >= launch_date]['revenue'].sum()
            market_share = (total_revenue / total_market_revenue * 100) if total_market_revenue > 0 else 0
            
            launch_performance.append({
                'product_id': product_id,
                'product_name': product['product_name'],
                'brand': product['brand'],
                'type': product['type'],
                'launch_date': launch_date,
                'total_revenue': total_revenue,
                'total_units': total_units,
                'total_transactions': total_transactions,
                'growth_rate_pct': growth_rate,
                'market_share_pct': market_share,
                'performance_score': total_revenue * (1 + growth_rate / 100)
            })
        
        performance_df = pd.DataFrame(launch_performance)
        performance_df = performance_df.sort_values('performance_score', ascending=False)
        
        return performance_df
    
    def _select_top_launches(self, top_n: int) -> pd.DataFrame:
        """Select top N launches based on performance"""
        if len(self.results['launch_performance']) == 0:
            return pd.DataFrame()
        
        top_launches = self.results['launch_performance'].head(top_n)
        return top_launches
    
    def _identify_cannibalization_targets(self) -> Dict:
        """Identify existing products that might be cannibalized"""
        cannibalization_targets = {}
        
        for _, launch in self.results['top_launches'].iterrows():
            new_product_id = launch['product_id']
            new_product_type = launch['type']
            new_product_brand = launch['brand']
            launch_date = launch['launch_date']
            
            # Find existing products in same category and brand
            existing_products = self.products_df[
                (self.products_df['type'] == new_product_type) &
                (self.products_df['brand'] == new_product_brand) &
                (self.products_df['launch_date'] < launch_date)
            ]
            
            if len(existing_products) > 0:
                cannibalization_targets[new_product_id] = {
                    'new_product': launch['product_name'],
                    'targets': existing_products[['product_id', 'product_name', 'launch_date']].to_dict('records')
                }
        
        return cannibalization_targets
    
    def _print_summary(self):
        """Print summary of new launches"""
        print("\n📊 New Launch Summary:")
        print(f"   Total New Launches (12 months): {len(self.results['new_launches'])}")
        
        if len(self.results['top_launches']) > 0:
            print(f"\n   Top {len(self.results['top_launches'])} Launches Selected for Analysis:")
            for idx, (_, launch) in enumerate(self.results['top_launches'].iterrows(), 1):
                print(f"      {idx}. {launch['product_name']}")
                print(f"         • Launch Date: {launch['launch_date'].strftime('%Y-%m-%d')}")
                print(f"         • Total Revenue: Rp {launch['total_revenue']:,.0f}")
                print(f"         • Market Share: {launch['market_share_pct']:.2f}%")
                print(f"         • Growth Rate: {launch['growth_rate_pct']:.1f}%")
        
        if len(self.results['cannibalization_targets']) > 0:
            print(f"\n   Potential Cannibalization Targets:")
            for new_product_id, targets_info in self.results['cannibalization_targets'].items():
                print(f"      • {targets_info['new_product']}:")
                for target in targets_info['targets']:
                    print(f"        - {target['product_name']} (Launched: {target['launch_date']})")

