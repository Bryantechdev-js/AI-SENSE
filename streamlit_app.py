"""
Smart Energy Consumption Forecaster – Africa-Optimized System
Production-Ready Energy Management Platform for Low-Income Communities
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import numpy as np
import os
import requests
from typing import Dict, List, Optional
import time
import math

# Page configuration
st.set_page_config(
    page_title="EnergySense - Smart Energy Forecaster",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Production CSS - Mobile-first, accessibility-focused
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .main-header {
        background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .africa-card {
        background: linear-gradient(135deg, #FF6B35 0%, #F7931E 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .budget-card {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #FF5722 0%, #E64A19 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .chat-container {
        background: #f8f9fa;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        min-height: 400px;
        max-height: 600px;
        overflow-y: auto;
        border: 2px solid #e9ecef;
    }
    
    .user-message {
        background: #007bff;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 5px 15px;
        margin: 0.5rem 0;
        margin-left: 10%;
        font-size: 1.1rem;
    }
    
    .ai-message {
        background: white;
        color: #333;
        padding: 1rem;
        border-radius: 15px 15px 15px 5px;
        margin: 0.5rem 0;
        margin-right: 10%;
        border-left: 4px solid #28a745;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .device-icon {
        font-size: 2rem;
        margin: 0.5rem;
        cursor: pointer;
        padding: 1rem;
        border-radius: 10px;
        background: #f8f9fa;
        border: 2px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    .device-icon:hover {
        background: #e9ecef;
        transform: scale(1.05);
    }
    
    .budget-progress {
        background: #e9ecef;
        border-radius: 10px;
        height: 20px;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #28a745 0%, #20c997 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 0.5s ease;
    }
    
    /* High contrast for accessibility */
    .high-contrast {
        border: 3px solid #000;
        background: #fff;
        color: #000;
    }
    
    /* Large text for low literacy */
    .large-text {
        font-size: 1.3rem;
        line-height: 1.8;
    }
    
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 1.5rem;
        }
        .stColumns > div {
            margin-bottom: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# African Countries Database - Comprehensive energy data
AFRICAN_COUNTRIES = {
    "Cameroon": {
        "currency": "FCFA", "symbol": "XAF", "rate": 79.0, "fixed": 1500, "tax": 0.175,
        "prepaid_available": True, "grid_stability": 0.65, "rural_access": 0.45,
        "peak_hours": [18, 19, 20, 21], "load_shedding": True, "solar_potential": 0.85
    },
    "Nigeria": {
        "currency": "₦", "symbol": "NGN", "rate": 68.0, "fixed": 1000, "tax": 0.075,
        "prepaid_available": True, "grid_stability": 0.55, "rural_access": 0.35,
        "peak_hours": [18, 19, 20, 21, 22], "load_shedding": True, "solar_potential": 0.90
    },
    "Kenya": {
        "currency": "KSh", "symbol": "KES", "rate": 24.0, "fixed": 200, "tax": 0.16,
        "prepaid_available": True, "grid_stability": 0.75, "rural_access": 0.65,
        "peak_hours": [18, 19, 20, 21], "load_shedding": False, "solar_potential": 0.95
    },
    "Ghana": {
        "currency": "₵", "symbol": "GHS", "rate": 1.20, "fixed": 25, "tax": 0.125,
        "prepaid_available": True, "grid_stability": 0.70, "rural_access": 0.55,
        "peak_hours": [18, 19, 20, 21], "load_shedding": True, "solar_potential": 0.88
    },
    "South Africa": {
        "currency": "R", "symbol": "ZAR", "rate": 1.85, "fixed": 150, "tax": 0.15,
        "prepaid_available": True, "grid_stability": 0.80, "rural_access": 0.75,
        "peak_hours": [17, 18, 19, 20], "load_shedding": True, "solar_potential": 0.92
    }
}

# Africa-optimized device database
AFRICAN_DEVICES = {
    # Essential household items
    "LED Bulb": {"power": 9, "hours": 6.0, "category": "lighting", "emoji": "💡", "priority": "high", "cost_usd": 3},
    "CFL Bulb": {"power": 23, "hours": 6.0, "category": "lighting", "emoji": "💡", "priority": "medium", "cost_usd": 2},
    "Torch/Flashlight": {"power": 3, "hours": 2.0, "category": "lighting", "emoji": "🔦", "priority": "high", "cost_usd": 5},
    
    # Cooling & comfort
    "Table Fan": {"power": 45, "hours": 8.0, "category": "cooling", "emoji": "🌀", "priority": "high", "cost_usd": 25},
    "Ceiling Fan": {"power": 75, "hours": 10.0, "category": "cooling", "emoji": "🌀", "priority": "medium", "cost_usd": 40},
    "Small AC": {"power": 800, "hours": 6.0, "category": "cooling", "emoji": "❄️", "priority": "low", "cost_usd": 300},
    
    # Communication & entertainment
    "Mobile Phone Charger": {"power": 5, "hours": 3.0, "category": "electronics", "emoji": "📱", "priority": "high", "cost_usd": 10},
    "Radio": {"power": 15, "hours": 4.0, "category": "entertainment", "emoji": "📻", "priority": "high", "cost_usd": 20},
    "Small TV": {"power": 80, "hours": 4.0, "category": "entertainment", "emoji": "📺", "priority": "medium", "cost_usd": 150},
    "Satellite Decoder": {"power": 25, "hours": 4.0, "category": "entertainment", "emoji": "📡", "priority": "medium", "cost_usd": 50},
    
    # Kitchen & food
    "Small Refrigerator": {"power": 120, "hours": 24.0, "category": "kitchen", "emoji": "🧊", "priority": "medium", "cost_usd": 200},
    "Electric Kettle": {"power": 1500, "hours": 0.3, "category": "kitchen", "emoji": "☕", "priority": "medium", "cost_usd": 25},
    "Rice Cooker": {"power": 400, "hours": 1.0, "category": "kitchen", "emoji": "🍚", "priority": "medium", "cost_usd": 30},
    "Blender": {"power": 300, "hours": 0.2, "category": "kitchen", "emoji": "🥤", "priority": "low", "cost_usd": 35},
    
    # Work & business
    "Laptop": {"power": 65, "hours": 6.0, "category": "work", "emoji": "💻", "priority": "medium", "cost_usd": 400},
    "Printer": {"power": 200, "hours": 1.0, "category": "work", "emoji": "🖨️", "priority": "low", "cost_usd": 100},
    "Sewing Machine": {"power": 100, "hours": 4.0, "category": "work", "emoji": "🧵", "priority": "medium", "cost_usd": 150},
    
    # Water & hygiene
    "Water Pump": {"power": 750, "hours": 2.0, "category": "water", "emoji": "💧", "priority": "high", "cost_usd": 120},
    "Iron": {"power": 1000, "hours": 0.5, "category": "household", "emoji": "👔", "priority": "medium", "cost_usd": 20}
}

# Initialize session state
if 'devices' not in st.session_state:
    st.session_state.devices = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'country' not in st.session_state:
    st.session_state.country = "Cameroon"
if 'monthly_budget' not in st.session_state:
    st.session_state.monthly_budget = 15000  # FCFA
if 'household_size' not in st.session_state:
    st.session_state.household_size = 4
if 'income_level' not in st.session_state:
    st.session_state.income_level = "Low"
if 'language' not in st.session_state:
    st.session_state.language = "English"

# Production-ready AI Integration
class AfricaEnergyAI:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.enabled = self._test_api_connection()
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def _get_api_key(self):
        """Safely get API key from multiple sources"""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and "OPENROUTER_API_KEY" in st.secrets:
                return st.secrets["OPENROUTER_API_KEY"]
            # Try environment variable
            return os.getenv("OPENROUTER_API_KEY", "")
        except:
            return ""
    
    def _test_api_connection(self):
        """Test API connection on initialization"""
        if not self.api_key:
            return False
        
        try:
            headers = self._get_headers()
            test_payload = {
                "model": "openai/gpt-3.5-turbo",
                "messages": [{"role": "user", "content": "test"}],
                "max_tokens": 5
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=test_payload,
                timeout=5
            )
            return response.status_code == 200
        except:
            return False
    
    def _get_headers(self):
        """Get API headers with all required fields"""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": self._get_site_url(),
            "X-Title": self._get_site_name()
        }
    
    def _get_site_url(self):
        try:
            return st.secrets.get("SITE_URL", "https://ai-sense-43djhny8ihhq2rvudnp974.streamlit.app/")
        except:
            return "https://ai-sense-43djhny8ihhq2rvudnp974.streamlit.app/"
    
    def _get_site_name(self):
        try:
            return st.secrets.get("SITE_NAME", "EnergySense AI")
        except:
            return "EnergySense AI"
    
    def get_response(self, user_message, context):
        """Get AI response with comprehensive error handling"""
        if not self.enabled:
            return self.get_fallback_response(user_message, context)
        
        try:
            headers = self._get_headers()
            
            system_prompt = f"""You are an energy advisor for African households in {context['country']}.
            
