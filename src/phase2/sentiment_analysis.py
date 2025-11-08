"""
Step 2.2: Consumer Sentiment & Keyword Analysis
Menganalisis data ulasan, media sosial, dan search trends untuk menemukan 'emerging keywords'
"""

import pandas as pd
import numpy as np
from typing import Dict, List
import re
from collections import Counter


class SentimentAnalyzer:
    """Analyze consumer sentiment and emerging keywords"""
    
    def __init__(self, reviews_df: pd.DataFrame, product_metrics: pd.DataFrame = None):
        """
        Initialize SentimentAnalyzer
        
        Args:
            reviews_df: Customer reviews data
            product_metrics: Product performance metrics (optional)
        """
        self.reviews_df = reviews_df
        self.product_metrics = product_metrics
        self.results = {}
    
    def execute(self) -> Dict:
        """
        Execute sentiment and keyword analysis
        
        Returns:
            Dictionary with sentiment metrics and keyword analysis
        """
        print("="*80)
        print("PHASE 2.2: CONSUMER SENTIMENT & KEYWORD ANALYSIS")
        print("="*80)
        
        # Analyze sentiment by product
        self.results['sentiment_by_product'] = self._analyze_sentiment_by_product()
        
        # Extract keywords
        self.results['keywords'] = self._extract_keywords()
        
        # Analyze emerging keywords
        self.results['emerging_keywords'] = self._detect_emerging_keywords()
        
        # Correlate keywords with sales
        if self.product_metrics is not None:
            self.results['keyword_sales_correlation'] = self._correlate_keywords_with_sales()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Sentiment & Keyword Analysis Completed!")
        
        return self.results
    
    def _analyze_sentiment_by_product(self) -> pd.DataFrame:
        """Analyze sentiment distribution by product"""
        sentiment_analysis = self.reviews_df.groupby('product_id').agg({
            'rating': ['mean', 'std', 'count'],
            'sentiment': lambda x: {
                'positive': (x == 'Positive').sum(),
                'negative': (x == 'Negative').sum(),
                'neutral': (x == 'Neutral').sum()
            }
        }).round(2)
        
        sentiment_analysis.columns = ['_'.join(col).strip() if col[1] else col[0] 
                                     for col in sentiment_analysis.columns.values]
        sentiment_analysis = sentiment_analysis.reset_index()
        
        # Extract sentiment counts
        sentiment_counts = []
        for _, row in sentiment_analysis.iterrows():
            product_id = row['product_id']
            sentiment_dict = row.get('sentiment_<lambda>', {})
            if isinstance(sentiment_dict, dict):
                sentiment_counts.append({
                    'product_id': product_id,
                    'positive_count': sentiment_dict.get('positive', 0),
                    'negative_count': sentiment_dict.get('negative', 0),
                    'neutral_count': sentiment_dict.get('neutral', 0),
                    'total_reviews': row.get('rating_count', 0)
                })
        
        sentiment_df = pd.DataFrame(sentiment_counts)
        sentiment_df['positive_pct'] = (sentiment_df['positive_count'] / sentiment_df['total_reviews'] * 100).round(2)
        sentiment_df['negative_pct'] = (sentiment_df['negative_count'] / sentiment_df['total_reviews'] * 100).round(2)
        
        # Merge with rating metrics
        rating_metrics = sentiment_analysis[['product_id', 'rating_mean', 'rating_std']].rename(columns={
            'rating_mean': 'avg_rating',
            'rating_std': 'rating_volatility'
        })
        
        sentiment_df = sentiment_df.merge(rating_metrics, on='product_id', how='left')
        
        return sentiment_df
    
    def _extract_keywords(self) -> Dict:
        """Extract keywords from reviews"""
        # Common stopwords (Indonesian and English)
        stopwords = set([
            'yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 'ini', 'itu',
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did'
        ])
        
        # Extract keywords from comments
        all_keywords = []
        keywords_by_product = {}
        
        for product_id in self.reviews_df['product_id'].unique():
            product_reviews = self.reviews_df[self.reviews_df['product_id'] == product_id]
            product_keywords = []
            
            for comment in product_reviews['comment'].dropna():
                # Simple keyword extraction (split by space, remove punctuation)
                words = re.findall(r'\b[a-zA-Z]{3,}\b', str(comment).lower())
                words = [w for w in words if w not in stopwords]
                product_keywords.extend(words)
                all_keywords.extend(words)
            
            # Count keywords
            keyword_counts = Counter(product_keywords)
            keywords_by_product[product_id] = dict(keyword_counts.most_common(20))
        
        # Overall keyword frequency
        overall_keywords = Counter(all_keywords)
        
        return {
            'by_product': keywords_by_product,
            'overall': dict(overall_keywords.most_common(50))
        }
    
    def _detect_emerging_keywords(self) -> pd.DataFrame:
        """Detect emerging keywords over time"""
        if len(self.reviews_df) == 0:
            return pd.DataFrame(columns=['keyword', 'recent_mentions', 'old_mentions', 'growth_rate_pct'])
        
        # Group reviews by time period
        self.reviews_df['year_month'] = self.reviews_df['date'].dt.to_period('M')
        
        # Get recent and old periods
        unique_periods = sorted(self.reviews_df['year_month'].unique())
        if len(unique_periods) < 2:
            # Not enough data for comparison
            return pd.DataFrame(columns=['keyword', 'recent_mentions', 'old_mentions', 'growth_rate_pct'])
        
        latest_period = unique_periods[-1]
        # Use median period as split point, or 6 months back if available
        if len(unique_periods) > 6:
            split_idx = len(unique_periods) - 6
            old_period = unique_periods[split_idx]
        else:
            split_idx = len(unique_periods) // 2
            old_period = unique_periods[split_idx] if split_idx > 0 else unique_periods[0]
        
        recent_reviews = self.reviews_df[self.reviews_df['year_month'] >= old_period]
        old_reviews = self.reviews_df[self.reviews_df['year_month'] < old_period]
        
        # Extract keywords from each period
        def extract_keywords_period(reviews):
            stopwords = set(['yang', 'dan', 'di', 'ke', 'dari', 'untuk', 'pada', 'dengan', 
                           'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for'])
            keywords = []
            for comment in reviews['comment'].dropna():
                words = re.findall(r'\b[a-zA-Z]{3,}\b', str(comment).lower())
                words = [w for w in words if w not in stopwords]
                keywords.extend(words)
            return Counter(keywords)
        
        recent_keywords = extract_keywords_period(recent_reviews)
        old_keywords = extract_keywords_period(old_reviews)
        
        # Calculate growth in keyword mentions
        emerging_keywords = []
        all_keywords = set(list(recent_keywords.keys()) + list(old_keywords.keys()))
        
        for keyword in all_keywords:
            recent_count = recent_keywords.get(keyword, 0)
            old_count = old_keywords.get(keyword, 0)
            
            if old_count == 0 and recent_count > 0:
                # New keyword
                growth_rate = 100
            elif old_count > 0:
                growth_rate = ((recent_count - old_count) / old_count * 100)
            else:
                growth_rate = 0
            
            if recent_count > 5 and growth_rate > 50:  # Threshold for emerging
                emerging_keywords.append({
                    'keyword': keyword,
                    'recent_mentions': recent_count,
                    'old_mentions': old_count,
                    'growth_rate_pct': growth_rate
                })
        
        emerging_df = pd.DataFrame(emerging_keywords)
        
        # Handle empty DataFrame
        if len(emerging_df) == 0:
            # Return empty DataFrame with expected columns
            return pd.DataFrame(columns=['keyword', 'recent_mentions', 'old_mentions', 'growth_rate_pct'])
        
        # Sort if column exists
        if 'growth_rate_pct' in emerging_df.columns:
            emerging_df = emerging_df.sort_values('growth_rate_pct', ascending=False)
        
        return emerging_df
    
    def _correlate_keywords_with_sales(self) -> pd.DataFrame:
        """Correlate keyword mentions with product sales performance"""
        if self.product_metrics is None or len(self.results['sentiment_by_product']) == 0:
            return pd.DataFrame(columns=['avg_rating', 'positive_sentiment', 'total_reviews'])
        
        # Merge sentiment analysis with product metrics
        try:
            sentiment_sales = self.results['sentiment_by_product'].merge(
                self.product_metrics[['product_id', 'total_revenue', 'revenue_growth_3m_pct', 'market_share_pct']],
                on='product_id',
                how='inner'
            )
            
            if len(sentiment_sales) == 0:
                return pd.DataFrame(columns=['avg_rating', 'positive_sentiment', 'total_reviews'])
            
            # Calculate correlations
            correlations = {
                'avg_rating': sentiment_sales['avg_rating'].corr(sentiment_sales['total_revenue']),
                'positive_sentiment': sentiment_sales['positive_pct'].corr(sentiment_sales['total_revenue']),
                'total_reviews': sentiment_sales['total_reviews'].corr(sentiment_sales['total_revenue'])
            }
            
            return pd.DataFrame([correlations])
        except Exception as e:
            print(f"⚠️ Warning: Could not correlate keywords with sales: {str(e)}")
            return pd.DataFrame(columns=['avg_rating', 'positive_sentiment', 'total_reviews'])
    
    def _print_summary(self):
        """Print summary of sentiment analysis"""
        print("\n📊 Sentiment Analysis Summary:")
        
        if len(self.results['sentiment_by_product']) > 0:
            top_rated = self.results['sentiment_by_product'].nlargest(5, 'avg_rating')
            print("\n   Top 5 Products by Average Rating:")
            for _, row in top_rated.iterrows():
                print(f"      • Product {row['product_id']}: {row['avg_rating']:.2f} "
                      f"({row['positive_pct']:.1f}% positive)")
        
        if len(self.results['emerging_keywords']) > 0:
            print(f"\n   Emerging Keywords: {len(self.results['emerging_keywords'])}")
            print("   Top 10 Emerging Keywords:")
            top_keywords = self.results['emerging_keywords'].head(10)
            for _, row in top_keywords.iterrows():
                if 'keyword' in row and 'recent_mentions' in row and 'growth_rate_pct' in row:
                    print(f"      • {row['keyword']}: {row['recent_mentions']} mentions "
                          f"({row['growth_rate_pct']:.1f}% growth)")
        else:
            print("\n   Emerging Keywords: 0 (No emerging keywords found matching criteria)")

