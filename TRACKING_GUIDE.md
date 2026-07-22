# 📚 Guide: Tracking des Projets et Historique

## Qu'est-ce que c'est ?

Le **système de tracking** vous permet de :
- ✅ Voir tous les projets uploadés précédemment
- ✅ Revisiter un ancien projet pour l'analyser à nouveau
- ✅ Voir l'historique d'indexation (fichiers, chunks, temps)
- ✅ Consulter toutes les analyses générées (explain, recommend, etc.)
- ✅ Exporter les données d'un projet

---

## 🎯 Utiliser le système

### 1. **Voir les projets précédents**

Dans le **panneau latéral gauche**, vous verrez une section **"📁 Projets précédents"** qui liste tous vos projets :

```
✓ ACTIF  Mon Projet v1    14 sept, 14:32
         Projet Backup     13 sept, 10:15
         Test API         12 sept, 09:00
```

### 2. **Activer un projet existant**

Cliquez sur le bouton **"Activer"** pour charger un ancien projet :

```
Mon Projet v1  [Activer]  <- Cliquez ici
```

Une fois activé:
- ✅ Vous pouvez poser des questions (`explain`)
- ✅ Générer de nouvelles analyses (`recommend`, `doc`, etc.)
- ✅ Explorer son architecture (`overview`)

**Note**: Un seul projet peut être actif à la fois.

### 3. **Voir les détails d'un projet**

Cliquez sur un projet pour voir:
- 📝 ID de la collection vectorielle
- 🕐 Date d'upload complète
- 📊 Historique d'indexation
  - Nombre de fichiers
  - Nombre de chunks créés
  - Temps d'embedding
- 📈 Analyses sauvegardées
  - Combien d'`explain`, `recommend`, etc.

### 4. **Rafraîchir la liste**

Cliquez sur **🔄 Rafraîchir** pour mettre à jour la liste si vous ajoutez des projets depuis un autre navigateur.

---

## 🔄 Flux complet

### Scénario: Analyser un projet, puis revenir plus tard

```
1️⃣ JOUR 1
   └─ Uploader "my-app.zip"
   └─ Poser 5 questions avec explain
   └─ Générer doc et recommend
   └─ Exporter les analyses

2️⃣ JOUR 2 (1 semaine plus tard)
   └─ Ouvrir l'appli
   └─ Voir "my-app.zip" dans "Projets précédents"
   └─ Cliquer "Activer"
   └─ Continuer les analyses (explain, doc, etc.)

3️⃣ JOUR 3
   └─ Uploader "new-project.zip"
   └─ Celui-ci devient "ACTIF"
   └─ "my-app.zip" passe en mode "inactif"
   └─ On peut switcher entre eux quand on veut
```

---

## 🗄️ Données stockées

### Qu'est-ce qui est sauvegardé ?

Quand vous uploadez un projet, on enregistre:

#### 1. **Métadonnées du projet**
```json
{
  "id": 1,
  "name": "mon-projet.zip",
  "uploaded_at": "2024-09-14T14:32:00Z",
  "collection_id": "code_chunks_a1b2c3d4"
}
```

#### 2. **Historique d'indexation**
```json
{
  "project_id": 1,
  "files_found": 42,
  "chunks_created": 156,
  "embedding_time_ms": 2345,
  "files_metadata": [
    {"path": "src/main.py", "size": 5120},
    {"path": "src/utils.js", "size": 3240},
    ...
  ]
}
```

#### 3. **Analyses générées**
```json
{
  "project_id": 1,
  "feature": "explain",
  "question": "Que fait la fonction login ?",
  "response": "La fonction login ...",
  "created_at": "2024-09-14T15:00:00Z"
}
```

---

## 📡 Endpoints API

Si vous appelez l'API directement:

### **Lister tous les projets**
```bash
GET /projects
```

**Réponse:**
```json
{
  "total": 3,
  "active_collection": "code_chunks_a1b2c3d4",
  "projects": [
    {
      "id": 1,
      "name": "mon-app",
      "uploaded_at": "2024-09-14T14:32:00Z",
      "collection_id": "code_chunks_a1b2c3d4",
      "is_active": true
    },
    ...
  ]
}
```

