
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_context
 
_SYSTEM_PROMPT = """Tu es un assistant qui aide un développeur à retrouver du code dans un projet.
On te donne une liste de résultats de recherche (chunks de code) trouvés par similarité sémantique
pour une question donnée. Pour CHAQUE résultat, indique en une phrase pourquoi il est pertinent
ou non par rapport à la question. Réponds en français, sous forme de liste concise et numérotée.

IMPORTANT : Tu ne dois JAMAIS répondre à la question de l'utilisateur elle-même avec tes
connaissances générales, même si tu la connais. Ton seul rôle est d'évaluer la pertinence
des résultats de code par rapport à la question. Si aucun résultat n'est pertinent, dis-le
et arrête-toi là -- ne fournis aucune information supplémentaire hors du code fourni."""
 
 
def search(question: str, top_k: int = 20) -> str:
    """
    Recherche naturelle dans le projet.
 
    On garde les chunks bruts (retrieve_context, pas retrieve_and_format)
    car on a besoin de les numéroter nous-mêmes avant de les passer au
    LLM -- format_context() ne numérote pas, il est pensé pour explain/
    doc/recommend qui traitent le contexte comme un seul bloc.
    """
    matches = retrieve_context(question, top_k=top_k)
 
    if not matches:
        return "Aucun résultat trouvé dans le projet pour cette recherche."
 
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