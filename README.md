# 📊 Analisis Data FMCG Personal Care - End-to-End Analysis

## 📋 Project Overview

Proyek analisis data komprehensif untuk kategori FMCG Personal Care dengan pendekatan end-to-end dari data profiling hingga modeling dan evaluasi. Analisis ini mencakup:

1. **Data Profiling & Cleaning** - Analisis kualitas data dan pembersihan menyeluruh
2. **Feature Engineering** - Pembuatan fitur bisnis FMCG-specific yang relevan
3. **Exploratory Data Analysis** - Eksplorasi data dengan visualisasi komprehensif
4. **Modeling & Evaluation** - Pembangunan model prediksi dengan uji asumsi statistik
5. **Bias & Validity Analysis** - Identifikasi bias dan validitas data
6. **Business Insights** - Insight bisnis yang actionable

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
├── DSC2025_Analysis_FMCG_PersonalCare.ipynb  # Main analysis notebook
├── Gelar_Rasa/
│   └── data/
│       └── fmcg_personalcare/
│           └── fmcg_personalcare/
│               ├── sales.csv
│               ├── products.csv
│               ├── marketing.csv
│               ├── reviews.csv
│               └── README_FMCG_Personal_Care.txt
├── data/
│   └── clean/              # Cleaned & engineered datasets
├── reports/
│   ├── profiling/          # Data profiling reports
│   ├── eda/                # EDA visualizations
│   ├── insights.md         # Business insights
│   ├── bias_analysis.csv   # Bias analysis results
│   └── cleaning_log.csv    # Data cleaning log
├── archive/
│   └── unneeded/           # Archived files
├── src/                    # Source code modules (optional)
├── requirements.txt        # Python dependencies
└── README.md              # This file
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

### Menjalankan Analisis

1. Buka notebook `DSC2025_Analysis_FMCG_PersonalCare.ipynb`
2. Jalankan semua cells secara berurutan
3. Hasil analisis akan tersimpan di:
   - `reports/profiling/` - Data profiling reports
   - `reports/eda/` - Visualisasi EDA
   - `reports/insights.md` - Insight bisnis
   - `data/clean/` - Dataset yang sudah dibersihkan

## 📊 Analisis yang Dilakukan

### 1. Data Profiling & Ingestion
- ✅ Load dan analisis semua dataset (sales, products, marketing, reviews)
- ✅ Profiling komprehensif: missing values, distribusi, tipe data
- ✅ Simpan hasil profiling ke CSV

### 2. Data Cleaning
- ✅ Normalisasi nama kolom (snake_case)
- ✅ Konversi kolom waktu ke datetime
- ✅ Handling missing values (impute dengan median/mode/default)
- ✅ Hapus duplikat
- ✅ Deteksi outlier (IQR method)
- ✅ Validasi data numerik (harga, quantity tidak negatif)

### 3. Feature Engineering (FMCG-Specific)
- ✅ Fitur waktu: day_of_week, month, year, is_weekend, is_holiday
- ✅ Fitur promosi: promo_flag, promo_depth, promo_intensity
- ✅ Fitur harga: price_ratio_to_base, relative_price_to_avg, price_tier
- ✅ Fitur historis: lag_qty (1, 7, 30 hari), rolling_mean (7, 30 hari)
- ✅ Fitur kategori: sku_category, store_type, pack_size
- ✅ Elastisitas harga: correlation log(qty) vs log(price)

### 4. Exploratory Data Analysis (EDA)
- ✅ Visualisasi tren penjualan (total & per kategori)
- ✅ Distribusi harga, quantity, dan promo lift
- ✅ Korelasi antar fitur (heatmap)
- ✅ Analisis musiman
- ✅ Top performer: toko & SKU
- ✅ SKU dengan promo paling efektif

### 5. Modeling & Evaluation
- ✅ Baseline models: Linear Regression, Ridge, Lasso, Random Forest, Gradient Boosting
- ✅ Metrik evaluasi: MAE, RMSE, MAPE, R²
- ✅ Uji asumsi model:
  - Normalitas residual (Shapiro-Wilk / Jarque-Bera)
  - Homoskedastisitas (Breusch-Pagan)
  - Autokorelasi (Durbin-Watson, Ljung-Box)
  - Multikolinearitas (VIF)
- ✅ Interpretasi feature importance
- ✅ Evaluasi komprehensif dengan rekomendasi perbaikan

### 6. Bias & Validity Analysis
- ✅ Deteksi bias waktu (distribusi per tahun/bulan)
- ✅ Deteksi bias lokasi (distribusi per region)
- ✅ Deteksi bias promo (distribusi dengan/tanpa promo)
- ✅ Analisis confounding (promo vs musim)
- ✅ Kuantifikasi tingkat bias

