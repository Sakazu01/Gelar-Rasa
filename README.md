# Strategi Analisis Data FMCG Personal Care

## 📋 Project Overview

Proyek analisis data strategis untuk kategori FMCG Personal Care dengan fokus pada tiga tujuan utama:
1. **Innovation Radar** - Identifikasi produk dengan potensi pertumbuhan tinggi
2. **Trend Forecasting** - Prediksi tren penjualan dan preferensi konsumen
3. **Product Cannibalization Analysis** - Evaluasi dampak produk baru terhadap produk existing

## 🎯 Project Goals

### 1. Innovation Radar
- Mengidentifikasi produk dengan potensi pertumbuhan tinggi atau inovasi yang menarik minat konsumen
- Analisis growth outlier dan rising stars
- Analisis sentimen konsumen dan emerging keywords
- Identifikasi white space opportunities

### 2. Trend Analysis
- Analisis tren penjualan per kategori, brand, dan channel
- Analisis tren harga dan diskon
- Identifikasi pola musiman (seasonal patterns)
- Visualisasi tren dengan interactive charts

### 3. Trend Forecasting
- Memprediksi tren penjualan 6-12 bulan ke depan
- Modeling pergeseran preferensi konsumen
- Analisis time series dengan SARIMA, Prophet, dan Ensemble methods

### 4. Product Cannibalization Analysis
- Evaluasi apakah peluncuran produk baru mengurangi penjualan produk lain
- Source of Volume (SOV) analysis
- Net portfolio impact calculation

## 📁 Project Structure

```
Gelar-Rasa/
├── src/
│   ├── phase1/              # Foundational Analysis
│   │   ├── data_integration.py
│   │   ├── market_snapshot.py
│   │   └── product_portfolio.py
│   ├── phase2/              # Innovation Radar
│   │   ├── growth_outlier.py
│   │   ├── sentiment_analysis.py
│   │   └── white_space.py
│   ├── phase3/              # Trend Forecasting
│   │   ├── time_series_forecast.py
│   │   └── preference_shift.py
│   ├── phase4/              # Product Cannibalization
│   │   ├── new_launch.py
│   │   ├── sov_analysis.py
│   │   └── portfolio_impact.py
│   └── utils/               # Utility functions
│       ├── data_loader.py
│       ├── data_cleaner.py
│       └── visualizer.py
├── outputs/
│   ├── dashboards/          # Visualization outputs
│   └── reports/             # Analysis reports
├── data/
│   ├── raw/                 # Raw data files
│   └── processed/           # Processed data files
├── main.py                  # Main execution script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or navigate to the project directory:
```bash
cd Gelar-Rasa
```

2. Create a virtual environment (recommended):
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Data Setup

Ensure your data files are located at:
```
Gelar_Rasa/data/fmcg_personalcare/fmcg_personalcare/
├── sales.csv
├── products.csv
├── marketing.csv
└── reviews.csv
```

## 📊 Execution Plan

### Phase 1: Foundational Analysis

#### Step 1.1: Data Integration & Preprocessing
- Menggabungkan, membersihkan, dan memvalidasi semua sumber data
- Missing value analysis
- Outlier detection
- Feature engineering

#### Step 1.2: Overall Market Snapshot
- Total Market Size
- Company Market Share
- Category Growth YoY

#### Step 1.3: Detailed Product Portfolio Analysis
- Sales Performance (volume, value, growth, seasonality)
- Distribution Analysis (by channel)
- Pricing & Promotion (price elasticity)
- Consumer Profile (demographics, psychographics)

### Phase 2: Innovation Radar

#### Step 2.1: Growth Outlier Detection
- Identifikasi SKU dengan pertumbuhan di atas rata-rata kategori
- Rising stars detection (low base, high growth)

#### Step 2.2: Consumer Sentiment & Keyword Analysis
- Analisis data ulasan dan media sosial
- Emerging keywords identification
- Keyword-sales correlation

#### Step 2.3: White Space & Competitor Innovation Analysis
- Pemetaan atribut produk vs kebutuhan konsumen
- White space identification
- Competitor positioning analysis

### Phase 3: Trend Forecasting

#### Step 3.1: Sales Time-Series Forecasting
- SARIMA model
- Prophet model
- Ensemble forecasting
- Forecast horizon: 6-12 months

#### Step 3.2: Consumer Preference Shift Modeling
- Analisis pergeseran sentimen
- Prediksi atribut pendorong utama di masa depan
- Preference trend projection

### Phase 4: Product Cannibalization Analysis

#### Step 4.1: New Launch Identification
- Identifikasi 3-5 peluncuran produk baru terbesar (12 bulan terakhir)
- Launch performance calculation

#### Step 4.2: Source of Volume (SOV) Analysis
- Analisis sumber penjualan produk baru:
  - Kompetitor
  - Ekspansi pasar
  - Produk internal lain (kanibalisasi)

#### Step 4.3: Net Portfolio Impact
- Dampak bersih pada total penjualan portofolio
- Klasifikasi: Additive vs Substitutive
- ROI calculation

## 🎨 Visualization Outputs

### Phase 1
- Master Product Dashboard (interaktif)
- Grafik tren penjualan historis (Pareto - top 20%)

### Phase 2
- Growth Opportunity Matrix (Bubble chart)
- Word cloud / Emerging Keyword Trendline

### Phase 3
- Sales Forecast vs. Actual (dengan confidence interval)
- Consumer Preference Map (pergeseran kepentingan atribut)

### Phase 4
- Stacked Area Chart (Source of Volume)
- Pre-Post Launch Trend Comparison

## 🔧 Usage

### Run Complete Analysis

Execute the main script to run all phases:
```bash
python main.py
```

### Run Individual Phases

You can also import and run individual phases:

```python
from src.phase1.data_integration import DataIntegration
from src.phase1.market_snapshot import MarketSnapshot

