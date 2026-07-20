# 🤖 AI Code Assistant — v3.0 

> Un **assistant IA** qui explique, documente et recommande architectures pour ton code.  
> **Production-ready** avec PostgreSQL, historique, et génération d'architectures cloud.

## ✨ Status: v3.0 Complete

**3 remarques de l'encadrant - Toutes implémentées ✅**

| # | Feature | Statut |
|----|---------|--------|
| 1️⃣ | Architecture déploiement paramétrée (AWS/Azure/Private + Small/Huge) | ✅ FAIT |
| 2️⃣ | Code pertinent avec relevance filtering + sources [fichier:ligne] | ✅ FAIT |
| 3️⃣ | PostgreSQL + Tracking + Export JSON + Docker | ✅ FAIT |

### 🎯 Core Capabilities

1. **📖 Expliquer** (`explain`) — Comprendre le code en détail + sources précises
2. **🔍 Vue d'ensemble** (`overview`) — Architecture complète du projet
3. **📚 Documenter** (`doc`) — Générer README automatiquement
4. **✅ Recommander** (`recommend`) — Suggestions d'amélioration
5. **🆕 Architecture** (`deployment`) — Plan de déploiement cloud paramétrés
6. **🆕 Projets** (`projects`) — Historique + export des analyses

---

## 🚀 Quick Start

### Option 1: Development (SQLite)
```bash
# Install
pip install -r requirements.txt

# Backend
python -m uvicorn backend.api.server:app --port 8000 --reload

# Frontend (autre terminal)
cd frontend && npm install && npm run dev

# Open http://localhost:5173
```

### Option 2: Production (Docker + PostgreSQL)
```bash
docker-compose up -d
# Open http://localhost:5173
```

### Encore plus simple:
```bash
make dev       # Development
make prod      # Production
make help      # Toutes les commandes
```

---

## 📖 Documentation (Lire Ici!)

| Fichier | Pour Qui | Temps |
|---------|----------|-------|
| **README_REMARQUES.md** | Tout le monde | 5 min |
| **POUR_ENCADRANT.md** | Encadrant | 10 min |
| **DEPLOYMENT_GUIDE.md** | Développeurs | 20 min |
| **IMPLEMENTATION_SUMMARY.md** | Tech leads | 30 min |

**Besoin d'aide?**
```bash
make help     # Voir toutes les commandes
make docs     # Lister les fichiers docs
```

---

## 🏗️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq API (Llama 3.3 70B) | AI generation & analysis |
| **Embeddings** | sentence-transformers | Semantic search |
| **Vector DB** | ChromaDB | Vector storage |
| **Database** | SQLAlchemy + SQLite/PostgreSQL | Project tracking |
| **Backend** | FastAPI (Python 3.11+) | REST API |
| **Frontend** | React + Vite | Modern UI |
| **Parsing** | Python AST + Tree-sitter | Code structure |
| **Container** | Docker + docker-compose | Production deployment |

---

## 📊 Nouveaux Endpoints (v3.0)

### Deployment
```
POST /deployment
├─ Input: project_name, service (AWS/Azure/Private), usage_level (small/huge)
└─ Output: Architecture complète + IaC + Docker
```

### Projects (Tracking)
```
GET  /projects                    → Liste tous les projets
GET  /projects/{id}               → Détails + historique
GET  /projects/{id}/export        → Exporte JSON
```

### Database Schema
```sql
projects          → Tous les projets uploadés
├─ id, name, uploaded_at
└─ vectorstore_collection_id (UNIQUE)

index_histories   → Stats chaque indexation
├─ project_id (FK)
├─ files_found, chunks_created
├─ embedding_time_ms
└─ indexed_at

analyses          → Chaque analyse générée
├─ project_id (FK)
├─ feature ("explain", "recommend", etc.)
├─ question, response
└─ created_at
```

---

## ⚡ Performance

- **Upload**: 20-30 secondes
- **Embedding**: 3-5ms par chunk (batch processing)
- **Retrieval**: <100ms
- **LLM Response**: 2-5 secondes

### Optimizations
- ✅ Batch embedding (5-10x speedup)
- ✅ In-memory ZIP processing
- ✅ Automatic rate limit handling
- ✅ Relevance filtering (moins d'appels LLM)

---

## 🔧 API Endpoints

### Core (Existant)
```
POST   /ingest             Uploader + indexer
POST   /explain            Expliquer du code
POST   /recommend          Recommandations
GET    /overview           Vue d'ensemble
POST   /doc                Générer README
GET    /health             Health check
```

### Nouveaux (v3.0)
```
POST   /deployment         Architecture cloud paramétrée
GET    /projects           Lister les projets
GET    /projects/{id}      Détails + historique
GET    /projects/{id}/export Exporter analyses JSON
```

---

## 🧪 Testing

```bash
make test-health       # Vérifier serveur
make test-deployment   # Tester architecture endpoint
make test-projects     # Voir les projets
make test              # Tests complets
```

---

## 📁 Project Structure

```
ai-code-assistant/
├── backend/
│   ├── api/              # Endpoints FastAPI
│   ├── assistant/        # Features (explain, recommend, deployment)
│   ├── parsing/          # Code parsers
│   ├── rag/              # Embeddings + vectorstore
│   ├── services/         # Business logic (NEW!)
│   ├── models.py         # Database models (NEW!)
│   ├── db.py             # Connection management (NEW!)
│   └── config.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main component
│   │   ├── api.js        # API client
│   │   └── components/
│   └── index.html
├── data/
│   ├── uploads/
│   ├── vectorstore/
│   └── ai_assistant.db
├── docker-compose.yml    # Production stack (NEW!)
├── Dockerfile            # Container image (NEW!)
├── Makefile              # Commands (NEW!)
└── requirements.txt
```
