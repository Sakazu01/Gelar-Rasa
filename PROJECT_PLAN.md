# Project Execution Plan
## Strategi Analisis Data FMCG Personal Care

### Project Information
- **Project Title**: Strategi Analisis Data FMCG Personal Care
- **Requester**: User (Pimpinan)
- **Analyst**: Gemini (Pakar Bisnis & Data)
- **Competition**: Gelar Rasa 2025 Data Science Competition

---

## Project Goals

1. **Innovation Radar** - Identifikasi produk dengan potensi pertumbuhan tinggi
2. **Trend Forecasting** - Prediksi tren penjualan dan preferensi konsumen
3. **Product Cannibalization Analysis** - Evaluasi dampak produk baru

---

## Execution Plan

### Phase 1: Foundational Analysis
**Objective**: Membangun pemahaman dasar yang komprehensif dari semua produk

#### Step 1.1: Data Integration & Preprocessing
- ✅ Menggabungkan semua sumber data (Sales, SKU Master, Marketing, Reviews)
- ✅ Data cleaning dan validation
- ✅ Missing value analysis
- ✅ Outlier detection
- ✅ Feature engineering

#### Step 1.2: Overall Market Snapshot
- ✅ Total Market Size
- ✅ Company Market Share
- ✅ Category Growth YoY
- ✅ Channel Distribution
- ✅ Regional Analysis

#### Step 1.3: Detailed Product Portfolio Analysis
- ✅ Sales Performance (volume, value, growth, seasonality)
- ✅ Distribution Analysis (by channel)
- ✅ Pricing & Promotion (price elasticity)
- ✅ Consumer Profile (from reviews)

**Visualization Outputs**:
- Master Product Dashboard (interaktif)
- Grafik tren penjualan historis (Pareto - top 20%)

---

### Phase 2: Innovation Radar
**Objective**: Mengidentifikasi produk dengan potensi pertumbuhan tinggi atau inovasi yang menarik

#### Step 2.1: Growth Outlier Detection
- ✅ Identifikasi SKU dengan pertumbuhan di atas rata-rata kategori
- ✅ Rising stars detection (low base, high growth)
- ✅ Growth momentum calculation

#### Step 2.2: Consumer Sentiment & Keyword Analysis
- ✅ Analisis data ulasan dan media sosial
- ✅ Emerging keywords identification
- ✅ Keyword-sales correlation
- ✅ Sentiment trends over time

#### Step 2.3: White Space & Competitor Innovation Analysis
- ✅ Pemetaan atribut produk vs kebutuhan konsumen
- ✅ White space identification
- ✅ Competitor positioning analysis
- ✅ Attribute gap analysis

**Visualization Outputs**:
- Growth Opportunity Matrix (Bubble chart)
- Word cloud / Emerging Keyword Trendline

---

### Phase 3: Trend Forecasting
**Objective**: Memprediksi tren penjualan dan preferensi konsumen di masa mendatang

#### Step 3.1: Sales Time-Series Forecasting
- ✅ Time series decomposition (trend, seasonal, residual)
- ✅ SARIMA model
- ✅ Prophet model
- ✅ Ensemble forecasting
- ✅ Forecast horizon: 6-12 months

#### Step 3.2: Consumer Preference Shift Modeling
- ✅ Analisis pergeseran sentimen
- ✅ Attribute preference extraction
- ✅ Preference shift modeling
- ✅ Future preference prediction

**Visualization Outputs**:
- Sales Forecast vs. Actual (dengan confidence interval)
- Consumer Preference Map (pergeseran kepentingan atribut)

---

### Phase 4: Product Cannibalization Analysis
**Objective**: Mengevaluasi apakah peluncuran produk baru mengurangi penjualan produk lain

#### Step 4.1: New Launch Identification
- ✅ Identifikasi 3-5 peluncuran produk baru terbesar (12 bulan terakhir)
- ✅ Launch performance calculation
- ✅ Identification of potential cannibalization targets

#### Step 4.2: Source of Volume (SOV) Analysis
- ✅ Analisis sumber penjualan produk baru:
  - Kompetitor
  - Ekspansi pasar
  - Produk internal lain (kanibalisasi)
- ✅ Statistical significance testing (DiD)

#### Step 4.3: Net Portfolio Impact
- ✅ Dampak bersih pada total penjualan portofolio
- ✅ Klasifikasi: Additive vs Substitutive
- ✅ ROI calculation
- ✅ Category and brand level impact

**Visualization Outputs**:
- Stacked Area Chart (Source of Volume)
- Pre-Post Launch Trend Comparison

---

## Implementation Status

### ✅ Completed
- [x] Project structure setup
- [x] Data integration modules
- [x] Market snapshot analysis
- [x] Product portfolio analysis
- [x] Growth outlier detection
- [x] Sentiment analysis
- [x] White space analysis
- [x] Time series forecasting
- [x] Preference shift modeling
- [x] New launch identification
- [x] SOV analysis
- [x] Portfolio impact analysis
- [x] Main execution script
- [x] Documentation (README, requirements.txt)

### 🔄 In Progress
- [ ] Visualization dashboards (interactive)
- [ ] Report generation
- [ ] Model optimization

### 📋 TODO
- [ ] Unit tests
- [ ] Performance optimization
- [ ] Additional visualizations
- [ ] Export to Excel/PDF reports

---

## Key Deliverables

1. **Data Quality Report**
   - Validation results
   - Missing values analysis
   - Outlier detection

2. **Market Analysis Report**
   - Market snapshot
   - Market share analysis
   - Growth metrics

3. **Innovation Radar Report**
   - Growth outliers
   - Rising stars
   - Emerging keywords
   - White space opportunities

4. **Forecast Report**
   - Sales forecasts (6-12 months)
   - Confidence intervals
   - Model performance metrics

5. **Cannibalization Report**
   - SOV analysis
   - Net portfolio impact
   - Launch classification
   - Strategic recommendations

---

## Methodology

### Statistical Methods
- **Time Series Analysis**: SARIMA, Prophet, Ensemble
- **Statistical Testing**: DiD (Difference-in-Differences), t-tests
- **Machine Learning**: K-Means clustering, PCA
- **NLP**: Keyword extraction, sentiment analysis

### Key Metrics
- **Market Share**: Revenue-based market share
- **Growth Rate**: YoY, QoQ, 3-month growth
- **Forecast Accuracy**: MAPE, RMSE, MAE
- **Cannibalization**: Revenue loss, percentage impact
- **Innovation Score**: Composite score based on multiple factors

---

## Next Steps

1. Run complete analysis: `python main.py`
2. Review outputs in `outputs/` directory
3. Generate visualizations and dashboards
4. Create executive summary report
5. Present findings and recommendations

---

## Contact

For questions or issues regarding this project, please refer to the documentation in the README.md file.

**Project Date**: November 2025  
**Competition**: Gelar Rasa 2025 Data Science Competition

