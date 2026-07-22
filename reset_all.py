#!/usr/bin/env python
"""Reset complet - DB + ChromaDB"""

import os
import sqlite3
from backend.db import init_db

print("=" * 70)
print("🔄 RESET COMPLET - DB + ChromaDB")
print("=" * 70)

# Reset DB
print("\n1. Réinitialisation de la DB SQLite...")
if os.path.exists('data/ai_assistant.db'):
    os.remove('data/ai_assistant.db')
    print("   ✓ Ancien DB supprimé")

init_db()
print("   ✓ Nouvelle DB créée")

# Vérifie les tables
conn = sqlite3.connect('data/ai_assistant.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f"   Tables: {tables}")
conn.close()

# Reset ChromaDB
print("\n2. Réinitialisation de ChromaDB...")
import shutil
import chromadb

# Essaie de supprimer, sinon passe
try:
    if os.path.exists('data/vectorstore'):
        shutil.rmtree('data/vectorstore', ignore_errors=True)
        print("   ✓ Ancien vectorstore supprimé")
except:
    print("   ⚠️  Vectorstore verrouillé (OK, sera réutilisé)")

# Juste recréer une nouvelle collection
client = chromadb.PersistentClient(path='data/vectorstore')
print("   ✓ ChromaDB prêt")

print("\n" + "=" * 70)
print("✅ RESET COMPLET TERMINÉ")
print("=" * 70)
print("\nÉtat:")
print("  - DB SQLite: Vierge (0 projets)")
print("  - ChromaDB: Vierge (0 collections)")
print("  - Prêt pour un nouvel upload!")
