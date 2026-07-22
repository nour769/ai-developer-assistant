#!/usr/bin/env python
"""Debug what retrieve_and_format returns for recommend questions."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.rag.retriever import retrieve_context, format_context, AUCUN_CONTEXTE_PERTINENT

questions = [
    "Quels sont les problèmes de sécurité?",
    "Comment optimiser les performances?",
    "Explique la fonction authenticate",
    "password vulnerability injection"
]

for question in questions:
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    # Try different max_distance values
    for max_dist in [0.9, 1.0, 1.2, 1.5]:
        matches = retrieve_context(question, top_k=20, max_distance=max_dist)
        print(f"\nmax_distance={max_dist}:")
        print(f"  Résultats trouvés: {len(matches)}")
        
        if matches:
            for i, m in enumerate(matches[:3]):  # First 3
                meta = m["metadata"]
                dist = m.get("distance", "?")
                print(f"    {i+1}. {meta['file']}:{meta['lineno']} ({meta['name']}) - distance={dist:.3f}")
        else:
            print(f"  ❌ Aucun résultat")
