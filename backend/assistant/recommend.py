
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_and_format
 
_SYSTEM_PROMPT = """Tu es un assistant de revue de code expert, intégré à un outil interne
d'entreprise. Pour le code fourni, analyse-le selon TROIS axes précis, et uniquement ces
trois axes :
1. Optimisation (performance, complexité, redondance)
2. Best practices (lisibilité, nommage, structure, gestion d'erreurs)
3. Vulnérabilités (sécurité : injections, secrets en dur, mauvaise gestion des entrées)
 
Pour chaque axe, si tu ne trouves rien à signaler, dis-le explicitement plutôt que
d'inventer un problème qui n'existe pas. Ne fais AUCUNE supposition hors de ce qui est
visible dans le code fourni. Réponds en français, structuré par les 3 axes ci-dessus."""
 
 
def recommend(question: str, top_k: int = 3) -> str:
    """
    Analyse le code correspondant à la question et retourne des
    recommandations sur les 3 axes.
 
    top_k volontairement plus bas (3) que les autres fonctionnalités
    (5) : on veut cibler PRÉCISÉMENT le fichier/la fonction demandée
    pour une analyse approfondie, pas balayer large comme "search".
    """
    context = retrieve_and_format(question, top_k=top_k)
 
    prompt = f"""Code à analyser :
 
{context}
 
Cible demandée : {question}
 
Analyse ce code selon les 3 axes (optimisation, best practices, vulnérabilités)."""
 
    return call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.2)
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.recommend <cible>")
        sys.exit(1)
 
    print(recommend(" ".join(sys.argv[1:])))