# 🗄️ PostgreSQL Configuration Guide

## Overview

L'application supporte **SQLite en développement** et **PostgreSQL en production**. Cette guide explique comment configurer chacun.

---

## 📍 Où est PostgreSQL ?

PostgreSQL **n'est pas installé par défaut** dans le projet. Vous avez 2 options :

### Option 1: Développement avec SQLite ✅ (Défaut)
- Fichier: `data/ai_assistant.db`
- Avantage: Zéro configuration, tout fonctionne out-of-the-box
- Inconvénient: Single-user, pas de concurrence
- **C'est le mode par défaut**

### Option 2: Production avec PostgreSQL
- Serveur PostgreSQL séparé (cloud ou local)
- Avantage: Multi-user, haute disponibilité, scalabilité
- Inconvénient: Nécessite configuration

---

## 🚀 Activer PostgreSQL

### Étape 1: Installer PostgreSQL

**Windows:**
```bash
# Télécharger depuis https://www.postgresql.org/download/windows/
# Ou via Chocolatey:
choco install postgresql
```

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

### Étape 2: Créer la base de données

```bash
# Connexion par défaut (user: postgres)
psql -U postgres

# Créer la base
CREATE DATABASE ai_assistant;
CREATE USER ai_user WITH PASSWORD 'your_secure_password';
ALTER ROLE ai_user SET client_encoding TO 'utf8';
ALTER ROLE ai_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ai_user SET default_transaction_deferrable TO on;
GRANT ALL PRIVILEGES ON DATABASE ai_assistant TO ai_user;
\q
```

### Étape 3: Configurer l'environnement

Créer/modifier `.env` à la racine du projet :

```bash
# Activer PostgreSQL
USE_POSTGRES=true

# Chaîne de connexion
DATABASE_URL=postgresql://ai_user:your_secure_password@localhost:5432/ai_assistant

# Autres configs (inchangé)
GROQ_API_KEY=gsk_xxxxx
GROQ_MODEL=llama-3.3-70b-versatile
```

### Étape 4: Initialiser la BD

```bash
python -c "from backend.db import init_db; init_db()"
```

Vous devriez voir: `✓ Database initialized (postgresql://...)`

---

## 🐳 PostgreSQL via Docker (Production Recommandé)

Le `docker-compose.yml` **inclut déjà PostgreSQL**:

```bash
# Démarrer tout (API + PostgreSQL)
docker-compose up -d

# Vérifier que PostgreSQL est prêt
docker-compose logs postgres
```

C'est automatiquement configuré avec:
- User: `postgres`
- Password: `postgres`
- Database: `ai_assistant`
- Host: `postgres` (depuis le container)

---

## 📊 Vérifier que ça marche

### Via SQLAlchemy:
```bash
python -c "
from backend.db import SessionLocal
db = SessionLocal()
print('✓ Connexion OK')
db.close()
"
```

### Via psql (si PostgreSQL local):
```bash
psql -U ai_user -d ai_assistant -c 'SELECT * FROM projects LIMIT 1;'
```

---

## 🔄 Switching SQLite ↔ PostgreSQL

Si vous travaillez localement en SQLite et voulez tester PostgreSQL:

```bash
# Développement (SQLite) - défaut
unset USE_POSTGRES  # ou USE_POSTGRES=false

# Production (PostgreSQL)
export USE_POSTGRES=true
export DATABASE_URL="postgresql://ai_user:password@localhost:5432/ai_assistant"
```

Puis redémarrer l'API:
```bash
python -m uvicorn backend.api.server:app --reload
```

---

## 📚 Tables de la BD

PostgreSQL crée automatiquement ces tables:

```sql
-- Projets uploadés
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    uploaded_at TIMESTAMP DEFAULT NOW(),
    vectorstore_collection_id VARCHAR(255) UNIQUE
);

-- Historique d'indexation (chunks, temps, fichiers)
CREATE TABLE index_histories (
    id SERIAL PRIMARY KEY,
    project_id INTEGER FOREIGN KEY,
    files_found INTEGER,
    chunks_created INTEGER,
    files_metadata JSON,
    embedding_time_ms INTEGER,
    indexed_at TIMESTAMP DEFAULT NOW()
);

-- Analyses sauvegardées (explain, recommend, etc.)
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    project_id INTEGER FOREIGN KEY,
    feature VARCHAR(50),  -- "explain", "recommend", "doc", "deployment"
    question TEXT,
    response TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🆘 Troubleshooting

### "FATAL: Ident authentication failed"
```bash
# Problème: pg_hba.conf utilise "ident" au lieu de "md5"
# Solution: Modifier /etc/postgresql/*/main/pg_hba.conf
# Changer: ident → md5
sudo nano /etc/postgresql/15/main/pg_hba.conf
sudo systemctl restart postgresql
```

### "Connection refused"
```bash
# PostgreSQL n'est pas lancé
# Redémarrer:
sudo systemctl start postgresql  # Linux
brew services start postgresql@15  # macOS
# Ou via l'application Windows Services
```

### "Database does not exist"
```bash
# Créer la base:
psql -U postgres -c "CREATE DATABASE ai_assistant;"
```

### "invalid password"
```bash
# Vérifier DATABASE_URL dans .env
# Tester la connexion:
psql -U ai_user -d ai_assistant -h localhost
```

---

## 🔐 Sécurité en Production

**À NE PAS FAIRE:**
- ❌ Pas de mot de passe en dur dans le code
- ❌ Pas d'authentification "ident" sur le réseau
- ❌ Pas de port 5432 exposé à Internet

**À FAIRE:**
- ✅ Utiliser des secrets (AWS Secrets Manager, Azure Key Vault, etc.)
- ✅ Enable SSL/TLS pour la connexion
- ✅ Firewall restrictif (port 5432 accessible UNIQUEMENT depuis l'app)
- ✅ Backups réguliers

Exemple config sécurisée:
```bash
DATABASE_URL="postgresql://user:password@postgres.internal:5432/ai_assistant?sslmode=require"
```

---

## 📌 Résumé

| Mode | Fichier | Configuration | Idéal pour |
|------|---------|---------------|-----------|
| **SQLite** | `data/ai_assistant.db` | Aucune | Développement |
| **PostgreSQL Local** | Serveur `localhost:5432` | `.env` | Tests intégration |
| **PostgreSQL Docker** | Container `postgres:15` | `docker-compose.yml` | Staging/Production |
| **PostgreSQL Cloud** | AWS RDS, Azure DB, etc. | Variables d'env | Production |

---

## 📖 Liens utiles

- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [SQLAlchemy PostgreSQL](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
- [psql Cheat Sheet](https://www.postgresqltutorial.com/psql-commands/)
