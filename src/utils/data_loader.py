"""
Data loading and integration utilities
"""

import pandas as pd
import os
from pathlib import Path


class DataLoader:
    """Load and integrate all data sources"""
    
    def __init__(self, data_path: str = None):
        """
        Initialize DataLoader
        
        Args:
            data_path: Path to data directory. If None, uses default path.
        """
        if data_path is None:
            # Default path relative to project root
            base_path = Path(__file__).parent.parent.parent
            self.data_path = base_path / 'Gelar_Rasa' / 'data' / 'fmcg_personalcare' / 'fmcg_personalcare'
        else:
            self.data_path = Path(data_path)
        
        self.sales_df = None
        self.products_df = None
        self.marketing_df = None
        self.reviews_df = None
    
    def load_all_data(self):
        """Load all data sources"""
        print("📂 Loading datasets...")
        
        # Load sales data
        self.sales_df = pd.read_csv(self.data_path / 'sales.csv')
        self.sales_df['date'] = pd.to_datetime(self.sales_df['date'])
        
        # Load products data
        self.products_df = pd.read_csv(self.data_path / 'products.csv')
        self.products_df['launch_date'] = pd.to_datetime(self.products_df['launch_date'])
        
        # Load marketing data
        self.marketing_df = pd.read_csv(self.data_path / 'marketing.csv')
        self.marketing_df['start_date'] = pd.to_datetime(self.marketing_df['start_date'])
        self.marketing_df['end_date'] = pd.to_datetime(self.marketing_df['end_date'])
        
        # Load reviews data
        self.reviews_df = pd.read_csv(self.data_path / 'reviews.csv')
        self.reviews_df['date'] = pd.to_datetime(self.reviews_df['date'])
        
        print(f"✅ Sales: {self.sales_df.shape[0]:,} rows × {self.sales_df.shape[1]} columns")
        print(f"✅ Products: {self.products_df.shape[0]:,} rows × {self.products_df.shape[1]} columns")
        print(f"✅ Marketing: {self.marketing_df.shape[0]:,} rows × {self.marketing_df.shape[1]} columns")
        print(f"✅ Reviews: {self.reviews_df.shape[0]:,} rows × {self.reviews_df.shape[1]} columns")
        
        return self
    
    def get_integrated_data(self):
        """Merge all data sources into a single integrated dataset"""
        if self.sales_df is None:
            self.load_all_data()
        
        # Merge sales with products
        integrated = self.sales_df.merge(
            self.products_df,
            on='product_id',
            how='left'
        )
        
        return integrated
    
    def get_data_summary(self):
        """Get summary statistics of all datasets"""
        summary = {
            'sales': {
                'rows': len(self.sales_df),
                'columns': list(self.sales_df.columns),
                'date_range': (self.sales_df['date'].min(), self.sales_df['date'].max()),
                'products': self.sales_df['product_id'].nunique(),
                'regions': self.sales_df['region'].nunique(),
                'channels': self.sales_df['channel'].nunique()
            },
            'products': {
                'total': len(self.products_df),
                'brands': self.products_df['brand'].nunique(),
                'categories': self.products_df['type'].nunique(),
                'launch_range': (self.products_df['launch_date'].min(), self.products_df['launch_date'].max())
            },
            'marketing': {
                'campaigns': len(self.marketing_df),
                'products_covered': self.marketing_df['product_id'].nunique(),
                'total_spend': self.marketing_df['spend_idr'].sum()
            },
            'reviews': {
                'total_reviews': len(self.reviews_df),
                'products_reviewed': self.reviews_df['product_id'].nunique(),
                'avg_rating': self.reviews_df['rating'].mean()
            }
        }
        
        return summary

