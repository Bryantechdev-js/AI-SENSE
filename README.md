# EnergySense AI - Setup Instructions

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key (Optional - for AI Assistant)

#### Option A: Local Development (.env file)
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here
```

#### Option B: Streamlit Cloud Deployment
1. Go to your Streamlit Cloud app settings
2. Add secrets in the "Secrets" section:
```toml
OPENROUTER_API_KEY = "sk-or-v1-your-actual-api-key-here"
SITE_URL = "https://your-app-url.streamlit.app/"
```

### 3. Get OpenRouter API Key (Optional)
1. Go to https://openrouter.ai/keys
2. Create a new API key
3. Copy the key (starts with `sk-or-v1-`)

### 4. Launch Application
```bash
streamlit run streamlit_app.py
```

## 🔧 Features

### ✅ Without API Key
- Device Management
- Bill Calculations
- Real-time Simulation
- Analytics Dashboard
- **Smart Fallback Responses** (Works offline!)

### 🤖 With API Key
- **AI Energy Assistant** (OpenRouter-powered)
- Personalized recommendations
- Advanced energy analysis
- Natural language queries

## 🔒 Security Features
- API keys stored in environment variables
- No sensitive data in code repository
- Secure fallback when API unavailable
- Local processing for privacy

## 🌍 Supported Countries
5 African countries with real tariff data:
- Cameroon, Nigeria, Kenya, Ghana, South Africa

## 📊 Key Features
- **Multi-device management** with quantities
- **Real-time simulation** like a driving simulator
- **AI-like interface** with smart fallback responses
- **Comprehensive analytics** with KPIs
- **African-focused** billing calculations
- **Mobile-first design** for accessibility

## 🚫 Important Security Notes
- Never commit `.env` or `secrets.toml` files with real API keys
- Use `.env.example` as template
- The app works fully without API keys using intelligent fallback responses