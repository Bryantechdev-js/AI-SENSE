"""
Test script for AI functionality
"""
import requests
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_key():
    """Get API key from secrets or environment"""
    try:
        # Try Streamlit secrets first (for cloud deployment)
        if hasattr(st, 'secrets') and "OPENROUTER_API_KEY" in st.secrets:
            return st.secrets["OPENROUTER_API_KEY"]
        # Try environment variable (for local development)
        return os.getenv("OPENROUTER_API_KEY", "")
    except:
        return os.getenv("OPENROUTER_API_KEY", "")

def test_openrouter_api():
    """Test OpenRouter API directly"""
    api_key = get_api_key()
    
    if not api_key:
        print("No API key found in environment or secrets")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-sense-43djhny8ihhq2rvudnp974.streamlit.app/",
        "X-Title": "EnergySense AI"
    }
    
    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "user", "content": "Hello, test message"}
        ],
        "max_tokens": 50
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result:
                print(f"AI Response: {result['choices'][0]['message']['content']}")
                return True
        
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing OpenRouter API...")
    success = test_openrouter_api()
    print(f"Test {'PASSED' if success else 'FAILED'}")