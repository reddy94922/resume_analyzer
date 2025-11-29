#!/usr/bin/env python
"""Check available Gemini models."""
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

# List available models
import requests
url = f'https://generativelanguage.googleapis.com/v1beta/models?key={api_key}'

try:
    print('Fetching available models...')
    response = requests.get(url, timeout=10)
    print(f'Status: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f'\nAvailable models ({len(models)} total):')
        for model in models:
            name = model.get('name', 'unknown')
            methods = model.get('supportedGenerationMethods', [])
            if 'generateContent' in methods:
                print(f'  ✓ {name}')
    else:
        print(f'Error: {response.text[:300]}')
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')
