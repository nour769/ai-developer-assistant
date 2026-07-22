import sqlite3

conn = sqlite3.connect('data/ai_assistant.db')
cursor = conn.cursor()

# Supprimer tous les agentic-rag
cursor.execute("DELETE FROM index_histories WHERE project_id IN (SELECT id FROM projects WHERE name='agentic-rag')")
print(f'Index histories supprimées: {cursor.rowcount}')

cursor.execute("DELETE FROM analyses WHERE project_id IN (SELECT id FROM projects WHERE name='agentic-rag')")
print(f'Analyses supprimées: {cursor.rowcount}')

cursor.execute("DELETE FROM projects WHERE name='agentic-rag'")
print(f'Projets agentic-rag supprimés: {cursor.rowcount}')

conn.commit()

# Afficher ce qui reste
cursor.execute('SELECT id, name, vectorstore_collection_id FROM projects')
projects = cursor.fetchall()
print(f'\n✓ Projets restants: {len(projects)}')
for p in projects:
    print(f'  ID={p[0]}, Name={p[1]}, Collection={p[2]}')
    cursor.execute('SELECT chunks_created FROM index_histories WHERE project_id = ?', (p[0],))
    hist = cursor.fetchone()
    if hist:
        print(f'    → {hist[0]} chunks')

conn.close()
