"""
Service pour gérer les projets et l'historique des indexations.
"""

from sqlalchemy.orm import Session
from datetime import datetime
from backend.models import Project, IndexHistory, Analysis


class ProjectService:
    """Gestion des projets et historique."""
    
    @staticmethod
    def create_project(db: Session, name: str, collection_id: str, description: str = None) -> Project:
        """Crée un nouveau projet."""
        project = Project(
            name=name,
            description=description,
            vectorstore_collection_id=collection_id
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    
    @staticmethod
    def get_project_by_collection(db: Session, collection_id: str) -> Project:
        """Récupère le projet par son collection_id."""
        return db.query(Project).filter(
            Project.vectorstore_collection_id == collection_id
        ).first()
    
    @staticmethod
    def list_projects(db: Session, limit: int = 50) -> list[Project]:
        """Liste tous les projets (plus récents en premier)."""
        return db.query(Project).order_by(Project.uploaded_at.desc()).limit(limit).all()
    
    @staticmethod
    def get_project(db: Session, project_id: int) -> Project:
        """Récupère un projet par son ID."""
        return db.query(Project).filter(Project.id == project_id).first()
    
    @staticmethod
    def save_index_history(
        db: Session,
        project_id: int,
        files_found: int,
        chunks_created: int,
        files_metadata: dict = None,
        embedding_time_ms: int = None
    ) -> IndexHistory:
        """Enregistre l'historique d'une indexation."""
        history = IndexHistory(
            project_id=project_id,
            files_found=files_found,
            chunks_created=chunks_created,
            files_metadata=files_metadata,
            embedding_time_ms=embedding_time_ms
        )
        db.add(history)
        db.commit()
        db.refresh(history)
        return history
    
    @staticmethod
    def get_project_history(db: Session, project_id: int) -> list[IndexHistory]:
        """Récupère l'historique d'indexation d'un projet."""
        return db.query(IndexHistory).filter(
            IndexHistory.project_id == project_id
        ).order_by(IndexHistory.indexed_at.desc()).all()
    
    @staticmethod
    def save_analysis(
        db: Session,
        project_id: int,
        feature: str,
        response: str,
        question: str = None
    ) -> Analysis:
        """Enregistre une analyse générée."""
        analysis = Analysis(
            project_id=project_id,
            feature=feature,
            response=response,
            question=question
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis
    
    @staticmethod
    def get_analyses_by_feature(db: Session, project_id: int, feature: str) -> list[Analysis]:
        """Récupère toutes les analyses d'une feature pour un projet."""
        return db.query(Analysis).filter(
            Analysis.project_id == project_id,
            Analysis.feature == feature
        ).order_by(Analysis.created_at.desc()).all()
    
    @staticmethod
    def export_project_analyses(db: Session, project_id: int) -> dict:
        """Exporte toutes les analyses d'un projet."""
        project = ProjectService.get_project(db, project_id)
        if not project:
            return None
        
        return {
            "project": {
                "id": project.id,
                "name": project.name,
                "uploaded_at": project.uploaded_at.isoformat(),
                "collection_id": project.vectorstore_collection_id
            },
            "histories": [
                {
                    "indexed_at": h.indexed_at.isoformat(),
                    "files": h.files_found,
                    "chunks": h.chunks_created,
                    "embedding_time_ms": h.embedding_time_ms
                }
                for h in project.index_histories
            ],
            "analyses": [
                {
                    "feature": a.feature,
                    "question": a.question,
                    "response": a.response,
                    "created_at": a.created_at.isoformat()
                }
                for a in project.analyses
            ]
        }
