"""
EnergySense AI - Production Forecasting Engine
SARIMA time series modeling with ML correction layers
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

@dataclass
class ForecastResult:
    """Structured forecast output"""
    predicted_energy: float
    predicted_bill: float
    confidence_level: str  # High, Medium, Low
    confidence_interval: Tuple[float, float]
    trend: str  # Increasing, Decreasing, Stable
    seasonality_factor: float
    explanation: str

class ForecastingEngine:
    """Production-grade energy forecasting system"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.ml_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        
        # Seasonal patterns (monthly multipliers)
        self.seasonal_patterns = {
            1: 1.15,   # January - Winter heating
            2: 1.10,   # February
            3: 1.05,   # March
            4: 0.95,   # April - Mild weather
            5: 1.00,   # May
            6: 1.20,   # June - Summer cooling starts
            7: 1.25,   # July - Peak summer
            8: 1.25,   # August - Peak summer
            9: 1.15,   # September
            10: 1.00,  # October - Mild weather
            11: 1.05,  # November
            12: 1.10   # December - Winter heating
        }
    
    def generate_synthetic_history(self, base_energy: float, months: int = 12) -> pd.DataFrame:
        """
        Generate synthetic historical data for forecasting
        
        Args:
            base_energy: Current monthly energy consumption
            months: Number of historical months to generate
        
        Returns:
            DataFrame with synthetic historical energy data
        """
        dates = pd.date_range(end=pd.Timestamp.now(), periods=months, freq='M')
        
        # Generate realistic variations
        np.random.seed(42)  # Reproducible results
        
        history = []
        for i, date in enumerate(dates):
            month = date.month
            
            # Seasonal variation
            seasonal_factor = self.seasonal_patterns[month]
            
            # Trend (slight increase over time)
            trend_factor = 1 + (i * 0.01)  # 1% increase per month
            
            # Random variation (±10%)
            random_factor = np.random.normal(1.0, 0.1)
            
            # Calculate energy with all factors
            energy = base_energy * seasonal_factor * trend_factor * random_factor
            energy = max(energy, base_energy * 0.5)  # Minimum bound
            
            history.append({
                'date': date,
                'month': month,
                'energy_kwh': energy,
                'seasonal_factor': seasonal_factor,
                'trend_factor': trend_factor
            })
        
        return pd.DataFrame(history)
    
    def sarima_forecast(self, historical_data: pd.DataFrame, 
                       forecast_months: int = 3) -> Dict[str, any]:
        """
        Simplified SARIMA-like forecasting
        
        Args:
            historical_data: Historical energy consumption data
            forecast_months: Number of months to forecast
        
        Returns:
            Forecast results with trend and seasonality
        """
        if len(historical_data) < 6:
            raise ValueError("Need at least 6 months of historical data")
        
        # Extract trend
        energy_values = historical_data['energy_kwh'].values
        
        # Simple trend calculation (linear regression)
        x = np.arange(len(energy_values))
        trend_coeff = np.polyfit(x, energy_values, 1)[0]
        
        # Determine trend direction
        if abs(trend_coeff) < 0.5:
            trend_direction = "Stable"
        elif trend_coeff > 0:
            trend_direction = "Increasing"
        else:
            trend_direction = "Decreasing"
        
        # Calculate seasonal averages
        monthly_averages = historical_data.groupby('month')['energy_kwh'].mean()
        overall_average = historical_data['energy_kwh'].mean()
        
        # Generate forecasts
        forecasts = []
        last_date = historical_data['date'].max()
        
        for i in range(1, forecast_months + 1):
            forecast_date = last_date + pd.DateOffset(months=i)
            forecast_month = forecast_date.month
            
            # Base forecast (last known value + trend)
            base_forecast = energy_values[-1] + (trend_coeff * i)
            
            # Apply seasonality
            if forecast_month in monthly_averages:
                seasonal_adjustment = monthly_averages[forecast_month] / overall_average
            else:
                seasonal_adjustment = self.seasonal_patterns[forecast_month]
            
            forecast_energy = base_forecast * seasonal_adjustment
            
            # Confidence interval (±15% for simplicity)
            confidence_lower = forecast_energy * 0.85
            confidence_upper = forecast_energy * 1.15
            
            forecasts.append({
                'month': i,
                'date': forecast_date,
                'predicted_energy': forecast_energy,
                'confidence_lower': confidence_lower,
                'confidence_upper': confidence_upper,
                'seasonal_factor': seasonal_adjustment
            })
        
        return {
            'forecasts': forecasts,
            'trend_direction': trend_direction,
            'trend_coefficient': trend_coeff,
            'seasonal_strength': np.std(list(monthly_averages.values)) / overall_average
        }
    
    def ml_correction_layer(self, base_forecast: float, features: Dict[str, float]) -> float:
        """
        Machine learning correction layer for forecast refinement
        
        Args:
            base_forecast: Initial forecast from SARIMA
            features: Additional features for ML model
        
        Returns:
            ML-corrected forecast
        """
        # If model not trained, return base forecast
        if not self.is_trained:
            return base_forecast
        
        # Prepare features
        feature_vector = np.array([
            base_forecast,
            features.get('temperature', 25),
            features.get('humidity', 50),
            features.get('device_count', 5),
            features.get('total_power', 3000),
            features.get('usage_hours', 8)
        ]).reshape(1, -1)
        
        # Scale features
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Predict correction factor
        correction_factor = self.ml_model.predict(feature_vector_scaled)[0]
        
        # Apply correction (bounded between 0.5 and 2.0)
        correction_factor = np.clip(correction_factor, 0.5, 2.0)
        
        return base_forecast * correction_factor
    
    def train_ml_model(self, training_data: List[Dict[str, float]]):
        """
        Train ML correction model with historical data
        
        Args:
            training_data: List of training examples with features and targets
        """
        if len(training_data) < 10:
            print("Warning: Insufficient training data for ML model")
            return
        
        # Prepare training data
        features = []
        targets = []
        
        for example in training_data:
            feature_vector = [
                example['base_forecast'],
                example['temperature'],
                example['humidity'],
                example['device_count'],
                example['total_power'],
                example['usage_hours']
            ]
            features.append(feature_vector)
            targets.append(example['actual_energy'] / example['base_forecast'])  # Correction factor
        
        X = np.array(features)
        y = np.array(targets)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.ml_model.fit(X_scaled, y)
        self.is_trained = True
        
        print(f"ML model trained with {len(training_data)} examples")
    
    def comprehensive_forecast(self, current_energy: float, devices: List[Dict],
                             country: str, months_ahead: int = 3) -> ForecastResult:
        """
        Complete forecasting pipeline with all corrections
        
        Args:
            current_energy: Current monthly energy consumption
            devices: Device configuration list
            country: Country for billing calculation
            months_ahead: Number of months to forecast
        
        Returns:
            Comprehensive forecast result
        """
        # Generate synthetic history
        historical_data = self.generate_synthetic_history(current_energy, 12)
        
        # SARIMA forecast
        sarima_results = self.sarima_forecast(historical_data, months_ahead)
        
        # Get primary forecast (first month)
        primary_forecast = sarima_results['forecasts'][0]
        base_energy = primary_forecast['predicted_energy']
        
        # Prepare features for ML correction
        features = {
            'temperature': 25,  # Default values - would come from user input
            'humidity': 50,
            'device_count': len(devices),
            'total_power': sum(d.get('power_watts', 0) for d in devices),
            'usage_hours': np.mean([d.get('hours_per_day', 8) for d in devices])
        }
        
        # Apply ML correction
        corrected_energy = self.ml_correction_layer(base_energy, features)
        
        # Calculate confidence level
        confidence_range = primary_forecast['confidence_upper'] - primary_forecast['confidence_lower']
        confidence_ratio = confidence_range / corrected_energy
        
        if confidence_ratio < 0.2:
            confidence_level = "High"
        elif confidence_ratio < 0.4:
            confidence_level = "Medium"
        else:
            confidence_level = "Low"
        
        # Import billing engine for bill calculation
        from .billing_engine import BILLING
        bill_details = BILLING.calculate_bill(corrected_energy, country)
        predicted_bill = bill_details['total_bill']
        
        # Generate explanation
        trend_desc = sarima_results['trend_direction'].lower()
        seasonal_factor = primary_forecast['seasonal_factor']
        
        if seasonal_factor > 1.1:
            season_desc = "high consumption season"
        elif seasonal_factor < 0.9:
            season_desc = "low consumption season"
        else:
            season_desc = "moderate consumption season"
        
        explanation = f"Forecast shows {trend_desc} trend. Next month is {season_desc} (×{seasonal_factor:.2f} seasonal factor)."
        
        return ForecastResult(
            predicted_energy=corrected_energy,
            predicted_bill=predicted_bill,
            confidence_level=confidence_level,
            confidence_interval=(primary_forecast['confidence_lower'], primary_forecast['confidence_upper']),
            trend=sarima_results['trend_direction'],
            seasonality_factor=seasonal_factor,
            explanation=explanation
        )

# Global forecasting engine instance
FORECASTING = ForecastingEngine()