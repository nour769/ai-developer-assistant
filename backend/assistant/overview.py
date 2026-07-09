 
from collections import defaultdict
 
from backend.assistant.llm_client import call_llm
from backend.rag.vectorstore import get_all_chunks
 
_SYSTEM_PROMPT = """Tu es un assistant qui aide un développeur à comprendre rapidement
l'architecture d'un projet de code qu'il découvre. Tu reçois la liste structurée des
fichiers, classes et fonctions du projet (sans le code complet, pour rester concis).
Réponds en français avec une vue d'ensemble claire : à quoi sert probablement le projet,
comment il est organisé, et quels semblent être les modules/fichiers principaux."""
 
 
def overview() -> str:
    """
    Génère une vue d'ensemble du projet entier, à partir des
    métadonnées de TOUS les chunks stockés.
    """
    chunks = get_all_chunks()
 
    if not chunks:
        return "Aucun code indexé pour le moment. Ingère un projet d'abord."
 
    by_file = defaultdict(list)
    for chunk in chunks:
        meta = chunk["metadata"]
        by_file[meta["file"]].append(f"{meta['type']} {meta['name']} (ligne {meta['lineno']})")
 
    structure = "\n".join(
        f"- {file} :\n  " + "\n  ".join(items)
        for file, items in sorted(by_file.items())
    )
 
    prompt = f"""Voici la structure du projet ({len(chunks)} éléments répartis sur {len(by_file)} fichiers) :
 
{structure}
 
Donne une vue d'ensemble du projet : son objectif probable, son organisation générale,
et les modules qui semblent centraux."""
 
    return call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.3)
 
 
if __name__ == "__main__":
    print(overview())
 