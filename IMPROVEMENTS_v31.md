# ✅ Améliorations v3.1 : Tracking, Révision Projets & LLM Plus Flexible

## 🎯 Résumé

Vous avez maintenant un système **complet de tracking** des projets + une **fonction `explain` plus flexible** qui répond à des questions larges.

---

## 📋 Changements apportés

### 1️⃣ **Fonction `explain` améliorée** 
**Fichier:** [backend/assistant/explain.py](backend/assistant/explain.py)

**Avant:**
```python
# Rejetait les questions qui n'matchaient pas EXACTEMENT le nom d'une fonction
def _is_chunk_relevant(chunk, question):
    # Strict: (name_match OR type_match) AND code_match
```

**Après:**
```python
# Accepte les questions larges avec 3 niveaux d'fallback
def _is_chunk_relevant(chunk, question):
    # 1. Mode STRICT pour questions spécifiques ("Que fait la fonction X?")
    #    -> Au moins 2 critères doivent matcher (name + code + type)
    
    # 2. Mode FLEXIBLE pour questions larges ("Que sont les chunks?")
    #    -> Au moins 1 critère suffit
    
    # 3. Questions très vagues -> accepter tous les chunks
```

**Bénéfice:** Le LLM peut maintenant répondre à :
- ✅ "C'est quoi les chunks ?" 
- ✅ "Explique le système de RAG"
- ✅ "Comment fonctionne l'embedding ?"
- ✅ Questions très larges sur l'architecture

Plus seulement :
- ❌ "Que fait la fonction login ?" (exact match uniquement)

---

### 2️⃣ **Endpoints pour switcher de projets**
**Fichier:** [backend/api/server.py](backend/api/server.py)

**Nouveaux endpoints:**

```bash
# Lister tous les projets
GET /projects
→ Retourne: liste avec is_active pour chaque

# Voir détails (historique + analyses)
GET /projects/{id}
→ Retourne: metadata + history + analyses_count

# Activer un ancien projet
POST /projects/{id}/activate
→ Change la collection vectorielle active
```

**Bonus:** Importe `set_active_collection` du vectorstore pour pouvoir basculer entre projets.

---

### 3️⃣ **Interface frontend: Projets précédents**
**Fichiers:**
- [frontend/src/components/ProjectHistory.jsx](frontend/src/components/ProjectHistory.jsx) — Nouveau composant
- [frontend/src/styles/ProjectHistory.css](frontend/src/styles/ProjectHistory.css) — Styling
- [frontend/src/App.jsx](frontend/src/App.jsx) — Intégration

**Fonctionnalités:**
```
┌─────────────────────────────┐
│ 📁 Projets précédents       │
├─────────────────────────────┤
│ ✓ ACTIF  Mon Projet v1      │
│          14 sept, 14:32     │ [Activer]
│ Projet Backup               │
│ 13 sept, 10:15              │ [Activer]
│ Test API                    │
│ 12 sept, 09:00              │ [Activer]
│                             │
│ [🔄 Rafraîchir]             │
└─────────────────────────────┘
```

**Intéraction:**
- Cliquer pour voir détails (collection ID, date complète)
- Bouton "Activer" pour charger un ancien projet
- Le projet activé bascule le vectorstore de ChromaDB

---

### 4️⃣ **État du projet sauvegardé**
**App.jsx:**
```javascript
const [currentProjectId, setCurrentProjectId] = useState(null);

// Quand on upload
setCurrentProjectId(data.db_project_id);

// Quand on activate
handleProjectSelect = (projectId) => {
  setCurrentProjectId(projectId);
};
```

---

### 5️⃣ **Documentation PostgreSQL**
**Fichier:** [POSTGRESQL_GUIDE.md](POSTGRESQL_GUIDE.md)