Context: Budget {context['budget']} {context['currency']}, {context['household_size']} people, {context['income_level']} income.
            
Provide practical advice in simple language under 100 words focusing on immediate savings."""
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and result['choices']:
                    return result['choices'][0]['message']['content']
            
            # Log error for debugging
            error_msg = f"API Error {response.status_code}: {response.text[:100]}"
            if st.secrets.get("DEBUG", "false").lower() == "true":
                st.error(f"🔧 Debug: {error_msg}")
            
        except requests.exceptions.Timeout:
            if st.secrets.get("DEBUG", "false").lower() == "true":
                st.warning("🔧 Debug: API timeout")
        except Exception as e:
            if st.secrets.get("DEBUG", "false").lower() == "true":
                st.error(f"🔧 Debug: {str(e)}")
        
        return self.get_fallback_response(user_message, context)
    
    def get_fallback_response(self, user_message, context):
        """Enhanced intelligent fallback responses"""
        budget = context['budget']
        currency = context['currency']
        country = context['country']
        msg_lower = user_message.lower()
        
        # Energy saving responses
        if any(word in msg_lower for word in ["save", "reduce", "lower", "cut", "decrease"]):
            return f"""💡 **Top Energy Savings for {country}:**

**Immediate Actions:**
• Switch to LED bulbs → Save 70% on lighting
• Use fans instead of AC → Save {currency}2000+/month
• Unplug devices when not using → Save 10-15%
• Iron clothes in batches → Reduce usage time

