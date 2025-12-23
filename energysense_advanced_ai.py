"""
EnergySense AI - Advanced Predictive AI System
OpenRouter Integration + Comprehensive Energy Intelligence
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import random
import time
import numpy as np
import os
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Optional
import asyncio
import base64
from io import BytesIO

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="EnergySense AI - Advanced Predictive System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced CSS styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .ai-chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        min-height: 500px;
        max-height: 700px;
        overflow-y: auto;
        border: 1px solid #e0e0e0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        margin-left: 15%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        animation: slideInRight 0.3s ease;
    }
    
    .ai-message {
        background: white;
        color: #333;
        padding: 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        margin-right: 15%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #667eea;
        animation: slideInLeft 0.3s ease;
    }
    
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes slideInLeft {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .ai-thinking {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        margin-right: 15%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 5px solid #ffa500;
    }
    
    .typing-dots {
        display: inline-block;
        animation: typing 1.5s infinite;
    }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
    
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        text-align: center;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #4ECDC4;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .ai-capability {
        background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# OpenRouter Configuration
def setup_openrouter_client():
    """Setup OpenRouter client"""
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        return client
    return None

# African Countries Database
AFRICAN_COUNTRIES = {
    "Nigeria": {"currency": "₦", "rate": 68.0, "fixed": 1000, "tax": 0.075, "peak_rate": 85.0, "climate": "tropical"},
    "South Africa": {"currency": "R", "rate": 1.85, "fixed": 150, "tax": 0.15, "peak_rate": 2.50, "climate": "temperate"},
    "Egypt": {"currency": "£E", "rate": 1.45, "fixed": 50, "tax": 0.10, "peak_rate": 2.20, "climate": "arid"},
    "Kenya": {"currency": "KSh", "rate": 24.0, "fixed": 200, "tax": 0.16, "peak_rate": 35.0, "climate": "tropical"},
    "Ghana": {"currency": "₵", "rate": 1.20, "fixed": 25, "tax": 0.125, "peak_rate": 1.80, "climate": "tropical"},
    "Morocco": {"currency": "DH", "rate": 1.15, "fixed": 30, "tax": 0.20, "peak_rate": 1.65, "climate": "mediterranean"},
    "Ethiopia": {"currency": "Br", "rate": 6.50, "fixed": 15, "tax": 0.15, "peak_rate": 9.75, "climate": "highland"},
    "Tanzania": {"currency": "TSh", "rate": 280, "fixed": 5000, "tax": 0.18, "peak_rate": 420, "climate": "tropical"},
    "Uganda": {"currency": "USh", "rate": 420, "fixed": 8000, "tax": 0.18, "peak_rate": 630, "climate": "tropical"},
    "Algeria": {"currency": "DA", "rate": 18.5, "fixed": 200, "tax": 0.19, "peak_rate": 27.8, "climate": "arid"},
    "Cameroon": {"currency": "Xaf", "rate": 18.5, "fixed": 200, "tax": 0.19, "peak_rate": 27.8, "climate": "arid"},
}

# Enhanced Device Database
DEVICE_SPECS = {
    "Air Conditioner": {"power": 1200, "hours": 8.0, "category": "cooling", "emoji": "❄️", "efficiency": 0.85, "lifespan": 10},
    "Television": {"power": 120, "hours": 6.0, "category": "entertainment", "emoji": "📺", "efficiency": 0.90, "lifespan": 8},
    "Refrigerator": {"power": 150, "hours": 24.0, "category": "kitchen", "emoji": "🧊", "efficiency": 0.88, "lifespan": 12},
    "Washing Machine": {"power": 500, "hours": 1.0, "category": "laundry", "emoji": "👕", "efficiency": 0.82, "lifespan": 10},
    "Microwave": {"power": 1200, "hours": 0.5, "category": "kitchen", "emoji": "🔥", "efficiency": 0.75, "lifespan": 8},
    "LED Bulb": {"power": 10, "hours": 6.0, "category": "lighting", "emoji": "💡", "efficiency": 0.95, "lifespan": 15},
    "Ceiling Fan": {"power": 75, "hours": 12.0, "category": "cooling", "emoji": "🌀", "efficiency": 0.85, "lifespan": 12},
    "Water Heater": {"power": 2000, "hours": 2.0, "category": "heating", "emoji": "🚿", "efficiency": 0.78, "lifespan": 8},
    "Electric Kettle": {"power": 1500, "hours": 0.25, "category": "kitchen", "emoji": "☕", "efficiency": 0.85, "lifespan": 5},
    "Laptop": {"power": 65, "hours": 8.0, "category": "electronics", "emoji": "💻", "efficiency": 0.88, "lifespan": 5},
    "Desktop Computer": {"power": 300, "hours": 8.0, "category": "electronics", "emoji": "🖥️", "efficiency": 0.75, "lifespan": 6},
    "Gaming Console": {"power": 150, "hours": 4.0, "category": "entertainment", "emoji": "🎮", "efficiency": 0.70, "lifespan": 7},
    "Iron": {"power": 1000, "hours": 0.5, "category": "laundry", "emoji": "👔", "efficiency": 0.80, "lifespan": 8},
    "Hair Dryer": {"power": 1800, "hours": 0.25, "category": "personal", "emoji": "💇", "efficiency": 0.75, "lifespan": 5},
    "Vacuum Cleaner": {"power": 1400, "hours": 0.5, "category": "cleaning", "emoji": "🧹", "efficiency": 0.70, "lifespan": 8}
}

# Initialize session state
if 'devices' not in st.session_state:
    st.session_state.devices = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'country' not in st.session_state:
    st.session_state.country = "Nigeria"
if 'ai_client' not in st.session_state:
    st.session_state.ai_client = setup_openrouter_client()
if 'ai_analysis' not in st.session_state:
    st.session_state.ai_analysis = {}

# Advanced AI Functions
class EnergyAI:
    def __init__(self, client):
        self.client = client
        self.model = os.getenv('AI_MODEL', 'openai/gpt-4o-mini')
        self.site_url = os.getenv('SITE_URL', 'https://energysense-ai.com')
        self.site_name = os.getenv('SITE_NAME', 'EnergySense AI')
    
    def get_comprehensive_analysis(self, devices, country, temperature, user_query=""):
        """Get comprehensive AI analysis of energy consumption"""
        if not self.client:
            return "⚠️ AI service not available. Please configure OpenRouter API key."
        
        # Prepare detailed context
        total_devices = len(devices)
        total_power = sum(d["power"] * d["quantity"] for d in devices)
        
        device_breakdown = []
        for device in devices:
            energy = (device["power"] * device["hours"] * 30 * device["quantity"]) / 1000
            device_breakdown.append(f"- {device['name']}: {device['power']}W × {device['quantity']} = {energy:.1f} kWh/month")
        
        country_info = AFRICAN_COUNTRIES[country]
        
        context = f"""
        ENERGY CONSUMPTION ANALYSIS REQUEST
        
        Location: {country} ({country_info['climate']} climate)
        Currency: {country_info['currency']}
        Electricity Rate: {country_info['rate']} {country_info['currency']}/kWh
        Temperature: {temperature}°C
        
        HOUSEHOLD DEVICES ({total_devices} total):
        {chr(10).join(device_breakdown)}
        
        Total Power Capacity: {total_power}W
        
        USER QUERY: {user_query if user_query else "Provide comprehensive energy analysis and recommendations"}
        """
        
        system_prompt = """You are an expert energy consultant specializing in African energy markets. 
        Provide detailed, actionable analysis covering:
        
        1. ENERGY EFFICIENCY ASSESSMENT
        2. COST OPTIMIZATION STRATEGIES  
        3. SEASONAL PLANNING ADVICE
        4. DEVICE UPGRADE RECOMMENDATIONS
        5. BEHAVIORAL CHANGE SUGGESTIONS
        6. RENEWABLE ENERGY OPPORTUNITIES
        7. LOAD MANAGEMENT STRATEGIES
        8. CARBON FOOTPRINT REDUCTION
        
        Be specific, practical, and consider African energy challenges like grid instability, high costs, and climate factors.
        Provide numerical estimates where possible."""
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                max_tokens=int(os.getenv('MAX_TOKENS', 2000)),
                temperature=float(os.getenv('TEMPERATURE', 0.7))
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            return f"⚠️ AI analysis temporarily unavailable: {str(e)}"
    
    def predict_future_consumption(self, devices, country, months=12):
        """Predict future energy consumption with AI"""
        if not self.client:
            return {"error": "AI service not available"}
        
        current_energy = sum((d["power"] * d["hours"] * 30 * d["quantity"]) / 1000 for d in devices)
        
        context = f"""
        ENERGY FORECASTING REQUEST
        
        Current monthly consumption: {current_energy:.1f} kWh
        Location: {country}
        Devices: {len(devices)} total
        Forecast period: {months} months
        
        Provide month-by-month predictions considering:
        - Seasonal variations in {country}
        - Device aging and efficiency degradation
        - Typical usage pattern changes
        - Economic factors affecting consumption
        
        Return predictions as JSON format:
        {{"predictions": [{{"month": 1, "energy_kwh": 450, "confidence": 0.85, "factors": ["seasonal_increase"]}}, ...]}}
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an energy forecasting AI. Provide accurate predictions in JSON format."},
                    {"role": "user", "content": context}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            response = completion.choices[0].message.content
            # Try to extract JSON from response
            try:
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            
            return {"error": "Could not parse prediction data", "raw_response": response}
        
        except Exception as e:
            return {"error": f"Prediction failed: {str(e)}"}
    
    def optimize_energy_usage(self, devices, country, target_reduction=20):
        """AI-powered energy optimization recommendations"""
        if not self.client:
            return "AI optimization not available"
        
        context = f"""
        ENERGY OPTIMIZATION REQUEST
        
        Target: Reduce consumption by {target_reduction}%
        Country: {country}
        
        Current devices and usage:
        {json.dumps([{
            'name': d['name'], 
            'power': d['power'], 
            'hours': d['hours'], 
            'quantity': d['quantity']
        } for d in devices], indent=2)}
        
        Provide specific optimization strategies with:
        1. Device-specific recommendations
        2. Usage pattern changes
        3. Technology upgrades
        4. Behavioral modifications
        5. Expected savings for each recommendation
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an energy optimization expert. Provide actionable, specific recommendations."},
                    {"role": "user", "content": context}
                ],
                max_tokens=1500,
                temperature=0.5
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            return f"Optimization analysis failed: {str(e)}"
    
    def analyze_energy_anomalies(self, consumption_data):
        """Detect and explain energy consumption anomalies"""
        if not self.client:
            return "Anomaly detection not available"
        
        context = f"""
        ENERGY ANOMALY DETECTION
        
        Consumption data: {json.dumps(consumption_data)}
        
        Analyze for:
        1. Unusual consumption spikes
        2. Efficiency degradation patterns
        3. Seasonal anomalies
        4. Device malfunction indicators
        5. Billing discrepancies
        
        Provide explanations and corrective actions.
        """
        
        try:
            completion = self.client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": self.site_url,
                    "X-Title": self.site_name,
                },
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an energy anomaly detection specialist."},
                    {"role": "user", "content": context}
                ],
                max_tokens=1000,
                temperature=0.4
            )
            
            return completion.choices[0].message.content
        
        except Exception as e:
            return f"Anomaly analysis failed: {str(e)}"

# Helper functions
def calculate_energy(power, hours, days, quantity):
    return (power * hours * days * quantity) / 1000

def calculate_comprehensive_bill(devices, country, temperature=28):
    config = AFRICAN_COUNTRIES[country]
    total_energy = 0
    device_breakdown = []
    
    for device in devices:
        base_energy = calculate_energy(device["power"], device["hours"], 30, device["quantity"])
        # Temperature adjustment
        adjusted_energy = base_energy * (1 + 0.03 * (temperature - 22) / 22)
        total_energy += adjusted_energy
        
        device_breakdown.append({
            "name": device["name"],
            "energy": adjusted_energy,
            "cost": adjusted_energy * config["rate"]
        })
    
    energy_cost = total_energy * config["rate"]
    subtotal = energy_cost + config["fixed"]
    tax = subtotal * config["tax"]
    total_bill = subtotal + tax
    
    return {
        "total_energy": total_energy,
        "energy_cost": energy_cost,
        "fixed_charge": config["fixed"],
        "tax": tax,
        "total_bill": total_bill,
        "currency": config["currency"],
        "device_breakdown": device_breakdown
    }

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="color: #1f77b4; font-size: 1.8rem; margin: 0;">⚡ EnergySense AI</h1>
        <p style="color: #666; font-size: 0.9rem; margin: 0;">Advanced Predictive System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # AI Status
    if st.session_state.ai_client:
        st.success("🤖 Advanced AI: Active")
        st.info(f"Model: {os.getenv('AI_MODEL', 'gpt-4o-mini')}")
    else:
        st.error("🤖 AI: Not Configured")
        with st.expander("🔑 Setup Instructions"):
            st.markdown("""
            1. Get OpenRouter API key from https://openrouter.ai
            2. Copy `.env.example` to `.env`
            3. Add your API key:
            ```
            OPENROUTER_API_KEY=your_key_here
            ```
            4. Restart application
            """)
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Device Manager", "🤖 Advanced AI Assistant", "📊 Predictive Analytics", "🔮 Future Insights"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Settings
    st.markdown("### 🌍 Settings")
    st.session_state.country = st.selectbox("Country", list(AFRICAN_COUNTRIES.keys()))
    temperature = st.slider("🌡️ Temperature (°C)", 15.0, 40.0, 28.0)

# Initialize AI
energy_ai = EnergyAI(st.session_state.ai_client)

# Main application
page_name = page.split(" ", 1)[1]

if page_name == "Device Manager":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🏠 Smart Device Manager</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">AI-Powered Device Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick device addition
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        device_type = st.selectbox("Device Type", list(DEVICE_SPECS.keys()))
    with col2:
        quantity = st.number_input("Quantity", 1, 10, 1)
    with col3:
        hours = st.slider("Hours/Day", 0.0, 24.0, DEVICE_SPECS[device_type]["hours"], 0.5)
    with col4:
        if st.button("➕ Add Device", type="primary"):
            device = {
                "name": f"{device_type} #{len(st.session_state.devices)+1}",
                "type": device_type,
                "power": DEVICE_SPECS[device_type]["power"],
                "quantity": quantity,
                "hours": hours,
                "days": 30,
                "category": DEVICE_SPECS[device_type]["category"],
                "emoji": DEVICE_SPECS[device_type]["emoji"],
                "efficiency": DEVICE_SPECS[device_type]["efficiency"],
                "lifespan": DEVICE_SPECS[device_type]["lifespan"]
            }
            st.session_state.devices.append(device)
            st.success(f"✅ Added {quantity}x {device_type}")
            st.rerun()
    
    # Device management interface
    if st.session_state.devices:
        st.subheader("📱 Your Smart Home Devices")
        
        # AI-powered device insights
        if st.session_state.ai_client:
            with st.expander("🤖 AI Device Insights", expanded=False):
                if st.button("🔍 Analyze My Devices"):
                    with st.spinner("AI analyzing your devices..."):
                        analysis = energy_ai.get_comprehensive_analysis(
                            st.session_state.devices, 
                            st.session_state.country, 
                            temperature,
                            "Analyze my current device setup and provide optimization recommendations"
                        )
                        st.markdown(f"**AI Analysis:**\n\n{analysis}")
        
        # Device list with advanced features
        for i, device in enumerate(st.session_state.devices):
            with st.container():
                col1, col2, col3, col4, col5, col6 = st.columns([3, 1, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"{device['emoji']} **{device['name']}** (×{device['quantity']})")
                    efficiency_color = "🟢" if device['efficiency'] > 0.85 else "🟡" if device['efficiency'] > 0.75 else "🔴"
                    st.write(f"⚡ {device['power']}W • {efficiency_color} {device['efficiency']*100:.0f}% efficient")
                
                with col2:
                    energy = calculate_energy(device['power'], device['hours'], 30, device['quantity'])
                    st.metric("kWh/month", f"{energy:.1f}")
                
                with col3:
                    bill = calculate_comprehensive_bill([device], st.session_state.country, temperature)
                    st.metric("Cost/month", f"{bill['currency']}{bill['total_bill']:.0f}")
                
                with col4:
                    # Age tracking for efficiency degradation
                    age = st.number_input("Age (years)", 0, 20, 0, key=f"age_{i}")
                    degradation = max(0, 1 - (age * 0.02))  # 2% per year
                    if age > 0:
                        st.write(f"Efficiency: {device['efficiency']*degradation*100:.0f}%")
                
                with col5:
                    new_hours = st.slider("Hours/day", 0.0, 24.0, device['hours'], 0.5, key=f"hours_{i}")
                    if new_hours != device['hours']:
                        st.session_state.devices[i]['hours'] = new_hours
                        st.rerun()
                
                with col6:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.devices.pop(i)
                        st.rerun()
        
        # Comprehensive analysis
        st.markdown("---")
        bill_data = calculate_comprehensive_bill(st.session_state.devices, st.session_state.country, temperature)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Energy", f"{bill_data['total_energy']:.1f} kWh")
        with col2:
            st.metric("Monthly Bill", f"{bill_data['currency']}{bill_data['total_bill']:.2f}")
        with col3:
            carbon_footprint = bill_data['total_energy'] * 0.85  # kg CO2 per kWh
            st.metric("Carbon Footprint", f"{carbon_footprint:.1f} kg CO2")
        with col4:
            avg_efficiency = np.mean([d['efficiency'] for d in st.session_state.devices])
            st.metric("Avg Efficiency", f"{avg_efficiency*100:.0f}%")

elif page_name == "Advanced AI Assistant":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🤖 Advanced AI Energy Assistant</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Powered by GPT-4 • Specialized in African Energy Markets</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.ai_client:
        st.error("🔑 Please configure OpenRouter API key to use the AI assistant")
        st.stop()
    
    # AI Capabilities Overview
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    
    capabilities = [
        "🔍 Comprehensive Energy Analysis",
        "📈 Future Consumption Prediction", 
        "⚡ Smart Optimization Strategies",
        "🚨 Anomaly Detection & Alerts",
        "💰 Cost Reduction Planning",
        "🌱 Carbon Footprint Analysis",
        "🏠 Smart Home Integration",
        "📊 Seasonal Planning Advice"
    ]
    
    cols = st.columns(4)
    for i, capability in enumerate(capabilities):
        with cols[i % 4]:
            st.markdown(f'<div class="ai-capability">{capability}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat interface
    st.markdown('<div class="ai-chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Advanced chat input
    col1, col2, col3 = st.columns([6, 1, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your AI energy consultant anything...", 
            key="ai_chat_input",
            placeholder="e.g., How can I reduce my bill by 30% while maintaining comfort?"
        )
    
    with col2:
        if st.button("🚀 Send", type="primary"):
            if user_input:
                # Add user message
                st.session_state.chat_history.append({"type": "user", "content": user_input})
                
                # Show thinking indicator
                thinking_placeholder = st.empty()
                thinking_placeholder.markdown('<div class="ai-thinking">🤖 <span class="typing-dots">Analyzing your energy data...</span></div>', unsafe_allow_html=True)
                
                # Get AI response
                ai_response = energy_ai.get_comprehensive_analysis(
                    st.session_state.devices,
                    st.session_state.country,
                    temperature,
                    user_input
                )
                
                thinking_placeholder.empty()
                
                # Add AI response
                st.session_state.chat_history.append({"type": "ai", "content": ai_response})
                st.rerun()
    
    with col3:
        if st.button("🗑️ Clear"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Quick AI Actions
    st.subheader("⚡ Quick AI Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🔍 Full Energy Audit", use_container_width=True):
            if st.session_state.devices:
                with st.spinner("Conducting comprehensive audit..."):
                    audit = energy_ai.get_comprehensive_analysis(
                        st.session_state.devices,
                        st.session_state.country,
                        temperature,
                        "Conduct a comprehensive energy audit of my home"
                    )
                    st.session_state.chat_history.append({"type": "ai", "content": audit})
                    st.rerun()
    
    with col2:
        if st.button("📈 Predict Future Bills", use_container_width=True):
            if st.session_state.devices:
                with st.spinner("Generating predictions..."):
                    predictions = energy_ai.predict_future_consumption(
                        st.session_state.devices,
                        st.session_state.country
                    )
                    response = f"**12-Month Energy Forecast:**\n\n{json.dumps(predictions, indent=2)}"
                    st.session_state.chat_history.append({"type": "ai", "content": response})
                    st.rerun()
    
    with col3:
        if st.button("⚡ Optimize Usage", use_container_width=True):
            if st.session_state.devices:
                with st.spinner("Optimizing energy usage..."):
                    optimization = energy_ai.optimize_energy_usage(
                        st.session_state.devices,
                        st.session_state.country
                    )
                    st.session_state.chat_history.append({"type": "ai", "content": optimization})
                    st.rerun()
    
    with col4:
        if st.button("🚨 Detect Anomalies", use_container_width=True):
            if st.session_state.devices:
                # Generate sample consumption data
                consumption_data = []
                for i in range(30):
                    daily_consumption = sum(
                        (d["power"] * d["hours"] * d["quantity"]) / 1000 
                        for d in st.session_state.devices
                    ) * (1 + random.uniform(-0.2, 0.2))  # Add variation
                    consumption_data.append({"day": i+1, "kwh": daily_consumption})
                
                with st.spinner("Analyzing consumption patterns..."):
                    anomalies = energy_ai.analyze_energy_anomalies(consumption_data)
                    st.session_state.chat_history.append({"type": "ai", "content": anomalies})
                    st.rerun()

elif page_name == "Predictive Analytics":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">📊 Predictive Analytics Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">AI-Powered Energy Forecasting & Insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.devices:
        st.info("🏠 Add devices to see predictive analytics")
    else:
        # Generate predictions
        if st.session_state.ai_client:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.subheader("🔮 AI-Powered Predictions")
                
                if st.button("🚀 Generate AI Predictions", type="primary"):
                    with st.spinner("AI analyzing patterns and generating predictions..."):
                        predictions = energy_ai.predict_future_consumption(
                            st.session_state.devices,
                            st.session_state.country,
                            12
                        )
                        st.session_state.ai_analysis['predictions'] = predictions
                        st.success("✅ AI predictions generated!")
            
            with col2:
                st.subheader("📈 Prediction Settings")
                forecast_months = st.slider("Forecast Period (months)", 3, 24, 12)
                confidence_threshold = st.slider("Confidence Threshold", 0.5, 0.95, 0.8)
        
        # Display predictions if available
        if 'predictions' in st.session_state.ai_analysis:
            predictions = st.session_state.ai_analysis['predictions']
            
            if 'error' not in predictions:
                # Create prediction charts
                pred_data = predictions.get('predictions', [])
                
                if pred_data:
                    df_pred = pd.DataFrame(pred_data)
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig_energy = px.line(
                            df_pred, 
                            x='month', 
                            y='energy_kwh',
                            title="AI Energy Consumption Forecast"
                        )
                        fig_energy.add_scatter(
                            x=df_pred['month'],
                            y=df_pred['energy_kwh'],
                            mode='markers',
                            name='Predictions'
                        )
                        st.plotly_chart(fig_energy, use_container_width=True)
                    
                    with col2:
                        fig_confidence = px.bar(
                            df_pred,
                            x='month',
                            y='confidence',
                            title="Prediction Confidence Levels"
                        )
                        st.plotly_chart(fig_confidence, use_container_width=True)
                    
                    # Prediction insights
                    st.subheader("🎯 AI Insights")
                    
                    avg_energy = np.mean([p['energy_kwh'] for p in pred_data])
                    avg_confidence = np.mean([p['confidence'] for p in pred_data])
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Avg Monthly Energy", f"{avg_energy:.1f} kWh")
                    with col2:
                        st.metric("Avg Confidence", f"{avg_confidence*100:.0f}%")
                    with col3:
                        trend = "Increasing" if pred_data[-1]['energy_kwh'] > pred_data[0]['energy_kwh'] else "Decreasing"
                        st.metric("Trend", trend)
            
            else:
                st.error(f"Prediction error: {predictions['error']}")
        
        # Current analytics
        bill_data = calculate_comprehensive_bill(st.session_state.devices, st.session_state.country, temperature)
        
        st.subheader("📊 Current Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.metric("Monthly Energy", f"{bill_data['total_energy']:.1f} kWh")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.metric("Monthly Cost", f"{bill_data['currency']}{bill_data['total_bill']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            yearly_cost = bill_data['total_bill'] * 12
            st.metric("Yearly Projection", f"{bill_data['currency']}{yearly_cost:.0f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            efficiency = np.mean([d['efficiency'] for d in st.session_state.devices]) * 100
            st.metric("System Efficiency", f"{efficiency:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)

elif page_name == "Future Insights":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🔮 Future Energy Insights</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Advanced AI Modeling & Scenario Planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.ai_client:
        st.error("🔑 Advanced AI features require OpenRouter API configuration")
    elif not st.session_state.devices:
        st.info("🏠 Add devices to explore future insights")
    else:
        # Scenario planning
        st.subheader("🎯 Scenario Planning")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**What-If Scenarios:**")
            
            scenario_type = st.selectbox("Scenario Type", [
                "Device Upgrade Impact",
                "Usage Pattern Change", 
                "Seasonal Variation",
                "Economic Impact",
                "Technology Adoption"
            ])
            
            if scenario_type == "Device Upgrade Impact":
                upgrade_device = st.selectbox("Device to Upgrade", [d['name'] for d in st.session_state.devices])
                efficiency_improvement = st.slider("Efficiency Improvement (%)", 10, 50, 25)
                
                if st.button("🔍 Analyze Upgrade Impact"):
                    with st.spinner("AI analyzing upgrade scenario..."):
                        scenario_query = f"Analyze the impact of upgrading {upgrade_device} with {efficiency_improvement}% better efficiency"
                        analysis = energy_ai.get_comprehensive_analysis(
                            st.session_state.devices,
                            st.session_state.country,
                            temperature,
                            scenario_query
                        )
                        st.success("**Upgrade Analysis:**")
                        st.write(analysis)
        
        with col2:
            st.markdown("**Future Technology Impact:**")
            
            tech_adoption = st.multiselect("Future Technologies", [
                "Smart Thermostats",
                "Solar Panels", 
                "Battery Storage",
                "Smart Appliances",
                "LED Conversion",
                "Heat Pumps"
            ])
            
            adoption_timeline = st.slider("Adoption Timeline (years)", 1, 10, 3)
            
            if tech_adoption and st.button("🚀 Predict Technology Impact"):
                with st.spinner("AI modeling technology adoption..."):
                    tech_query = f"Predict the impact of adopting {', '.join(tech_adoption)} over {adoption_timeline} years"
                    tech_analysis = energy_ai.get_comprehensive_analysis(
                        st.session_state.devices,
                        st.session_state.country,
                        temperature,
                        tech_query
                    )
                    st.success("**Technology Impact Analysis:**")
                    st.write(tech_analysis)
        
        # Advanced insights
        st.subheader("🧠 Advanced AI Insights")
        
        insight_tabs = st.tabs(["💡 Optimization", "📈 Trends", "🌍 Climate Impact", "💰 ROI Analysis"])
        
        with insight_tabs[0]:
            if st.button("🎯 Generate Optimization Plan"):
                with st.spinner("AI creating personalized optimization plan..."):
                    optimization = energy_ai.optimize_energy_usage(
                        st.session_state.devices,
                        st.session_state.country,
                        30  # 30% target reduction
                    )
                    st.write(optimization)
        
        with insight_tabs[1]:
            st.write("**Energy Trend Analysis**")
            # Generate trend data
            months = list(range(1, 13))
            current_energy = sum((d["power"] * d["hours"] * 30 * d["quantity"]) / 1000 for d in st.session_state.devices)
            
            # Simulate seasonal trends
            seasonal_factors = [1.15, 1.10, 1.05, 0.95, 1.00, 1.20, 1.25, 1.25, 1.15, 1.00, 1.05, 1.10]
            trend_data = [current_energy * factor for factor in seasonal_factors]
            
            df_trend = pd.DataFrame({
                'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                'Energy': trend_data
            })
            
            fig_trend = px.line(df_trend, x='Month', y='Energy', title="Seasonal Energy Trends")
            st.plotly_chart(fig_trend, use_container_width=True)
        
        with insight_tabs[2]:
            st.write("**Climate Impact Assessment**")
            
            current_carbon = sum((d["power"] * d["hours"] * 30 * d["quantity"]) / 1000 for d in st.session_state.devices) * 0.85
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current CO2", f"{current_carbon:.1f} kg/month")
            with col2:
                yearly_carbon = current_carbon * 12
                st.metric("Yearly CO2", f"{yearly_carbon:.0f} kg")
            with col3:
                trees_needed = yearly_carbon / 22  # 22kg CO2 per tree per year
                st.metric("Trees to Offset", f"{trees_needed:.0f}")
        
        with insight_tabs[3]:
            st.write("**ROI Analysis for Upgrades**")
            
            # Sample ROI calculations
            upgrade_costs = {
                "LED Conversion": {"cost": 200, "savings_percent": 15, "payback_months": 8},
                "Smart Thermostat": {"cost": 150, "savings_percent": 12, "payback_months": 10},
                "Energy Efficient AC": {"cost": 800, "savings_percent": 30, "payback_months": 18}
            }
            
            for upgrade, data in upgrade_costs.items():
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.write(f"**{upgrade}**")
                with col2:
                    st.write(f"Cost: ${data['cost']}")
                with col3:
                    st.write(f"Savings: {data['savings_percent']}%")
                with col4:
                    st.write(f"Payback: {data['payback_months']} months")

# Footer
st.markdown("---")
st.markdown("**EnergySense AI Advanced** - OpenRouter Powered • Comprehensive Energy Intelligence • African Energy Solutions")