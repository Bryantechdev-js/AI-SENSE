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
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# African Countries Database
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
    "LED Bulb": {"power": 9, "hours": 6.0, "category": "lighting", "emoji": "💡", "priority": "high", "cost_usd": 3},
    "Table Fan": {"power": 45, "hours": 8.0, "category": "cooling", "emoji": "🌀", "priority": "high", "cost_usd": 25},
    "Mobile Phone Charger": {"power": 5, "hours": 3.0, "category": "electronics", "emoji": "📱", "priority": "high", "cost_usd": 10},
    "Radio": {"power": 15, "hours": 4.0, "category": "entertainment", "emoji": "📻", "priority": "high", "cost_usd": 20},
    "Small TV": {"power": 80, "hours": 4.0, "category": "entertainment", "emoji": "📺", "priority": "medium", "cost_usd": 150},
    "Small Refrigerator": {"power": 120, "hours": 24.0, "category": "kitchen", "emoji": "🧊", "priority": "medium", "cost_usd": 200},
    "Electric Kettle": {"power": 1500, "hours": 0.3, "category": "kitchen", "emoji": "☕", "priority": "medium", "cost_usd": 25},
    "Laptop": {"power": 65, "hours": 6.0, "category": "work", "emoji": "💻", "priority": "medium", "cost_usd": 400},
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
    st.session_state.monthly_budget = 15000
if 'household_size' not in st.session_state:
    st.session_state.household_size = 4
if 'income_level' not in st.session_state:
    st.session_state.income_level = "Low"

# Production-ready AI Integration
class AfricaEnergyAI:
    def __init__(self):
        self.api_key = self._get_api_key()
        self.enabled = bool(self.api_key)
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"
        
    def _get_api_key(self):
        """Safely get API key from multiple sources"""
        try:
            # Try Streamlit secrets first
            if hasattr(st, 'secrets') and "OPENROUTER_API_KEY" in st.secrets:
                key = st.secrets["OPENROUTER_API_KEY"]
                if key and key != "your-openrouter-api-key-here":
                    return key
            # Try environment variable
            key = os.getenv("OPENROUTER_API_KEY", "")
            if key and key != "your-openrouter-api-key-here":
                return key
            return ""
        except:
            return ""
    
    def get_response(self, user_message, context):
        """Get AI response with comprehensive error handling"""
        if not self.enabled:
            return self.get_fallback_response(user_message, context)
        
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://ai-sense-43djhny8ihhq2rvudnp974.streamlit.app/",
                "X-Title": "EnergySense AI"
            }
            
            payload = {
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": f"You are an energy advisor for African households in {context['country']}. Provide practical advice in simple language under 100 words."},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 200,
                "temperature": 0.7
            }
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and result['choices']:
                    return result['choices'][0]['message']['content']
            
            st.toast("🤖 AI temporarily unavailable, using smart responses", icon="ℹ️")
            
        except Exception as e:
            st.toast("🤖 AI offline, using smart responses", icon="ℹ️")
        
        return self.get_fallback_response(user_message, context)
    
    def get_fallback_response(self, user_message, context):
        """Enhanced intelligent fallback responses"""
        budget = context['budget']
        currency = context['currency']
        country = context['country']
        msg_lower = user_message.lower()
        
        if any(word in msg_lower for word in ["save", "reduce", "lower", "cut"]):
            return f"""💡 **Top Energy Savings for {country}:**

**Immediate Actions:**
• Switch to LED bulbs → Save 70% on lighting
• Use fans instead of AC → Save {currency}2000+/month
• Unplug devices when not using → Save 10-15%

**Budget Impact:** These changes can save {currency}{int(budget*0.3)}/month!"""

        elif any(word in msg_lower for word in ["budget", "money", "cost"]):
            daily_budget = budget // 30
            return f"""💰 **Smart Budget Management:**

**Your Budget Breakdown:**
• Daily limit: {currency}{daily_budget}
• Weekly target: {currency}{budget//4}

**Priority Spending:**
1. Essential lighting: {currency}{int(budget*0.25)}
2. Phone/communication: {currency}{int(budget*0.15)}
3. Cooling/comfort: {currency}{int(budget*0.35)}"""

        else:
            return f"""🏠 **Energy Assistant for {country}**

I help families manage electricity costs effectively!

**I can help you with:**
• Reducing monthly bills
• Choosing efficient devices
• Managing tight budgets

**Your Profile:**
• Budget: {currency}{budget}/month
• Country: {country}
• Household: {context['household_size']} people

**Ask me:** "How can I save money?" or "What devices should I avoid?" """

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

