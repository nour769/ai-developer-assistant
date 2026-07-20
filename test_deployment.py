#!/usr/bin/env python3
import requests
import json
import sys

body = {
    'project_name': 'AI Assistant',
    'service': 'AWS',
    'usage_level': 'small'
}

print("Testing deployment endpoint...")
response = requests.post('http://localhost:8000/deployment', json=body, timeout=60)
result = response.json()

print(f"✓ Service: {result['parameters']['service']}")
print(f"✓ Usage Level: {result['parameters']['usage_level']}")
print(f"\nResponse preview (first 500 chars):")
print(result['result'][:500])
print("\n... [truncated]")
