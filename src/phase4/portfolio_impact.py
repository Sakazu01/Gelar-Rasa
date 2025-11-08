"""
Step 4.3: Net Portfolio Impact
Menghitung dampak bersih pada total penjualan portofolio
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta


class PortfolioImpactAnalyzer:
    """Analyze net portfolio impact of new launches"""
    
    def __init__(self, integrated_df: pd.DataFrame, new_launches: pd.DataFrame, 
                 sov_results: Dict):
        """
        Initialize PortfolioImpactAnalyzer
        
        Args:
            integrated_df: Integrated sales data
            new_launches: New launch information
            sov_results: SOV analysis results from Phase 4.2
        """
        self.df = integrated_df
        self.new_launches = new_launches
        self.sov_results = sov_results
        self.results = {}
    
    def execute(self, window_months: int = 6) -> Dict:
        """
        Execute portfolio impact analysis
        
        Args:
            window_months: Months before/after launch to analyze
        
        Returns:
            Dictionary with portfolio impact results
        """
        print("="*80)
        print("PHASE 4.3: NET PORTFOLIO IMPACT")
        print("="*80)
        
        # Calculate net portfolio impact for each launch
        self.results['portfolio_impact'] = self._calculate_portfolio_impact(window_months)
        
        # Calculate category-level impact
        self.results['category_impact'] = self._calculate_category_impact()
        
        # Calculate brand-level impact
        self.results['brand_impact'] = self._calculate_brand_impact()
        
        # Classify launches (additive vs substitutive)
        self.results['launch_classification'] = self._classify_launches()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Portfolio Impact Analysis Completed!")
        
        return self.results
    
    def _calculate_portfolio_impact(self, window_months: int) -> pd.DataFrame:
        """Calculate net portfolio impact for each launch"""
        impact_results = []
        
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
            
            # Get SOV data
            if new_product_id not in self.sov_results['sov_by_launch']:
                continue
            
            sov_data = self.sov_results['sov_by_launch'][new_product_id]
            
            # New product revenue
            new_product_revenue = sov_data['new_product_revenue']
            
            # Lost revenue from existing products (cannibalization)
            lost_revenue = sov_data['cannibalized_revenue']
            
            # Net portfolio impact
            net_impact = new_product_revenue - lost_revenue
            net_impact_pct = (net_impact / new_product_revenue * 100) if new_product_revenue > 0 else 0
            
            # Portfolio growth rate
            pre_portfolio_revenue = self.df[
                (self.df['date'] >= pre_start) &
                (self.df['date'] < pre_end) &
                (self.df['type'] == product_type) &
                (self.df['brand'] == product_brand)
            ]['revenue'].sum()
            
            post_portfolio_revenue = self.df[
                (self.df['date'] >= post_start) &
                (self.df['date'] < post_end) &
                (self.df['type'] == product_type) &
                (self.df['brand'] == product_brand)
            ]['revenue'].sum()
            
            portfolio_growth = ((post_portfolio_revenue - pre_portfolio_revenue) / pre_portfolio_revenue * 100) if pre_portfolio_revenue > 0 else 0
            
            # Classification
            if net_impact > 0:
                launch_type = 'Additive'
            elif net_impact < -new_product_revenue * 0.1:  # Lost more than 10% of new product revenue
                launch_type = 'Substitutive'
            else:
                launch_type = 'Neutral'
            
            impact_results.append({
                'product_id': new_product_id,
                'product_name': launch['product_name'],
                'launch_date': launch_date,
                'new_product_revenue': new_product_revenue,
                'lost_revenue': lost_revenue,
                'net_impact': net_impact,
                'net_impact_pct': net_impact_pct,
                'portfolio_growth_pct': portfolio_growth,
                'launch_type': launch_type,
                'roi': (net_impact / lost_revenue * 100) if lost_revenue > 0 else float('inf')
            })
        
        impact_df = pd.DataFrame(impact_results)
        impact_df = impact_df.sort_values('net_impact', ascending=False)
        
        return impact_df
    
    def _calculate_category_impact(self) -> pd.DataFrame:
        """Calculate impact at category level"""
        category_impacts = []
        
        for category in self.new_launches['type'].unique():
            category_launches = self.new_launches[self.new_launches['type'] == category]
            
            total_new_revenue = 0
            total_lost_revenue = 0
            
            for _, launch in category_launches.iterrows():
                product_id = launch['product_id']
                if product_id in self.sov_results['sov_by_launch']:
                    sov_data = self.sov_results['sov_by_launch'][product_id]
                    total_new_revenue += sov_data['new_product_revenue']
                    total_lost_revenue += sov_data['cannibalized_revenue']
            
            net_impact = total_new_revenue - total_lost_revenue
            net_impact_pct = (net_impact / total_new_revenue * 100) if total_new_revenue > 0 else 0
            
            category_impacts.append({
                'category': category,
                'num_launches': len(category_launches),
                'total_new_revenue': total_new_revenue,
                'total_lost_revenue': total_lost_revenue,
                'net_impact': net_impact,
                'net_impact_pct': net_impact_pct
            })
        
        category_df = pd.DataFrame(category_impacts)
        category_df = category_df.sort_values('net_impact', ascending=False)
        
        return category_df
    
    def _calculate_brand_impact(self) -> pd.DataFrame:
        """Calculate impact at brand level"""
        brand_impacts = []
        
        for brand in self.new_launches['brand'].unique():
            brand_launches = self.new_launches[self.new_launches['brand'] == brand]
            
            total_new_revenue = 0
            total_lost_revenue = 0
            
            for _, launch in brand_launches.iterrows():
                product_id = launch['product_id']
                if product_id in self.sov_results['sov_by_launch']:
                    sov_data = self.sov_results['sov_by_launch'][product_id]
                    total_new_revenue += sov_data['new_product_revenue']
                    total_lost_revenue += sov_data['cannibalized_revenue']
            
            net_impact = total_new_revenue - total_lost_revenue
            net_impact_pct = (net_impact / total_new_revenue * 100) if total_new_revenue > 0 else 0
            
            brand_impacts.append({
                'brand': brand,
                'num_launches': len(brand_launches),
                'total_new_revenue': total_new_revenue,
                'total_lost_revenue': total_lost_revenue,
                'net_impact': net_impact,
                'net_impact_pct': net_impact_pct
            })
        
        brand_df = pd.DataFrame(brand_impacts)
        brand_df = brand_df.sort_values('net_impact', ascending=False)
        
        return brand_df
    
    def _classify_launches(self) -> pd.DataFrame:
        """Classify launches as additive, substitutive, or neutral"""
        classification = self.results['portfolio_impact'][[
            'product_id', 'product_name', 'launch_date',
            'new_product_revenue', 'lost_revenue', 'net_impact',
            'launch_type', 'roi'
        ]].copy()
        
        # Add performance rating
        classification['performance_rating'] = classification['net_impact'].apply(
            lambda x: 'Excellent' if x > 0 else ('Poor' if x < -1000000 else 'Moderate')
        )
        
        return classification
    
    def _print_summary(self):
        """Print summary of portfolio impact"""
        print("\n📊 Portfolio Impact Summary:")
        
        if len(self.results['portfolio_impact']) > 0:
            print("\n   Net Portfolio Impact by Launch:")
            for _, row in self.results['portfolio_impact'].iterrows():
                print(f"\n   {row['product_name']}:")
                print(f"      • New Product Revenue: Rp {row['new_product_revenue']:,.0f}")
                print(f"      • Lost Revenue (Cannibalization): Rp {row['lost_revenue']:,.0f}")
                print(f"      • Net Impact: Rp {row['net_impact']:,.0f} ({row['net_impact_pct']:.1f}%)")
                print(f"      • Launch Type: {row['launch_type']}")
                print(f"      • Portfolio Growth: {row['portfolio_growth_pct']:.1f}%")
        
        if len(self.results['category_impact']) > 0:
            print("\n   Category-Level Impact:")
            for _, row in self.results['category_impact'].iterrows():
                print(f"      • {row['category']}: Net Impact Rp {row['net_impact']:,.0f} "
                      f"({row['net_impact_pct']:.1f}%)")
        
        # Summary statistics
        additive_count = (self.results['portfolio_impact']['launch_type'] == 'Additive').sum()
        substitutive_count = (self.results['portfolio_impact']['launch_type'] == 'Substitutive').sum()
        neutral_count = (self.results['portfolio_impact']['launch_type'] == 'Neutral').sum()
        
        print(f"\n   Launch Classification:")
        print(f"      • Additive: {additive_count}")
        print(f"      • Substitutive: {substitutive_count}")
        print(f"      • Neutral: {neutral_count}")

