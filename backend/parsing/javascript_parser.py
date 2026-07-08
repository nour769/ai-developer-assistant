
from pathlib import Path
import tree_sitter_javascript as tsjs
from tree_sitter import Language, Parser

_JS_LANGUAGE = Language(tsjs.language())
_parser = Parser(_JS_LANGUAGE)


def parse_javascript_file(file_path: str) -> dict:
    """
    Parse un fichier JavaScript et retourne sa structure :
    - functions: liste de {name, source, lineno}
    - classes: liste de {name, methods, lineno}
    - imports: liste de noms de modules importés
    """
    source_bytes = Path(file_path).read_bytes()
    tree = _parser.parse(source_bytes)
    root = tree.root_node

    functions = []
    classes = []
    imports = []

    def get_text(node) -> str:
        return source_bytes[node.start_byte:node.end_byte].decode("utf-8")

    def walk(node):
        if node.type == "function_declaration":
            name_node = node.child_by_field_name("name")
            functions.append({
                "name": get_text(name_node) if name_node else "<anonymous>",
                "source": get_text(node),
                "lineno": node.start_point[0] + 1,
            })

        elif node.type == "variable_declarator":
            value_node = node.child_by_field_name("value")
            name_node = node.child_by_field_name("name")
            if value_node and value_node.type == "arrow_function":
                functions.append({
                    "name": get_text(name_node) if name_node else "<anonymous>",
                    "source": get_text(node),
                    "lineno": node.start_point[0] + 1,
                })

        elif node.type == "class_declaration":
            name_node = node.child_by_field_name("name")
            methods = []
            body_node = node.child_by_field_name("body")
            if body_node:
                for child in body_node.children:
                    if child.type == "method_definition":
                        method_name = child.child_by_field_name("name")
                        if method_name:
                            methods.append(get_text(method_name))

            classes.append({
                "name": get_text(name_node) if name_node else "<anonymous>",
                "source": get_text(node),
                "methods": methods,
                "lineno": node.start_point[0] + 1,
            })

        elif node.type == "import_statement":
            source_node = node.child_by_field_name("source")
            if source_node:
                imports.append(get_text(source_node).strip("'\""))

        elif node.type == "call_expression":
            fn_node = node.child_by_field_name("function")
            if fn_node and get_text(fn_node) == "require":
                args_node = node.child_by_field_name("arguments")
                if args_node and args_node.named_child_count > 0:
                    imports.append(get_text(args_node.named_children[0]).strip("'\""))

        for child in node.children:
            walk(child)

    walk(root)

    return {
        "file": file_path,
        "functions": functions,
        "classes": classes,
        "imports": imports,
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m backend.parsing.javascript_parser <fichier.js>")
        sys.exit(1)

    result = parse_javascript_file(sys.argv[1])
    print(f"Fichier : {result['file']}")
    print(f"Fonctions : {[f['name'] for f in result['functions']]}")
    print(f"Classes : {[c['name'] for c in result['classes']]}")
    print(f"Imports : {result['imports']}")