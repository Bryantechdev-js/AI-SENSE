"""
Test script for AI functionality
"""
import requests
import os

def test_openrouter_api():
    """Test OpenRouter API directly"""
    api_key = "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"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ai-sense-43djhny8ihhq2rvudnp974.streamlit.app/" or "http://localhost:8501/",
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