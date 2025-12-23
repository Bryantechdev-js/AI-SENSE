# EnergySense AI - Setup Instructions

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure OpenAI API (Required for AI Assistant)

#### Option A: Create .env file
1. Copy `.env.example` to `.env`
2. Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

#### Option B: Set Environment Variable
**Windows:**
```cmd
set OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

### 3. Get OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key (starts with `sk-`)

### 4. Launch Application
```bash
python run_production.py
```

## 🔧 Features

### ✅ Without API Key
- Device Management
- Bill Calculations
- Real-time Simulation
- Analytics Dashboard

### 🤖 With API Key
- **AI Energy Assistant** (ChatGPT-powered)
- Personalized recommendations
- Advanced energy analysis
- Natural language queries

## 🌍 Supported Countries
25 African countries with real tariff data:
- Nigeria, South Africa, Egypt, Kenya, Ghana
- Morocco, Ethiopia, Tanzania, Uganda, Algeria,cameroon
- And 15 more...

## 📊 Key Features
- **Multi-device management** with quantities
- **Real-time simulation** like a driving simulator
- **ChatGPT-like AI interface** for energy consulting
- **Comprehensive analytics** with KPIs
- **African-focused** billing calculations

## 🔒 Security
- API keys stored in environment variables
- No sensitive data transmitted
- Local processing for privacy"# AI-SENSE" 
