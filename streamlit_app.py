"""
EnergySense AI - Streamlit Cloud Entry Point
Advanced AI-Powered Energy Management System
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
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="EnergySense AI - Advanced Energy Management",
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
    
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        text-align: center;
    }
    
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #4ECDC4;
        transition: transform 0.3s ease;
        margin: 1rem 0;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .simulation-dashboard {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .device-status-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background: #ff4444;
        border-radius: 50%;
        animation: blink 1s infinite;
        margin-right: 8px;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
</style>
""", unsafe_allow_html=True)

# African Countries Database
AFRICAN_COUNTRIES = {
    "Nigeria": {"currency": "₦", "rate": 68.0, "fixed": 1000, "tax": 0.075, "peak_rate": 85.0},
    "South Africa": {"currency": "R", "rate": 1.85, "fixed": 150, "tax": 0.15, "peak_rate": 2.50},
    "Egypt": {"currency": "£E", "rate": 1.45, "fixed": 50, "tax": 0.10, "peak_rate": 2.20},
    "Kenya": {"currency": "KSh", "rate": 24.0, "fixed": 200, "tax": 0.16, "peak_rate": 35.0},
    "Ghana": {"currency": "₵", "rate": 1.20, "fixed": 25, "tax": 0.125, "peak_rate": 1.80},
    "Morocco": {"currency": "DH", "rate": 1.15, "fixed": 30, "tax": 0.20, "peak_rate": 1.65},
    "Ethiopia": {"currency": "Br", "rate": 6.50, "fixed": 15, "tax": 0.15, "peak_rate": 9.75},
    "Tanzania": {"currency": "TSh", "rate": 280, "fixed": 5000, "tax": 0.18, "peak_rate": 420},
    "Uganda": {"currency": "USh", "rate": 420, "fixed": 8000, "tax": 0.18, "peak_rate": 630},
    "Algeria": {"currency": "DA", "rate": 18.5, "fixed": 200, "tax": 0.19, "peak_rate": 27.8}
}

# Device Database
DEVICE_SPECS = {
    "Air Conditioner": {"power": 1200, "hours": 8.0, "category": "cooling", "emoji": "❄️", "efficiency": 0.85},
    "Television": {"power": 120, "hours": 6.0, "category": "entertainment", "emoji": "📺", "efficiency": 0.90},
    "Refrigerator": {"power": 150, "hours": 24.0, "category": "kitchen", "emoji": "🧊", "efficiency": 0.88},
    "Washing Machine": {"power": 500, "hours": 1.0, "category": "laundry", "emoji": "👕", "efficiency": 0.82},
    "Microwave": {"power": 1200, "hours": 0.5, "category": "kitchen", "emoji": "🔥", "efficiency": 0.75},
    "LED Bulb": {"power": 10, "hours": 6.0, "category": "lighting", "emoji": "💡", "efficiency": 0.95},
    "Ceiling Fan": {"power": 75, "hours": 12.0, "category": "cooling", "emoji": "🌀", "efficiency": 0.85},
    "Water Heater": {"power": 2000, "hours": 2.0, "category": "heating", "emoji": "🚿", "efficiency": 0.78},
    "Electric Kettle": {"power": 1500, "hours": 0.25, "category": "kitchen", "emoji": "☕", "efficiency": 0.85},
    "Laptop": {"power": 65, "hours": 8.0, "category": "electronics", "emoji": "💻", "efficiency": 0.88}
}

# Initialize session state
if 'devices' not in st.session_state:
    st.session_state.devices = []
if 'simulation_running' not in st.session_state:
    st.session_state.simulation_running = False
if 'simulation_data' not in st.session_state:
    st.session_state.simulation_data = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'country' not in st.session_state:
    st.session_state.country = "Nigeria"

# Helper functions
def calculate_energy(power, hours, days, quantity):
    return (power * hours * days * quantity) / 1000

def calculate_bill(devices, country, temperature=28):
    config = AFRICAN_COUNTRIES[country]
    total_energy = 0
    
    for device in devices:
        energy = calculate_energy(device["power"], device["hours"], 30, device["quantity"])
        # Temperature adjustment
        energy *= (1 + 0.03 * (temperature - 22) / 22)
        total_energy += energy
    
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
        "currency": config["currency"]
    }

