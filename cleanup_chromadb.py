import chromadb
import sqlite3

# Lire les collections valides en DB
conn = sqlite3.connect('data/ai_assistant.db')
cursor = conn.cursor()
cursor.execute('SELECT vectorstore_collection_id FROM projects')
valid_collections = {row[0] for row in cursor.fetchall()}
conn.close()

print(f'Collections valides en DB: {valid_collections}')

# Supprimer les orphelines dans ChromaDB
client = chromadb.PersistentClient(path='data/vectorstore')
all_collections = client.list_collections()

print(f'\nCollections dans ChromaDB: {len(all_collections)}')
for c in all_collections:
    if c.name not in valid_collections:
        print(f'  🗑️  Suppression: {c.name}')
        client.delete_collection(name=c.name)
    else:
        print(f'  ✓ Garde: {c.name}')

print('\n✓ Cleanup ChromaDB terminé')
