"""
EnergySense AI - Production Billing Engine
Regional tariff structures with mathematical billing calculations
"""
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import math

@dataclass
class TariffTier:
    """Tiered tariff structure"""
    max_kwh: Optional[float]  # None for unlimited top tier
    rate_per_kwh: float
    description: str

@dataclass
class RegionalBilling:
    """Complete regional billing configuration"""
    country: str
    currency: str
    currency_symbol: str
    tariff_type: str  # flat, tiered, time_of_use
    base_rate: float
    fixed_charge: float
    tax_rate: float
    tiers: Optional[List[TariffTier]] = None
    peak_hours: Optional[List[int]] = None
    peak_multiplier: float = 1.5

class BillingEngine:
    """Production-grade billing calculation system"""
    
    def __init__(self):
        self.regional_configs = {
            "Nigeria": RegionalBilling(
                country="Nigeria",
                currency="NGN",
                currency_symbol="₦",
                tariff_type="tiered",
                base_rate=68.0,
                fixed_charge=1000.0,
                tax_rate=0.075,
                tiers=[
                    TariffTier(50, 30.0, "Lifeline tariff"),
                    TariffTier(100, 50.0, "Residential R1"),
                    TariffTier(300, 68.0, "Residential R2"),
                    TariffTier(None, 85.0, "Residential R3")
                ]
            ),
            "USA": RegionalBilling(
                country="USA",
                currency="USD",
                currency_symbol="$",
                tariff_type="tiered",
                base_rate=0.15,
                fixed_charge=10.0,
                tax_rate=0.08,
                tiers=[
                    TariffTier(300, 0.12, "Baseline"),
                    TariffTier(600, 0.15, "Tier 1"),
                    TariffTier(None, 0.25, "Tier 2")
                ]
            ),
            "UK": RegionalBilling(
                country="UK",
                currency="GBP",
                currency_symbol="£",
                tariff_type="flat",
                base_rate=0.28,
                fixed_charge=25.0,
                tax_rate=0.05
            ),
            "India": RegionalBilling(
                country="India",
                currency="INR",
                currency_symbol="₹",
                tariff_type="tiered",
                base_rate=6.0,
                fixed_charge=50.0,
                tax_rate=0.12,
                tiers=[
                    TariffTier(100, 3.0, "Domestic LT-1A"),
                    TariffTier(200, 4.5, "Domestic LT-1B"),
                    TariffTier(300, 6.0, "Domestic LT-1C"),
                    TariffTier(None, 7.5, "Domestic LT-1D")
                ]
            )
        }
    
    def calculate_flat_tariff(self, energy_kwh: float, config: RegionalBilling) -> Dict[str, float]:
        """
        Calculate bill using flat tariff structure
        
        Mathematical Formula:
        Bill = (Energy × Rate) + Fixed_Charge + Tax
        """
        energy_cost = energy_kwh * config.base_rate
        subtotal = energy_cost + config.fixed_charge
        tax_amount = subtotal * config.tax_rate
        total_bill = subtotal + tax_amount
        
        return {
            "energy_cost": energy_cost,
            "fixed_charge": config.fixed_charge,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_bill": total_bill,
            "effective_rate": total_bill / energy_kwh if energy_kwh > 0 else 0
        }
    
    def calculate_tiered_tariff(self, energy_kwh: float, config: RegionalBilling) -> Dict[str, float]:
        """
        Calculate bill using tiered tariff structure
        
        Mathematical Formula:
        For each tier i: Cost_i = min(Energy_remaining, Tier_limit) × Rate_i
        Total = Σ(Cost_i) + Fixed_Charge + Tax
        """
        if not config.tiers:
            return self.calculate_flat_tariff(energy_kwh, config)
        
        energy_remaining = energy_kwh
        energy_cost = 0.0
        tier_breakdown = []
        
        for tier in config.tiers:
            if energy_remaining <= 0:
                break
            
            # Calculate energy consumed in this tier
            if tier.max_kwh is None:
                # Unlimited top tier
                tier_energy = energy_remaining
            else:
                tier_energy = min(energy_remaining, tier.max_kwh)
            
            tier_cost = tier_energy * tier.rate_per_kwh
            energy_cost += tier_cost
            
            tier_breakdown.append({
                "tier": tier.description,
                "energy_kwh": tier_energy,
                "rate": tier.rate_per_kwh,
                "cost": tier_cost
            })
            
            energy_remaining -= tier_energy
            
            # Move to next tier's starting point
            if tier.max_kwh is not None:
                energy_remaining = max(0, energy_remaining)
        
        subtotal = energy_cost + config.fixed_charge
        tax_amount = subtotal * config.tax_rate
        total_bill = subtotal + tax_amount
        
        return {
            "energy_cost": energy_cost,
            "fixed_charge": config.fixed_charge,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_bill": total_bill,
            "effective_rate": total_bill / energy_kwh if energy_kwh > 0 else 0,
            "tier_breakdown": tier_breakdown
        }
    
    def calculate_time_of_use_tariff(self, energy_kwh: float, peak_percentage: float, 
                                   config: RegionalBilling) -> Dict[str, float]:
        """
        Calculate bill using time-of-use tariff
        
        Args:
            energy_kwh: Total energy consumption
            peak_percentage: Percentage of energy used during peak hours (0-1)
        """
        peak_energy = energy_kwh * peak_percentage
        off_peak_energy = energy_kwh * (1 - peak_percentage)
        
        peak_rate = config.base_rate * config.peak_multiplier
        off_peak_rate = config.base_rate
        
        peak_cost = peak_energy * peak_rate
        off_peak_cost = off_peak_energy * off_peak_rate
        energy_cost = peak_cost + off_peak_cost
        
        subtotal = energy_cost + config.fixed_charge
        tax_amount = subtotal * config.tax_rate
        total_bill = subtotal + tax_amount
        
        return {
            "peak_energy": peak_energy,
            "off_peak_energy": off_peak_energy,
            "peak_cost": peak_cost,
            "off_peak_cost": off_peak_cost,
            "energy_cost": energy_cost,
            "fixed_charge": config.fixed_charge,
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "total_bill": total_bill,
            "effective_rate": total_bill / energy_kwh if energy_kwh > 0 else 0
        }
    
    def calculate_bill(self, energy_kwh: float, country: str, 
                      peak_percentage: float = 0.3) -> Dict[str, any]:
        """
        Calculate electricity bill based on regional configuration
        
        Args:
            energy_kwh: Total monthly energy consumption
            country: Country for billing rules
            peak_percentage: Percentage of energy used during peak hours
        
        Returns:
            Complete billing breakdown with mathematical explanation
        """
        config = self.regional_configs.get(country)
        if not config:
            raise ValueError(f"Billing configuration not available for {country}")
        
        # Input validation
        if energy_kwh < 0:
            raise ValueError("Energy consumption cannot be negative")
        
        # Calculate based on tariff type
        if config.tariff_type == "flat":
            bill_details = self.calculate_flat_tariff(energy_kwh, config)
        elif config.tariff_type == "tiered":
            bill_details = self.calculate_tiered_tariff(energy_kwh, config)
        elif config.tariff_type == "time_of_use":
            bill_details = self.calculate_time_of_use_tariff(energy_kwh, peak_percentage, config)
        else:
            raise ValueError(f"Unknown tariff type: {config.tariff_type}")
        
        # Add metadata
        bill_details.update({
            "country": config.country,
            "currency": config.currency,
            "currency_symbol": config.currency_symbol,
            "tariff_type": config.tariff_type,
            "energy_kwh": energy_kwh,
            "tax_rate_percent": config.tax_rate * 100
        })
        
        return bill_details
    
    def get_available_countries(self) -> List[str]:
        """Get list of supported countries"""
        return list(self.regional_configs.keys())
    
    def get_country_config(self, country: str) -> Optional[RegionalBilling]:
        """Get billing configuration for a country"""
        return self.regional_configs.get(country)
    
    def estimate_savings(self, current_kwh: float, reduced_kwh: float, 
                        country: str) -> Dict[str, float]:
        """
        Calculate potential savings from energy reduction
        
        Args:
            current_kwh: Current energy consumption
            reduced_kwh: Reduced energy consumption
            country: Country for billing calculation
        
        Returns:
            Savings breakdown
        """
        current_bill = self.calculate_bill(current_kwh, country)
        reduced_bill = self.calculate_bill(reduced_kwh, country)
        
        savings = {
            "energy_reduction_kwh": current_kwh - reduced_kwh,
            "energy_reduction_percent": ((current_kwh - reduced_kwh) / current_kwh) * 100,
            "cost_savings": current_bill["total_bill"] - reduced_bill["total_bill"],
            "cost_savings_percent": ((current_bill["total_bill"] - reduced_bill["total_bill"]) / current_bill["total_bill"]) * 100,
            "current_bill": current_bill["total_bill"],
            "reduced_bill": reduced_bill["total_bill"]
        }
        
        return savings

# Global billing engine instance
BILLING = BillingEngine()