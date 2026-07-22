#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug search endpoint response"""

import requests

API_BASE = "http://localhost:8000"

print("Testing Search endpoint...")
print("=" * 70)

try:
    resp = requests.post(f"{API_BASE}/search", 
                       json={"question": "password authentication"},
                       timeout=30)
    
    print(f"Status: {resp.status_code}")
    result = resp.json().get("result", "")
    
    print(f"Content length: {len(result)} chars")
    print(f"\n--- FULL RESPONSE ---")
    print(result)
    print(f"--- END RESPONSE ---\n")
    
    # Check for error patterns
    has_error = "pertinent" in result.lower() or "non trouve" in result.lower()
    has_cadre = "┌" in result  # CADRE box present
    
    print(f"Has error message: {has_error}")
    print(f"Has CADRE formatting: {has_cadre}")
    
    if has_cadre and not has_error:
        print("✅ SEARCH IS WORKING - Contains CADRE formatted results!")
    elif not has_error and len(result) > 200:
        print("✅ SEARCH IS WORKING - Has content!")
    else:
        print("❌ SEARCH STILL FAILING")
        
except Exception as e:
    print(f"❌ Error: {e}")
