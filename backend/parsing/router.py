
from pathlib import Path
from backend.parsing.python_parser import parse_python_file
from backend.parsing.javascript_parser import parse_javascript_file

_PARSERS = {
    ".py": parse_python_file,
    ".js": parse_javascript_file,
}


def parse_file(file_path: str) -> dict:
    """Choisit le bon parser selon l'extension du fichier et l'exécute."""
    extension = Path(file_path).suffix

    parser_fn = _PARSERS.get(extension)
    if parser_fn is None:
        raise ValueError(f"Aucun parser disponible pour l'extension '{extension}'")

    return parser_fn(file_path)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m backend.parsing.router <fichier.py|fichier.js>")
        sys.exit(1)

    result = parse_file(sys.argv[1])
    print(f"Fichier : {result['file']}")
    print(f"Fonctions : {[f['name'] for f in result['functions']]}")
    print(f"Classes : {[c['name'] for c in result['classes']]}")
    print(f"Imports : {result['imports']}")