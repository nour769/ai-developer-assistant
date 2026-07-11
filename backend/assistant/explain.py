 
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_and_format
 
_SYSTEM_PROMPT = """Tu es un assistant expert en revue de code, intégré à un outil interne d'entreprise.
Tu réponds UNIQUEMENT à partir du contexte de code fourni ci-dessous. Si le contexte ne
contient pas assez d'information pour répondre, dis-le clairement au lieu d'inventer.

IMPORTANT : Si la question posée n'a aucun rapport avec le développement logiciel ou le code
fourni, indique-le clairement et arrête-toi là -- n'explique PAS le code par défaut, et ne
réponds jamais avec des connaissances générales hors du périmètre du code.
git
Réponds en français, de façon claire et structurée, pour un développeur qui découvre ce code."""
 
 
def explain(question: str, top_k: int = 5) -> str:
    """
    Explique un bout de code en langage naturel.
 
    top_k=5 par défaut : assez large pour donner du contexte au LLM
    (ex: une fonction qui en appelle une autre) sans noyer le prompt.
    """
    context = retrieve_and_format(question, top_k=top_k)
 
    prompt = f"""Contexte (code du projet) :
 
{context}
 
Question de l'utilisateur : {question}
 
Explique ce code de façon claire : à quoi il sert, comment il fonctionne,
et signale s'il y a des points notables (paramètres importants, effets de bord)."""
 
    return call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.2)
 
 
if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.explain <question>")
        sys.exit(1)
 
    print(explain(" ".join(sys.argv[1:])))