def simulate_device_usage(device, current_hour):
    """Simulate realistic device usage"""
    usage_patterns = {
        "cooling": list(range(12, 18)) + list(range(22, 24)) + list(range(0, 6)),
        "entertainment": list(range(18, 24)),
        "kitchen": list(range(6, 9)) + list(range(17, 21)),
        "lighting": list(range(18, 24)) + list(range(0, 7))
    }
    
    category = device.get("category", "general")
    peak_hours = usage_patterns.get(category, list(range(24)))
    
    if device["name"] == "Refrigerator":
        return 1.0
    
    return 0.8 if current_hour in peak_hours else 0.2

def get_ai_response(user_message, context):
    """Simulate AI responses for demo"""
    responses = {
        "save": f"💡 To save energy in {context['country']}:\n• Set AC to 24°C (saves 20%)\n• Use LED bulbs (80% less energy)\n• Unplug devices when not in use\n• Your potential savings: {context['currency']}200/month",
        "bill": f"💰 Your monthly bill breakdown:\n• Energy: {context['currency']}{context.get('bill', 0):.0f}\n• You're using {context.get('energy', 0):.0f} kWh/month\n• Peak usage devices: AC and Water Heater",
        "predict": f"📈 Based on your {len(context['devices'])} devices:\n• Next month: {context.get('energy', 0)*1.1:.0f} kWh\n• Seasonal increase expected\n• Yearly cost: {context['currency']}{context.get('bill', 0)*12:.0f}",
        "optimize": f"⚡ Optimization recommendations:\n• Replace old bulbs with LEDs\n• Use AC timer (save 25%)\n• Upgrade to inverter appliances\n• Potential savings: {context['currency']}{context.get('bill', 0)*0.3:.0f}/month"
    }
    
    for keyword, response in responses.items():
        if keyword in user_message.lower():
            return response
    
    return f"🤖 I'm your AI energy consultant for {context['country']}! I can help with:\n• Energy saving tips\n• Bill predictions\n• Device optimization\n• Cost reduction strategies\n\nWhat would you like to know?"

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="color: #1f77b4; font-size: 1.8rem; margin: 0;">⚡ EnergySense AI</h1>
        <p style="color: #666; font-size: 0.9rem; margin: 0;">Advanced Energy Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Demo mode notice
    st.info("🌟 **Demo Mode**\nFull AI features available with API key")
    
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        ["🏠 Device Manager", "🤖 AI Assistant", "📊 Real-time Simulation", "📈 Analytics"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Settings
    st.markdown("### 🌍 Settings")
    st.session_state.country = st.selectbox("African Country", list(AFRICAN_COUNTRIES.keys()))
    temperature = st.slider("🌡️ Temperature (°C)", 15.0, 40.0, 28.0)
    
    # Quick stats
    if st.session_state.devices:
        st.markdown("### 📊 Quick Stats")
        total_devices = sum(d["quantity"] for d in st.session_state.devices)
        st.metric("Devices", total_devices)
        
        if st.session_state.simulation_running:
            st.markdown('<div class="live-indicator"></div>**LIVE**', unsafe_allow_html=True)

# Main application
page_name = page.split(" ", 1)[1]

if page_name == "Device Manager":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🏠 Smart Device Manager</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Manage Your Home Energy Devices</p>
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
                "efficiency": DEVICE_SPECS[device_type]["efficiency"]
            }
            st.session_state.devices.append(device)
            st.success(f"✅ Added {quantity}x {device_type}")
            st.rerun()
    
    # Device list
    if st.session_state.devices:
        st.subheader("📱 Your Devices")
        
        for i, device in enumerate(st.session_state.devices):
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
                
                with col1:
                    st.write(f"{device['emoji']} **{device['name']}** (×{device['quantity']})")
                    st.write(f"⚡ {device['power']}W • 🕐 {device['hours']}h/day")
                
                with col2:
                    energy = calculate_energy(device['power'], device['hours'], device['days'], device['quantity'])
                    st.metric("kWh/month", f"{energy:.1f}")
                
                with col3:
                    bill = calculate_bill([device], st.session_state.country, temperature)
                    st.metric("Cost/month", f"{bill['currency']}{bill['total_bill']:.0f}")
                
                with col4:
                    new_hours = st.slider("Hours", 0.0, 24.0, device['hours'], 0.5, key=f"hours_{i}")
                    if new_hours != device['hours']:
                        st.session_state.devices[i]['hours'] = new_hours
                        st.rerun()
                
                with col5:
                    if st.button("🗑️", key=f"del_{i}"):
                        st.session_state.devices.pop(i)
                        st.rerun()
        
        # Total calculation
        if len(st.session_state.devices) > 1:
            st.markdown("---")
            total_bill = calculate_bill(st.session_state.devices, st.session_state.country, temperature)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Energy", f"{total_bill['total_energy']:.1f} kWh")
            with col2:
                st.metric("Monthly Bill", f"{total_bill['currency']}{total_bill['total_bill']:.2f}")
            with col3:
                st.metric("Daily Cost", f"{total_bill['currency']}{total_bill['total_bill']/30:.2f}")
            with col4:
                st.metric("Yearly Cost", f"{total_bill['currency']}{total_bill['total_bill']*12:.0f}")

