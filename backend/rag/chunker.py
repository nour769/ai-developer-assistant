"""
Chunking — Semaine 2, Jour 1.

Rôle de ce module :
Transformer le résultat du parsing (fonctions, classes, imports) en
"chunks" — des morceaux de code autonomes, avec leurs métadonnées,
prêts à être transformés en embeddings.

Pourquoi chunker par fonction/classe plutôt que par nombre de
caractères ?
Un LLM comprend mieux "voici une fonction complète" que "voici les
1000 premiers caractères du fichier, qui coupent une fonction en
plein milieu". Chaque chunk doit avoir un sens complet tout seul.

Un chunk ressemble à ça :
{
    "id": "auth.py::login",
    "file": "auth.py",
    "type": "function",
    "name": "login",
    "language": "python",
    "code": "def login(username, password):\n    ...",
    "lineno": 12,
}
"""

from pathlib import Path
from backend.parsing.router import parse_file

_LANGUAGE_BY_EXTENSION = {
    ".py": "python",
    ".js": "javascript",
}


def chunk_file(file_path: str) -> list[dict]:
    """
    Parse un fichier et le découpe en chunks : un chunk par fonction,
    un chunk par classe.

    Retourne une liste de dicts, chacun prêt à être passé à un modèle
    d'embedding.
    """
    parsed = parse_file(file_path)
    language = _LANGUAGE_BY_EXTENSION.get(Path(file_path).suffix, "unknown")
    chunks = []

    for func in parsed["functions"]:
        chunks.append({
            "id": f"{file_path}::{func['name']}",
            "file": file_path,
            "type": "function",
            "name": func["name"],
            "language": language,
            "code": func["source"],
            "lineno": func["lineno"],
        })

    for cls in parsed["classes"]:
        chunks.append({
            "id": f"{file_path}::{cls['name']}",
            "file": file_path,
            "type": "class",
            "name": cls["name"],
            "language": language,
            "code": cls["source"],
            "lineno": cls["lineno"],
            "methods": cls["methods"],
        })

    return chunks


def chunk_project(files_info: list[dict]) -> list[dict]:
    """
    Prend la liste de fichiers retournée par scan_project() (loader.py)
    et chunk chacun d'entre eux.

    files_info : liste de dicts avec au moins une clé "path"
    (c'est exactement ce que retourne scan_project()).
    """
    all_chunks = []
    for file_info in files_info:
        try:
            chunks = chunk_file(file_info["path"])
            all_chunks.extend(chunks)
        except (SyntaxError, ValueError) as e:
            # Un fichier mal formé ne doit pas bloquer tout le pipeline
            print(f"Attention : impossible de parser {file_info['path']} ({e})")

    return all_chunks


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python -m backend.rag.chunker <fichier.py|fichier.js>")
        sys.exit(1)

    result = chunk_file(sys.argv[1])
    print(f"{len(result)} chunk(s) trouvé(s) :\n")
    for chunk in result:
        print(f"- [{chunk['type']}] {chunk['name']} (ligne {chunk['lineno']}, {chunk['language']})")