### **Voir les détails d'un projet**
```bash
GET /projects/1
```

**Réponse:**
```json
{
  "project": {
    "id": 1,
    "name": "mon-app",
    "uploaded_at": "2024-09-14T14:32:00Z",
    "collection_id": "code_chunks_a1b2c3d4"
  },
  "history": [
    {
      "indexed_at": "2024-09-14T14:32:00Z",
      "files": 42,
      "chunks": 156,
      "embedding_time_ms": 2345
    }
  ],
  "analyses_count": {
    "explain": 5,
    "recommend": 1,
    "doc": 1,
    "deployment": 0,
    "total": 7
  }
}
```

### **Activer un projet**
```bash
POST /projects/1/activate
```

**Réponse:**
```json
{
  "message": "Projet 'mon-app' activé",
  "project_id": 1,
  "collection_id": "code_chunks_a1b2c3d4"
}
```

### **Exporter les analyses d'un projet**
```bash
GET /projects/1/export
```

**Réponse:**
```json
{
  "project_id": 1,
  "project_name": "mon-app",
  "export_date": "2024-09-14T16:00:00Z",
  "analyses": [
    {
      "feature": "explain",
      "question": "Que fait login ?",
      "response": "..."
    },
    ...
  ]
}
```

---

## 💾 Where is the data stored?

### Mode SQLite (développement)
```
data/
  └─ ai_assistant.db          ← Base de données locale
     └─ Projects table
     └─ IndexHistory table
     └─ Analyses table
```

**Avantage:** Aucune installation
**Inconvénient:** Une seule personne à la fois

### Mode PostgreSQL (production)
```
PostgreSQL Server
  └─ ai_assistant database
     └─ projects table
     └─ index_histories table
     └─ analyses table
```

**Avantage:** Multi-user, scalable, backups
**Inconvénient:** Nécessite un serveur

Voir [POSTGRESQL_GUIDE.md](./POSTGRESQL_GUIDE.md) pour les détails.

---

## 🎬 Exemples pratiques

### Exemple 1: Revisiter un projet après 1 mois

```
1. Ouvrir l'appli
2. Voir dans "Projets précédents": "my-api v1.0"
3. Cliquer "Activer"
4. Poser la question: "Que fait la fonction getUserById ?"
5. Obtenir la réponse basée sur le code original
```

### Exemple 2: Comparer 2 versions d'un projet

```
1. Uploader "my-project-v1.zip" → devient ACTIF
2. Poser 5 questions
3. Uploader "my-project-v2.zip" → devient ACTIF
4. Poser les MÊMES 5 questions
5. Comparer les réponses côte à côte
```

### Exemple 3: Exporter pour documentation

```
1. Projet "my-project" actif
2. Générer: doc, recommend, overview, explain × 10
3. GET /projects/1/export
4. Télécharger JSON
5. Convertir en PDF/Word pour la présentation
```

---

## ⚠️ Limitations actuelles

### SQLite
- ❌ Une seule personne peut utiliser l'app
- ⚠️ Performance dégradée avec > 100k chunks

### PostgreSQL
- Nécessite un serveur PostgreSQL
- Nécessite configuration (voir POSTGRESQL_GUIDE.md)

---

## 🚀 Prochaines améliorations possibles

- [ ] Interface pour voir les analyses précédentes
- [ ] Comparer 2 projets côte à côte
- [ ] Supprimer un projet
- [ ] Archiver vs supprimer
- [ ] Collaboration multi-utilisateurs (avec PostgreSQL)
- [ ] Versioning des projets (v1, v2, v3)

---

## 📞 Support

**Question:** Où sont mes données?
**Réponse:** 
- SQLite: `data/ai_assistant.db`
- PostgreSQL: Votre serveur PostgreSQL

**Question:** Je peux effacer les anciens projets?
**Réponse:** Pas encore via l'UI, mais vous pouvez:
```bash
sqlite3 data/ai_assistant.db "DELETE FROM projects WHERE id = 1;"
```

**Question:** Puis-je backup mes projets?
**Réponse:** 
- SQLite: Copier `data/ai_assistant.db`
- PostgreSQL: `pg_dump -U ai_user -d ai_assistant > backup.sql`