elif page_name == "AI Assistant":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">🤖 AI Energy Assistant</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Your Personal Energy Consultant</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat interface
    st.markdown('<div class="ai-chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['type'] == 'user':
            st.markdown(f'<div class="user-message">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="ai-message">🤖 {message["content"]}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input("Ask about energy efficiency...", key="chat_input", placeholder="e.g., How can I reduce my electricity bill?")
    
    with col2:
        if st.button("Send", type="primary", use_container_width=True):
            if user_input:
                # Add user message
                st.session_state.chat_history.append({"type": "user", "content": user_input})
                
                # Prepare context
                context = {
                    'country': st.session_state.country,
                    'devices': st.session_state.devices,
                    'currency': AFRICAN_COUNTRIES[st.session_state.country]['currency']
                }
                
                if st.session_state.devices:
                    bill_data = calculate_bill(st.session_state.devices, st.session_state.country, temperature)
                    context['energy'] = bill_data['total_energy']
                    context['bill'] = bill_data['total_bill']
                
                # Get AI response
                ai_response = get_ai_response(user_input, context)
                
                # Add AI response
                st.session_state.chat_history.append({"type": "ai", "content": ai_response})
                st.rerun()
    
    # Quick suggestions
    st.subheader("💡 Quick Questions")
    
    suggestions = [
        "How can I save energy?",
        "Predict my next bill",
        "Optimize my devices",
        "Analyze my consumption"
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(suggestion, key=f"suggest_{i}"):
                st.session_state.chat_history.append({"type": "user", "content": suggestion})
                
                context = {
                    'country': st.session_state.country,
                    'devices': st.session_state.devices,
                    'currency': AFRICAN_COUNTRIES[st.session_state.country]['currency']
                }
                
                if st.session_state.devices:
                    bill_data = calculate_bill(st.session_state.devices, st.session_state.country, temperature)
                    context['energy'] = bill_data['total_energy']
                    context['bill'] = bill_data['total_bill']
                
                ai_response = get_ai_response(suggestion, context)
                st.session_state.chat_history.append({"type": "ai", "content": ai_response})
                st.rerun()

elif page_name == "Real-time Simulation":
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 2.5rem;">📊 Real-time Energy Simulation</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Live Energy Monitoring Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.devices:
        st.info("🏠 Add devices first to start the simulation")
    else:
        # Simulation controls
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("▶️ Start Simulation", type="primary", use_container_width=True):
                st.session_state.simulation_running = True
                st.session_state.simulation_data = []
        
        with col2:
            if st.button("⏸️ Pause", use_container_width=True):
                st.session_state.simulation_running = False
        
        with col3:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.simulation_running = False
                st.session_state.simulation_data = []
        
        with col4:
            speed = st.selectbox("Speed", ["1x", "2x", "5x"], index=0)
        
        if st.session_state.simulation_running:
            # Live simulation
            st.markdown('<div class="simulation-dashboard">', unsafe_allow_html=True)
            
            current_hour = datetime.now().hour
            total_power = 0
            device_statuses = []
            
            for device in st.session_state.devices:
                usage_factor = simulate_device_usage(device, current_hour)
                current_power = device["power"] * device["quantity"] * usage_factor
                total_power += current_power
                
                device_statuses.append({
                    "name": device["name"],
                    "emoji": device["emoji"],
                    "power": current_power,
                    "status": "ON" if usage_factor > 0.5 else "STANDBY" if usage_factor > 0.1 else "OFF"
                })
            
            # Add to simulation data
            st.session_state.simulation_data.append({
                "time": datetime.now(),
                "power": total_power / 1000,
                "cost_per_hour": (total_power / 1000) * AFRICAN_COUNTRIES[st.session_state.country]["rate"]
            })
            
            # Keep last 20 points
            if len(st.session_state.simulation_data) > 20:
                st.session_state.simulation_data = st.session_state.simulation_data[-20:]
            
            # Live metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Current Power", f"{total_power/1000:.2f} kW")
            
            with col2:
                hourly_cost = (total_power / 1000) * AFRICAN_COUNTRIES[st.session_state.country]["rate"]
                st.metric("Cost/Hour", f"{AFRICAN_COUNTRIES[st.session_state.country]['currency']}{hourly_cost:.2f}")
            
            with col3:
                daily_projection = hourly_cost * 24
                st.metric("Daily Projection", f"{AFRICAN_COUNTRIES[st.session_state.country]['currency']}{daily_projection:.2f}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Device status
            st.subheader("🔴 Live Device Status")
            
            cols = st.columns(min(3, len(device_statuses)))
            for i, device_status in enumerate(device_statuses):
                with cols[i % 3]:
                    status_color = {"ON": "🟢", "STANDBY": "🟡", "OFF": "🔴"}[device_status["status"]]
                    
                    st.markdown(f'''
                    <div class="device-status-card">
                        <h4>{device_status["emoji"]} {device_status["name"]}</h4>
                        <p>{status_color} {device_status["status"]}</p>
                        <p><strong>{device_status["power"]:.0f}W</strong></p>
                    </div>
                    ''', unsafe_allow_html=True)
            
            # Real-time chart
            if len(st.session_state.simulation_data) > 1:
                df_sim = pd.DataFrame(st.session_state.simulation_data)
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df_sim['time'],
                    y=df_sim['power'],
                    mode='lines+markers',
                    name='Power Consumption',
                    line=dict(color='#4ECDC4', width=3)
                ))
                
                fig.update_layout(
                    title="Live Power Consumption",
                    xaxis_title="Time",
                    yaxis_title="Power (kW)",
                    showlegend=False,
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Auto-refresh
            time.sleep(2)
            st.rerun()
        
        else:
            st.info("▶️ Click 'Start Simulation' to begin live monitoring")

elif page_name == "Analytics":
    st.title("📈 Energy Analytics")
    
    if st.session_state.devices:
        bill_data = calculate_bill(st.session_state.devices, st.session_state.country, temperature)
        
        # KPI Dashboard
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.metric("Monthly Energy", f"{bill_data['total_energy']:.1f} kWh")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            st.metric("Monthly Bill", f"{bill_data['currency']}{bill_data['total_bill']:.2f}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            efficiency = np.mean([d['efficiency'] for d in st.session_state.devices]) * 100
            st.metric("Avg Efficiency", f"{efficiency:.0f}%")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col4:
            st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
            carbon = bill_data['total_energy'] * 0.85
            st.metric("CO2 Footprint", f"{carbon:.1f} kg")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Device breakdown
            device_data = []
            for device in st.session_state.devices:
                energy = calculate_energy(device['power'], device['hours'], device['days'], device['quantity'])
                device_data.append({'Device': device['name'], 'Energy': energy})
            
            df_devices = pd.DataFrame(device_data)
            fig_pie = px.pie(df_devices, values='Energy', names='Device', title="Energy Distribution")
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Category breakdown
            category_data = {}
            for device in st.session_state.devices:
                category = device['category']
                energy = calculate_energy(device['power'], device['hours'], device['days'], device['quantity'])
                category_data[category] = category_data.get(category, 0) + energy
            
            df_category = pd.DataFrame(list(category_data.items()), columns=['Category', 'Energy'])
            fig_bar = px.bar(df_category, x='Category', y='Energy', title="Energy by Category")
            st.plotly_chart(fig_bar, use_container_width=True)
        
        # Seasonal projections
        st.subheader("📅 Seasonal Projections")
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        seasonal_factors = [1.15, 1.10, 1.05, 0.95, 1.00, 1.20, 1.25, 1.25, 1.15, 1.00, 1.05, 1.10]
        
        seasonal_data = []
        for i, month in enumerate(months):
            monthly_bill = bill_data['total_bill'] * seasonal_factors[i]
            seasonal_data.append({'Month': month, 'Bill': monthly_bill})
        
        df_seasonal = pd.DataFrame(seasonal_data)
        fig_seasonal = px.line(df_seasonal, x='Month', y='Bill', title="Yearly Bill Projection")
        st.plotly_chart(fig_seasonal, use_container_width=True)
    
    else:
        st.info("🏠 Add devices to see analytics")

# Footer
st.markdown("---")
st.markdown("**EnergySense AI** - Advanced Energy Management for Africa | [GitHub](https://github.com) | [Documentation](https://docs.energysense.ai)")