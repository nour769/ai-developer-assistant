"""
Vector store — Semaine 2, Jour 3.

Rôle de ce module :
Stocker les chunks (avec leur embedding, leur code, et leurs
métadonnées) dans Chroma, et permettre de retrouver les chunks les
plus pertinents pour une question donnée (recherche par similarité).

Chroma stocke tout ça sur disque (dossier VECTORSTORE_PATH), donc les
données persistent d'une exécution à l'autre.
"""

import chromadb
from backend.config import VECTORSTORE_PATH
from backend.rag.embeddings import embed_text

_client = chromadb.PersistentClient(path=VECTORSTORE_PATH)
_collection = _client.get_or_create_collection("code_chunks")


def store_chunks(chunks: list[dict]) -> None:
    """
    Stocke une liste de chunks (déjà enrichis d'un embedding par
    embed_chunks()) dans la base vectorielle.
    """
    if not chunks:
        return

    _collection.add(
        ids=[chunk["id"] for chunk in chunks],
        embeddings=[chunk["embedding"] for chunk in chunks],
        documents=[chunk["code"] for chunk in chunks],
        metadatas=[
            {
                "file": chunk["file"],
                "name": chunk["name"],
                "type": chunk["type"],
                "language": chunk["language"],
                "lineno": chunk["lineno"],
            }
            for chunk in chunks
        ],
    )


def search(question: str, top_k: int = 5) -> list[dict]:
    """
    Transforme la question en embedding, puis retrouve les top_k
    chunks les plus proches dans la base vectorielle.

    Retourne une liste de dicts : {"code": ..., "metadata": ..., "distance": ...}
    """
    question_vector = embed_text(question)

    results = _collection.query(
        query_embeddings=[question_vector],
        n_results=top_k,
    )

    matches = []
    for i in range(len(results["ids"][0])):
        matches.append({
            "code": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return matches


if __name__ == "__main__":
    import sys
    from backend.rag.chunker import chunk_file
    from backend.rag.embeddings import embed_chunks

    if len(sys.argv) < 2:
        print("Usage: python -m backend.rag.vectorstore <fichier.py|.js> <question>")
        sys.exit(1)

    chunks = chunk_file(sys.argv[1])
    chunks = embed_chunks(chunks)
    store_chunks(chunks)
    print(f"{len(chunks)} chunk(s) stocké(s).")

    if len(sys.argv) > 2:
        question = sys.argv[2]
        results = search(question, top_k=3)
        print(f"\nRésultats pour : '{question}'")
        for r in results:
            print(f"- {r['metadata']['name']} ({r['metadata']['type']}, distance={r['distance']:.3f})")