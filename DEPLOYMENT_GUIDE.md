# 🚀 Guide de Déploiement - 3 Remarques Implémentées

## 1️⃣ Feature Deployment (Architecture Cloud Paramétrée)

### Usage Local
```bash
# Démarrer le serveur
python -m uvicorn backend.api.server:app --port 8000

# Tester l'endpoint
curl -X POST http://localhost:8000/deployment \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "AI Assistant",
    "service": "AWS",
    "usage_level": "small"
  }'
```

### Paramètres Disponibles

**Service Cloud:**
- `AWS` - Amazon Web Services
- `Azure` - Microsoft Azure
- `Private` - Serveur privé (on-premise)

**Volume d'Usage:**
- `small` - < 1,000 req/day, < 100 users simultanés
- `huge` - > 100,000 req/day, > 10,000 users simultanés

### Exemple de Réponse
```json
{
  "result": "## 📋 Vue d'ensemble\n...[Architecture complète]...",
  "parameters": {
    "service": "AWS",
    "usage_level": "small"
  }
}
```

---

## 2️⃣ Code Targeting avec Relevance Filtering

### Comment ça marche

**Avant (Ancien Comportement):**
- L'API retournait les N chunks les plus proches sémantiquement
- Même s'ils n'étaient pas vraiment pertinents pour la question
- Résultat: "Pourquoi tu me montres ça?" ❌

**Après (Nouveau Comportement):**
- `_is_chunk_relevant()` valide 3 critères:
  1. **Nom match**: Le nom du chunk contient les keywords de la question
  2. **Type match**: Si demandé (fonction/classe), on filtré par type
  3. **Code match**: Le code source contient les keywords
- Si aucun chunk valide → message d'erreur utile avec suggestions

### Testing

```bash
# Test Explain avec un vraie fonction
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Que fait la fonction embed_chunks?"
  }'

# Résultat: Affiche UNIQUEMENT la fonction embed_chunks 
# avec ses sources précises [backend/rag/embeddings.py:ligne]
```

---

## 3️⃣ PostgreSQL + Project Tracking

### Installation Locale

**Option A: Docker (Recommandé)**
```bash
# Démarrer PostgreSQL + Backend + Frontend
docker-compose up -d

# Vérifier
docker-compose ps
```

**Option B: PostgreSQL Manual**
```bash
# Installer PostgreSQL 15+
# macOS:
brew install postgresql@15
brew services start postgresql@15

# Linux:
sudo apt-get install postgresql postgresql-contrib

# Windows:
# Télécharger depuis https://www.postgresql.org/download/windows/
```

### Configuration

**Fichier .env pour PostgreSQL:**
```bash
USE_POSTGRES=true
DATABASE_URL=postgresql://postgres:password@localhost/ai_assistant
GROQ_API_KEY=gsk_...
```

### Endpoints Disponibles

#### Lister tous les projets
```bash
GET /projects

# Réponse:
{
  "total": 3,
  "projects": [
    {
      "id": 1,
      "name": "mon_app.zip",
      "uploaded_at": "2026-07-16T10:30:00",
      "collection_id": "uuid-123"
    }
  ]
}
```

#### Détails d'un projet
```bash
GET /projects/{project_id}

# Réponse:
{
  "project": {
    "id": 1,
    "name": "mon_app.zip",
    "uploaded_at": "2026-07-16T10:30:00"
  },
  "history": [
    {
      "indexed_at": "2026-07-16T10:30:00",
      "files": 42,
      "chunks": 156,
      "embedding_time_ms": 12340
    }
  ]
}
```

#### Exporter les analyses d'un projet
```bash
GET /projects/{project_id}/export

# Télécharge un JSON avec:
# - Project metadata
# - Tous les IndexHistory
# - Toutes les analyses (explain, recommend, etc.)
```

### Structure de la Base de Données

**Table: projects**
```sql
CREATE TABLE projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  uploaded_at TIMESTAMP DEFAULT NOW(),
  vectorstore_collection_id VARCHAR(255) UNIQUE NOT NULL
);
```

**Table: index_histories**
```sql
CREATE TABLE index_histories (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  files_found INTEGER NOT NULL,
  chunks_created INTEGER NOT NULL,
  files_metadata JSON,
  embedding_time_ms INTEGER,
  indexed_at TIMESTAMP DEFAULT NOW()
);
```

