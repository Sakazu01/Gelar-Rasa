# Quick Start Guide
## FMCG Personal Care Analysis - Gelar Rasa 2025

## 🚀 Quick Setup

```bash
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Verify Data Location
Ensure your data files are at:
```
Gelar_Rasa/data/fmcg_personalcare/fmcg_personalcare/
├── sales.csv
├── products.csv
├── marketing.csv
└── reviews.csv
```

### 3. Run Analysis
```bash
python main.py
```

## 📊 What to Expect

The analysis will execute 5 phases:

1. **Phase 1**: Foundational Analysis (Data Integration, Market Snapshot, Product Portfolio)
2. **Phase 2**: Innovation Radar (Growth Outliers, Sentiment Analysis, White Space)
3. **Phase 3**: Trend Analysis (Category, Brand, Channel, Price, Seasonal Trends) - NEW
4. **Phase 4**: Trend Forecasting (Time Series, Preference Shifts)
5. **Phase 5**: Cannibalization Analysis (SOV, Portfolio Impact)

## 📁 Output Structure

After running, you'll find:
- Analysis results in console output
- Processed data (if saved) in `data/processed/`
- Visualizations (when implemented) in `outputs/dashboards/`
- Reports (when implemented) in `outputs/reports/`

## 🎯 Key Outputs

### Phase 1 Results
- Market size and growth metrics
- Product portfolio performance
- Channel and regional analysis

### Phase 2 Results
- Growth outliers and rising stars
- Emerging keywords
- White space opportunities

### Phase 3 Results
- Sales trends by category, brand, and channel
- Price and discount trends
- Seasonal patterns analysis
- Market share evolution

### Phase 4 Results
- Sales forecasts (6-12 months)
- Preference shift predictions
- Model performance metrics

### Phase 5 Results
- Source of Volume (SOV) breakdown
- Net portfolio impact
- Launch classification (Additive/Substitutive)

## 🔧 Running Individual Phases

You can run individual phases by importing modules:

```python
# Phase 1: Foundational Analysis
from src.phase1.data_integration import DataIntegration
from src.phase1.market_snapshot import MarketSnapshot
from src.phase1.product_portfolio import ProductPortfolio

# Phase 2: Innovation Radar
from src.phase2.growth_outlier import GrowthOutlierDetector
from src.phase2.sentiment_analysis import SentimentAnalyzer
from src.phase2.white_space import WhiteSpaceAnalyzer

# Phase 3: Trend Forecasting
from src.phase3.time_series_forecast import TimeSeriesForecaster
from src.phase3.preference_shift import PreferenceShiftModel

# Phase 4: Cannibalization
from src.phase4.new_launch import NewLaunchIdentifier
from src.phase4.sov_analysis import SOVAnalyzer
from src.phase4.portfolio_impact import PortfolioImpactAnalyzer
```

## 📝 Example Usage

```python
from src.utils.data_loader import DataLoader

# Load data
loader = DataLoader()
loader.load_all_data()

# Get integrated data
integrated_df = loader.get_integrated_data()

# Run Phase 1
from src.phase1.market_snapshot import MarketSnapshot
market_snapshot = MarketSnapshot(integrated_df)
results = market_snapshot.execute()
```

## ⚠️ Troubleshooting

### Import Errors
If you encounter import errors, make sure you're running from the project root:
```bash
cd Gelar-Rasa
python main.py
```

### Missing Data
Ensure all data files are in the correct location:
- `Gelar_Rasa/data/fmcg_personalcare/fmcg_personalcare/sales.csv`
- `Gelar_Rasa/data/fmcg_personalcare/fmcg_personalcare/products.csv`
- `Gelar_Rasa/data/fmcg_personalcare/fmcg_personalcare/marketing.csv`
- `Gelar_Rasa/data/fmcg_personalcare/fmcg_personalcare/reviews.csv`

### Memory Issues
If you encounter memory issues with large datasets:
- Process data in chunks
- Use sampling for initial analysis
- Clear intermediate variables

## 📚 Documentation

- **README.md**: Complete project documentation
- **PROJECT_PLAN.md**: Detailed execution plan
- **requirements.txt**: Python dependencies

## 🆘 Support

For issues or questions, refer to:
1. README.md for detailed documentation
2. PROJECT_PLAN.md for execution plan
3. Module docstrings for API documentation

## ✅ Next Steps

1. Run the analysis: `python main.py`
2. Review console output for results
3. Check outputs directory for generated files
4. Review insights and recommendations
5. Generate visualizations (when implemented)

---

**Happy Analyzing! 🚀**

