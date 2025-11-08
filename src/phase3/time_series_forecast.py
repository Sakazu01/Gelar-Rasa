"""
Step 3.1: Sales Time-Series Forecasting
Menerapkan model peramalan pada data penjualan historis
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, Optional
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

try:
    from statsmodels.tsa.seasonal import seasonal_decompose
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    from statsmodels.tsa.stattools import adfuller
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    print("⚠️ statsmodels not available. SARIMA forecasting will be skipped.")

try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    print("⚠️ Prophet not available. Prophet forecasting will be skipped.")

from sklearn.metrics import mean_squared_error, mean_absolute_error


class TimeSeriesForecaster:
    """Forecast sales using time series models"""
    
    def __init__(self, integrated_df: pd.DataFrame):
        """
        Initialize TimeSeriesForecaster
        
        Args:
            integrated_df: Integrated sales data
        """
        self.df = integrated_df
        self.results = {}
        self.forecasts = {}
    
    def execute(self, forecast_horizon: int = 12, category: str = None) -> Dict:
        """
        Execute time series forecasting
        
        Args:
            forecast_horizon: Number of months to forecast ahead
            category: Specific category to forecast (None for overall)
        
        Returns:
            Dictionary with forecast results
        """
        print("="*80)
        print("PHASE 3.1: SALES TIME-SERIES FORECASTING")
        print("="*80)
        
        # Prepare time series data
        ts_data = self._prepare_time_series(category)
        
        # Time series decomposition
        self.results['decomposition'] = self._decompose_time_series(ts_data)
        
        # Train-test split
        train_size = int(len(ts_data) * 0.8)
        train = ts_data[:train_size]
        test = ts_data[train_size:]
        
        # SARIMA forecast
        if STATSMODELS_AVAILABLE:
            self.results['sarima'] = self._sarima_forecast(train, test, forecast_horizon)
        
        # Prophet forecast
        if PROPHET_AVAILABLE:
            self.results['prophet'] = self._prophet_forecast(train, test, forecast_horizon)
        
        # Ensemble forecast
        if 'sarima' in self.results and 'prophet' in self.results:
            self.results['ensemble'] = self._create_ensemble_forecast(
                self.results['sarima'], 
                self.results['prophet'],
                test
            )
        
        # Print summary
        self._print_summary()
        
        print("\n✅ Time Series Forecasting Completed!")
        
        return self.results
    
    def _prepare_time_series(self, category: str = None) -> pd.Series:
        """Prepare time series data for forecasting"""
        if category:
            df_filtered = self.df[self.df['type'] == category]
        else:
            df_filtered = self.df
        
        # Aggregate monthly
        monthly_sales = df_filtered.groupby(
            df_filtered['date'].dt.to_period('M')
        )['revenue'].sum()
        
        monthly_sales.index = monthly_sales.index.to_timestamp()
        monthly_sales = monthly_sales.sort_index()
        
        return monthly_sales
    
    def _decompose_time_series(self, ts_data: pd.Series) -> Dict:
        """Decompose time series into trend, seasonal, and residual"""
        if not STATSMODELS_AVAILABLE:
            return {}
        
        try:
            # Resample to weekly if needed for smoother decomposition
            if len(ts_data) > 52:
                decomposition = seasonal_decompose(
                    ts_data,
                    model='multiplicative',
                    period=12  # 12 months
                )
            else:
                decomposition = seasonal_decompose(
                    ts_data,
                    model='additive',
                    period=min(12, len(ts_data) // 2)
                )
            
            # Calculate trend slope
            trend_data = decomposition.trend.dropna()
            if len(trend_data) > 1:
                trend_slope = np.polyfit(range(len(trend_data)), trend_data, 1)[0]
            else:
                trend_slope = 0
            
            return {
                'trend': decomposition.trend,
                'seasonal': decomposition.seasonal,
                'residual': decomposition.resid,
                'trend_slope': trend_slope,
                'seasonality_strength': decomposition.seasonal.std()
            }
        except Exception as e:
            print(f"⚠️ Decomposition failed: {str(e)}")
            return {}
    
    def _sarima_forecast(self, train: pd.Series, test: pd.Series, 
                        forecast_horizon: int) -> Dict:
        """Forecast using SARIMA model"""
        try:
            # Test for stationarity
            adf_result = adfuller(train)
            is_stationary = adf_result[1] < 0.05
            
            # Build SARIMA model
            # Order (p,d,q) x (P,D,Q,s)
            model = SARIMAX(
                train,
                order=(1, 1, 1),
                seasonal_order=(1, 1, 1, 12),
                enforce_stationarity=False,
                enforce_invertibility=False
            )
            
            fitted_model = model.fit(disp=False, maxiter=200)
            
            # Forecast
            forecast = fitted_model.forecast(steps=len(test))
            future_forecast = fitted_model.forecast(steps=forecast_horizon)
            
            # Calculate metrics
            mse = mean_squared_error(test, forecast)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(test, forecast)
            mape = np.mean(np.abs((test - forecast) / test)) * 100
            
            return {
                'forecast': forecast,
                'future_forecast': future_forecast,
                'metrics': {
                    'mse': mse,
                    'rmse': rmse,
                    'mae': mae,
                    'mape': mape
                },
                'model': fitted_model,
                'is_stationary': is_stationary
            }
        except Exception as e:
            print(f"⚠️ SARIMA forecast failed: {str(e)}")
            return {}
    
    def _prophet_forecast(self, train: pd.Series, test: pd.Series, 
                         forecast_horizon: int) -> Dict:
        """Forecast using Prophet model"""
        try:
            # Prepare data for Prophet
            prophet_data = train.reset_index()
            prophet_data.columns = ['ds', 'y']
            
            # Initialize and fit Prophet
            model = Prophet(
                yearly_seasonality=True,
                weekly_seasonality=False,
                daily_seasonality=False,
                seasonality_mode='multiplicative',
                changepoint_prior_scale=0.05
            )
            
            model.fit(prophet_data)
            
            # Make predictions
            future = model.make_future_dataframe(periods=len(test), freq='MS')
            forecast = model.predict(future)
            
            # Extract test predictions
            test_pred = forecast['yhat'].iloc[-len(test):].values
            
            # Future forecast
            future_df = model.make_future_dataframe(periods=forecast_horizon, freq='MS')
            future_forecast_df = model.predict(future_df)
            future_forecast = future_forecast_df['yhat'].iloc[-forecast_horizon:].values
            
            # Calculate metrics
            mse = mean_squared_error(test, test_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(test, test_pred)
            mape = np.mean(np.abs((test - test_pred) / test)) * 100
            
            # Confidence intervals
            confidence_lower = forecast['yhat_lower'].iloc[-len(test):].values
            confidence_upper = forecast['yhat_upper'].iloc[-len(test):].values
            
            return {
                'forecast': pd.Series(test_pred, index=test.index),
                'future_forecast': future_forecast,
                'confidence_lower': confidence_lower,
                'confidence_upper': confidence_upper,
                'metrics': {
                    'mse': mse,
                    'rmse': rmse,
                    'mae': mae,
                    'mape': mape
                },
                'model': model
            }
        except Exception as e:
            print(f"⚠️ Prophet forecast failed: {str(e)}")
            return {}
    
    def _create_ensemble_forecast(self, sarima_results: Dict, prophet_results: Dict, 
                                 test: pd.Series) -> Dict:
        """Create ensemble forecast from multiple models"""
        if not sarima_results or not prophet_results:
            return {}
        
        # Simple averaging
        ensemble_forecast = (
            sarima_results['forecast'].values + 
            prophet_results['forecast'].values
        ) / 2
        
        # Weighted ensemble based on MAPE
        sarima_mape = sarima_results['metrics']['mape']
        prophet_mape = prophet_results['metrics']['mape']
        
        sarima_weight = 1 / (sarima_mape + 0.001)
        prophet_weight = 1 / (prophet_mape + 0.001)
        total_weight = sarima_weight + prophet_weight
        
        weighted_ensemble = (
            sarima_results['forecast'].values * (sarima_weight / total_weight) +
            prophet_results['forecast'].values * (prophet_weight / total_weight)
        )
        
        # Calculate metrics
        mse_ensemble = mean_squared_error(test, ensemble_forecast)
        rmse_ensemble = np.sqrt(mse_ensemble)
        mae_ensemble = mean_absolute_error(test, ensemble_forecast)
        mape_ensemble = np.mean(np.abs((test - ensemble_forecast) / test)) * 100
        
        mse_weighted = mean_squared_error(test, weighted_ensemble)
        rmse_weighted = np.sqrt(mse_weighted)
        mae_weighted = mean_absolute_error(test, weighted_ensemble)
        mape_weighted = np.mean(np.abs((test - weighted_ensemble) / test)) * 100
        
        return {
            'simple_ensemble': pd.Series(ensemble_forecast, index=test.index),
            'weighted_ensemble': pd.Series(weighted_ensemble, index=test.index),
            'metrics': {
                'simple': {
                    'mse': mse_ensemble,
                    'rmse': rmse_ensemble,
                    'mae': mae_ensemble,
                    'mape': mape_ensemble
                },
                'weighted': {
                    'mse': mse_weighted,
                    'rmse': rmse_weighted,
                    'mae': mae_weighted,
                    'mape': mape_weighted
                }
            }
        }
    
    def _print_summary(self):
        """Print summary of forecasting results"""
        print("\n📊 Forecasting Summary:")
        
        if 'sarima' in self.results and self.results['sarima']:
            metrics = self.results['sarima']['metrics']
            print(f"\n   SARIMA Model:")
            print(f"      MAPE: {metrics['mape']:.2f}%")
            print(f"      RMSE: Rp {metrics['rmse']:,.0f}")
        
        if 'prophet' in self.results and self.results['prophet']:
            metrics = self.results['prophet']['metrics']
            print(f"\n   Prophet Model:")
            print(f"      MAPE: {metrics['mape']:.2f}%")
            print(f"      RMSE: Rp {metrics['rmse']:,.0f}")
        
        if 'ensemble' in self.results and self.results['ensemble']:
            weighted_metrics = self.results['ensemble']['metrics']['weighted']
            print(f"\n   Ensemble Model (Weighted):")
            print(f"      MAPE: {weighted_metrics['mape']:.2f}%")
            print(f"      RMSE: Rp {weighted_metrics['rmse']:,.0f}")
            
            # Determine best model
            all_mape = []
            if 'sarima' in self.results and self.results['sarima']:
                all_mape.append(('SARIMA', self.results['sarima']['metrics']['mape']))
            if 'prophet' in self.results and self.results['prophet']:
                all_mape.append(('Prophet', self.results['prophet']['metrics']['mape']))
            if 'ensemble' in self.results and self.results['ensemble']:
                all_mape.append(('Ensemble', weighted_metrics['mape']))
            
            if all_mape:
                best_model = min(all_mape, key=lambda x: x[1])
                print(f"\n   🏆 Best Model: {best_model[0]} (MAPE: {best_model[1]:.2f}%)")

