"""
Step 3.2: Consumer Preference Shift Modeling
Menganalisis pergeseran sentimen untuk memprediksi atribut yang akan menjadi pendorong utama
"""

import pandas as pd
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta
import re
from collections import Counter


class PreferenceShiftModel:
    """Model consumer preference shifts over time"""
    
    def __init__(self, reviews_df: pd.DataFrame, product_metrics: pd.DataFrame = None):
        """
        Initialize PreferenceShiftModel
        
        Args:
            reviews_df: Customer reviews data
            product_metrics: Product performance metrics (optional)
        """
        self.reviews_df = reviews_df
        self.product_metrics = product_metrics
        self.results = {}
    
    def execute(self) -> Dict:
        """
        Execute preference shift modeling
        
        Returns:
            Dictionary with preference shift analysis
        """
        print("="*80)
        print("PHASE 3.2: CONSUMER PREFERENCE SHIFT MODELING")
        print("="*80)
        
        # Analyze sentiment trends over time
        self.results['sentiment_trends'] = self._analyze_sentiment_trends()
        
        # Extract attribute preferences
        self.results['attribute_preferences'] = self._extract_attribute_preferences()
        
        # Model preference shifts
        self.results['preference_shifts'] = self._model_preference_shifts()
        
        # Predict future preferences
        self.results['future_preferences'] = self._predict_future_preferences()
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Preference Shift Modeling Completed!")
        
        return self.results
    
    def _analyze_sentiment_trends(self) -> pd.DataFrame:
        """Analyze sentiment trends over time"""
        # Group by time period
        self.reviews_df['year_month'] = self.reviews_df['date'].dt.to_period('M')
        
        # Calculate sentiment metrics over time
        sentiment_trends = self.reviews_df.groupby('year_month').agg({
            'rating': 'mean',
            'sentiment': lambda x: {
                'positive': (x == 'Positive').sum(),
                'negative': (x == 'Negative').sum(),
                'neutral': (x == 'Neutral').sum()
            }
        }).reset_index()
        
        # Extract sentiment counts
        sentiment_counts = []
        for _, row in sentiment_trends.iterrows():
            period = row['year_month']
            sentiment_dict = row['sentiment']
            if isinstance(sentiment_dict, dict):
                total = sum(sentiment_dict.values())
                sentiment_counts.append({
                    'period': period,
                    'avg_rating': row['rating'],
                    'positive_pct': (sentiment_dict.get('positive', 0) / total * 100) if total > 0 else 0,
                    'negative_pct': (sentiment_dict.get('negative', 0) / total * 100) if total > 0 else 0,
                    'neutral_pct': (sentiment_dict.get('neutral', 0) / total * 100) if total > 0 else 0
                })
        
        sentiment_trends_df = pd.DataFrame(sentiment_counts)
        sentiment_trends_df['period'] = sentiment_trends_df['period'].astype(str)
        
        return sentiment_trends_df
    
    def _extract_attribute_preferences(self) -> Dict:
        """Extract product attribute preferences from reviews"""
        # Common product attributes/keywords
        attribute_keywords = {
            'quality': ['quality', 'kualitas', 'durable', 'tahan lama', 'good', 'bagus'],
            'price': ['price', 'harga', 'cheap', 'murah', 'expensive', 'mahal', 'value'],
            'packaging': ['packaging', 'kemasan', 'bottle', 'botol', 'container'],
            'effectiveness': ['effective', 'efektif', 'works', 'berfungsi', 'results', 'hasil'],
            'fragrance': ['smell', 'aroma', 'fragrance', 'wangi', 'scent'],
            'texture': ['texture', 'tekstur', 'smooth', 'halus', 'creamy', 'krim'],
            'natural': ['natural', 'alami', 'organic', 'organik', 'vegan'],
            'whitening': ['whitening', 'mencerahkan', 'bright', 'cerah'],
            'moisturizing': ['moisturizing', 'melembabkan', 'hydrating', 'hidrasi'],
            'anti-aging': ['anti-aging', 'anti penuaan', 'wrinkle', 'kerutan']
        }
        
        # Extract attributes mentioned in reviews
        attribute_mentions = {attr: [] for attr in attribute_keywords.keys()}
        
        for _, review in self.reviews_df.iterrows():
            comment = str(review['comment']).lower()
            product_id = review['product_id']
            date = review['date']
            
            for attribute, keywords in attribute_keywords.items():
                if any(keyword in comment for keyword in keywords):
                    attribute_mentions[attribute].append({
                        'product_id': product_id,
                        'date': date,
                        'rating': review['rating'],
                        'sentiment': review['sentiment']
                    })
        
        # Calculate attribute preference scores over time
        attribute_preferences = {}
        
        for attribute, mentions in attribute_mentions.items():
            if len(mentions) == 0:
                continue
            
            mentions_df = pd.DataFrame(mentions)
            mentions_df['year_month'] = pd.to_datetime(mentions_df['date']).dt.to_period('M')
            
            # Calculate average rating and sentiment by period
            attribute_trend = mentions_df.groupby('year_month').agg({
                'rating': 'mean',
                'sentiment': lambda x: (x == 'Positive').sum() / len(x) * 100
            }).reset_index()
            
            attribute_preferences[attribute] = {
                'total_mentions': len(mentions),
                'trend': attribute_trend,
                'avg_rating': mentions_df['rating'].mean(),
                'positive_sentiment_pct': (mentions_df['sentiment'] == 'Positive').sum() / len(mentions_df) * 100
            }
        
        return attribute_preferences
    
    def _model_preference_shifts(self) -> pd.DataFrame:
        """Model shifts in attribute preferences over time"""
        shifts = []
        
        for attribute, data in self.results['attribute_preferences'].items():
            trend = data['trend']
            
            if len(trend) < 2:
                continue
            
            # Calculate trend direction
            recent_periods = trend.tail(6)  # Last 6 months
            old_periods = trend.head(max(1, len(trend) - 6))  # Older periods
            
            if len(recent_periods) > 0 and len(old_periods) > 0:
                recent_avg_rating = recent_periods['rating'].mean()
                old_avg_rating = old_periods['rating'].mean()
                
                recent_sentiment = recent_periods['sentiment'].mean()
                old_sentiment = old_periods['sentiment'].mean()
                
                rating_shift = recent_avg_rating - old_avg_rating
                sentiment_shift = recent_sentiment - old_sentiment
                
                # Calculate growth in mentions
                recent_mentions = len(recent_periods)
                old_mentions = len(old_periods)
                mention_growth = ((recent_mentions - old_mentions) / old_mentions * 100) if old_mentions > 0 else 0
                
                shifts.append({
                    'attribute': attribute,
                    'rating_shift': rating_shift,
                    'sentiment_shift': sentiment_shift,
                    'mention_growth_pct': mention_growth,
                    'current_rating': recent_avg_rating,
                    'current_sentiment': recent_sentiment,
                    'shift_score': (rating_shift * 0.4 + sentiment_shift * 0.4 + mention_growth * 0.2)
                })
        
        shifts_df = pd.DataFrame(shifts)
        shifts_df = shifts_df.sort_values('shift_score', ascending=False)
        
        return shifts_df
    
    def _predict_future_preferences(self) -> pd.DataFrame:
        """Predict future attribute preferences"""
        if len(self.results['preference_shifts']) == 0:
            return pd.DataFrame()
        
        # Simple linear projection based on current trends
        future_preferences = []
        
        for _, shift in self.results['preference_shifts'].iterrows():
            # Project 6 months ahead
            projected_rating = shift['current_rating'] + (shift['rating_shift'] * 2)
            projected_sentiment = shift['current_sentiment'] + (shift['sentiment_shift'] * 2)
            projected_mentions = shift['mention_growth_pct'] * 1.5
            
            future_preferences.append({
                'attribute': shift['attribute'],
                'current_rating': shift['current_rating'],
                'projected_rating': projected_rating,
                'current_sentiment': shift['current_sentiment'],
                'projected_sentiment': projected_sentiment,
                'trend_direction': 'Increasing' if shift['shift_score'] > 0 else 'Decreasing',
                'importance_score': abs(shift['shift_score']) + abs(projected_mentions)
            })
        
        future_df = pd.DataFrame(future_preferences)
        future_df = future_df.sort_values('importance_score', ascending=False)
        
        return future_df
    
    def _print_summary(self):
        """Print summary of preference shift analysis"""
        print("\n📊 Preference Shift Summary:")
        
        if len(self.results['preference_shifts']) > 0:
            print("\n   Top Attribute Shifts:")
            top_shifts = self.results['preference_shifts'].head(5)
            for _, row in top_shifts.iterrows():
                direction = "📈 Increasing" if row['shift_score'] > 0 else "📉 Decreasing"
                print(f"      • {row['attribute']}: {direction} "
                      f"(Rating: {row['current_rating']:.2f}, "
                      f"Sentiment: {row['current_sentiment']:.1f}%)")
        
        if len(self.results['future_preferences']) > 0:
            print("\n   Predicted Future Preferences (6 months):")
            top_future = self.results['future_preferences'].head(5)
            for _, row in top_future.iterrows():
                print(f"      • {row['attribute']}: {row['trend_direction']} "
                      f"(Projected Rating: {row['projected_rating']:.2f}, "
                      f"Projected Sentiment: {row['projected_sentiment']:.1f}%)")

