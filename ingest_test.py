#!/usr/bin/env python
"""
Ingère le fichier de test pour pouvoir tester les endpoints recommend, explain, etc.
"""

import sys
import os

# Setup path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.parsing.router import extract_code
from backend.rag.vectorstore import insert_chunks, reset_collection
from backend.services.project_service import create_project

def ingest_test_code():
    """Ingère le fichier de test."""
    
    # 1. Reset la collection
    collection_name = reset_collection()
    print(f"✅ Nouvelle collection créée: {collection_name}")
    
    # 2. Extrait le code du fichier test
    test_file_path = "test_code_sample.py"
    
    if not os.path.exists(test_file_path):
        print(f"❌ Fichier {test_file_path} non trouvé")
        return
    
    print(f"📂 Extraction du code depuis {test_file_path}...")
    
    try:
        chunks = extract_code(test_file_path, "test-sample")
        print(f"✅ {len(chunks)} chunks extraits")
        
        # 3. Insère les chunks dans le vectorstore
        for chunk in chunks:
            print(f"  - {chunk['metadata']['file']}: {chunk['metadata']['name']} (ligne {chunk['metadata']['lineno']})")
        
        insert_chunks(chunks)
        print(f"✅ Chunks insérés dans le vectorstore")
        
        # 4. Crée le projet dans la DB
        project = create_project(
            name="test-sample",
            description="Fichier de test avec intentional vulnerabilities et mauvaises practices"
        )
        print(f"✅ Projet créé: {project.name} (ID: {project.id})")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ingestion: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = ingest_test_code()
    sys.exit(0 if success else 1)
