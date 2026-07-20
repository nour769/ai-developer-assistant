.PHONY: help install dev prod test clean migrate

help:
	@echo "🚀 AI Assistant - Available Commands"
	@echo ""
	@echo "Development:"
	@echo "  make dev              - Start dev server (SQLite)"
	@echo "  make install          - Install Python dependencies"
	@echo "  make clean            - Clean cache, test files"
	@echo ""
	@echo "Production:"
	@echo "  make prod             - Start with docker-compose (PostgreSQL)"
	@echo "  make prod-logs        - View production logs"
	@echo "  make prod-stop        - Stop docker containers"
	@echo ""
	@echo "Database:"
	@echo "  make migrate          - Initialize database"
	@echo "  make db-shell         - Open SQLite shell"
	@echo "  make db-postgres      - Open PostgreSQL shell"
	@echo ""
	@echo "Testing:"
	@echo "  make test             - Run test suite"
	@echo "  make test-deployment  - Test deployment endpoint"
	@echo ""
	@echo "Frontend:"
	@echo "  make frontend-dev     - Start frontend dev server"
	@echo "  make frontend-build   - Build frontend production"

install:
	pip install -r requirements.txt
	@echo "✅ Dependencies installed"

dev:
	@echo "🚀 Starting development server..."
	python -m uvicorn backend.api.server:app --port 8000 --reload

prod:
	@echo "🐳 Starting production with Docker..."
	docker-compose up -d
	@echo "✅ Services running"
	@echo "  Backend:   http://localhost:8000"
	@echo "  Frontend:  http://localhost:5173"
	@echo "  Database:  localhost:5432"

prod-logs:
	docker-compose logs -f

prod-stop:
	docker-compose down
	@echo "✅ Services stopped"

migrate:
	python -c "from backend.db import init_db; init_db()"
	@echo "✅ Database initialized"

db-shell:
	sqlite3 ./data/ai_assistant.db

db-postgres:
	psql -U postgres -d ai_assistant -h localhost

test:
	pytest backend/tests/ -v

test-deployment:
	python -c "\
	import requests; \
	resp = requests.post('http://localhost:8000/deployment', json={ \
	  'project_name': 'Test', \
	  'service': 'AWS', \
	  'usage_level': 'small' \
	}); \
	print(resp.json())"

test-projects:
	curl http://localhost:8000/projects | python -m json.tool

test-health:
	curl http://localhost:8000/health

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf .coverage
	@echo "✅ Cache cleaned"

frontend-dev:
	cd frontend && npm install && npm run dev

frontend-build:
	cd frontend && npm install && npm run build

docs:
	@echo "📖 Documentation Files:"
	@echo "  - README_REMARQUES.md      (Start here!)"
	@echo "  - POUR_ENCADRANT.md        (Executive summary)"
	@echo "  - DEPLOYMENT_GUIDE.md      (Complete guide)"
	@echo "  - IMPLEMENTATION_SUMMARY.md (Technical details)"
	@echo "  - CHANGELOG.md             (All changes)"

.DEFAULT_GOAL := help