def calculate_africa_bill(devices, country):
    """Calculate bill with Africa-specific factors"""
    config = AFRICAN_COUNTRIES[country]
    
    total_energy = 0
    device_costs = []
    
    for device in devices:
        energy = calculate_device_energy(device["power"], device["hours"], 30, device["quantity"])
        energy *= config["grid_stability"]  # Grid instability factor
        total_energy += energy
        
        device_cost = energy * config["rate"]
        device_costs.append({"name": device["name"], "energy": energy, "cost": device_cost})
    
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
        "device_costs": device_costs
    }

# Initialize AI system
@st.cache_resource
def initialize_ai():
    return AfricaEnergyAI()

africa_ai = initialize_ai()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%); border-radius: 10px; color: white; margin-bottom: 1rem;">
        <h2 style="margin: 0;">⚡ EnergySense</h2>
        <p style="margin: 0; font-size: 0.9rem;">Smart Energy for Africa</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.session_state.country = st.selectbox("Country", list(AFRICAN_COUNTRIES.keys()))
    st.session_state.household_size = st.slider("👥 Household Size", 1, 12, 4)
    st.session_state.income_level = st.selectbox("💰 Income Level", ["Very Low", "Low", "Medium", "High"])
    
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

# Main navigation
page = st.radio(
    "📱 Navigation",
    ["🏠 Home", "💡 My Devices", "🤖 Energy Assistant", "📊 Budget Tracker"],
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
    else:
        st.info("👆 Add your devices to start tracking energy costs!")

# MY DEVICES PAGE
elif page == "💡 My Devices":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2rem;">My Devices</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Add and manage your electrical devices</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📱 Add New Device")
    
    device_name = st.selectbox("Choose Device", list(AFRICAN_DEVICES.keys()))
    
    if device_name:
        device_info = AFRICAN_DEVICES[device_name]
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            quantity = st.number_input("How many?", 1, 20, 1)
        
        with col2:
            hours = st.slider("Hours per day", 0.0, 24.0, device_info["hours"], 0.5)
        
        with col3:
            custom_name = st.text_input("Custom name (optional)", device_name)
        
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
                "emoji": device_info["emoji"]
            }
            st.session_state.devices.append(device)
            st.success(f"✅ Added {quantity}x {custom_name}")
            st.rerun()
    
    if st.session_state.devices:
        st.markdown("### 🏠 Your Current Devices")
        
        for i, device in enumerate(st.session_state.devices):
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                st.write(f"{device['emoji']} **{device['name']}**")
                st.write(f"⚡ {device['power']}W × {device['quantity']}")
            
            with col2:
                energy = calculate_device_energy(device['power'], device['hours'], 30, device['quantity'])
                st.metric("kWh/month", f"{energy:.1f}")
            
            with col3:
                cost = energy * AFRICAN_COUNTRIES[st.session_state.country]["rate"]
                st.metric("Cost/month", f"{currency}{cost:.0f}")
            
            with col4:
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
    
    status_msg, status_type = africa_ai.get_status_message()
    if status_type == "success":
        st.success(status_msg)
    else:
        st.info(status_msg)
    
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">{message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
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
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Ask me anything about saving energy:", placeholder="Type your question here...")
        submitted = st.form_submit_button("Send", type="primary", use_container_width=True)
        
        if submitted and user_input:
            st.session_state.chat_history.append({"type": "user", "content": user_input})
            
            context = {
                'country': st.session_state.country,
                'budget': st.session_state.monthly_budget,
                'currency': currency,
                'household_size': st.session_state.household_size,
                'income_level': st.session_state.income_level,
                'grid_stability': AFRICAN_COUNTRIES[st.session_state.country]['grid_stability']
            }
            
            with st.spinner("🤖 Thinking..."):
                ai_response = africa_ai.get_response(user_input, context)
            
            st.session_state.chat_history.append({"type": "ai", "content": ai_response})
            st.rerun()
    
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
        
        st.markdown("### 💰 Where Your Money Goes")
        
        device_costs = pd.DataFrame([
            {"Device": d["name"], "Monthly Cost": d["cost"]}
            for d in bill_data["device_costs"]
        ]).sort_values("Monthly Cost", ascending=False)
        
        if not device_costs.empty:
            fig_pie = px.pie(device_costs, values='Monthly Cost', names='Device', title="Cost by Device")
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("📱 Add your devices first to see budget tracking")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #666;">
    <p><strong>EnergySense - Smart Energy Forecaster for Africa</strong></p>
    <p>Helping families manage electricity costs • Built for African communities</p>
    <p>🌍 Supporting sustainable energy access across Africa</p>
</div>
""", unsafe_allow_html=True)