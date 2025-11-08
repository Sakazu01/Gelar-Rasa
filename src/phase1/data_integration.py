"""
Step 1.1: Data Integration & Preprocessing
Menggabungkan, membersihkan, dan memvalidasi semua sumber data
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from utils.data_loader import DataLoader
from utils.data_cleaner import DataCleaner


class DataIntegration:
    """Handle data integration and preprocessing"""
    
    def __init__(self, data_path: str = None):
        """Initialize DataIntegration"""
        self.loader = DataLoader(data_path)
        self.cleaner = DataCleaner()
        self.sales_df = None
        self.products_df = None
        self.marketing_df = None
        self.reviews_df = None
        self.integrated_df = None
    
    def execute(self) -> Dict:
        """
        Execute data integration and preprocessing
        
        Returns:
            Dictionary with integrated data and validation results
        """
        print("="*80)
        print("PHASE 1.1: DATA INTEGRATION & PREPROCESSING")
        print("="*80)
        
        # Load all data
        self.loader.load_all_data()
        self.sales_df = self.loader.sales_df
        self.products_df = self.loader.products_df
        self.marketing_df = self.loader.marketing_df
        self.reviews_df = self.loader.reviews_df
        
        # Validate data quality
        validation_results = self._validate_data_quality()
        
        # Clean sales data
        self.sales_df = self.cleaner.clean_sales_data(self.sales_df)
        
        # Create temporal features
        self.sales_df = self.cleaner.create_temporal_features(self.sales_df)
        
        # Create product lifecycle features
        self.integrated_df = self.cleaner.create_product_lifecycle_features(
            self.sales_df, self.products_df
        )
        
        # Get data summary
        summary = self.loader.get_data_summary()
        
        print("\n✅ Data Integration & Preprocessing Completed!")
        
        return {
            'sales_df': self.sales_df,
            'products_df': self.products_df,
            'marketing_df': self.marketing_df,
            'reviews_df': self.reviews_df,
            'integrated_df': self.integrated_df,
            'validation_results': validation_results,
            'summary': summary
        }
    
    def _validate_data_quality(self) -> Dict:
        """Validate data quality"""
        results = {}
        
        # Check missing values
        print("\n📊 Data Quality Validation:")
        results['missing_values'] = {
            'sales': self.cleaner.analyze_missing_values(self.sales_df, 'Sales'),
            'products': self.cleaner.analyze_missing_values(self.products_df, 'Products'),
            'marketing': self.cleaner.analyze_missing_values(self.marketing_df, 'Marketing'),
            'reviews': self.cleaner.analyze_missing_values(self.reviews_df, 'Reviews')
        }
        
        # Check duplicates
        print("\n🔍 Duplicate Check:")
        results['duplicates'] = {
            'sales': self.sales_df.duplicated(subset=['transaction_id']).sum(),
            'products': self.products_df.duplicated(subset=['product_id']).sum(),
            'marketing': self.marketing_df.duplicated(subset=['campaign_id']).sum(),
            'reviews': self.reviews_df.duplicated(subset=['review_id']).sum()
        }
        
        for key, value in results['duplicates'].items():
            print(f"   {key.capitalize()}: {value:,} duplicates")
        
        # Check outliers
        print("\n📈 Outlier Detection:")
        numeric_cols = ['units_sold', 'avg_price', 'discount_pct', 'revenue']
        results['outliers'] = self.cleaner.detect_outliers_iqr(self.sales_df, numeric_cols)
        
        for col, info in results['outliers'].items():
            print(f"   {col}: {info['count']:,} outliers ({info['percentage']:.2f}%)")
        
        return results

