
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_and_format, AUCUN_CONTEXTE_PERTINENT
 
_SYSTEM_PROMPT = """Tu es un assistant qui génère de la documentation technique claire pour du code.
On te donne un ou plusieurs extraits de code (fonctions/classes). Pour chacun, génère
une docstring complète (description, paramètres, valeur de retour) dans le style approprié
au langage (docstring style Google pour Python, JSDoc pour JavaScript).

Règles de sortie :
- Donne la docstring entière dans le style adéquat (Google/JSDoc), prête à être collée.
- Pour chaque paramètre, fournis : nom, type estimé (si identifiable), description concise.
- Si un type ne peut pas être déterminé, écris `type: unknown` et demande une précision.
- Ajoute un court **Exemple d'utilisation** si possible.
- Cite la source en fin de réponse sous la forme `[chemin/vers/fichier:numero_de_ligne]`.

✨ FORMATAGE FANCY POUR CODE:
Quand tu mentionnes une FONCTION ou CLASS EXACTE, utilise un CADRE:

┌────────────────────────────────┐
│ **nom_fonction() / NomClass**  │
│ [fichier:ligne]               │
│ Signature et détails...        │
└────────────────────────────────┘

Rédige les descriptions en français, mais garde la syntaxe standard de docstring/JSDoc.

IMPORTANT SUR LES CITATIONS :
Ne répète pas la même citation [fichier:ligne] à chaque phrase si elle provient du même
bloc de code déjà cité juste avant. Cite une source une fois par bloc de code distinct."""
 
 
def generate_doc(question: str, top_k: int = 20) -> str:
    """
    Génère la documentation pour le code correspondant à la demande.
    """
    # Validation : question non vide
    if not question or not question.strip():
        return "Merci de poser une question."
    
    context = retrieve_and_format(question, top_k=top_k)
    
    # Vérification : contexte pertinent trouvé?
    if context == AUCUN_CONTEXTE_PERTINENT:
        return (
            "Je n'ai trouvé aucun code pertinent dans le projet indexé pour répondre "
            "à cette question. Reformule ta question ou vérifie qu'un projet a bien été ingéré."
        )
 
    prompt = f"""Code à documenter :
 
{context}
 
Demande : {question}
 
Génère la docstring manquante pour ce code, dans le style adapté au langage."""
 
    return call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.2)
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.doc_generator <demande>")
        sys.exit(1)
 
    print(generate_doc(" ".join(sys.argv[1:])))
 