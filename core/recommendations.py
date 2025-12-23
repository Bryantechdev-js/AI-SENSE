def generate_recommendations(total_energy):
    """Generate smart energy recommendations based on consumption"""
    tips = []
    
    if total_energy > 800:
        tips.extend([
            "🏠 Consider solar panels - your high usage makes it cost-effective",
            "❄️ Upgrade to inverter AC - can save 30-40% on cooling costs",
            "💡 Install smart home automation to optimize device scheduling"
        ])
    elif total_energy > 600:
        tips.extend([
            "🌡️ Set AC to 24°C instead of 18°C - saves 20% energy",
            "⚡ Replace old appliances with 5-star rated models",
            "🔌 Use power strips to eliminate phantom loads"
        ])
    elif total_energy > 400:
        tips.extend([
            "💡 Switch all bulbs to LED - 80% energy savings",
            "🌀 Use ceiling fans with AC to feel cooler at higher temperatures",
            "📺 Enable power saving mode on electronics"
        ])
    elif total_energy > 200:
        tips.extend([
            "🔋 Unplug chargers when not in use",
            "🌞 Use natural light during daytime",
            "❄️ Keep refrigerator at optimal temperature (3-4°C)"
        ])
    else:
        tips.extend([
            "✅ Great job! Your energy usage is very efficient",
            "📊 Monitor usage patterns to maintain efficiency",
            "🌱 Consider sharing your energy-saving tips with others"
        ])
    
    # Add seasonal recommendations
    import datetime
    month = datetime.datetime.now().month
    
    if month in [6, 7, 8]:  # Summer
        tips.append("☀️ Summer tip: Use curtains to block sunlight and reduce AC load")
    elif month in [12, 1, 2]:  # Winter
        tips.append("❄️ Winter tip: Use programmable thermostats for heating efficiency")
    
    return tips
