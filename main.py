"""
Main execution script for FMCG Personal Care Analysis
Strategi Analisis Data FMCG Personal Care - Gelar Rasa 2025
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from utils.data_loader import DataLoader
from phase1.data_integration import DataIntegration
from phase1.market_snapshot import MarketSnapshot
from phase1.product_portfolio import ProductPortfolio
from phase2.growth_outlier import GrowthOutlierDetector
from phase2.sentiment_analysis import SentimentAnalyzer
from phase2.white_space import WhiteSpaceAnalyzer
from phase3.time_series_forecast import TimeSeriesForecaster
from phase3.preference_shift import PreferenceShiftModel
from phase4.new_launch import NewLaunchIdentifier
from phase4.sov_analysis import SOVAnalyzer
from phase4.portfolio_impact import PortfolioImpactAnalyzer


def main():
    """Main execution function"""
    print("="*80)
    print("FMCG PERSONAL CARE - STRATEGIC DATA ANALYSIS")
    print("Gelar Rasa 2025 Data Science Competition")
    print("="*80)
    print("\n")
    
    # ============================================================================
    # PHASE 1: FOUNDATIONAL ANALYSIS
    # ============================================================================
    print("\n" + "="*80)
    print("STARTING PHASE 1: FOUNDATIONAL ANALYSIS")
    print("="*80 + "\n")
    
    # Step 1.1: Data Integration & Preprocessing
    data_integration = DataIntegration()
    phase1_results = data_integration.execute()
    
    integrated_df = phase1_results['integrated_df']
    products_df = phase1_results['products_df']
    marketing_df = phase1_results['marketing_df']
    reviews_df = phase1_results['reviews_df']
    
    # Step 1.2: Overall Market Snapshot
    market_snapshot = MarketSnapshot(integrated_df)
    market_results = market_snapshot.execute()
    
    # Step 1.3: Detailed Product Portfolio Analysis
    product_portfolio = ProductPortfolio(integrated_df, marketing_df, reviews_df)
    portfolio_results = product_portfolio.execute()
    product_metrics = portfolio_results['product_metrics']
    
    # ============================================================================
    # PHASE 2: INNOVATION RADAR
    # ============================================================================
    print("\n" + "="*80)
    print("STARTING PHASE 2: INNOVATION RADAR")
    print("="*80 + "\n")
    
    # Step 2.1: Growth Outlier Detection
    growth_outlier = GrowthOutlierDetector(product_metrics, integrated_df)
    growth_results = growth_outlier.execute()
    
    # Step 2.2: Consumer Sentiment & Keyword Analysis
    sentiment_analyzer = SentimentAnalyzer(reviews_df, product_metrics)
    sentiment_results = sentiment_analyzer.execute()
    
    # Step 2.3: White Space & Competitor Innovation Analysis
    white_space = WhiteSpaceAnalyzer(product_metrics, reviews_df, products_df)
    white_space_results = white_space.execute()
    
    # ============================================================================
    # PHASE 3: TREND FORECASTING
    # ============================================================================
    print("\n" + "="*80)
    print("STARTING PHASE 3: TREND FORECASTING")
    print("="*80 + "\n")
    
    # Step 3.1: Sales Time-Series Forecasting
    forecaster = TimeSeriesForecaster(integrated_df)
    forecast_results = forecaster.execute(forecast_horizon=12)
    
    # Step 3.2: Consumer Preference Shift Modeling
    preference_shift = PreferenceShiftModel(reviews_df, product_metrics)
    preference_results = preference_shift.execute()
    
    # ============================================================================
    # PHASE 4: PRODUCT CANNIBALIZATION ANALYSIS
    # ============================================================================
    print("\n" + "="*80)
    print("STARTING PHASE 4: PRODUCT CANNIBALIZATION ANALYSIS")
    print("="*80 + "\n")
    
    # Step 4.1: New Launch Identification
    new_launch_identifier = NewLaunchIdentifier(products_df, integrated_df)
    new_launch_results = new_launch_identifier.execute(months=12, top_n=5)
    top_launches = new_launch_results['top_launches']
    
    # Step 4.2: Source of Volume (SOV) Analysis
    if len(top_launches) > 0:
        sov_analyzer = SOVAnalyzer(integrated_df, top_launches)
        sov_results = sov_analyzer.execute()
        
        # Step 4.3: Net Portfolio Impact
        portfolio_impact = PortfolioImpactAnalyzer(
            integrated_df, 
            top_launches, 
            sov_results
        )
        impact_results = portfolio_impact.execute()
    else:
        print("⚠️ No new launches found for cannibalization analysis")
        sov_results = {}
        impact_results = {}
    
    # ============================================================================
    # FINAL SUMMARY
    # ============================================================================
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - EXECUTIVE SUMMARY")
    print("="*80 + "\n")
    
    print_summary(
        market_results,
        portfolio_results,
        growth_results,
        sentiment_results,
        forecast_results,
        impact_results
    )
    
    print("\n" + "="*80)
    print("✅ ALL PHASES COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")
    
    return {
        'phase1': {
            'data_integration': phase1_results,
            'market_snapshot': market_results,
            'product_portfolio': portfolio_results
        },
        'phase2': {
            'growth_outlier': growth_results,
            'sentiment': sentiment_results,
            'white_space': white_space_results
        },
        'phase3': {
            'forecasting': forecast_results,
            'preference_shift': preference_results
        },
        'phase4': {
            'new_launches': new_launch_results,
            'sov': sov_results,
            'portfolio_impact': impact_results
        }
    }


def print_summary(market_results, portfolio_results, growth_results, 
                 sentiment_results, forecast_results, impact_results):
    """Print executive summary"""
    print("📊 KEY FINDINGS:\n")
    
    # Market Overview
    if 'total_market_size' in market_results:
        market_size = market_results['total_market_size']
        print(f"1. MARKET OVERVIEW:")
        print(f"   • Total Market Revenue: Rp {market_size['total_revenue']:,.0f}")
        print(f"   • YoY Growth: {market_size['yoy_growth_pct']:.2f}%")
        print()
    
    # Innovation Radar
    if 'rising_stars' in growth_results and len(growth_results['rising_stars']) > 0:
        print(f"2. INNOVATION RADAR:")
        print(f"   • Rising Stars: {len(growth_results['rising_stars'])} products identified")
        top_star = growth_results['rising_stars'].iloc[0]
        print(f"   • Top Rising Star: {top_star['product_name']} "
              f"({top_star['revenue_growth_3m_pct']:.1f}% growth)")
        print()
    
    # Forecasting
    if 'ensemble' in forecast_results and forecast_results['ensemble']:
        ensemble_metrics = forecast_results['ensemble']['metrics']['weighted']
        print(f"3. TREND FORECASTING:")
        print(f"   • Best Model: Ensemble (Weighted)")
        print(f"   • Forecast Accuracy (MAPE): {ensemble_metrics['mape']:.2f}%")
        print()
    
    # Cannibalization
    if 'portfolio_impact' in impact_results and len(impact_results['portfolio_impact']) > 0:
        impact_df = impact_results['portfolio_impact']
        additive_count = (impact_df['launch_type'] == 'Additive').sum()
        print(f"4. CANNIBALIZATION ANALYSIS:")
        print(f"   • Additive Launches: {additive_count}")
        print(f"   • Substitutive Launches: {(impact_df['launch_type'] == 'Substitutive').sum()}")
        if additive_count > 0:
            avg_net_impact = impact_df[impact_df['launch_type'] == 'Additive']['net_impact'].mean()
            print(f"   • Average Net Impact (Additive): Rp {avg_net_impact:,.0f}")
        print()


if __name__ == '__main__':
    results = main()

