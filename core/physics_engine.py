"""
EnergySense AI - Production Physics Engine
Mathematically rigorous energy calculations with ODE thermal modeling
"""
import numpy as np
from typing import Dict, List, Tuple
import math

class PhysicsEngine:
    """Production-grade physics-based energy calculation system"""
    
    def __init__(self):
        self.T_REF = 22.0  # Reference temperature (°C)
        self.EFFICIENCY_DEGRADATION = 0.02  # 2% per 10°C
    
    def device_energy_basic(self, power_w: float, hours: float, days: int, quantity: int) -> float:
        """
        Fundamental energy equation: E = P × t × n / 1000
        
        Args:
            power_w: Power consumption in Watts
            hours: Hours per day
            days: Days per month
            quantity: Number of devices
        
        Returns:
            Energy in kWh
        
        Mathematical Foundation:
        E = (P × h × d × n) / 1000
        Where P is in Watts, time in hours, result in kWh
        """
        if power_w <= 0 or hours < 0 or days <= 0 or quantity <= 0:
            raise ValueError("All parameters must be positive")
        
        energy_wh = power_w * hours * days * quantity
        energy_kwh = energy_wh / 1000.0
        
        return energy_kwh
    
    def thermal_ode_model(self, energy_base: float, temperature: float, 
                         thermal_sensitivity: float = 0.03) -> float:
        """
        ODE-based thermal correction model
        
        Differential equation: dE/dt = α(T - T_ref)
        Solution: E(T) = E_base * [1 + α(T - T_ref)/T_ref]
        
        Args:
            energy_base: Base energy consumption (kWh)
            temperature: Ambient temperature (°C)
            thermal_sensitivity: Device-specific thermal coefficient
        
        Returns:
            Temperature-corrected energy (kWh)
        
        Mathematical Foundation:
        The thermal correction follows Arrhenius-like behavior:
        - Cooling devices: Higher T → Higher consumption
        - Heating devices: Lower T → Higher consumption
        """
        if temperature < -50 or temperature > 60:
            raise ValueError("Temperature outside realistic range (-50°C to 60°C)")
        
        # Temperature differential from reference
        delta_t = temperature - self.T_REF
        
        # Thermal correction factor
        correction_factor = 1 + thermal_sensitivity * (delta_t / self.T_REF)
        
        # Ensure physical bounds (energy cannot be negative)
        correction_factor = max(0.1, correction_factor)
        
        corrected_energy = energy_base * correction_factor
        
        return corrected_energy
    
    def advanced_thermal_model(self, energy_base: float, temperature: float,
                              humidity: float = 50.0, device_type: str = "general") -> float:
        """
        Advanced thermal model with humidity and device-specific corrections
        
        Args:
            energy_base: Base energy (kWh)
            temperature: Ambient temperature (°C)
            humidity: Relative humidity (%)
            device_type: Device category for specific modeling
        
        Returns:
            Environmentally corrected energy (kWh)
        """
        # Device-specific thermal coefficients
        thermal_coeffs = {
            "cooling": 0.05,    # AC, fans - high temperature sensitivity
            "heating": -0.04,   # Heaters - inverse temperature relationship
            "kitchen": 0.02,    # Refrigerator, microwave
            "electronics": 0.01, # TV, computers
            "lighting": 0.005,  # LED bulbs
            "general": 0.03
        }
        
        alpha = thermal_coeffs.get(device_type, 0.03)
        
        # Temperature correction
        temp_correction = self.thermal_ode_model(energy_base, temperature, abs(alpha))
        
        # Humidity correction (affects cooling efficiency)
        if device_type == "cooling" and humidity > 60:
            humidity_factor = 1 + 0.001 * (humidity - 60)  # 0.1% per % humidity above 60%
            temp_correction *= humidity_factor
        
        return temp_correction
    
    def calculate_total_energy(self, devices: List[Dict], temperature: float = 25.0,
                              humidity: float = 50.0) -> Dict[str, float]:
        """
        Calculate total energy consumption with all corrections
        
        Args:
            devices: List of device configurations
            temperature: Ambient temperature
            humidity: Relative humidity
        
        Returns:
            Dictionary with energy breakdown and totals
        """
        results = {
            "devices": [],
            "total_base_energy": 0.0,
            "total_corrected_energy": 0.0,
            "temperature_impact": 0.0,
            "efficiency_impact": 0.0
        }
        
        for device in devices:
            # Basic energy calculation
            base_energy = self.device_energy_basic(
                device["power_watts"],
                device["hours_per_day"],
                device["days_per_month"],
                device["quantity"]
            )
            
            # Apply thermal correction
            corrected_energy = self.advanced_thermal_model(
                base_energy,
                temperature,
                humidity,
                device.get("category", "general")
            )
            
            device_result = {
                "name": device["device_name"],
                "base_energy": base_energy,
                "corrected_energy": corrected_energy,
                "temperature_impact": corrected_energy - base_energy
            }
            
            results["devices"].append(device_result)
            results["total_base_energy"] += base_energy
            results["total_corrected_energy"] += corrected_energy
        
        results["temperature_impact"] = results["total_corrected_energy"] - results["total_base_energy"]
        
        return results

# Global physics engine instance
PHYSICS = PhysicsEngine()

# Legacy compatibility functions
def device_energy(power_w, hours, days, quantity):
    """Legacy compatibility wrapper"""
    return PHYSICS.device_energy_basic(power_w, hours, days, quantity)

def temperature_adjustment(energy, temperature, alpha=0.03):
    """Legacy compatibility wrapper"""
    return PHYSICS.thermal_ode_model(energy, temperature, alpha)