from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_context, format_context

_SYSTEM_PROMPT = """Tu es un expert en analyse de code. Tu expliques le code de manière PRÉCISE et FACTUELLE.

RÈGLES ABSOLUES (NON NÉGOCIABLES) :
1. Réponds UNIQUEMENT avec le code du contexte fourni.
2. JAMAIS de code inventé. JAMAIS de suppositions sur du code qui n'est pas là.
3. Chaque affirmation DOIT être tracée à une ligne du code fourni : [fichier:ligne]
4. Si le contexte est insuffisant ou non pertinent, dis-le explicitement : « Contexte insuffisant pour répondre. »
5. Ne pas utiliser les connaissances générales — seulement le code fourni.

FORMAT DE RÉPONSE (OBLIGATOIRE) :
## 📖 Résumé
[1-2 phrases max : LE BUT du code]

## 🔧 Comment ça marche
[Numéroté : les étapes clés du code, avec références exactes aux lignes]

## ⚠️ Points clés
[Liste à puces : ce qui importe vraiment]

## 📍 Sources
[Références précises : [fichier:ligne] pour chaque affirmation]

QUALITÉ : Préfère être incomplet mais exact qu'complet mais faux."""

def _is_chunk_relevant(chunk: dict, question: str) -> bool:
    """
    Vérifie si un chunk est réellement pertinent pour la question.
    Évite d'expliquer du code complètement hors sujet.
    """
    if not chunk or not chunk.get("metadata"):
        return False
    
    meta = chunk.get("metadata", {})
    code = chunk.get("code", "").lower()
    name = meta.get("name", "").lower()
    chunk_type = meta.get("type", "").lower()
    question_lower = question.lower()
    
    # Extrait les mots-clés principaux de la question
    # Exemple: "que fait la fonction login" -> ["fonction", "login"]
    question_words = [w.strip() for w in question_lower.split() if len(w.strip()) > 2]
    
    # Le nom du chunk DOIT contenir au moins un mot clé de la question
    name_match = any(word in name for word in question_words)
    
    # OU le type (function/class) doit être explicitement demandé
    if "fonction" in question_lower or "function" in question_lower:
        type_match = chunk_type == "function"
    elif "classe" in question_lower or "class" in question_lower:
        type_match = chunk_type == "class"
    else:
        type_match = True  # Accepte tous les types si pas spécifié
    
    # Le code lui-même doit contenir des mots clés
    code_match = any(word in code for word in question_words)
    
    # Pertinent si : (le nom correspond OU le type correspond) ET le code contient des mots clés
    is_relevant = (name_match or type_match) and code_match
    
    return is_relevant

def explain(question: str, top_k: int = 20) -> str:
    """
    Explique un bout de code en langage naturel avec certitude totale.
    
    Valide que le contexte existe et est VRAIMENT pertinent avant de répondre.
    """
    matches = retrieve_context(question, top_k=top_k)
    
    # Filtre les résultats pour garder UNIQUEMENT les chunks pertinents
    relevant_matches = [m for m in matches if _is_chunk_relevant(m, question)]
    
    # Validation : le contexte doit contenir du code pertinent
    if not relevant_matches:
        return f"""❌ **Impossible d'expliquer**

Je n'ai pas trouvé de code pertinent pour ta question : **"{question}"**

**Suggestions :**
1. Assure-toi que ton projet est correctement uploadé
2. Essaie avec le **nom exact** de la fonction/classe (ex: "login", "authenticate", etc.)
3. Reformule ta question de manière plus spécifique
4. Utilise le bouton "Vue d'ensemble" pour voir la structure du projet

**Exemple de question valide :**
- "Que fait la fonction est_tdr ?"
- "Explique la classe Retriever"
- "Montre-moi comment fonctionne le chunker"
"""
    
    # Garde les meilleurs résultats (max 5 pour ne pas diluer)
    best_matches = relevant_matches[:5]
    context = format_context(best_matches)
    
    prompt = f"""Tu vas expliquer du code de manière PRÉCISE et TRAÇABLE.

CODE À EXPLIQUER (trouvé dans le projet) :
{context}

QUESTION DE L'UTILISATEUR : {question}

Respecte TOUJOURS le format ci-dessus.
"""
    
    response = call_llm(_SYSTEM_PROMPT, prompt, temperature=0.1)
    return response


if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.explain <question>")
        sys.exit(1)
 
    print(explain(" ".join(sys.argv[1:])))