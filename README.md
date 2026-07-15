# 🤖 AI Code Assistant — EY Internship Project

> An **AI-powered assistant** designed to improve developer productivity by analyzing, explaining, and documenting source code with intelligent recommendations.

## 📋 Overview

The **AI Code Assistant** is a modern software tool that helps development teams work more efficiently with their codebase. By leveraging advanced language models and semantic search, it provides instant access to code explanations, generates technical documentation, and delivers actionable development recommendations.

### Core Capabilities

1. **📖 Code Explanations** (`explain`) — Understand what specific functions, classes, or modules do
2. **🔍 Semantic Search** (`search`) — Find relevant code snippets by natural language queries
3. **📚 Documentation Generation** (`doc`) — Auto-generate docstrings and technical documentation
4. **✅ Development Recommendations** (`recommend`) — Get optimization, best practices, and security analysis
5. **🏗️ Project Overview** (`overview`) — Generate a high-level architecture summary
6. **📤 Project Upload** — Ingest entire projects (ZIP files) in 20-30 seconds

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone and navigate
git clone <repo>
cd ai-code-assistant

# 2. Set up Python environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your Groq API key:
# GROQ_API_KEY=your_key_here
# GROQ_MODEL=llama-3.3-70b-versatile
```

### Run the Application

**Backend (FastAPI, port 8000):**
```bash
.venv\Scripts\python.exe -m uvicorn backend.api.server:app --host 0.0.0.0 --port 8000
```

**Frontend (React/Vite, port 5173):**
```bash
cd frontend
npm install
npm run dev
```

Open your browser to **http://localhost:5173**

---

## 📖 Usage

### 1. Upload Your Project

1. Click **"Upload Project"** in the web interface
2. Select a ZIP file containing your source code
3. Wait 20-30 seconds for ingestion (ingest, parse, chunk, embed, index)

### 2. Ask Questions

**Explain Code:**
```
"Qu'est-ce que la fonction est_tdr() ?"
"Comment fonctionne le parsing JavaScript ?"
```

**Search Code:**
```
"Trouve-moi du code lié à la vectorisation"
"Quels fichiers gèrent les embeddings ?"
```

**Generate Documentation:**
```
"Génère la documentation pour la classe Retriever"
```

**Get Recommendations:**
```
"Recommande des optimisations pour embeddings.py"
"Analyse la sécurité de loader.py"
```

**Project Overview:**
```
"Donne-moi un aperçu de l'architecture du projet"
```

---

## 🏗️ Architecture

```
ai-code-assistant/
├── backend/                    # Python FastAPI application
│   ├── ingestion/              # ZIP upload → in-memory extraction
│   ├── parsing/                # AST analysis (Python + JavaScript)
│   ├── rag/                    # RAG pipeline (chunking, embeddings, retrieval)
│   │   ├── chunker.py          # Split code by function/class
│   │   ├── embeddings.py       # Batch vectorization (sentence-transformers)
│   │   ├── vectorstore.py      # ChromaDB persistence
│   │   └── retriever.py        # Semantic search gateway
│   ├── assistant/              # Business logic modules
│   │   ├── llm_client.py       # Groq API with retry logic
│   │   ├── explain.py          # Code explanation
│   │   ├── search.py           # Semantic search
│   │   ├── doc_generator.py    # Documentation generation
│   │   ├── recommend.py        # Development recommendations
│   │   └── overview.py         # Project architecture summary
│   └── api/
│       └── server.py           # FastAPI endpoints
│
├── frontend/                   # React + Vite
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadZone.jsx
│   │   │   └── ResultPanel.jsx
│   │   ├── App.jsx
│   │   └── api.js
│   └── index.html
│
├── data/
│   ├── uploads/                # Temporary project storage
│   └── vectorstore/            # ChromaDB persistence
│
└── requirements.txt
```

---

## 💡 Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **LLM** | Groq API (Llama 3.3 70B) | Code generation & analysis |
| **Embeddings** | sentence-transformers | Semantic search (all-MiniLM-L6-v2) |
| **Vector DB** | ChromaDB | Persistent vector storage |
| **Backend** | FastAPI (Python 3.11+) | REST API & business logic |
| **Frontend** | React + Vite | Modern UI |
| **Code Parsing** | Python AST + Tree-sitter | Structure extraction |

---

## ⚡ Performance Optimizations

### 1. Batch Embedding (5-10x speedup)
- Instead of encoding chunks one-by-one, all embeddings are computed in a single batch operation
- Configuration: `batch_size=32` in `embeddings.py`

### 2. In-Memory ZIP Processing (10x faster ingestion)
- Project files are extracted directly from ZIP in memory
- Eliminates disk I/O bottleneck (~177s saved)
- Ingestion time: **20-30 seconds for typical projects**

### 3. Automatic Rate Limit Handling
- Groq API rate limits are detected and managed automatically
- Exponential backoff retry (3s, 6s, 12s, 24s, 48s)
- Zero user intervention needed

### 4. Semantic Search Optimization
- Distance threshold set to infinity (accept all semantically valid results)
- Increased `top_k` to 20-50 results for better context
- Results ranked by semantic relevance

---

## 🔧 API Endpoints

### POST `/ingest`
Upload and index a project
```json
{
  "zip_file": "project.zip"
}
```
**Response:** `{ "indexed_chunks": 64, "time_seconds": 22.5 }`

### POST `/explain`
Explain a specific code element
```json
{
  "question": "What does the Retriever class do?",
  "top_k": 20
}
```
**Response:** Markdown explanation with code citations

### POST `/search`
Find relevant code by semantic query
```json
{
  "question": "Show me code related to embeddings",
  "top_k": 20
}
```
**Response:** List of relevant code snippets with sources

### POST `/doc`
Generate documentation
```json
{
  "question": "Generate docs for the chunker module",
  "top_k": 20
}
```
**Response:** Markdown documentation

### POST `/recommend`
Get code recommendations
```json
{
  "question": "Recommend optimizations for embeddings.py",
  "top_k": 20
}
```
**Response:** Structured recommendations (optimization, best practices, security)

### GET `/overview`
Get project architecture summary
**Response:** Markdown project overview

---

## 🛠️ Development Features

### System Prompts
All assistant modules use strict system prompts to prevent hallucinations:
- "Only use code from the provided CONTEXT"
- "Never invent functionality"
- "Cite the source [file:line] for every observation"
- Temperature: 0.1 (factual, stable responses)

### Logging
Comprehensive logging at each pipeline stage:
```
✓ Scan: 0.32s
✓ Chunking: 0.40s
✓ Embedding: 12.33s
✓ Storage: 2.23s
```

---

## 📊 Project Status

| Feature | Status | Notes |
|---------|--------|-------|
| Project Upload (ZIP) | ✅ Complete | 20-30s ingestion time |
| Code Explanation | ✅ Complete | Supports Python & JavaScript |
| Semantic Search | ✅ Complete | Optimized with batch embedding |
| Documentation Generation | ✅ Complete | Auto-generates docstrings |
| Development Recommendations | ✅ Complete | Optimization, best practices, security |
| Project Overview | ✅ Complete | Architecture summary |
| Rate Limit Handling | ✅ Complete | Automatic retry with backoff |
| UI/UX | ✅ Complete | React + responsive design |

---

## 🚀 Download & Use

To use this project:

1. **Download** the source code:
   ```bash
   git clone <repository-url>
   cd ai-code-assistant
   ```

2. **Install dependencies** (see Quick Start above)

3. **Configure your Groq API key** in `.env`

4. **Run both backend and frontend**

5. **Open** http://localhost:5173 in your browser

6. **Upload a project ZIP** and start analyzing!

---

## 🎯 Future Improvements (Out of Scope)

- [ ] Support for C/C++, Java, Go parsing
- [ ] Multi-LLM support (local LLaMA, Claude, etc.)
- [ ] Advanced code refactoring suggestions
- [ ] Team collaboration features
- [ ] CI/CD integration
- [ ] Web-based IDE integration

---

## 📝 License

This project was developed as part of the EY internship program.

---

## 👨‍💼 About

**Developed by:** [Your Name]  
**Internship:** EY — 2024  
**Purpose:** Improve developer productivity through AI-assisted code analysis and documentation  
**Stack:** Python + FastAPI + React + Groq API  
**Duration:** [Internship Period]

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
