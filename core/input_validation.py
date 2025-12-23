"""
EnergySense AI - Production Input Validation System
Physics-aware validation with mathematical constraints
"""
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import streamlit as st

@dataclass
class DeviceInput:
    """Validated device input schema"""
    device_type: str
    device_name: str
    power_watts: float
    voltage: float
    quantity: int
    hours_per_day: float
    days_per_month: int
    room: str
    usage_pattern: str
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Physics-based validation with error reporting"""
        errors = []
        
        # Power validation (physics constraints)
        if self.power_watts <= 0 or self.power_watts > 10000:
            errors.append(f"Power {self.power_watts}W outside realistic range (1-10000W)")
        
        # Voltage validation (electrical safety)
        if self.voltage not in [110, 120, 220, 230, 240]:
            errors.append(f"Voltage {self.voltage}V not standard (110/120/220/230/240V)")
        
        # Usage validation (temporal constraints)
        if self.hours_per_day > 24:
            errors.append("Hours per day cannot exceed 24")
        
        if self.days_per_month > 31:
            errors.append("Days per month cannot exceed 31")
        
        # Energy consumption sanity check
        monthly_kwh = (self.power_watts * self.hours_per_day * self.days_per_month * self.quantity) / 1000
        if monthly_kwh > 2000:  # Extremely high usage flag
            errors.append(f"Monthly consumption {monthly_kwh:.1f} kWh seems unrealistic")
        
        return len(errors) == 0, errors

@dataclass
class BillingConfig:
    """Regional billing configuration"""
    country: str
    currency: str
    tariff_type: str  # flat, tiered, time_of_use
    base_rate: float
    fixed_charge: float
    tax_rate: float
    peak_hours: Optional[List[int]] = None
    tiers: Optional[List[Dict]] = None
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate billing configuration"""
        errors = []
        
        if self.base_rate <= 0:
            errors.append("Base rate must be positive")
        
        if self.tax_rate < 0 or self.tax_rate > 1:
            errors.append("Tax rate must be between 0 and 1")
        
        if self.tariff_type == "tiered" and not self.tiers:
            errors.append("Tiered tariff requires tier definitions")
        
        return len(errors) == 0, errors

class InputValidator:
    """Production-grade input validation system"""
    
    @staticmethod
    def create_device_form() -> Optional[DeviceInput]:
        """Create validated device input form"""
        st.subheader("📱 Device Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            device_type = st.selectbox("Device Type", [
                "Air Conditioner", "Television", "Refrigerator", "Washing Machine",
                "Microwave", "Water Heater", "LED Bulb", "Fan", "Electric Kettle"
            ])
            
            device_name = st.text_input("Device Name", f"My {device_type}")
            power_watts = st.number_input("Power Rating (W)", min_value=1, max_value=10000, value=100)
            voltage = st.selectbox("Voltage (V)", [110, 120, 220, 230, 240], index=3)
        
        with col2:
            quantity = st.number_input("Quantity", min_value=1, max_value=20, value=1)
            hours_per_day = st.slider("Hours per Day", 0.0, 24.0, 8.0, 0.5)
            days_per_month = st.slider("Days per Month", 1, 31, 30)
            room = st.selectbox("Room/Zone", ["Living Room", "Bedroom", "Kitchen", "Office", "Bathroom"])
            usage_pattern = st.selectbox("Usage Pattern", ["continuous", "intermittent", "peak_only"])
        
        device = DeviceInput(
            device_type=device_type,
            device_name=device_name,
            power_watts=power_watts,
            voltage=voltage,
            quantity=quantity,
            hours_per_day=hours_per_day,
            days_per_month=days_per_month,
            room=room,
            usage_pattern=usage_pattern
        )
        
        # Real-time validation
        is_valid, errors = device.validate()
        
        if not is_valid:
            for error in errors:
                st.error(f"⚠️ {error}")
            return None
        
        # Show calculated energy preview
        monthly_kwh = (power_watts * hours_per_day * days_per_month * quantity) / 1000
        st.info(f"📊 Estimated monthly consumption: {monthly_kwh:.2f} kWh")
        
        return device
    
    @staticmethod
    def create_billing_form() -> Optional[BillingConfig]:
        """Create validated billing configuration form"""
        st.subheader("💰 Billing Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            country = st.selectbox("Country", ["Nigeria", "USA", "UK", "India", "South Africa"])
            currency = st.selectbox("Currency", ["NGN", "USD", "GBP", "INR", "ZAR"])
            tariff_type = st.selectbox("Tariff Type", ["flat", "tiered", "time_of_use"])
        
        with col2:
            base_rate = st.number_input("Base Rate per kWh", min_value=0.01, value=0.15, step=0.01)
            fixed_charge = st.number_input("Fixed Monthly Charge", min_value=0.0, value=10.0)
            tax_rate = st.slider("Tax Rate (%)", 0.0, 25.0, 7.5) / 100
        
        billing = BillingConfig(
            country=country,
            currency=currency,
            tariff_type=tariff_type,
            base_rate=base_rate,
            fixed_charge=fixed_charge,
            tax_rate=tax_rate
        )
        
        # Validation
        is_valid, errors = billing.validate()
        
        if not is_valid:
            for error in errors:
                st.error(f"⚠️ {error}")
            return None
        
        return billing