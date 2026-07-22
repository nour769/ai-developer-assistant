#!/usr/bin/env python
"""
Ingère le fichier test_project.zip via l'API.
"""

import requests
import sys
import time

API_BASE = "http://localhost:8000"

def ingest():
    """Ingère le projet via l'API."""
    zip_path = "test_project.zip"
    
    print(f"📦 Ingestion de {zip_path}...")
    
    try:
        with open(zip_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(f"{API_BASE}/ingest", files=files, timeout=60)
        
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"✅ Ingestion réussie!")
            print(f"   Project ID: {data.get('project_id')}")
            print(f"   Fichiers trouvés: {data.get('files_found')}")
            print(f"   Chunks créés: {data.get('chunks_created')}")
            print(f"   Temps embedding: {data.get('embedding_time_ms')}ms")
            return True
        else:
            print(f"❌ Erreur: {resp.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de connecter à l'API. Est-ce que le serveur est lancé?")
        print(f"   Essayez: python -m backend.api.cli")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False


if __name__ == "__main__":
    success = ingest()
    sys.exit(0 if success else 1)
