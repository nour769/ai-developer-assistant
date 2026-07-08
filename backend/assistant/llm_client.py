"""
Client LLM — point d'entrée UNIQUE pour parler à Groq.

Pourquoi isoler ça dans une seule fonction ?
- Si demain on te demande de passer sur un LLM local (question de
  confidentialité, cf. Q4 posée à ton encadrant), tu changes CE fichier
  uniquement. Aucun autre module du projet ne doit appeler Groq
  directement.
"""

from groq import Groq
from backend.config import GROQ_API_KEY, GROQ_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt: str, system_prompt: str = "", temperature: float = 0.2) -> str:
    """
    Envoie un prompt au LLM et retourne la réponse texte.

    temperature basse (0.2) car on veut des réponses factuelles et
    stables sur du code, pas de la créativité.
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    response = _client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content
