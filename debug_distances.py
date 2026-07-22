#!/usr/bin/env python
"""Debug what distances are returned for retrieval."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.rag.vectorstore import search

questions = [
    "Quels sont les problèmes de sécurité?",
    "Comment optimiser les performances?",
    "authenticate password",
    "vulnerability injection",
]

print("Debugging retrieval distances...\n")

for question in questions:
    print(f"Question: {question}")
    
    # Try with different max_distance values
    for max_dist in [0.5, 0.9, 1.0, 1.5, 2.0]:
        matches = search(question, top_k=5, max_distance=max_dist)
        print(f"  max_distance={max_dist}: {len(matches)} results")
        
        if matches:
            # Show distances of top 2 results
            for i, m in enumerate(matches[:2]):
                dist = m.get("distance", "?")
                name = m["metadata"]["name"]
                print(f"    #{i+1}: {name} - distance={dist:.3f}")
    
    print()
