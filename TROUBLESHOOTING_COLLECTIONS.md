# 🔧 Troubleshooting: Projets vides après activation

## Le problème
Vous activez un projet, mais vous obtenez: **"❌ Aucun code pertinent trouvé"** 

Même si le projet avait du code avant.

---

## 🔍 Diagnostic rapide

### 1. Vérifiez le nombre de chunks affichés

**Avant v3.1:** Pas d'info visible
**Après v3.1:** Cliquez sur un projet → voyez `📦 Chunks: X`

```
✓ ACTIF  Mon Projet  14 sept
         14 sept, 14:32        [✓ Activé]
         
Expand pour voir:
  📦 Chunks: 156    ← C'est bon!
  🆔 Collection: code_chunks_a1b2...
```

**Si vous voyez `📦 Chunks: 0` → C'est le problème!**

---

## 🛠️ Solutions

### Solution 1: Réuploader le projet

La collection est corrompue. La plus simple:

```
1. Supprimez le fichier data/ai_assistant.db (ou la BD PostgreSQL)
2. Réuploadez le zip
3. Essayez l'explain
```

Vous verrez alors `📦 Chunks: 156` et ça devrait marcher.

### Solution 2: Vérifier la BD (SQLite)

Utilisez un client SQLite pour inspecter:

```bash
# Installer sqlite3 CLI (si pas présent)
# Puis:
sqlite3 data/ai_assistant.db

# Voir tous les projets
SELECT id, name, vectorstore_collection_id FROM projects;

# Voir combien de fois chaque projet a été indexé
SELECT project_id, files_found, chunks_created FROM index_histories;
```

**Résultat attendu:**
```
project_id | files_found | chunks_created
1          | 42          | 156
```

**Résultat problématique:**
```
project_id | files_found | chunks_created
1          | 42          | 0    ← 0 chunks = problème!
```

### Solution 3: Vérifier ChromaDB directement

```bash
python -c "
from backend.rag.vectorstore import _client, get_collection_count

# Lister toutes les collections
all_cols = _client.list_collections()
print(f'Collections trouvées: {len(all_cols)}')
for col in all_cols:
    count = get_collection_count(col.name)
    print(f'  - {col.name}: {count} chunks')
"
```

**Résultat attendu:**
```
Collections trouvées: 2
  - code_chunks_a1b2c3d4: 156 chunks
  - code_chunks_e5f6g7h8: 0 chunks  (l'ancienne peut être vide)
```

---

## 📋 Ce qui a changé en v3.1

### Avant (bugué)
```
set_active_collection() → get_or_create_collection()
                          → si n'existe pas: CRÉE UNE VIDE!
                          → cherche dedans: 0 résultats ❌
```

### Après (fixé)
```
set_active_collection() → get_collection()
                       → si n'existe pas: ERREUR explicite!
POST /projects/1/activate retourne:
  ❌ si collection vide: "La collection est vide..."
  ✓ si OK: "Project activé (156 chunks trouvés)"
```

---

## 🚀 Flux de test recommandé

### 1. Vérifier la liste des projets

```bash
curl http://localhost:8000/projects | python -m json.tool
```

Résultat:
```json
{
  "projects": [
    {
      "id": 1,
      "name": "mon-projet",
      "chunks_count": 156,      ← C'est l'info clé!
      "is_active": false
    }
  ]
}
```

### 2. Activer le projet

```bash
curl -X POST http://localhost:8000/projects/1/activate | python -m json.tool
```

Résultat attendu:
```json
{
  "message": "✓ Projet 'mon-projet' activé (156 chunks trouvés)",
  "chunks_count": 156
}
```

Résultat problématique:
```json
{
  "detail": "⚠️ La collection pour 'mon-projet' est vide..."
}
```

### 3. Tester explain

```bash
curl -X POST http://localhost:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"question": "Que fait la fonction main ?"}' | python -m json.tool
```

Résultat:
```json
{
  "result": "La fonction main..."
}
```

---

## 🐛 Cas limites

### Cas 1: Collection existe mais est vide

**Symptôme:** `📦 Chunks: 0`
**Cause:** L'upload a échoué silencieusement
**Solution:** Réuploader

### Cas 2: Collection introuvable

**Symptôme:** Erreur lors de l'activation
**Cause:** ChromaDB ne peut pas trouver le fichier
**Solution:** `rm -rf data/vectorstore/` puis réupload

### Cas 3: Plusieurs collections pour 1 projet

**Symptôme:** Confusing
**Cause:** Ancien bug du reset
**Solution:** Nettoyer la BD et recommencer

---

## 🔄 Workflow sûr

Si vous doutez, faites ça:

```bash
# 1. Arrêter l'API
# (Ctrl+C dans le terminal)

# 2. Nettoyer les données (⚠️ tout est perdu!)
rm data/ai_assistant.db
rm -rf data/vectorstore/

# 3. Redémarrer l'API
python -m uvicorn backend.api.server:app --reload

# 4. Réuploader vos projets
# (Via l'UI)

# 5. Tester explain
# (Via l'UI)
```

---

## 📞 Déboguer en détail

Si ça marche toujours pas, fournissez:

1. **Sortie de GET /projects:**
```bash
curl http://localhost:8000/projects | python -m json.tool
```

2. **Sortie de POST /activate:**
```bash
curl -X POST http://localhost:8000/projects/1/activate | python -m json.tool
```

3. **Logs du backend:**
```bash
# Regarder les erreurs Python
# dans le terminal où vous avez lancé l'API
```

4. **Vérifier ChromaDB:**
```bash
ls -lah data/vectorstore/
ls -lah data/vectorstore/*/  # Voir les collections
```

---

## ✅ Validation

Vous saurez que c'est fixé quand:

- ✅ L'interface montre `📦 Chunks: 156` (ou votre nombre)
- ✅ POST /activate retourne un message de succès
- ✅ explain() retourne du code pertinent
- ✅ Pas d'erreur ChromaDB dans le terminal

**Bonne chance!** 🚀
