from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_context, format_context, AUCUN_CONTEXTE_PERTINENT
from backend.rag.vectorstore import get_active_collection_name, get_collection_count

_SYSTEM_PROMPT = """Tu es un expert en analyse de code. Tu expliques le code de manière PRÉCISE et FACTUELLE.

RÈGLES ABSOLUES (NON NÉGOCIABLES) :
1. Réponds UNIQUEMENT avec le code du contexte fourni.
2. JAMAIS de code inventé. JAMAIS de suppositions sur du code qui n'est pas là.
3. Chaque affirmation DOIT être tracée à une ligne du code fourni : [fichier:ligne]
4. Si le contexte est insuffisant ou non pertinent, dis-le explicitement : « Contexte insuffisant pour répondre. »
5. Ne pas utiliser les connaissances générales — seulement le code fourni.
6. Ne répète pas la même citation [fichier:ligne] à chaque phrase si elle provient du même bloc de code
   déjà cité juste avant. Cite une source une fois par bloc de code distinct.

✨ FORMATAGE FANCY POUR CODE EXACTE:
Quand tu mentionnes une FONCTION, CLASS, ou CODE EXACTE:
- Mets le nom en **GRAS**: **fonction_name()**
- Ajoute une référence précise: [fichier:ligne]
- Utilise un CADRE pour le SURLIGHER:

┌────────────────────────────┐
│ **fonction_exacte()**      │
│ [fichier:ligne]           │
│ Détail ou explication      │
└────────────────────────────┘

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
    Vérifie si un chunk est pertinent pour la question.
    
    STRATÉGIE (3 niveaux) :
    1. Strict match: nom du chunk + type + code contiennent les mots-clés
    2. Flexible match: un des 3 critères suffit
    3. Fallback: accepter tous les chunks (pour questions larges)
    """
    if not chunk or not chunk.get("metadata"):
        return False
    
    meta = chunk.get("metadata", {})
    code = chunk.get("code", "").lower()
    name = meta.get("name", "").lower()
    chunk_type = meta.get("type", "").lower()
    question_lower = question.lower()
    
    # Extraction des mots-clés (min 2 caractères)
    question_words = [w.strip() for w in question_lower.split() if len(w.strip()) > 2]
    
    if not question_words:
        # Question trop vague -> accepter tous les chunks
        return True
    
    # 3 critères de pertinence
    name_match = any(word in name for word in question_words)
    code_match = any(word in code for word in question_words)
    type_match = any(qword in chunk_type for qword in question_words)
    
    # STRATÉGIE :
    # - Si la question est spécifique (demande une fonction/classe), être strict
    # - Si la question est large (générale), être flexible
    
    is_specific_question = any(keyword in question_lower for keyword in [
        "fonction", "function", "classe", "class", "méthode", "method"
    ])
    
    if is_specific_question:
        # Mode strict : au moins 2 critères doivent être vrais
        return (name_match + code_match + type_match) >= 2
    else:
        # Mode flexible : au moins 1 critère suffit
        return name_match or code_match or type_match

def explain(question: str, top_k: int = 20) -> str:
    """
    Explique un bout de code en langage naturel.
    
    IMPORTANT: Utilise max_distance=2.0 comme recommend() et search()
    pour capturer les résultats génériques.
    """
    # Validation : question non vide
    if not question or not question.strip():
        return "Merci de poser une question."
    
    # Permissif: max_distance=2.0 pour capturer les résultats génériques
    matches = retrieve_context(question, top_k=top_k, max_distance=2.0)
    
    # Filtre les résultats pour garder les chunks pertinents
    relevant_matches = [m for m in matches if _is_chunk_relevant(m, question)]
    
    # Vérification explicite : contexte pertinent trouvé?
    if not relevant_matches:
        return (
            "Je n'ai trouvé aucun code pertinent dans le projet indexé pour répondre "
            "à cette question. Reformule ta question ou vérifie qu'un projet a bien été ingéré."
        )
    
    # FALLBACK 1 : Si des chunks pertinents existent
    if relevant_matches:
        best_matches = relevant_matches[:5]  # Max 5 chunks
        context = format_context(best_matches)
        prompt = f"""Tu vas expliquer du code de manière PRÉCISE et TRAÇABLE.

CODE À EXPLIQUER (trouvé dans le projet) :
{context}

QUESTION DE L'UTILISATEUR : {question}

Respecte TOUJOURS le format ci-dessus.
"""
        response = call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.1)
        return response
    
    # FALLBACK 2 : Aucun chunk pertinent trouvé, mais on a du contexte général
    if matches:
        context = format_context(matches[:3])
        prompt = f"""L'utilisateur a posé une question générale : "{question}"

Je n'ai pas trouvé de code spécifiquement pertinent, mais voici du contexte du projet :

{context}

Utilise ce contexte pour répondre de manière générale et honnête.
Si tu n'as vraiment pas assez d'infos, dis-le explicitement.
"""
        response = call_llm(prompt, system_prompt=_SYSTEM_PROMPT, temperature=0.3)
        return response
    
    # FALLBACK 3 : Aucun match du tout
    # Vérifier si la collection est vide ou s'il y a vraiment un problème
    active_collection = get_active_collection_name()
    chunk_count = get_collection_count(active_collection)
    
    if chunk_count == 0:
        return f"""❌ **Aucun code chargé**

La collection active est **vide** ({active_collection}).

**Que faire :**
1. Retourne à la liste des projets (sidebar gauche)
2. Clique sur un projet existant → "Activer"
3. Ou upload un **nouveau projet** (.zip)
4. Vérifie que le .zip contient des fichiers .py ou .js

**Note:** Si tu as activé un projet mais ça dit vide:
- Le projet peut être corrompu
- Réupload-le et ça devrait marcher
"""
    
    return f"""❌ **Contexte insuffisant**

Je n'ai trouvé aucun code pertinent pour : **"{question}"**

Je dois avoir:
- 1. Un projet actif avec du code ✓ ({chunk_count} chunks trouvés)
- 2. Une question qui correspond à du code dans le projet ✗

**Suggestions :**
1. Réformule avec le **nom exact** d'une fonction/classe
2. Essaie une question plus générale
3. Utilise "Vue d'ensemble" pour voir les structures disponibles

**Exemples :**
- "Que fait la fonction authenticate ?"
- "Explique la classe UserService"
- "Comment fonctionne le RAG ?"
"""


if __name__ == "__main__":
    import sys
 
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.explain <question>")
        sys.exit(1)
 
    print(explain(" ".join(sys.argv[1:])))