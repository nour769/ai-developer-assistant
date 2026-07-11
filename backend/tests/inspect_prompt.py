# backend/tests/inspect_prompt.py
"""
Diagnostic : affiche le prompt complet qui serait envoyé au LLM,
sans l'appeler -- pour vérifier que le contexte injecté est correct.
Usage : python -m backend.tests.inspect_prompt "ma question"
"""

import sys
from backend.rag.retriever import retrieve_and_format

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m backend.tests.inspect_prompt <question>")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    context = retrieve_and_format(question, top_k=5)

    print("=" * 60)
    print("CONTEXTE QUI SERA ENVOYÉ AU LLM :")
    print("=" * 60)
    print(context)
    print("=" * 60)

if __name__ == "__main__":
    main()