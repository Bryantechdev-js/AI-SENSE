# 🚀 EnergySense AI - Production Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Security Verification
- [ ] No API keys in code repository
- [ ] `.env` and `secrets.toml` in `.gitignore`
- [ ] Only `.env.example` committed to repo
- [ ] All sensitive data in environment variables

### ✅ Local Testing
```bash
# 1. Clone repository
git clone <your-repo-url>
cd EnergySenseAI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment (optional for AI features)
cp .env.example .env
# Edit .env with your API key if needed

# 4. Test locally
streamlit run streamlit_app.py
```

## 🌐 Streamlit Cloud Deployment

### Step 1: Repository Setup
1. Push code to GitHub (without API keys)
2. Ensure `.gitignore` excludes sensitive files
3. Verify `.env.example` is included

### Step 2: Streamlit Cloud Configuration
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub repository
3. Set main file: `streamlit_app.py`

### Step 3: Add Secrets (Optional - for AI features)
In Streamlit Cloud app settings, add to "Secrets":
```toml
OPENROUTER_API_KEY = "sk-or-v1-your-actual-api-key-here"
SITE_URL = "https://your-app-url.streamlit.app/"
SITE_NAME = "EnergySense AI - Smart Energy Forecaster"
AI_MODEL = "openai/gpt-4o-mini"
MAX_TOKENS = "200"
TEMPERATURE = "0.7"
DEBUG = "false"
LOG_LEVEL = "INFO"
```

## 🔒 Security Best Practices

### ✅ API Key Management
- **Never** commit API keys to repository
- Use environment variables for all sensitive data
- Rotate API keys regularly
- Monitor API usage and costs

### ✅ Production Settings
- Set `DEBUG = "false"` in production
- Use HTTPS URLs for `SITE_URL`
- Monitor application logs
- Set appropriate rate limits

## 🧪 Testing Deployment

### Without API Key (Fallback Mode)
- All core features work
- Smart fallback responses active
- Device management functional
- Budget tracking operational

### With API Key (Full AI Mode)
- AI assistant responds with OpenRouter
- Personalized recommendations
- Advanced energy analysis
- Natural language processing

## 🚨 Troubleshooting

### Common Issues
1. **"AI Assistant: Offline"** - Normal without API key
2. **Import errors** - Check requirements.txt
3. **Secrets not loading** - Verify TOML format
4. **API errors** - Check key validity and credits

### Debug Mode
Set `DEBUG = "true"` in secrets to see detailed error messages.

## 📊 Production Monitoring

### Key Metrics to Monitor
- Application uptime
- API response times
- Error rates
- User engagement
- API usage costs

### Health Checks
- Test all major features monthly
- Verify AI responses quality
- Check calculation accuracy
- Monitor performance metrics

## 🔄 Updates and Maintenance

### Regular Tasks
- Update dependencies quarterly
- Review API usage and costs
- Test new features in staging
- Monitor user feedback
- Update device database

### Version Control
- Use semantic versioning
- Tag releases
- Maintain changelog
- Test before deployment