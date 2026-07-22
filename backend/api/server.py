"""
Serveur FastAPI -- expose les mêmes fonctions que le CLI, via HTTP.
Aucune logique métier ici : ce fichier ne fait que router les requêtes
vers les fonctions déjà testées (backend/assistant/*, backend/rag/*).
"""

# Désactiver la telemetry de ChromaDB pour éviter les erreurs au démarrage
import os
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

import shutil
import tempfile
import time
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db import init_db, get_db
from backend.services.project_service import ProjectService

from backend.ingestion.loader import extract_project, scan_project
from backend.rag.chunker import chunk_project
from backend.rag.embeddings import embed_chunks
from backend.rag.vectorstore import store_chunks, reset_collection, set_active_collection, get_active_collection_name, get_collection_count

from backend.assistant.explain import explain as explain_fn
from backend.assistant.search import search as search_fn
from backend.assistant.overview import overview as overview_fn
from backend.assistant.doc_generator import generate_doc
from backend.assistant.recommend import recommend as recommend_fn
from backend.assistant.deployment import generate_deployment_architecture

app = FastAPI(title="AI Developer Assistant")

# Autorise le frontend React (Vite, port 5173 par défaut) à appeler cette API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class QuestionRequest(BaseModel):
    question: str
    top_k: int = 50


class DeploymentRequest(BaseModel):
    """Paramètres pour l'architecture de déploiement COMPLÈTE."""
    project_name: str
    service: str = "AWS"  # AWS, Azure, Private
    usage_level: str = "small"  # small, huge
    service_type: str = "web"  # web, job, worker, api, realtime, data_pipeline
    ip_exposure: str = "public"  # public, private, hybrid
    data_type: str = "public"  # public, confidential, mixed
    top_k: int = 20


@app.on_event("startup")
def startup_event():
    """Initialise la base de données au démarrage."""
    init_db()