# Phase 1.1: Data Integration
data_integration = DataIntegration()
results = data_integration.execute()

# Phase 1.2: Market Snapshot
market_snapshot = MarketSnapshot(results['integrated_df'])
market_results = market_snapshot.execute()
```

## 📈 Key Features

- **Modular Architecture**: Each phase is independently executable
- **Comprehensive Analysis**: Covers all aspects from data integration to strategic insights
- **Statistical Rigor**: Uses advanced statistical methods (DiD, time series, clustering)
- **Visualization**: Interactive dashboards using Plotly
- **Reproducibility**: Clear documentation and structured code

## 📝 Methodology

### Data Preprocessing
- Missing value analysis and imputation
- Outlier detection (IQR method)
- Feature engineering (30+ features)
- Temporal features (seasonality, trends)

### Innovation Radar
- BCG Matrix analysis
- K-Means clustering for innovation scoring
- Sentiment analysis and keyword extraction
- White space identification

### Trend Forecasting
- Time series decomposition (trend, seasonal, residual)
- SARIMA model with seasonal components
- Facebook Prophet for automatic trend detection
- Ensemble forecasting for robustness

### Cannibalization Analysis
- Difference-in-Differences (DiD) analysis
- Cross-price elasticity calculation
- Statistical significance testing (t-tests)
- Source of Volume (SOV) breakdown

## 🛠️ Technologies Used

- **Python 3.8+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **scikit-learn** - Machine learning
- **statsmodels** - Statistical modeling
- **prophet** - Time series forecasting
- **plotly** - Interactive visualizations
- **scipy** - Scientific computing

## 📊 Expected Outputs

1. **Data Quality Report**: Validation results, missing values, outliers
2. **Market Snapshot**: Overall market metrics, market share, growth rates
3. **Product Portfolio Analysis**: Detailed metrics per product/SKU
4. **Innovation Radar Report**: Growth outliers, rising stars, emerging keywords
5. **Forecast Report**: Sales forecasts with confidence intervals
6. **Cannibalization Report**: SOV analysis, net portfolio impact

## 🎯 Key Insights & Recommendations

The analysis provides:

1. **Product Strategy Recommendations**
   - Invest in Star products
   - Increase marketing for Question Mark products
   - Harvest Cash Cow products
   - Phase out Dog products

2. **Marketing Optimization**
   - Focus budget on high-innovation score products
   - Leverage seasonal patterns
   - Optimize channel mix

3. **Portfolio Management**
   - Monitor cannibalization effects
   - Differentiate products with high cross-elasticity
   - Implement dynamic pricing strategies

4. **Forecasting & Planning**
   - Use ensemble forecasting for demand planning
   - Account for seasonality in inventory management
   - Prepare for identified trend directions

## 📚 Documentation

- Each module contains detailed docstrings
- Method documentation explains parameters and returns
- Code comments explain complex logic

## 🤝 Contributing

This is a competition project for Gelar Rasa 2025. For questions or issues, please refer to the project documentation.

## 📄 License

This project is for educational and competition purposes.

## 👥 Authors

- **Analyst**: Gemini (Pakar Bisnis & Data)
- **Requester**: User (Pimpinan)
- **Project**: Data Science Competition Gelar Rasa 2025

## 📅 Project Date

November 2025

---

**Prepared for:** Data Science Competition Gelar Rasa 2025  
**Dataset:** FMCG Personal Care - Synthetic Dataset  
**Analysis Period:** 2020-2025

