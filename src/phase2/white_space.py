"""
Step 2.3: White Space & Competitor Innovation Analysis
Memetakan atribut produk yang ada terhadap kebutuhan konsumen untuk menemukan 'white space'
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class WhiteSpaceAnalyzer:
    """Analyze white space opportunities and competitor innovation"""
    
    def __init__(self, product_metrics: pd.DataFrame, reviews_df: pd.DataFrame = None, 
                 products_df: pd.DataFrame = None):
        """
        Initialize WhiteSpaceAnalyzer
        
        Args:
            product_metrics: Product performance metrics
            reviews_df: Customer reviews data
            products_df: Product master data
        """
        self.product_metrics = product_metrics
        self.reviews_df = reviews_df
        self.products_df = products_df
        self.results = {}
    
    def execute(self) -> Dict:
        """
        Execute white space analysis
        
        Returns:
            Dictionary with white space opportunities
        """
        print("="*80)
        print("PHASE 2.3: WHITE SPACE & COMPETITOR INNOVATION ANALYSIS")
        print("="*80)
        
        # Analyze product attribute gaps
        self.results['attribute_gaps'] = self._analyze_attribute_gaps()
        
        # Identify white space opportunities
        self.results['white_space'] = self._identify_white_space()
        
        # Analyze competitor positioning
        if self.products_df is not None:
            self.results['competitor_positioning'] = self._analyze_competitor_positioning()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ White Space Analysis Completed!")
        
        return self.results
    
    def _analyze_attribute_gaps(self) -> pd.DataFrame:
        """Analyze gaps in product attributes based on consumer needs"""
        # This is a simplified analysis - in practice, you'd use more sophisticated NLP
        # to extract product attributes from descriptions and reviews
        
        gaps = []
        
        # Analyze by category
        for category in self.product_metrics['type'].unique():
            category_products = self.product_metrics[self.product_metrics['type'] == category]
            
            # Identify underperforming areas
            avg_rating = category_products['avg_rating'].mean() if 'avg_rating' in category_products.columns else 0
            avg_growth = category_products['revenue_growth_3m_pct'].mean()
            avg_market_share = category_products['market_share_pct'].mean()
            
            # Products below average
            underperformers = category_products[
                (category_products.get('avg_rating', 0) < avg_rating * 0.9) |
                (category_products['revenue_growth_3m_pct'] < avg_growth * 0.5) |
                (category_products['market_share_pct'] < avg_market_share * 0.5)
            ]
            
            if len(underperformers) > 0:
                gaps.append({
                    'category': category,
                    'underperforming_products': len(underperformers),
                    'avg_rating_gap': avg_rating - underperformers.get('avg_rating', pd.Series([0])).mean(),
                    'growth_gap': avg_growth - underperformers['revenue_growth_3m_pct'].mean(),
                    'opportunity_score': len(underperformers) * (avg_growth - underperformers['revenue_growth_3m_pct'].mean())
                })
        
        gaps_df = pd.DataFrame(gaps)
        gaps_df = gaps_df.sort_values('opportunity_score', ascending=False)
        
        return gaps_df
    
    def _identify_white_space(self) -> pd.DataFrame:
        """Identify white space opportunities"""
        white_space_opportunities = []
        
        # Analyze category coverage
        category_coverage = self.product_metrics.groupby('type').agg({
            'product_id': 'count',
            'total_revenue': 'sum',
            'revenue_growth_3m_pct': 'mean',
            'market_share_pct': 'sum'
        }).reset_index()
        
        category_coverage.columns = ['category', 'product_count', 'total_revenue', 
                                    'avg_growth', 'total_market_share']
        
        # Identify underserved categories
        avg_products_per_category = category_coverage['product_count'].mean()
        avg_growth = category_coverage['avg_growth'].mean()
        
        # White space: categories with few products but high growth potential
        white_space = category_coverage[
            (category_coverage['product_count'] < avg_products_per_category * 0.7) |
            (category_coverage['avg_growth'] > avg_growth * 1.5)
        ].copy()
        
        white_space['white_space_score'] = (
            (avg_growth - white_space['avg_growth']) * 0.5 +
            (avg_products_per_category - white_space['product_count']) * 0.5
        )
        white_space = white_space.sort_values('white_space_score', ascending=False)
        
        return white_space
    
    def _analyze_competitor_positioning(self) -> pd.DataFrame:
        """Analyze competitor positioning in the market"""
        if self.products_df is None:
            return pd.DataFrame()
        
        # Merge with product metrics
        positioning = self.products_df.merge(
            self.product_metrics[['product_id', 'market_share_pct', 'revenue_growth_3m_pct', 
                                'total_revenue', 'avg_rating']],
            on='product_id',
            how='left'
        )
        
        # Analyze by brand
        brand_positioning = positioning.groupby('brand').agg({
            'product_id': 'count',
            'market_share_pct': 'sum',
            'revenue_growth_3m_pct': 'mean',
            'total_revenue': 'sum',
            'avg_rating': 'mean'
        }).reset_index()
        
        brand_positioning.columns = ['brand', 'product_count', 'total_market_share', 
                                   'avg_growth', 'total_revenue', 'avg_rating']
        
        brand_positioning = brand_positioning.sort_values('total_market_share', ascending=False)
        
        return brand_positioning
    
    def _print_summary(self):
        """Print summary of white space analysis"""
        print("\n📊 White Space Analysis Summary:")
        
        if len(self.results['white_space']) > 0:
            print("\n   White Space Opportunities:")
            for _, row in self.results['white_space'].head(5).iterrows():
                print(f"      • {row['category']}: {row['product_count']} products, "
                      f"{row['avg_growth']:.1f}% growth, "
                      f"Market share: {row['total_market_share']:.1f}%")
        
        if len(self.results['competitor_positioning']) > 0:
            print("\n   Top Brands by Market Share:")
            top_brands = self.results['competitor_positioning'].head(5)
            for _, row in top_brands.iterrows():
                print(f"      • {row['brand']}: {row['total_market_share']:.1f}% share, "
                      f"{row['product_count']} products, {row['avg_growth']:.1f}% growth")

