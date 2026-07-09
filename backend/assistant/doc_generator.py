
from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_and_format
 
_SYSTEM_PROMPT = """Tu es un assistant qui génère de la documentation technique claire pour du
code. On te donne un ou plusieurs extraits de code (fonctions/classes). Pour chacun, génère
une docstring complète (description, paramètres, valeur de retour) dans le style approprié
au langage (docstring style Google pour Python, JSDoc pour JavaScript). Rédige les
descriptions en français, mais garde la syntaxe standard de docstring/JSDoc."""
 
 
def generate_doc(question: str, top_k: int = 5) -> str:
    """
    Génère la documentation pour le code correspondant à la demande.
    """
    context = retrieve_and_format(question, top_k=top_k)
 
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
 