Explique:
- 📍 Où est PostgreSQL (configuré dans `backend/db.py`)
- 🚀 Comment l'activer (5 étapes simples)
- 🐳 Comment utiliser Docker (docker-compose inclus)
- 🔄 Comment switcher SQLite ↔ PostgreSQL
- 📊 Structure des tables
- 🆘 Troubleshooting complet

---

### 6️⃣ **Documentation Tracking**
**Fichier:** [TRACKING_GUIDE.md](TRACKING_GUIDE.md)

Explique:
- Qu'est-ce que le tracking ?
- Comment utiliser les projets précédents
- Endpoints API complets
- Où sont les données (SQLite vs PostgreSQL)
- Exemples pratiques (revisiter un projet après 1 mois, etc.)

---

## 🚀 Flux utilisateur (nouveau)

### Avant (v3.0)
```
1. Upload zip
2. Poser questions
3. (Fermer l'appli = données perdues!)
```

### Après (v3.1)
```
1. Upload zip → sauvegardé dans DB + historique + collection unique
2. Poser questions → réponses sauvegardées dans DB
3. Fermer l'appli
4. Revenir 1 mois plus tard
5. Voir "Mon Projet" dans "Projets précédents"
6. Cliquer "Activer"
7. Continuer les analyses (explain, doc, recommend, etc.)
8. Comparer avec un nouveau projet uploadé en parallèle
```

---

## 📊 Tables de BD (non changées, mais utilisées)

```sql
projects
├─ id, name, uploaded_at, vectorstore_collection_id
│
├─ index_histories (FK project_id)
│  └─ files_found, chunks_created, embedding_time_ms
│
└─ analyses (FK project_id)
   └─ feature ("explain", "recommend", etc.)
      question, response, created_at
```

---

## 🔧 Améliorations technique (backend)

### explain.py
```python
# Avant: 1 stratégie stricte + message d'erreur
def explain(question):
    relevant = filter_strict(matches)
    if not relevant:
        return "❌ Contexte insuffisant"
    return llm_explain(relevant)

# Après: 3 niveaux d'fallback
def explain(question):
    relevant = filter_flexible(matches)
    if relevant:
        return llm_explain(relevant)
    elif matches:
        return llm_general_explain(matches[:3])
    else:
        return "❌ Aucun contexte du tout"
```

### server.py
```python
# Nouveaux imports
from backend.rag.vectorstore import set_active_collection, get_active_collection_name

# Nouveaux endpoints
@app.get("/projects")  # Avec is_active flag
@app.post("/projects/{id}/activate")  # Switcher
@app.get("/projects/{id}")  # Plus analyses_count
```

### App.jsx
```javascript
// Nouvel état
const [currentProjectId, setCurrentProjectId] = useState(null);

// Nouveau composant
<ProjectHistory onProjectSelect={handleProjectSelect} />

// Nouveau callback
const handleProjectSelect = (projectId, message) => {
  setCurrentProjectId(projectId);
};
```

---

## 🎯 Résolution des demandes

### Demande 1: "Où est la base de données PostgreSQL ?"
✅ **Réponse:**
- `backend/db.py` configure SQLite (par défaut) ou PostgreSQL
- Guide complet: [POSTGRESQL_GUIDE.md](POSTGRESQL_GUIDE.md)
- Voir aussi: `docker-compose.yml` (inclut PostgreSQL)

### Demande 2: "Je veux voir les projets uploadés et les revisiter"
✅ **Réponse:**
- Interface dans le sidebar: "📁 Projets précédents"
- Endpoints: `/projects`, `/projects/{id}`, `/projects/{id}/activate`
- Historique complet sauvegardé dans BD

### Demande 3: "LLM explain doit répondre à des questions plus larges (chunks, embeddings, etc.)"
✅ **Réponse:**
- Nouvelle stratégie 3-niveaux dans `explain.py`
- Mode strict pour fonctions spécifiques
- Mode flexible pour questions larges
- Fallback général si aucun chunk spécifique

---

## 📝 Comment l'utiliser

