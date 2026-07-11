# backend/tests/inspect_index.py
"""
Diagnostic : liste tout ce qui est actuellement stocké dans Chroma.
Usage : python -m backend.tests.inspect_index
"""

from backend.rag.vectorstore import get_all_chunks

def main():
    chunks = get_all_chunks()

    if not chunks:
        print("⚠️  Base vectorielle VIDE. Aucune ingestion n'a réussi.")
        return

    print(f"Total : {len(chunks)} chunk(s) indexés\n")

    by_file = {}
    for c in chunks:
        meta = c["metadata"]
        by_file.setdefault(meta["file"], []).append(meta)

    for file, items in sorted(by_file.items()):
        print(f"📄 {file} ({len(items)} chunk(s))")
        for item in items:
            print(f"   - {item['type']} `{item['name']}` (ligne {item['lineno']})")
    print()

if __name__ == "__main__":
    main()