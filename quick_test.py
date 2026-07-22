#!/usr/bin/env python
"""Quick test of endpoints after code changes."""

import requests
import json

API = "http://localhost:8000"

print("Testing endpoints after recommend fix...\n")

tests = [
    ("Recommend Security", "recommend", "Quels sont les problèmes de sécurité?"),
    ("Recommend Performance", "recommend", "Comment optimiser les performances?"),
    ("Explain Function", "explain", "Explique la fonction authenticate"),
    ("Search Password", "search", "password vulnerability injection"),
]

passed = 0

for test_name, endpoint, question in tests:
    print(f"Test: {test_name}")
    try:
        resp = requests.post(f"{API}/{endpoint}", 
            json={"question": question}, timeout=15)
        
        status = resp.status_code
        result = resp.json()["result"]
        
        # Check if code was found (not "aucun code" message)
        has_code = ("aucun code" not in result.lower() and 
                   "aucun contexte" not in result.lower() and
                   len(result) > 250)
        
        if status == 200 and has_code:
            print(f"  OK Status {status} - Code FOUND ({len(result)} chars)")
            passed += 1
        elif status == 200:
            print(f"  FAIL Status {status} - No code found ({len(result)} chars)")
            print(f"       First 150 chars: {result[:150]}")
        else:
            print(f"  FAIL Status {status}")
            
    except requests.exceptions.ConnectionError:
        print(f"  FAIL Cannot connect to API")
    except Exception as e:
        print(f"  FAIL Error: {e}")
    
    print()

print(f"RESULT: {passed}/{len(tests)} tests passed")
