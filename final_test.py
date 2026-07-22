#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Final test after fix: ingests data and tests all endpoints
"""

import requests
import time
import sys

API_BASE = "http://localhost:8000"

print("=" * 70)
print("ÉTAPE 1: Ingest test_project.zip")
print("=" * 70)

try:
    with open("test_project.zip", "rb") as f:
        files = {"file": f}
        resp = requests.post(f"{API_BASE}/ingest", files=files, timeout=30)
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Ingestion réussie!")
        print(f"   Project ID: {data.get('project_id')}")
        print(f"   Fichiers: {data.get('files_count')}")
        print(f"   Chunks: {data.get('chunks_count')}")
    else:
        print(f"❌ Ingestion échouée: {resp.status_code}")
        print(f"   Response: {resp.text[:200]}")
        sys.exit(1)
except Exception as e:
    print(f"❌ Erreur ingestion: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("ÉTAPE 2: Test des endpoints")
print("=" * 70)

time.sleep(1)  # Wait a bit for indexing

tests = [
    ("Recommend Security", "/recommend", "Quels sont les problemes de securite?"),
    ("Recommend Performance", "/recommend", "Comment optimiser les performances?"),
    ("Explain Function", "/explain", "Explique la fonction authenticate"),
    ("Search Password", "/search", "password authentication"),
]

passed = 0
failed = 0

for test_name, endpoint, question in tests:
    print(f"\n📝 Test: {test_name}")
    try:
        resp = requests.post(f"{API_BASE}{endpoint}", 
                           json={"question": question},
                           timeout=30)
        
        if resp.status_code != 200:
            print(f"   ❌ HTTP {resp.status_code}")
            failed += 1
            continue
        
        result = resp.json().get("result", "")
        
        # Check if code was found
        # Error pattern: "Je n'ai trouvé aucun code pertinent" or "non trouvé"
        has_error = ("je n'ai trouve" in result.lower() or 
                    "aucun code pertinent" in result.lower() or
                    "non trouve" in result.lower())
        has_content = len(result) > 200
        
        if has_error and not has_content:
            print(f"   ❌ No code found")
            print(f"      {result[:150]}")
            failed += 1
        elif has_content:
            print(f"   ✅ Code found! ({len(result)} chars)")
            # Show first non-whitespace content
            preview = result.strip().split('\n')[0][:120]
            print(f"      {preview}...")
            passed += 1
        else:
            print(f"   ⚠️  Short response ({len(result)} chars)")
            print(f"      {result[:150]}")
            failed += 1
            
    except Exception as e:
        print(f"   ❌ Error: {e}")
        failed += 1

print("\n" + "=" * 70)
print("RÉSUMÉ")
print("=" * 70)
print(f"✅ Passed: {passed}/{len(tests)}")
print(f"❌ Failed: {failed}/{len(tests)}")

if passed == len(tests):
    print("\n🎉 TOUS LES TESTS RÉUSSIS! Le problème est résolu!")
    sys.exit(0)
else:
    print(f"\n⚠️  {failed} test(s) encore en échec")
    sys.exit(1)
