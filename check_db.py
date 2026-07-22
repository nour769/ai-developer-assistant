import sqlite3
from backend.db import init_db

# Force init
print("Initializing database...")
init_db()

conn = sqlite3.connect('data/ai_assistant.db')
cursor = conn.cursor()

# Check tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cursor.fetchall()]
print(f'\n✓ Tables: {tables}')

# Check projects
if 'project' in tables:
    cursor.execute('SELECT id, name, vectorstore_collection_id FROM project')
    projects = cursor.fetchall()
    print(f'✓ Projects: {len(projects)} trouvés')
    for p in projects:
        print(f'  - {p[1]} (Collection: {p[2]})')
        
        # Check chunks in this collection
        cursor.execute('SELECT chunks_created FROM index_history WHERE project_id = ?', (p[0],))
        hist = cursor.fetchone()
        if hist:
            print(f'    Chunks: {hist[0]}')

conn.close()