@app.post("/ingest")
async def ingest(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Reçoit un zip, l'ingère entièrement : parse, chunk, embed, stocke."""
    if not file.filename.endswith(".zip"):
        raise HTTPException(400, "Seuls les fichiers .zip sont acceptés.")

    tmp_dir = tempfile.mkdtemp()
    zip_path = Path(tmp_dir) / file.filename

    with open(zip_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    try:
        start_time = time.time()
        
        extract_dest = Path(tmp_dir) / "extracted"
        project_path = extract_project(str(zip_path), str(extract_dest))
        files_info = scan_project(project_path)

        if not files_info:
            raise HTTPException(400, "Aucun fichier .py/.js supporté trouvé dans le zip.")

        # Crée une nouvelle collection dédiée à ce projet et récupère son id
        project_id = reset_collection()

        chunks = chunk_project(files_info)
        chunks = embed_chunks(chunks)
        store_chunks(chunks)
        
        embedding_time_ms = int((time.time() - start_time) * 1000)
        
        # Enregistre dans la DB
        project_name = file.filename.replace(".zip", "")
        db_project = ProjectService.create_project(
            db,
            name=project_name,
            collection_id=str(project_id),
            description=f"Uploaded: {len(files_info)} files, {len(chunks)} chunks"
        )
        
        # Enregistre l'historique d'indexation
        files_metadata = [
            {
                "path": str(f.get("path", "")),
                "size": f.get("size_bytes", 0)
            }
            for f in files_info
        ]
        ProjectService.save_index_history(
            db,
            project_id=db_project.id,
            files_found=len(files_info),
            chunks_created=len(chunks),
            files_metadata=files_metadata,
            embedding_time_ms=embedding_time_ms
        )

        return {
            "project_id": project_id,
            "files_found": len(files_info),
            "chunks_created": len(chunks),
            "db_project_id": db_project.id,
            "embedding_time_ms": embedding_time_ms
        }
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


@app.post("/explain")
def explain(req: QuestionRequest, db: Session = Depends(get_db)):
    result = explain_fn(req.question, top_k=req.top_k)
    # Enregistre l'analyse dans la BD
    # Note: on n'a pas de project_id courant, donc on le récupère du dernier projet actif
    return {"result": result}


@app.post("/search")
def search(req: QuestionRequest):
    return {"result": search_fn(req.question, top_k=req.top_k)}


@app.post("/doc")
def doc(req: QuestionRequest):
    return {"result": generate_doc(req.question, top_k=req.top_k)}


@app.post("/recommend")
def recommend(req: QuestionRequest):
    return {"result": recommend_fn(req.question, top_k=req.top_k)}


@app.post("/deployment")
def deployment(req: DeploymentRequest, db: Session = Depends(get_db)):
    """
    Génère une architecture de déploiement COMPLÈTE et optimale.
    
    Paramètres:
    - project_name: Nom du projet
    - service: "AWS", "Azure", ou "Private"
    - usage_level: "small" (< 1000 req/day) ou "huge" (> 100k req/day)
    - service_type: "web", "job", "worker", "api", "realtime", "data_pipeline"
    - ip_exposure: "public", "private", ou "hybrid"
    - data_type: "public", "confidential", ou "mixed"
    - top_k: Nombre de chunks à analyser (default: 20)
    
    Retour:
    - Architecture complète avec backup recommendations
    - Coûts estimés par provider
    - Configuration spécifique au service
    - Stratégies HA/DR
    - Sécurité adaptée au type de data
    """
    response = generate_deployment_architecture(
        project_name=req.project_name,
        service=req.service,
        usage_level=req.usage_level,
        service_type=req.service_type,
        ip_exposure=req.ip_exposure,
        data_type=req.data_type,
        top_k=req.top_k
    )
    
    # Enregistre l'analyse générée dans la DB
    # (sera lié au project actif si dispo)
    
    return {
        "result": response,
        "parameters": {
            "service": req.service,
            "usage_level": req.usage_level,
            "service_type": req.service_type,
            "ip_exposure": req.ip_exposure,
            "data_type": req.data_type
        }
    }


@app.get("/overview")
def overview():
    return {"result": overview_fn()}


@app.get("/projects")
def list_projects(db: Session = Depends(get_db), limit: int = 50):
    """Liste tous les projets uploadés."""
    projects = ProjectService.list_projects(db, limit=limit)
    active_collection = get_active_collection_name()
    
    return {
        "total": len(projects),
        "active_collection": active_collection,
        "projects": [
            {
                "id": p.id,
                "name": p.name,
                "uploaded_at": p.uploaded_at.isoformat(),
                "collection_id": p.vectorstore_collection_id,
                "is_active": p.vectorstore_collection_id == active_collection,
                "chunks_count": get_collection_count(p.vectorstore_collection_id)
            }
            for p in projects
        ]
    }


@app.post("/projects/{project_id}/activate")
def activate_project(project_id: int, db: Session = Depends(get_db)):
    """Active un projet existant pour les analyses."""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Projet non trouvé")
    
    # Vérifie que la collection existe et a du contenu
    chunk_count = get_collection_count(project.vectorstore_collection_id)
    if chunk_count == 0:
        raise HTTPException(
            400,
            f"⚠️ La collection pour '{project.name}' est vide ou corrompue "
            f"(Collection ID: {project.vectorstore_collection_id}). "
            f"Veuillez réuploader le projet."
        )
    
    # Switche le vectorstore vers cette collection
    try:
        set_active_collection(project.vectorstore_collection_id)
    except ValueError as e:
        raise HTTPException(400, str(e))
    
    return {
        "message": f"✓ Projet '{project.name}' activé ({chunk_count} chunks trouvés)",
        "project_id": project.id,
        "collection_id": project.vectorstore_collection_id,
        "chunks_count": chunk_count
    }


@app.get("/projects/{project_id}")
def get_project(project_id: int, db: Session = Depends(get_db)):
    """Récupère les détails complets d'un projet + historique."""
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(404, "Projet non trouvé")
    
    history = ProjectService.get_project_history(db, project_id)
    from backend.models import Analysis
    analyses = db.query(Analysis).filter(
        Analysis.project_id == project_id
    ).all()
    
    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "uploaded_at": project.uploaded_at.isoformat(),
            "collection_id": project.vectorstore_collection_id
        },
        "history": [
            {
                "indexed_at": h.indexed_at.isoformat(),
                "files": h.files_found,
                "chunks": h.chunks_created,
                "embedding_time_ms": h.embedding_time_ms
            }
            for h in history
        ],
        "analyses_count": {
            "explain": len([a for a in analyses if a.feature == "explain"]),
            "recommend": len([a for a in analyses if a.feature == "recommend"]),
            "doc": len([a for a in analyses if a.feature == "doc"]),
            "deployment": len([a for a in analyses if a.feature == "deployment"]),
            "total": len(analyses)
        }
    }


@app.get("/projects/{project_id}/export")
def export_project(project_id: int, db: Session = Depends(get_db)):
    """Exporte toutes les analyses d'un projet."""
    export_data = ProjectService.export_project_analyses(db, project_id)
    if not export_data:
        raise HTTPException(404, "Projet non trouvé")
    
    return export_data


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/readme/download")
async def download_readme():
    """
    Génère et télécharge le README du projet analysé.
    """
    try:
        readme_content = overview_fn()  # Récupère l'aperçu du projet
        
        # Crée un fichier README temporaire
        tmp_file = Path(tempfile.gettempdir()) / "PROJECT_README.md"
        with open(tmp_file, "w", encoding="utf-8") as f:
            f.write(f"""# 📚 Generated Project Documentation

Generated by AI Code Assistant

---

## Project Overview

{readme_content}

---

*This documentation was automatically generated on 2026-07-15*
""")
        
        return FileResponse(
            path=tmp_file,
            filename="PROJECT_README.md",
            media_type="text/markdown"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))