**Table: analyses**
```sql
CREATE TABLE analyses (
  id SERIAL PRIMARY KEY,
  project_id INTEGER REFERENCES projects(id),
  feature VARCHAR(50),  -- "explain", "recommend", etc.
  question TEXT,
  response TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔄 Workflow Complet

### 1. Upload d'un projet
```bash
# Frontend upload mon_app.zip
POST /ingest

# Backend:
# 1. Extrait le ZIP
# 2. Scan les fichiers
# 3. Crée chunks et embeddings
# 4. Crée un entry Project en DB
# 5. Enregistre IndexHistory avec stats

# Réponse:
{
  "project_id": "uuid-123",
  "files_found": 42,
  "chunks_created": 156,
  "db_project_id": 1,
  "embedding_time_ms": 12340
}
```

### 2. Utiliser une feature (ex: Explain)
```bash
POST /explain
{
  "question": "Que fait la fonction embed_chunks?"
}

# Backend:
# 1. Retrieve context (top_k=20)
# 2. Filtre avec _is_chunk_relevant()
# 3. Appelle LLM avec system prompt strict
# 4. Enregistre Analysis en DB
# 5. Retourne réponse

# Frontend affiche:
# [Code cible avec syntax highlighting]
# + Explications
# + Sources [fichier:ligne]
```

### 3. Consulter l'historique
```bash
GET /projects

# Affiche timeline des uploads
# +Pouvoir comparer 2 versions (UI future)
# + Exporter les analyses
```

---

## 📊 Monitoring & Métriques

### Vérifier la DB
```bash
# Se connecter à PostgreSQL
psql -U postgres -d ai_assistant

# Voir les projets
SELECT * FROM projects;

# Voir l'historique d'indexation
SELECT * FROM index_histories ORDER BY indexed_at DESC;

# Voir les analyses
SELECT feature, COUNT(*) FROM analyses GROUP BY feature;
```

### Logs Backend
```bash
# Voir les logs (Docker)
docker logs ai_assistant_backend -f

# Chercher les erreurs
docker logs ai_assistant_backend | grep ERROR
```

---

## 🔐 Sécurité en Production

### Checklist Pre-Deploy
- [ ] `GROQ_API_KEY` stockée en secret management (AWS Secrets, Azure KeyVault)
- [ ] `DATABASE_URL` avec password strong (min 20 caractères)
- [ ] HTTPS activé (CloudFront, Azure Front Door, ou Nginx reverse proxy)
- [ ] CORS whitelist au lieu de `*`
- [ ] Rate limiting par IP/user
- [ ] Backups PostgreSQL quotidiens
- [ ] Logs centralisés (CloudWatch, Application Insights)
- [ ] WAF activé pour DDoS protection

### Certificat SSL
```bash
# Avec Let's Encrypt
certbot certonly --standalone -d yourdomain.com

# Nginx reverse proxy avec SSL
```

---

## 🎯 Prochaines Étapes

### UI Historique (À faire)
- [ ] Component "ProjectHistory" 
- [ ] Timeline des uploads
- [ ] Comparateur: version1 vs version2
- [ ] Stats agrégées

### Performance
- [ ] Cache Redis pour embeddings
- [ ] Pagination des projets
- [ ] Compression des réponses gzip

### Monitoring
- [ ] Dashboard Grafana
- [ ] Alertes si embedding > 30s
- [ ] Tracking des coûts (API Groq, espace DB)

---

## 📞 Support & Troubleshooting

### Erreur: "Database URL not recognized"
```bash
# Vérifier USE_POSTGRES dans .env
USE_POSTGRES=false  # Pour SQLite (défaut)
USE_POSTGRES=true   # Pour PostgreSQL
```

### Erreur: "psycopg2 not found"
```bash
# Installer uniquement en production
pip install psycopg2-binary  # (backend uniquement)
```

### Erreur: "Connection refused to postgres:5432"
```bash
# Vérifier que PostgreSQL est running
docker ps | grep postgres

# Ou redémarrer
docker-compose restart postgres
```

---

**Version**: 3.0 | **Date**: 2026-07-16 | **Status**: ✅ Production-Ready
