import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"
import uuid
import chromadb
from backend.config import VECTORSTORE_PATH
from backend.rag.embeddings import embed_text

# File used to persist the name of the active collection (avoids accidental reuse)
_ACTIVE_COLLECTION_FILE = os.path.join(VECTORSTORE_PATH, "active_collection.txt")

_client = chromadb.PersistentClient(path=VECTORSTORE_PATH)


def _load_active_collection_name() -> str:
    try:
        with open(_ACTIVE_COLLECTION_FILE, "r", encoding="utf-8") as f:
            name = f.read().strip()
            if name:
                return name
    except Exception:
        pass
    return "code_chunks"


def _persist_active_collection_name(name: str) -> None:
    try:
        os.makedirs(VECTORSTORE_PATH, exist_ok=True)
        with open(_ACTIVE_COLLECTION_FILE, "w", encoding="utf-8") as f:
            f.write(name)
    except Exception:
        # Pas critique; on continue en mémoire uniquement.
        pass


# Initialise la collection active (peut être changée par reset_collection)
_collection_name = _load_active_collection_name()
_collection = _client.get_or_create_collection(_collection_name)


def reset_collection() -> str:
    """
    Crée une NOUVELLE collection dédiée au prochain projet et renvoie
    son nom. L'ancienne collection est supprimée si possible.

    Retourne le nom de la nouvelle collection (utile pour le frontend
    si vous souhaitez conserver un project_id explicite).
    """
    global _collection, _collection_name

    # Génère un nom unique pour éviter tout chevauchement entre projets
    new_name = f"code_chunks_{uuid.uuid4().hex[:8]}"

    # Tenter de supprimer l'ancienne collection proprement
    try:
        _client.delete_collection(_collection_name)
    except Exception:
        pass

    # Crée (ou récupère) la nouvelle collection et persiste son nom
    _collection = _client.get_or_create_collection(new_name)
    _collection_name = new_name
    _persist_active_collection_name(new_name)

    return new_name


def set_active_collection(name: str) -> None:
    """Force l'utilisation d'une collection existante (utile pour tests)."""
    global _collection, _collection_name
    _collection = _client.get_or_create_collection(name)
    _collection_name = name
    _persist_active_collection_name(name)


def get_active_collection_name() -> str:
    return _collection_name


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