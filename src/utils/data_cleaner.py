"""
Data cleaning and preprocessing utilities
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional


class DataCleaner:
    """Clean and preprocess data"""
    
    @staticmethod
    def analyze_missing_values(df: pd.DataFrame, df_name: str = "DataFrame") -> pd.DataFrame:
        """Analyze missing values in dataframe"""
        missing = df.isnull().sum()
        missing_pct = 100 * missing / len(df)
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing_Count': missing.values,
            'Percentage': missing_pct.values
        })
        missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values('Missing_Count', ascending=False)
        
        if len(missing_df) == 0:
            print(f"✅ {df_name}: No missing values found!")
        else:
            print(f"⚠️ {df_name}: Found {len(missing_df)} columns with missing values")
        
        return missing_df
    
    @staticmethod
    def detect_outliers_iqr(df: pd.DataFrame, columns: List[str]) -> Dict:
        """Detect outliers using IQR method"""
        outlier_info = {}
        
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            outlier_pct = 100 * len(outliers) / len(df)
            
            outlier_info[col] = {
                'count': len(outliers),
                'percentage': outlier_pct,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        return outlier_info
    
    @staticmethod
    def clean_sales_data(sales_df: pd.DataFrame, cap_outliers: bool = True) -> pd.DataFrame:
        """Clean sales data"""
        cleaned = sales_df.copy()
        
        print(f"🧹 Cleaning sales data...")
        print(f"   Original records: {len(cleaned):,}")
        
        # Remove duplicates
        initial_count = len(cleaned)
        cleaned = cleaned.drop_duplicates(subset=['transaction_id'])
        print(f"   After removing duplicates: {len(cleaned):,} (-{initial_count - len(cleaned):,})")
        
        # Handle extreme outliers in revenue
        if cap_outliers:
            revenue_99 = cleaned['revenue'].quantile(0.99)
            cleaned['revenue_capped'] = cleaned['revenue'].clip(upper=revenue_99)
            print(f"   Revenue capped at 99th percentile: Rp {revenue_99:,.0f}")
        
        # Create additional flags
        cleaned['is_discounted'] = cleaned['discount_pct'] > 0
        cleaned['discount_category'] = pd.cut(
            cleaned['discount_pct'],
            bins=[-0.1, 0, 10, 20, 100],
            labels=['No Discount', 'Low (0-10%)', 'Medium (10-20%)', 'High (>20%)']
        )
        
        print(f"✅ Data cleaning completed! Final records: {len(cleaned):,}")
        
        return cleaned
    
    @staticmethod
    def create_temporal_features(df: pd.DataFrame, date_col: str = 'date') -> pd.DataFrame:
        """Create temporal features from date column"""
        df = df.copy()
        df['year'] = df[date_col].dt.year
        df['month'] = df[date_col].dt.month
        df['quarter'] = df[date_col].dt.quarter
        df['week'] = df[date_col].dt.isocalendar().week
        df['day_of_week'] = df[date_col].dt.dayofweek
        df['day_of_year'] = df[date_col].dt.dayofyear
        df['is_weekend'] = df['day_of_week'].isin([5, 6])
        df['month_name'] = df[date_col].dt.strftime('%B')
        df['year_month'] = df[date_col].dt.to_period('M')
        
        # Seasonal indicators (Indonesian context)
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Year End/New Year'
            elif month in [3, 4, 5]:
                return 'Ramadan Period'
            elif month in [6, 7, 8]:
                return 'Mid Year/Back to School'
            else:
                return 'Regular Period'
        
        df['season'] = df['month'].apply(get_season)
        
        return df
    
    @staticmethod
    def create_product_lifecycle_features(sales_df: pd.DataFrame, products_df: pd.DataFrame) -> pd.DataFrame:
        """Create product lifecycle features"""
        df = sales_df.merge(products_df, on='product_id', how='left')
        
        # Product age
        df['product_age_days'] = (df['date'] - df['launch_date']).dt.days
        df['product_age_months'] = df['product_age_days'] / 30.44
        df['product_age_years'] = df['product_age_days'] / 365.25
        
        # Lifecycle stage
        def classify_lifecycle_stage(age_months):
            if age_months < 0:
                return 'Pre-Launch'
            elif age_months <= 6:
                return 'Introduction'
            elif age_months <= 18:
                return 'Growth'
            elif age_months <= 36:
                return 'Maturity'
            else:
                return 'Decline/Sustain'
        
        df['lifecycle_stage'] = df['product_age_months'].apply(classify_lifecycle_stage)
        
        # Price positioning
        df['price_vs_base'] = (df['avg_price'] / df['base_price'] - 1) * 100
        df['effective_discount'] = df['base_price'] - df['avg_price']
        
        return df

