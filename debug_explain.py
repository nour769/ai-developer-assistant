#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Debug explain endpoint in detail"""

import requests

API_BASE = "http://localhost:8000"

questions = [
    "Explique la fonction authenticate",
    "Explique ce que fait ce projet",
    "Quelles sont les functions principales",
]

for question in questions:
    print("=" * 70)
    print(f"Question: {question}")
    print("=" * 70)
    
    try:
        resp = requests.post(f"{API_BASE}/explain", 
                           json={"question": question},
                           timeout=30)
        
        print(f"Status: {resp.status_code}")
        result = resp.json().get("result", "")
        
        print(f"Content length: {len(result)} chars")
        
        # Check for error patterns
        has_error = ("je n'ai trouve" in result.lower() or 
                    "aucun code pertinent" in result.lower() or
                    "non trouve" in result.lower())
        
        print(f"Has error message: {has_error}")
        
        print(f"\nPreview:\n{result[:400]}\n")
        
        if has_error:
            print("❌ EXPLAIN FAILING - No code found")
        else:
            print("✅ EXPLAIN WORKING - Found content")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print()
