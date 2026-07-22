
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_context, AUCUN_CONTEXTE_PERTINENT
 
_SYSTEM_PROMPT = """Tu es un assistant qui aide un développeur à retrouver du code dans un projet.
On te donne une liste de résultats de recherche (chunks de code) trouvés par similarité sémantique
pour une question donnée. Pour CHAQUE résultat, indique en une phrase pourquoi il est pertinent
ou non par rapport à la question. Réponds en français, sous forme de liste concise et numérotée.

✨ FORMATAGE FANCY POUR RÉSULTATS:
Quand tu listes des résultats trouvés, utilise des CADRES pour les SURLIGHER:

1. ┌─────────────────────────┐
   │ **nom_fonction()**      │
   │ [fichier:ligne]        │
   │ Pourquoi c'est pertinent│
   └─────────────────────────┘

Cela rend les résultats CLAIRS et VISIBLES pour l'utilisateur!

IMPORTANT SUR LES CITATIONS :
Ne répète pas la même citation [fichier:ligne] à chaque phrase si elle provient du même
bloc de code déjà cité juste avant. Cite une source une fois par bloc de code distinct.

IMPORTANT : Tu ne dois JAMAIS répondre à la question de l'utilisateur elle-même avec tes
connaissances générales, même si tu la connais. Ton seul rôle est d'évaluer la pertinence
des résultats de code par rapport à la question. Si aucun résultat n'est pertinent, dis-le
et arrête-toi là -- ne fournis aucune information supplémentaire hors du code fourni."""
 
 
def search(question: str, top_k: int = 20) -> str:
    """
    Recherche naturelle dans le projet.
    
    IMPORTANT: Utilise max_distance=2.0 comme recommend() pour capturer
    les résultats génériques. Les recherches sémantiques sur des questions
    génériques ("password authentication") ont des distances plus élevées.
    """
    # Validation : question non vide
    if not question or not question.strip():
        return "Merci de poser une question."
    
    # Permissif: max_distance=2.0 pour capturer les résultats génériques
    # Limite à 5 pour éviter les timeouts
    matches = retrieve_context(question, top_k=5, max_distance=2.0)
 
    if not matches or (len(matches) == 1 and matches[0] == AUCUN_CONTEXTE_PERTINENT):
        return (
            "Je n'ai trouvé aucun code pertinent dans le projet indexé pour cette recherche. "
            "Reformule ta question ou vérifie qu'un projet a bien été ingéré."
        )
 
    listing = "\n\n".join(
        f"[{i + 1}] {m['metadata']['file']} -- {m['metadata']['type']} `{m['metadata']['name']}` "
        f"(ligne {m['metadata']['lineno']})\n{m['code']}"
        for i, m in enumerate(matches)
    )
 
    prompt = f"""Question de recherche : {question}
 
Résultats trouvés :
 
{listing}
 
Pour chaque résultat numéroté, explique en une phrase pourquoi il correspond à la recherche."""
 
    return call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.2)
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.search <question>")
        sys.exit(1)
 
    print(search(" ".join(sys.argv[1:])))