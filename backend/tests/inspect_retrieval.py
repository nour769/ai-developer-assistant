# backend/tests/inspect_retrieval.py
"""
Diagnostic : montre EXACTEMENT quels chunks sont récupérés pour une
question donnée, avec leur score de distance, avant tout passage au LLM.
Usage : python -m backend.tests.inspect_retrieval "ma question"
"""

import sys
from backend.rag.vectorstore import search

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.tests.inspect_retrieval <question>")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    results = search(question, top_k=5)

    print(f"Question : {question}\n")
    print(f"{len(results)} résultat(s) trouvé(s) :\n")

    for i, r in enumerate(results, 1):
        meta = r["metadata"]
        print(f"[{i}] distance={r['distance']:.4f} -- {meta['file']} :: {meta['type']} `{meta['name']}` (ligne {meta['lineno']})")
        print(f"    {r['code'][:150].strip()}...")
        print()

if __name__ == "__main__":
    main()