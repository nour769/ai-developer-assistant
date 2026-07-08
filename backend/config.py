"""
Configuration centralisée du projet.

Pourquoi un fichier config.py dédié ?
- Toutes les variables sensibles (clés API) et paramètres modifiables
  sont à un seul endroit.
- Si tu changes de LLM provider un jour (Groq -> autre chose), tu ne
  touches qu'ici, pas dans 10 fichiers différents.
"""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "data/vectorstore")

# Extensions de fichiers qu'on analyse (semaine 1 : Python seulement,
# tu pourras étendre cette liste plus tard)
SUPPORTED_EXTENSIONS = {".py"}

# Dossiers/fichiers à ignorer pendant l'ingestion
IGNORED_DIRS = {
    ".git", "node_modules", "venv", "__pycache__",
    ".idea", ".vscode", "dist", "build", ".pytest_cache",
}
