#!/usr/bin/env python
"""Désactive la telemetry de ChromaDB pour éviter les erreurs au démarrage."""

import os
import sys

# Désactiver la telemetry avant d'importer chromadb
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"

# Puis lancer l'app normalement
if __name__ == "__main__":
    from uvicorn import run
    from backend.api.server import app
    
    run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
