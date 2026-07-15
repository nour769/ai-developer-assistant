"""
Retriever — Semaine 3, Jour 1.
 
Rôle de ce module :
Faire le pont entre le vector store (recherche par similarité) et
le LLM : préparer un "contexte" texte lisible par le LLM à partir
des chunks trouvés, prêt à être injecté dans un prompt.
 
vectorstore.search() retourne déjà les chunks les plus pertinents
pour une question -- ce module se contente de les mettre en forme,
et sert de point d'entrée UNIQUE pour le retrieval (même logique que
llm_client.py pour le LLM : aucun autre module ne doit importer
vectorstore directement).
"""
 
from backend.rag.vectorstore import search
 
 
def retrieve_context(question: str, top_k: int = 5) -> list[dict]:
    """
    Recherche les chunks les plus pertinents pour une question donnée.
 
    Alias explicite autour de vectorstore.search() -- garder cette
    fonction séparée (plutôt que d'appeler search() partout) permet
    d'ajouter plus tard un filtrage ou un reranking ici, sans toucher
    au reste du code (assistant/*.py).
    """
    return search(question, top_k=top_k)
 
 
def format_context(matches: list[dict]) -> str:
    """
    Transforme une liste de chunks (sortie de retrieve_context) en un
    bloc de texte structuré, prêt à être inséré dans un prompt LLM.
 
    Exemple de sortie pour un chunk :
 
        # Fichier: auth.py -- function `login` (ligne 12)
        def login(username, password):
            ...
 
    On donne systématiquement le fichier, le type, le nom et la ligne
    en en-tête de chaque bloc de code : ça permet au LLM de citer
    précisément d'où vient le code dans sa réponse (utile pour les
    réponses "explain" et "search"), plutôt que de parler dans le
    vide sans référence au fichier source.
    """
    if not matches:
        return "Aucun code pertinent trouvé dans le projet."
 
    blocks = []
    for match in matches:
        meta = match["metadata"]
        dist = match.get("distance")
        dist_str = f" (distance={dist:.3f})" if dist is not None else ""
        header = f"# Fichier: {meta['file']} -- {meta['type']} `{meta['name']}` (ligne {meta['lineno']}){dist_str}"
        blocks.append(f"{header}\n{match['code']}")

    return "\n\n".join(blocks)
 
 
def retrieve_and_format(question: str, top_k: int = 5) -> str:
    """
    Raccourci pratique : recherche + mise en forme en un seul appel.
    C'est cette fonction que les modules assistant/*.py utiliseront
    le plus souvent -- une question entre, un contexte texte sort.
    """
    matches = retrieve_context(question, top_k=top_k)
    return format_context(matches)
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.rag.retriever <question>")
        sys.exit(1)
 
    question = " ".join(sys.argv[1:])
    context = retrieve_and_format(question)
    print(context)
