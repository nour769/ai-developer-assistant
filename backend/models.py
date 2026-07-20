"""
Database models pour tracking des projets et historique.

Permet de :
1. Garder historique de tous les projets uploadés
2. Revenir à une version antérieure
3. Comparer 2 versions
4. Exporter les analyses
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Project(Base):
    """
    Représente un projet uploadé avec sa metadata.
    """
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow, index=True)
    vectorstore_collection_id = Column(String(255), unique=True, nullable=False)
    
    # Relations
    index_histories = relationship("IndexHistory", back_populates="project", cascade="all, delete-orphan")
    analyses = relationship("Analysis", back_populates="project", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Project {self.name} uploaded {self.uploaded_at}>"


class IndexHistory(Base):
    """
    Historique de chaque indexation avec stats.
    """
    __tablename__ = "index_histories"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    files_found = Column(Integer, nullable=False)
    chunks_created = Column(Integer, nullable=False)
    files_metadata = Column(JSON, nullable=True)  # Liste complète des fichiers avec tailles
    embedding_time_ms = Column(Integer, nullable=True)
    indexed_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    project = relationship("Project", back_populates="index_histories")
    
    def __repr__(self):
        return f"<IndexHistory project_id={self.project_id} chunks={self.chunks_created}>"


class Analysis(Base):
    """
    Stocke les analyses générées (explain, recommend, etc.)
    pour export et comparaison.
    """
    __tablename__ = "analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False, index=True)
    feature = Column(String(50), nullable=False)  # "explain", "recommend", "overview", "deployment"
    question = Column(Text, nullable=True)  # Utilisé pour explain, search
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relations
    project = relationship("Project", back_populates="analyses")
    
    def __repr__(self):
        return f"<Analysis {self.feature} on project_id={self.project_id}>"
