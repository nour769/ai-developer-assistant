
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_and_format, AUCUN_CONTEXTE_PERTINENT
 
_SYSTEM_PROMPT = """Tu es un assistant de revue de code expert, intégré à un outil interne
d'entreprise. Pour le code fourni, analyse-le selon TROIS axes précis, et uniquement ces
trois axes :
1. Optimisation (performance, complexité, redondance)
2. Best practices (lisibilité, nommage, structure, gestion d'erreurs)
3. Vulnérabilités (sécurité : injections, secrets en dur, mauvaise gestion des entrées)

Pour chaque axe, si tu ne trouves rien à signaler, dis-le explicitement plutôt que
d'inventer un problème qui n'existe pas. Ne fais AUCUNE supposition hors de ce qui est
visible dans le code fourni. Réponds en français, structuré par les 3 axes ci-dessus.

✨ FORMATAGE FANCY POUR CODE EXACTE:
Quand tu mentionnes une FONCTION, CLASS, ou CODE EXACTE, utilise un CADRE pour le SURLIGHER:

┌────────────────────────────┐
│ **nom_fonction()**         │
│ [fichier:ligne]           │
│ Problème ou détail...      │
└────────────────────────────┘

Cela rend le message CLAIR et BEL pour l'utilisateur!

IMPORTANT SUR LES CITATIONS :
Ne répète pas la même citation [fichier:ligne] à chaque phrase si elle provient du même
bloc de code déjà cité juste avant. Cite une source une fois par bloc de code distinct."""
 
 
def recommend(question: str, top_k: int = 20) -> str:
    """
    Analyse le code correspondant à la question et retourne des
    recommandations sur les 3 axes.
    
    IMPORTANT: Pour recommend, utilise max_distance=2.0 car les questions
    génériques ("vulnerabilites", "optimisations") ont des distances sémantiques
    plus élevées (1.4-1.6). Empiriquement: max_distance=2.0 pour 90% coverage.
    """
    # Validation : question non vide
    if not question or not question.strip():
        return "Merci de poser une question."
    
    # Pour recommend, on est TRÈS permissif (distance 2.0)
    # car les questions génériques trouvent des résultats loin
    # Limite à 5 chunks pour éviter les timeouts LLM
    context = retrieve_and_format(question, top_k=5, max_distance=2.0)
    
    # Vérification : contexte pertinent trouvé?
    if context == AUCUN_CONTEXTE_PERTINENT:
        return (
            "Je n'ai trouvé aucun code pertinent dans le projet indexé pour répondre "
            "à cette question. Reformule ta question ou vérifie qu'un projet a bien été ingéré."
        )
 
    prompt = f"""Code à analyser :
 
{context}
 
Cible demandée : {question}
 
Analyse ce code selon les 3 axes (optimisation, best practices, vulnérabilités).

💡 RAPPEL: Quand tu mentionnes une fonction ou code exacte, utilise un CADRE FANCY:
┌────────────────────────┐
│ **fonction_exacte()**  │
│ [fichier:ligne]       │
└────────────────────────┘"""
    
    return call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.2)
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.recommend <cible>")
        sys.exit(1)
 
    print(recommend(" ".join(sys.argv[1:])))