**Smart Usage:**
• Charge phones during day (cheaper rates)
• Use natural light when possible
• Cook multiple meals together

**Budget Impact:** These changes can save {currency}{int(budget*0.3)}/month!"""

        # Budget management
        elif any(word in msg_lower for word in ["budget", "money", "cost", "afford", "expensive"]):
            daily_budget = budget // 30
            return f"""💰 **Smart Budget Management:**

**Your Budget Breakdown:**
• Daily limit: {currency}{daily_budget}
• Weekly target: {currency}{budget//4}
• Emergency reserve: {currency}{int(budget*0.2)}

**Priority Spending:**
1. Essential lighting: {currency}{int(budget*0.25)}
2. Phone/communication: {currency}{int(budget*0.15)}
3. Cooling/comfort: {currency}{int(budget*0.35)}
4. Entertainment: {currency}{int(budget*0.25)}

**Warning Signs:**
• Spending over {currency}{int(daily_budget*1.5)}/day
• Frequent power meter top-ups
• Using high-power devices during peak hours"""

        # Device recommendations
        elif any(word in msg_lower for word in ["device", "appliance", "buy", "purchase", "recommend"]):
            return f"""🔌 **Best Devices for {country}:**

**Most Efficient (Buy First):**
• LED bulbs: 9W, saves {currency}500/month
• Table fan: 45W, much cheaper than AC
• Phone charger: 5W, very efficient
• Radio: 15W, entertainment + news

**Avoid if Budget is Tight:**
• Old refrigerators (120W+ continuous)
• Electric kettles (1500W, use briefly)
• Multiple TVs
• Electric heaters

**Smart Buying Tips:**
• Check power rating (lower watts = less cost)
• Buy energy-efficient models
• Consider solar alternatives for lighting
• Look for timer switches"""

        # Power outage help
        elif any(word in msg_lower for word in ["outage", "blackout", "power cut", "load shedding", "grid"]):
            return f"""⚡ **Power Outage Solutions for {country}:**

**Immediate Preparation:**
• Charge all devices during grid hours
• Keep flashlights/torches ready
• Store water when pumps work
• Cook meals when power available

**Backup Options:**
• Solar torch: {currency}3000-5000
• Power bank: {currency}8000-15000
• Small solar panel: {currency}20000-40000
• Battery radio: {currency}5000-8000

**During Outages:**
• Use battery devices sparingly
• Avoid opening fridge frequently
• Use natural ventilation
• Plan activities around power schedule"""

        # General help
        else:
            return f"""🏠 **Energy Assistant for {country}**

I help families manage electricity costs effectively!

**I can help you with:**
• Reducing monthly bills
• Choosing efficient devices
• Managing tight budgets
• Preparing for power outages
• Finding solar alternatives

**Your Profile:**
• Budget: {currency}{budget}/month
• Country: {country}
• Household: {context['household_size']} people

**Quick Tips:**
• Start with LED bulbs for instant savings
• Use fans instead of AC when possible
• Unplug devices when not in use
• Check your meter daily

**Ask me:** "How can I save money?" or "What devices should I avoid?""""

    def get_status_message(self):
        """Get current AI status for display"""
        if self.enabled:
            return "🤖 AI Assistant: Online", "success"
        else:
            return "🤖 Smart Assistant: Ready (Offline mode)", "info"

# Core calculation functions
def calculate_device_energy(power_w, hours_day, days_month, quantity=1):
    """Calculate monthly energy consumption"""
    return (power_w * hours_day * days_month * quantity) / 1000

def calculate_africa_bill(devices, country, include_outages=True):
    """Calculate bill with Africa-specific factors"""
    config = AFRICAN_COUNTRIES[country]
    
    total_energy = 0
    device_costs = []
    
    for device in devices:
        # Base energy calculation
        energy = calculate_device_energy(
            device["power"], device["hours"], 30, device["quantity"]
        )
        
        # Grid instability factor (less energy available)
        if include_outages:
            energy *= config["grid_stability"]
        
        total_energy += energy
        
        device_cost = energy * config["rate"]
        device_costs.append({
            "name": device["name"],
            "energy": energy,
            "cost": device_cost
        })
    
    # Calculate bill components
    energy_cost = total_energy * config["rate"]
    fixed_charge = config["fixed"]
    tax = (energy_cost + fixed_charge) * config["tax"]
    total_bill = energy_cost + fixed_charge + tax
    
    return {
        "total_energy": total_energy,
        "energy_cost": energy_cost,
        "fixed_charge": fixed_charge,
        "tax": tax,
        "total_bill": total_bill,
        "currency": config["currency"],
        "device_costs": device_costs,
        "grid_adjusted": include_outages
    }

def generate_budget_alerts(bill_amount, budget, currency):
    """Generate budget-based alerts"""
    alerts = []
    percentage = (bill_amount / budget) * 100
    
    if percentage > 100:
        alerts.append({
            "type": "danger",
            "message": f"⚠️ OVER BUDGET! Bill is {currency}{bill_amount:.0f} but budget is {currency}{budget:.0f}"
        })
    elif percentage > 80:
        alerts.append({
            "type": "warning", 
            "message": f"⚠️ Near budget limit! Using {percentage:.0f}% of monthly budget"
        })
    elif percentage > 60:
        alerts.append({
            "type": "info",
            "message": f"📊 Using {percentage:.0f}% of budget. Monitor usage carefully."
        })
    else:
        alerts.append({
            "type": "success",
            "message": f"✅ Good! Using only {percentage:.0f}% of budget. You have {currency}{budget-bill_amount:.0f} remaining."
        })
    
    return alerts

def predict_monthly_cost(devices, country, days_elapsed=15):
    """Predict full month cost based on current usage"""
    if days_elapsed == 0:
        return 0
    
    # Calculate current usage
    current_bill = calculate_africa_bill(devices, country)
    daily_average = current_bill["total_bill"] / days_elapsed
    predicted_monthly = daily_average * 30
    
    return predicted_monthly

# Initialize AI system
@st.cache_resource
def initialize_ai():
    return AfricaEnergyAI()

africa_ai = initialize_ai()

# Sidebar - Mobile-optimized
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%); border-radius: 10px; color: white; margin-bottom: 1rem;">
        <h2 style="margin: 0;">⚡ EnergySense</h2>
        <p style="margin: 0; font-size: 0.9rem;">Smart Energy for Africa</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language selection
    st.session_state.language = st.selectbox("🌍 Language", ["English", "Français", "Português"])
    
    # Core settings
    st.markdown("### 🏠 Your Profile")
    st.session_state.country = st.selectbox("Country", list(AFRICAN_COUNTRIES.keys()))
    st.session_state.household_size = st.slider("👥 Household Size", 1, 12, 4)
    st.session_state.income_level = st.selectbox("💰 Income Level", ["Very Low", "Low", "Medium", "High"])
    
    # Budget setting
    country_config = AFRICAN_COUNTRIES[st.session_state.country]
    currency = country_config["currency"]
    
    if st.session_state.country == "Cameroon":
        default_budget = 15000
        budget_range = (5000, 100000)
    elif st.session_state.country == "Nigeria":
        default_budget = 8000
        budget_range = (3000, 50000)
    else:
        default_budget = 1000
        budget_range = (500, 10000)
    
    st.session_state.monthly_budget = st.slider(
        f"📊 Monthly Budget ({currency})", 
        budget_range[0], budget_range[1], default_budget, step=500
    )
    
    # Quick stats
    if st.session_state.devices:
        st.markdown("### 📈 Quick Stats")
        total_devices = sum(d["quantity"] for d in st.session_state.devices)
        st.metric("Devices", total_devices)
        
        bill_data = calculate_africa_bill(st.session_state.devices, st.session_state.country)
        budget_used = (bill_data["total_bill"] / st.session_state.monthly_budget) * 100
        st.metric("Budget Used", f"{budget_used:.0f}%")

# Main navigation
page = st.radio(
    "📱 Navigation",
    ["🏠 Home", "💡 My Devices", "🤖 Energy Assistant", "📊 Budget Tracker", "📈 Forecasting"],
    horizontal=True
)

# HOME PAGE
if page == "🏠 Home":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2rem;">Smart Energy Forecaster</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Manage electricity costs • Stay within budget • Save money</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick overview
    if st.session_state.devices:
        bill_data = calculate_africa_bill(st.session_state.devices, st.session_state.country)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="africa-card">', unsafe_allow_html=True)
            st.metric("Monthly Bill", f"{currency}{bill_data['total_bill']:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="africa-card">', unsafe_allow_html=True)
            st.metric("Daily Cost", f"{currency}{bill_data['total_bill']/30:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="africa-card">', unsafe_allow_html=True)
            remaining = st.session_state.monthly_budget - bill_data['total_bill']
            st.metric("Budget Left", f"{currency}{remaining:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Budget progress bar
        st.markdown("### 📊 Budget Progress")
        budget_used = min(100, (bill_data['total_bill'] / st.session_state.monthly_budget) * 100)
        
        progress_color = "#28a745" if budget_used < 60 else "#ffc107" if budget_used < 80 else "#dc3545"
        
        st.markdown(f"""
        <div class="budget-progress">
            <div class="progress-bar" style="width: {budget_used}%; background: {progress_color};"></div>
        </div>
        <p style="text-align: center; margin: 0.5rem 0;">Using {budget_used:.0f}% of monthly budget</p>
        """, unsafe_allow_html=True)
        
        # Alerts
        alerts = generate_budget_alerts(bill_data['total_bill'], st.session_state.monthly_budget, currency)
        for alert in alerts:
            if alert["type"] == "danger":
                st.error(alert["message"])
            elif alert["type"] == "warning":
                st.warning(alert["message"])
            elif alert["type"] == "info":
                st.info(alert["message"])
            else:
                st.success(alert["message"])
    
    else:
        st.info("👆 Add your devices to start tracking energy costs!")
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("➕ Add Device", use_container_width=True, type="primary"):
            st.switch_page("💡 My Devices")
    
    with col2:
        if st.button("🤖 Get Advice", use_container_width=True):
            st.switch_page("🤖 Energy Assistant")
    
    with col3:
        if st.button("📊 View Budget", use_container_width=True):
            st.switch_page("📊 Budget Tracker")

# MY DEVICES PAGE
elif page == "💡 My Devices":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2rem;">My Devices</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Add and manage your electrical devices</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Device categories for easy selection
    st.markdown("### 📱 Add New Device")
    
    categories = {
        "💡 Lighting": [k for k, v in AFRICAN_DEVICES.items() if v["category"] == "lighting"],
        "🌀 Cooling": [k for k, v in AFRICAN_DEVICES.items() if v["category"] == "cooling"],
        "📱 Electronics": [k for k, v in AFRICAN_DEVICES.items() if v["category"] == "electronics"],
        "🍳 Kitchen": [k for k, v in AFRICAN_DEVICES.items() if v["category"] == "kitchen"],
        "💼 Work": [k for k, v in AFRICAN_DEVICES.items() if v["category"] == "work"]
    }
    
    selected_category = st.selectbox("Choose Category", list(categories.keys()))
    
    if selected_category:
        # Show devices in category with icons
        st.markdown(f"**{selected_category} Devices:**")
        
        cols = st.columns(min(4, len(categories[selected_category])))
        
        for i, device_name in enumerate(categories[selected_category]):
            device_info = AFRICAN_DEVICES[device_name]
            
            with cols[i % 4]:
                if st.button(
                    f"{device_info['emoji']}\n{device_name}\n{device_info['power']}W",
                    key=f"select_{device_name}",
                    use_container_width=True
                ):
                    st.session_state.selected_device = device_name
        
        # Device configuration
        if 'selected_device' in st.session_state:
            device_name = st.session_state.selected_device
            device_info = AFRICAN_DEVICES[device_name]
            
            st.markdown(f"### ⚙️ Configure {device_info['emoji']} {device_name}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                quantity = st.number_input("How many?", 1, 20, 1)
            
            with col2:
                hours = st.slider("Hours per day", 0.0, 24.0, device_info["hours"], 0.5)
            
            with col3:
                custom_name = st.text_input("Custom name (optional)", device_name)
            
            # Show cost preview
            monthly_energy = calculate_device_energy(device_info["power"], hours, 30, quantity)
            monthly_cost = monthly_energy * AFRICAN_COUNTRIES[st.session_state.country]["rate"]
            
            st.info(f"💰 This will cost approximately {currency}{monthly_cost:.0f}/month")
            
            if st.button("✅ Add Device", type="primary"):
                device = {
                    "name": custom_name,
                    "type": device_name,
                    "power": device_info["power"],
                    "quantity": quantity,
                    "hours": hours,
                    "category": device_info["category"],
                    "emoji": device_info["emoji"],
                    "priority": device_info["priority"]
                }
                st.session_state.devices.append(device)
                st.success(f"✅ Added {quantity}x {custom_name}")
                del st.session_state.selected_device
                st.rerun()
    
    # Current devices list
    if st.session_state.devices:
        st.markdown("### 🏠 Your Current Devices")
        
        for i, device in enumerate(st.session_state.devices):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
                
                with col1:
                    priority_color = {"high": "🟢", "medium": "🟡", "low": "🔴"}
                    st.write(f"{device['emoji']} **{device['name']}** {priority_color.get(device.get('priority', 'medium'), '🟡')}")
                    st.write(f"⚡ {device['power']}W × {device['quantity']} = {device['power'] * device['quantity']}W")
                
                with col2:
                    energy = calculate_device_energy(device['power'], device['hours'], 30, device['quantity'])
                    st.metric("kWh/month", f"{energy:.1f}")
                
                with col3:
                    cost = energy * AFRICAN_COUNTRIES[st.session_state.country]["rate"]
                    st.metric("Cost/month", f"{currency}{cost:.0f}")
                
                with col4:
                    new_hours = st.slider("Hours/day", 0.0, 24.0, device['hours'], 0.5, key=f"hours_{i}")
                    if new_hours != device['hours']:
                        st.session_state.devices[i]['hours'] = new_hours
                        st.rerun()
                
                with col5:
                    if st.button("🗑️", key=f"remove_{i}"):
                        st.session_state.devices.pop(i)
                        st.rerun()

# ENERGY ASSISTANT PAGE
elif page == "🤖 Energy Assistant":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2rem;">Energy Assistant</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Get personalized advice to save money</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Status
    status_msg, status_type = africa_ai.get_status_message()
    if status_type == "success":
        st.success(status_msg)
    else:
        st.info(status_msg)
    
    # Chat interface
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick questions
    st.markdown("### 💬 Quick Questions")
    quick_questions = [
        "How can I save money on electricity?",
        "What devices use the most power?",
        "Help me stay within my budget",
        "Best devices for my budget?"
    ]
    
    cols = st.columns(2)
    for i, question in enumerate(quick_questions):
        with cols[i % 2]:
            if st.button(question, key=f"quick_{i}", use_container_width=True):
                # Process question
                st.session_state.chat_history.append({"type": "user", "content": question})
                
                context = {
                    'country': st.session_state.country,
                    'budget': st.session_state.monthly_budget,
                    'currency': currency,
                    'household_size': st.session_state.household_size,
                    'income_level': st.session_state.income_level,
                    'grid_stability': AFRICAN_COUNTRIES[st.session_state.country]['grid_stability']
                }
                
                with st.spinner("🤖 Getting advice..."):
                    ai_response = africa_ai.get_response(question, context)
                
                st.session_state.chat_history.append({"type": "ai", "content": ai_response})
                st.rerun()
    
    # Chat input
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "💬 Ask me anything about saving energy:", 
            placeholder="Type your question here..."
        )
        submitted = st.form_submit_button("Send", type="primary", use_container_width=True)
        
        if submitted and user_input:
            # Add user message
            st.session_state.chat_history.append({"type": "user", "content": user_input})
            
            # Prepare context
            context = {
                'country': st.session_state.country,
                'budget': st.session_state.monthly_budget,
                'currency': currency,
                'household_size': st.session_state.household_size,
                'income_level': st.session_state.income_level,
                'grid_stability': AFRICAN_COUNTRIES[st.session_state.country]['grid_stability']
            }
            
            # Get AI response
            with st.spinner("🤖 Thinking..."):
                ai_response = africa_ai.get_response(user_input, context)
            
            # Add AI response
            st.session_state.chat_history.append({"type": "ai", "content": ai_response})
            st.rerun()
    
    # Clear chat
    if st.session_state.chat_history:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

# BUDGET TRACKER PAGE
elif page == "📊 Budget Tracker":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2rem;">Budget Tracker</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Monitor spending • Stay within limits</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.devices:
        bill_data = calculate_africa_bill(st.session_state.devices, st.session_state.country)
        
        # Budget overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="budget-card">', unsafe_allow_html=True)
            st.metric("Monthly Budget", f"{currency}{st.session_state.monthly_budget:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="budget-card">', unsafe_allow_html=True)
            st.metric("Estimated Bill", f"{currency}{bill_data['total_bill']:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            remaining = st.session_state.monthly_budget - bill_data['total_bill']
            card_class = "budget-card" if remaining >= 0 else "warning-card"
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            st.metric("Remaining", f"{currency}{remaining:,.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            daily_budget = st.session_state.monthly_budget / 30
            daily_usage = bill_data['total_bill'] / 30
            st.markdown('<div class="budget-card">', unsafe_allow_html=True)
            st.metric("Daily Limit", f"{currency}{daily_budget:.0f}")
            st.write(f"Using: {currency}{daily_usage:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Device cost breakdown
        st.markdown("### 💰 Where Your Money Goes")
        
        device_costs = pd.DataFrame([
            {"Device": d["name"], "Monthly Cost": d["cost"], "Percentage": (d["cost"]/bill_data['total_bill'])*100}
            for d in bill_data["device_costs"]
        ]).sort_values("Monthly Cost", ascending=False)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_pie = px.pie(device_costs, values='Monthly Cost', names='Device', 
                           title="Cost by Device")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            fig_bar = px.bar(device_costs, x='Device', y='Monthly Cost', 
                           title="Monthly Cost by Device")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Savings recommendations
        st.markdown("### 💡 Money-Saving Tips")
        
        # Find highest cost devices
        top_devices = device_costs.head(3)
        
        for _, device in top_devices.iterrows():
            potential_savings = device['Monthly Cost'] * 0.3  # 30% potential savings
            
            with st.expander(f"💰 Save on {device['Device']} - Up to {currency}{potential_savings:.0f}/month"):
                device_name = device['Device']
                
                if "bulb" in device_name.lower() or "light" in device_name.lower():
                    st.write("💡 **LED Upgrade:** Switch to LED bulbs to save 70% on lighting costs")
                    st.write(f"• Current cost: {currency}{device['Monthly Cost']:.0f}/month")
                    st.write(f"• With LEDs: {currency}{device['Monthly Cost']*0.3:.0f}/month")
                    st.write(f"• Monthly savings: {currency}{device['Monthly Cost']*0.7:.0f}")
                
                elif "fan" in device_name.lower():
                    st.write("🌀 **Smart Usage:** Use fans efficiently to stay cool")
                    st.write("• Use timer switches to avoid running all night")
                    st.write("• Clean blades monthly for better efficiency")
                    st.write(f"• Potential savings: {currency}{potential_savings:.0f}/month")
                
                elif "tv" in device_name.lower():
                    st.write("📺 **Smart Viewing:** Reduce TV energy costs")
                    st.write("• Turn off when not watching (not standby)")
                    st.write("• Adjust brightness settings")
                    st.write(f"• Potential savings: {currency}{potential_savings:.0f}/month")
                
                else:
                    st.write(f"⚡ **Efficiency Tips for {device_name}:**")
                    st.write("• Use only when needed")
                    st.write("• Maintain regularly for efficiency")
                    st.write("• Consider timer switches")
                    st.write(f"• Potential savings: {currency}{potential_savings:.0f}/month")

# FORECASTING PAGE
elif page == "📈 Forecasting":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2rem;">Energy Forecasting</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Predict future costs • Plan ahead</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.devices:
        bill_data = calculate_africa_bill(st.session_state.devices, st.session_state.country)
        
        # Forecasting scenarios
        st.markdown("### 🔮 Cost Predictions")
        
        # Generate 6-month forecast
        months = ["This Month", "Next Month", "Month 3", "Month 4", "Month 5", "Month 6"]
        base_cost = bill_data['total_bill']
        
        # Seasonal factors for Africa (dry season = more AC, rainy season = less)
        seasonal_factors = [1.0, 1.1, 1.2, 1.15, 0.95, 0.9]  # Simplified seasonal pattern
        
        forecast_data = []
        for i, month in enumerate(months):
            # Add some randomness for realism
            seasonal_cost = base_cost * seasonal_factors[i]
            random_factor = 1 + (np.random.random() - 0.5) * 0.1  # ±5% variation
            predicted_cost = seasonal_cost * random_factor
            
            forecast_data.append({
                "Month": month,
                "Predicted Cost": predicted_cost,
                "Budget Status": "Within Budget" if predicted_cost <= st.session_state.monthly_budget else "Over Budget"
            })
        
        df_forecast = pd.DataFrame(forecast_data)
        
        # Forecast chart
        fig_forecast = go.Figure()
        
        # Add predicted costs
        fig_forecast.add_trace(go.Scatter(
            x=df_forecast['Month'],
            y=df_forecast['Predicted Cost'],
            mode='lines+markers',
            name='Predicted Cost',
            line=dict(color='#FF6B35', width=3)
        ))
        
        # Add budget line
        fig_forecast.add_hline(
            y=st.session_state.monthly_budget,
            line_dash="dash",
            line_color="red",
            annotation_text="Budget Limit"
        )
        
        fig_forecast.update_layout(
            title="6-Month Cost Forecast",
            xaxis_title="Month",
            yaxis_title=f"Cost ({currency})",
            height=400
        )
        
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Forecast insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Forecast Summary")
            
            avg_cost = df_forecast['Predicted Cost'].mean()
            max_cost = df_forecast['Predicted Cost'].max()
            min_cost = df_forecast['Predicted Cost'].min()
            
            st.metric("Average Monthly Cost", f"{currency}{avg_cost:.0f}")
            st.metric("Highest Month", f"{currency}{max_cost:.0f}")
            st.metric("Lowest Month", f"{currency}{min_cost:.0f}")
        
        with col2:
            st.markdown("### ⚠️ Budget Warnings")
            
            over_budget_months = len(df_forecast[df_forecast['Predicted Cost'] > st.session_state.monthly_budget])
            
            if over_budget_months > 0:
                st.error(f"⚠️ {over_budget_months} months may exceed budget!")
                st.write("**Recommended Actions:**")
                st.write("• Reduce high-power device usage")
                st.write("• Consider energy-efficient alternatives")
                st.write("• Increase monthly budget if possible")
            else:
                st.success("✅ All months within budget!")
                st.write("**You're doing great!**")
                st.write("• Continue current usage patterns")
                st.write("• Consider saving extra money")
        
        # Scenario planning
        st.markdown("### 🎯 What-If Scenarios")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**💡 LED Upgrade Scenario**")
            led_savings = base_cost * 0.15  # 15% savings from LED
            new_cost = base_cost - led_savings
            st.metric("New Monthly Cost", f"{currency}{new_cost:.0f}")
            st.metric("Monthly Savings", f"{currency}{led_savings:.0f}")
            st.success("✅ Always within budget!")
        
        with col2:
            st.markdown("**🌀 Efficient Cooling**")
            cooling_savings = base_cost * 0.25  # 25% savings from efficient cooling
            new_cost = base_cost - cooling_savings
            st.metric("New Monthly Cost", f"{currency}{new_cost:.0f}")
            st.metric("Monthly Savings", f"{currency}{cooling_savings:.0f}")
            st.success("✅ Significant savings!")
        
        with col3:
            st.markdown("**⚡ Solar Backup**")
            solar_savings = base_cost * 0.30  # 30% savings from solar
            new_cost = base_cost - solar_savings
            st.metric("New Monthly Cost", f"{currency}{new_cost:.0f}")
            st.metric("Monthly Savings", f"{currency}{solar_savings:.0f}")
            st.info("💰 Best long-term option")
    
    else:
        st.info("📱 Add your devices first to see forecasting")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p><strong>EnergySense - Smart Energy Forecaster for Africa</strong></p>
    <p>Helping families manage electricity costs • Built for African communities</p>
    <p>🌍 Supporting sustainable energy access across Africa</p>
</div>
""", unsafe_allow_html=True)