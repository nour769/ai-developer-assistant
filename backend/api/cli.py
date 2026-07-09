 
import click
 
from backend.ingestion.loader import extract_project, scan_project
from backend.rag.chunker import chunk_project
from backend.rag.embeddings import embed_chunks
from backend.rag.vectorstore import store_chunks
 
from backend.assistant.explain import explain as explain_fn
from backend.assistant.search import search as search_fn
from backend.assistant.overview import overview as overview_fn
from backend.assistant.doc_generator import generate_doc
from backend.assistant.recommend import recommend as recommend_fn
 
 
@click.group()
def cli():
    """Assistant IA pour développeurs -- CLI de test."""
    pass
 
 
@cli.command()
@click.argument("path")
def ingest(path):
    """Ingère un projet (dossier ou zip) : parse, chunk, embed, stocke dans Chroma."""
    if path.endswith(".zip"):
        path = extract_project(path)
 
    files_info = scan_project(path)
    click.echo(f"{len(files_info)} fichier(s) trouvé(s).")
 
    chunks = chunk_project(files_info)
    click.echo(f"{len(chunks)} chunk(s) générés.")
 
    chunks = embed_chunks(chunks)
    store_chunks(chunks)
    click.echo("Chunks stockés dans la base vectorielle.")
 
 
@cli.command()
@click.argument("question")
def explain(question):
    """Explique un bout de code."""
    click.echo(explain_fn(question))
 
 
@cli.command()
@click.argument("question")
def search(question):
    """Recherche naturelle dans le projet."""
    click.echo(search_fn(question))
 
 
@cli.command()
def overview():
    """Vue d'ensemble du projet entier."""
    click.echo(overview_fn())
 
 
@cli.command()
@click.argument("question")
def doc(question):
    """Génère la documentation manquante pour un bout de code."""
    click.echo(generate_doc(question))
 
 
@cli.command()
@click.argument("question")
def recommend(question):
    """Recommandations : optimisation, best practices, vulnérabilités."""
    click.echo(recommend_fn(question))
 
 
if __name__ == "__main__":
    cli()
 