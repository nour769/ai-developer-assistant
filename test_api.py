# -*- coding: utf-8 -*-
import requests
import json

API_BASE = "http://localhost:8000"

# Test 1: Recommend - Security vulnerabilities
print("=" * 60)
print("TEST 1: Recommend - Security vulnerabilities")
print("=" * 60)
try:
    resp = requests.post(f"{API_BASE}/recommend", 
        json={"question": "Quels sont les problemes de securite?"})
    print(f"Status: {resp.status_code}")
    result = resp.json()["result"]
    if "pertinent" in result.lower():
        print("? No code found (FAILED)")
    else:
        print("? Code found!")
        # Show first 300 chars
        print(f"Response preview: {result[:300]}")
except Exception as e:
    print(f"Connection failed: {e}")

# Test 2: Recommend - Performance optimization
print("\n" + "=" * 60)
print("TEST 2: Recommend - Performance optimization")
print("=" * 60)
try:
    resp = requests.post(f"{API_BASE}/recommend", 
        json={"question": "Comment optimiser les performances?"})
    print(f"Status: {resp.status_code}")
    result = resp.json()["result"]
    if "pertinent" in result.lower():
        print("? No code found (FAILED)")
    else:
        print("? Code found!")
        print(f"Response preview: {result[:300]}")
except Exception as e:
    print(f"Connection failed: {e}")

# Test 3: Explain - What does the code do
print("\n" + "=" * 60)
print("TEST 3: Explain - Project overview")
print("=" * 60)
try:
    resp = requests.post(f"{API_BASE}/explain", 
        json={"question": "Explique la fonction authenticate"})
    print(f"Status: {resp.status_code}")
    result = resp.json()["result"]
    if "pertinent" in result.lower():
        print("? No code found (FAILED)")
    else:
        print("? Code found!")
        print(f"Response preview: {result[:300]}")
except Exception as e:
    print(f"Connection failed: {e}")

# Test 4: Search
print("\n" + "=" * 60)
print("TEST 4: Search - Find password related code")
print("=" * 60)
try:
    resp = requests.post(f"{API_BASE}/search", 
        json={"question": "password authentication"})
    print(f"Status: {resp.status_code}")
    result = resp.json()["result"]
    if "pertinent" in result.lower():
        print("? No code found (FAILED)")
    else:
        print("? Code found!")
        print(f"Response preview: {result[:300]}")
except Exception as e:
    print(f"Connection failed: {e}")
