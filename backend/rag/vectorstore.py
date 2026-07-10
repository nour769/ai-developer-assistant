
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import chromadb
from backend.config import VECTORSTORE_PATH
from backend.rag.embeddings import embed_text
 
_client = chromadb.PersistentClient(path=VECTORSTORE_PATH)
_collection = _client.get_or_create_collection("code_chunks")
def reset_collection() -> None:
    """
    Supprime et recrée la collection Chroma.

    Nécessaire avant chaque nouvelle ingestion (mono-utilisateur) pour
    éviter de mélanger les chunks de deux projets différents. Réassigne
    la variable globale _collection -- sinon store_chunks()/search()
    continueraient d'utiliser une référence vers une collection supprimée.
    """
    global _collection
    try:
        _client.delete_collection("code_chunks")
    except Exception:
        pass
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
 
 
def get_all_chunks() -> list[dict]:
    """
    Retourne TOUS les chunks stockés dans la collection, sans
    recherche par similarité.
 
    Nécessaire pour "overview" : contrairement à explain/search/doc/
    recommend qui répondent à une question précise (donc un sous-
    ensemble pertinent de chunks suffit), overview doit voir
    l'ensemble du projet pour en décrire l'architecture globale.
 
    Retourne une liste de dicts : {"id": ..., "code": ..., "metadata": ...}
    (pas de "distance" ici, puisqu'il n'y a pas de comparaison à une
    question -- ça n'aurait pas de sens).
    """
    results = _collection.get(include=["documents", "metadatas"])
 
    chunks = []
    for i in range(len(results["ids"])):
        chunks.append({
            "id": results["ids"][i],
            "code": results["documents"][i],
            "metadata": results["metadatas"][i],
        })
    return chunks
 
 
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