"""
Ingestion — Jour 1-2 de la semaine 1.

Rôle de ce module :
1. Extraire un projet .zip uploadé
2. Parcourir récursivement le dossier extrait
3. Retourner la liste des fichiers pertinents (en filtrant .git,
   node_modules, venv, etc. — voir IGNORED_DIRS dans config.py)

C'est la toute première brique du pipeline :
    ZIP -> [ce module] -> liste de fichiers -> parsing -> chunking -> ...
"""

import zipfile
from pathlib import Path
from backend.config import IGNORED_DIRS, SUPPORTED_EXTENSIONS


def extract_project(zip_path: str, destination: str) -> Path:
    """Extrait un zip de projet vers un dossier de destination."""
    zip_path = Path(zip_path)
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(destination)

    return destination


def scan_project(project_path: str) -> list[dict]:
    """
    Parcourt récursivement le projet et retourne la liste des fichiers
    pertinents avec leurs métadonnées de base.

    Retourne une liste de dicts :
    [{"path": ..., "filename": ..., "extension": ..., "size_bytes": ...}, ...]
    """
    project_path = Path(project_path)
    files_info = []

    for file_path in project_path.rglob("*"):
        # Ignorer les dossiers non pertinents (n'importe quel niveau)
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue

        if not file_path.is_file():
            continue

        if file_path.suffix not in SUPPORTED_EXTENSIONS:
            continue

        files_info.append({
            "path": str(file_path),
            "filename": file_path.name,
            "extension": file_path.suffix,
            "size_bytes": file_path.stat().st_size,
        })

    return files_info


if __name__ == "__main__":
    # Petit test manuel : lance `python -m backend.ingestion.loader`
    # après avoir mis un zip de test dans data/uploads/
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m backend.ingestion.loader <chemin_vers_zip>")
        sys.exit(1)

    extracted = extract_project(sys.argv[1], "data/uploads/extracted")
    files = scan_project(extracted)
    print(f"{len(files)} fichiers trouvés :")
    for f in files:
        print(f"  - {f['path']} ({f['size_bytes']} octets)")
