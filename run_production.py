"""
EnergySense AI - Production Launcher
Launch the production-grade energy analytics system
"""
import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

if __name__ == "__main__":
    print("🚀 Launching EnergySense AI - Production System")
    print("=" * 50)
    print("Features:")
    print("✅ Physics-based energy calculations")
    print("✅ ODE thermal modeling")
    print("✅ Regional billing engines")
    print("✅ SARIMA forecasting")
    print("✅ ML correction layers")
    print("✅ Production-grade validation")
    print("✅ Advanced UI/UX")
    print("=" * 50)
    
    # Import and run the production app
    os.system("streamlit run energysense_advanced_ai.py --server.port 8501 --server.address localhost")