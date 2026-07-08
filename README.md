# AI Code Assistant — EY Internship Project

Assistant IA pour comprendre, documenter et analyser des projets de code source.

## Architecture

```
ai-code-assistant/
├── backend/
│   ├── ingestion/      # Upload + extraction de projets (zip -> arborescence)
│   ├── parsing/        # Analyse AST : extraction fonctions/classes/imports
│   ├── rag/             # Chunking, embeddings, stockage vectoriel, retrieval
│   ├── assistant/       # Logique métier : explain, search, overview, doc-gen
│   ├── api/             # Point d'entrée (CLI pour l'instant, API plus tard)
│   └── tests/           # Tests sur des mini-projets réels
├── data/
│   ├── uploads/          # Projets uploadés (zip extraits) — ignoré par git
│   └── vectorstore/      # Base vectorielle Chroma persistée — ignoré par git
├── .env.example
├── requirements.txt
└── README.md
```

## Pipeline global

```
ZIP projet
   ↓ ingestion/
Arborescence + fichiers filtrés
   ↓ parsing/
Fonctions, classes, imports (AST)
   ↓ rag/chunking
Chunks avec métadonnées (fichier, fonction, langage)
   ↓ rag/embeddings
Vecteurs
   ↓ rag/vectorstore
Base Chroma (vecteur + métadonnée + code source)
   ↓ assistant/
Question utilisateur → retrieval → prompt Groq → réponse
```

## Stack technique

- **Langage** : Python 3.11+
- **LLM** : Groq API (Llama 3.3) — génération de texte
- **Embeddings** : sentence-transformers (local, `all-MiniLM-L6-v2`)
- **Vector DB** : Chroma (local, simple à démarrer)
- **Parsing** : module `ast` natif Python (semaine 1), Tree-sitter en option si multi-langage
- **Interface** : CLI d'abord, Streamlit ensuite

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # puis remplir GROQ_API_KEY
```

## Utilisation (à venir au fil des semaines)

```bash
python -m backend.api.cli ingest data/uploads/mon_projet.zip
python -m backend.api.cli explain backend/ingestion/loader.py
python -m backend.api.cli ask "Where is authentication handled?"
```
