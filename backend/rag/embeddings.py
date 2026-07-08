"""
Embeddings — Semaine 2, Jour 2.

Rôle de ce module :
Transformer du texte (ici, le code d'un chunk) en un vecteur
numérique, grâce à un modèle pré-entraîné (sentence-transformers).

Ce vecteur "représente le sens" du texte : deux textes proches en
signification auront des vecteurs mathématiquement proches, même
s'ils n'utilisent pas les mêmes mots.

Le modèle tourne en LOCAL sur ta machine (téléchargé une seule fois
depuis Hugging Face au premier lancement, puis mis en cache) --
aucune donnée n'est envoyée à un service externe pour cette étape.
"""

from sentence_transformers import SentenceTransformer
from backend.config import EMBEDDING_MODEL

_model = SentenceTransformer(EMBEDDING_MODEL)


def embed_text(text: str) -> list[float]:
    """Transforme un texte en vecteur (liste de nombres flottants)."""
    vector = _model.encode(text)
    return vector.tolist()


def embed_chunks(chunks: list[dict]) -> list[dict]:
    """
    Prend une liste de chunks (sortie de chunker.py) et ajoute à
    chacun son embedding, sous la clé "embedding".
    """
    for chunk in chunks:
        chunk["embedding"] = embed_text(chunk["code"])
    return chunks


if __name__ == "__main__":
    vec = embed_text("def login(username, password): return check(username, password)")
    print(f"Dimension du vecteur : {len(vec)}")
    print(f"Premiers nombres : {vec[:5]}")