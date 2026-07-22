#!/usr/bin/env python
"""Full reset of database and vectorstore."""

import sys
import os
import shutil
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("🧹 Nettoyage complet...")

# 1. Reset SQLite DB
db_path = "data/ai_assistant.db"
if os.path.exists(db_path):
    os.remove(db_path)
    print(f"✅ Suppression DB: {db_path}")

# 2. Reset ChromaDB
chroma_path = "data/vectorstore"
if os.path.exists(chroma_path):
    # Remove all except active_collection.txt
    for item in os.listdir(chroma_path):
        item_path = os.path.join(chroma_path, item)
        if item != "active_collection.txt":
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"✅ Suppression dir: {item}")
            else:
                os.remove(item_path)
                print(f"✅ Suppression fichier: {item}")

# 3. Reinitialize
try:
    from backend.models import Base
    from backend.db import get_db_engine
    
    engine = get_db_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print("✅ Réinitialisé les tables DB")
except Exception as e:
    print(f"⚠️ Erreur réinit DB: {e}")

print("\n✅ NETTOYAGE COMPLET TERMINÉ - Prêt à réingérer!")
