#!/usr/bin/env python
"""Test recommend function directly without API."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.assistant.recommend import recommend
from backend.rag.vectorstore import search

print("Testing recommend() directly...\n")

# First, test retrieval distances
print("1. Checking retrieval distances:")
question = "Quels sont les problèmes de sécurité?"
matches = search(question, top_k=5, max_distance=2.0)
print(f"   Question: {question}")
print(f"   Results with max_distance=2.0: {len(matches)} chunks found")
if matches:
    for m in matches[:2]:
        print(f"     - {m['metadata']['name']}: distance={m.get('distance', '?'):.3f}")
print()

# Now test recommend function
print("2. Testing recommend() function:")
result = recommend("Quels sont les problèmes de sécurité?")
has_code = "pertinent" not in result.lower() and len(result) > 300
print(f"   Result: {'Found code!' if has_code else 'No code found'}")
print(f"   Length: {len(result)} chars")
if len(result) < 200:
    print(f"   Content: {result}")
else:
    print(f"   Preview: {result[:200]}...")
print()

# Test another question
print("3. Testing with performance question:")
result2 = recommend("Comment optimiser les performances?")
has_code2 = "pertinent" not in result2.lower() and len(result2) > 300
print(f"   Result: {'Found code!' if has_code2 else 'No code found'}")
print(f"   Length: {len(result2)} chars")
if len(result2) < 200:
    print(f"   Content: {result2}")
print()

if has_code and has_code2:
    print("✓ SUCCES: recommend() est maintenant fonctionnel!")
else:
    print("✗ ECHEC: recommend() ne trouve toujours pas de code")
