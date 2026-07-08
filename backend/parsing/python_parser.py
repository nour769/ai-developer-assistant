"""
Parsing AST — Jour 4-5 de la semaine 1.

Rôle de ce module :
Au lieu de traiter le code comme du texte brut, on le parse avec le
module `ast` (Abstract Syntax Tree) natif de Python pour en extraire
la STRUCTURE : fonctions, classes, imports, avec leur code source exact.

C'est cette étape qui rend le chunking "intelligent" possible en
semaine 2 : on va découper le code par fonction/classe, pas par un
nombre arbitraire de caractères.
"""

import ast
from pathlib import Path


def parse_python_file(file_path: str) -> dict:
    """
    Parse un fichier Python et retourne sa structure :
    - functions: liste de {name, source, lineno}
    - classes: liste de {name, methods, lineno}
    - imports: liste de noms de modules importés
    """
    source = Path(file_path).read_text(encoding="utf-8")
    tree = ast.parse(source, filename=file_path)

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and _is_top_level(node, tree):
            functions.append({
                "name": node.name,
                "source": ast.get_source_segment(source, node),
                "lineno": node.lineno,
            })

        elif isinstance(node, ast.ClassDef):
            methods = [
                n.name for n in node.body
                if isinstance(n, ast.FunctionDef)
            ]
            classes.append({
                "name": node.name,
                "source": ast.get_source_segment(source, node),
                "methods": methods,
                "lineno": node.lineno,
            })

        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module)

    return {
        "file": file_path,
        "functions": functions,
        "classes": classes,
        "imports": imports,
    }


def _is_top_level(node: ast.FunctionDef, tree: ast.Module) -> bool:
    """Évite de compter deux fois les méthodes de classe comme fonctions."""
    return node in tree.body


if __name__ == "__main__":
    # Test manuel sur ce fichier lui-même
    result = parse_python_file(__file__)
    print(f"Fichier : {result['file']}")
    print(f"Fonctions top-level : {[f['name'] for f in result['functions']]}")
    print(f"Classes : {[c['name'] for c in result['classes']]}")
    print(f"Imports : {result['imports']}")