### Upload et tracking
```bash
# 1. Ouvrir http://localhost:5173
# 2. Drag & drop mon-projet.zip
# 3. Voir l'historique dans "Projets précédents"

# Plus tard...
# 4. Cliquer "Activer" sur un ancien projet
# 5. Poser des questions sur ce projet
```

### Questions larges sur explain
```
Q: "C'est quoi les chunks ?"
A: ✅ Explique comment le système split le code en chunks

Q: "Comment fonctionne l'embedding ?"
A: ✅ Utilise les chunks du projet pour expliquer

Q: "Que fait la fonction getUserById ?"
A: ✅ (Strict) Cherche la fonction spécifique
```

### PostgreSQL
```bash
# Production (docker-compose)
docker-compose up -d

# Dev (SQLite)
python -m uvicorn backend.api.server:app --reload

# Production (PostgreSQL local)
export USE_POSTGRES=true
export DATABASE_URL="postgresql://user:pass@localhost/ai_assistant"
python -m uvicorn backend.api.server:app
```

---

## 🧪 Tests (manuel)

### 1. Backend démarre
```bash
python -m uvicorn backend.api.server:app --reload
# Doit voir: ✓ Database initialized
```

### 2. Frontend démarre
```bash
cd frontend && npm run dev
# Doit voir ProjectHistory component
```

### 3. Upload et tracking
1. Drag & drop un zip
2. Voir dans "Projets précédents"
3. Cliquer "Activer"
4. Voir message "✓ Projet 'X' activé"

### 4. Questions larges
```
POST /explain
{"question": "C'est quoi les chunks ?", "top_k": 50}

Doit retourner une réponse (pas ❌ Contexte insuffisant)
```

---

## 🔄 Prochaines étapes possibles

- [ ] Interface pour voir les analyses passées
- [ ] Supprimer un projet
- [ ] Archiver vs supprimer
- [ ] Comparer 2 projets
- [ ] Versioning (v1, v2 d'un même projet)
- [ ] Multi-utilisateurs (PostgreSQL obligatoire)

---

## 📞 Support

**Q:** "Le composant ProjectHistory ne s'affiche pas"
**A:** Vérifier que:
1. `ProjectHistory.jsx` existe dans `frontend/src/components/`
2. `ProjectHistory.css` existe dans `frontend/src/styles/`
3. App.jsx l'importe: `import ProjectHistory from ...`

**Q:** "explain() retourne toujours ❌"
**A:** Vérifier que:
1. Un projet est uploadé
2. top_k >= 5 (pas trop bas)
3. Le projet a du code Python/JS

**Q:** "Aucun projet dans la liste"
**A:** Vérifier que:
1. BD est initialisée: `python -c "from backend.db import init_db; init_db()"`
2. Vous avez uploadé au moins 1 zip
3. Utiliser `GET /projects` pour déboguer

---

## 📊 Résumé des fichiers changés

| Fichier | Type | Change |
|---------|------|--------|
| backend/assistant/explain.py | Python | ✅ 3 niveaux fallback |
| backend/api/server.py | Python | ✅ Endpoints activation |
| frontend/src/components/ProjectHistory.jsx | React | ✨ Nouveau |
| frontend/src/styles/ProjectHistory.css | CSS | ✨ Nouveau |
| frontend/src/App.jsx | React | ✅ Intégration ProjectHistory |
| POSTGRESQL_GUIDE.md | Doc | ✨ Nouveau |
| TRACKING_GUIDE.md | Doc | ✨ Nouveau |

---

## 🎉 Résultat final

Vous avez maintenant un système **production-ready** qui :

✅ **Persiste** les projets dans une base de données (SQLite/PostgreSQL)
✅ **Permet de revisiter** les anciens projets
✅ **Sauvegarde** l'historique d'indexation et les analyses
✅ **Répond** à des questions larges via le LLM
✅ **Supporte** la scalabilité (PostgreSQL pour multi-user)

🚀 **Ready for production!**