### 7. Documentation
- ✅ README dengan penjelasan proyek
- ✅ Laporan insights bisnis (insights.md)
- ✅ Struktur repository yang rapi

## 📈 Output Files

### Reports
- `reports/profiling/profiling_*.csv` - Data profiling untuk setiap dataset
- `reports/eda/*.png` - Visualisasi EDA (12+ grafik)
- `reports/insights.md` - Insight bisnis komprehensif
- `reports/bias_analysis.csv` - Hasil analisis bias
- `reports/cleaning_log.csv` - Log proses data cleaning

### Clean Data
- `data/clean/sales_with_features.csv` - Dataset yang sudah dibersihkan dan di-feature engineering

### Visualizations (EDA)
1. Tren penjualan total
2. Tren penjualan per kategori
3. Distribusi harga, quantity, discount, promo lift
4. Korelasi heatmap
5. Analisis musiman
6. Top performer (toko & SKU)
7. Promo effectiveness
8. Residual normality
9. Residual homoskedasticity
10. Feature importance (Linear Regression)
11. Feature importance (Random Forest)
12. Predicted vs Actual

## 🔧 Usage

### Menjalankan Analisis Lengkap

1. Buka Jupyter Notebook:
```bash
jupyter notebook DSC2025_Analysis_FMCG_PersonalCare.ipynb
```

2. Atau menggunakan JupyterLab:
```bash
jupyter lab DSC2025_Analysis_FMCG_PersonalCare.ipynb
```

3. Jalankan semua cells secara berurutan (Cell → Run All)

### Reproducibility

- **Random Seed**: 42 (untuk reproducibility)
- **Package Versions**: Dicatat di awal notebook
- Semua output disimpan dengan timestamp untuk tracking

### Struktur Notebook

Notebook dibagi menjadi 9 bagian utama:
1. Setup Environment & Reproducibility
2. Analisis Struktur Repository
3. Data Ingestion & Profiling
4. Data Cleaning
5. Feature Engineering
6. Exploratory Data Analysis
7. Modeling & Evaluasi
8. Analisis Bias & Validitas Data
9. Ringkasan & Insight Bisnis

## 📈 Key Features

- **Modular Architecture**: Each phase is independently executable
- **Comprehensive Analysis**: Covers all aspects from data integration to strategic insights
- **Statistical Rigor**: Uses advanced statistical methods (DiD, time series, clustering)
- **Visualization**: Interactive dashboards using Plotly
- **Reproducibility**: Clear documentation and structured code

## 📝 Methodology

### Data Preprocessing
- Missing value analysis dan imputation (median/mode/default)
- Outlier detection menggunakan IQR method (1.5 × IQR)
- Normalisasi nama kolom ke snake_case
- Validasi data numerik (harga, quantity tidak negatif)

### Feature Engineering
- **30+ fitur** yang dibuat mencakup:
  - Fitur waktu (8 fitur)
  - Fitur promosi (5 fitur)
  - Fitur harga (4 fitur)
  - Fitur historis (8 fitur)
  - Fitur kategori (5 fitur)
  - Elastisitas harga (1 fitur)

### Modeling
- Multiple baseline models: Linear, Ridge, Lasso, Random Forest, Gradient Boosting
- Time-based train-test split (80-20)
- StandardScaler untuk normalisasi fitur
- Evaluasi dengan MAE, RMSE, MAPE, R²

### Statistical Testing
- **Uji Asumsi Model**:
  - Normalitas residual (Shapiro-Wilk / Jarque-Bera)
  - Homoskedastisitas (Breusch-Pagan)
  - Autokorelasi (Durbin-Watson, Ljung-Box)
  - Multikolinearitas (VIF)
- **Bias Detection**:
  - Chi-square test untuk confounding
  - Distribusi persentase untuk bias waktu/lokasi/promo

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

Lihat file `reports/insights.md` untuk insight bisnis lengkap.

### Temuan Utama
- Dataset mencakup 1M+ transaksi dari 15 SKU
- Periode analisis: 2020-2025
- Total revenue dalam triliunan IDR
- Promo menunjukkan lift signifikan pada penjualan

### Dampak Bisnis
- Channel e-commerce mendominasi penjualan
- Promo efektif namun perlu optimasi timing
- Elastisitas harga bervariasi antar SKU
- Pola musiman terdeteksi untuk perencanaan inventory

### Rekomendasi Aksi
1. Fokus investasi marketing pada channel e-commerce dengan ROI tertinggi
2. Optimasi strategi promo berdasarkan analisis musiman
3. Implementasi dynamic pricing untuk SKU dengan elastisitas tinggi
4. Pengembangan model forecasting untuk perencanaan inventory
5. Monitoring dan mitigasi bias data untuk analisis yang lebih representatif

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

