"""
Deployment Architecture Generator - Agent Intelligent

Analyse le code ET propose une architecture de déploiement optimale basée sur:
- Service cloud (AWS, Azure, Private Server)
- Volume d'usage (small: <1000 req/day, huge: >10k req/day)

Génère configuration production-ready avec:
- Infrastructure as Code (Terraform/CloudFormation)
- Docker et orchestration
- Database scaling
- Load balancing
- Monitoring et observabilité
- Cost optimization
"""

from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_context, format_context


_SYSTEM_PROMPT_TEMPLATE = """Tu es un expert en architecture cloud et déploiement production.

CONTEXTE DE DÉPLOIEMENT:
- **Service Cloud**: {service}
- **Volume d'Usage**: {usage_level}
- **Charges Estimées**: {load_estimation}

Tu dois générer une architecture DE A À Z qui est:
1. **Optimale** pour ce service cloud spécifique
2. **Scalable** selon le volume d'usage
3. **Cost-effective** (pas overprovisionné)
4. **Production-ready** du jour 1
5. **Securisée** (secrets, auth, encryption)

STRUCTURE DE RÉPONSE (STRICTE):

## 📋 Vue d'ensemble
[Diagramme ASCII ou description courte du flux]

## 🏗️ Architecture Détaillée

### Frontend
- Où l'héberger
- CDN/Cache strategy
- Domain/SSL

### Backend
- Instance types/sizing
- Auto-scaling rules
- Load balancer config

### Database
- Type (PostgreSQL, managed ou self-hosted)
- Backup strategy
- Replication pour DR

### Cache & Message Queue
- Redis/ElastiCache
- Kafka/SQS configuration

## 🐳 Infrastructure as Code
[Terraform/CloudFormation/ARM template sample]

## 🔧 Docker & Containers
[Dockerfile optimisé]
[docker-compose ou Kubernetes spec si applicable]

## 💾 Environment Variables
.env.{service}.{usage_level} example

## 📊 Coûts Estimés
[Par service cloud]

## 🚀 Déploiement Par Étapes
1. Dev local
2. Staging
3. Production (blue-green deployment)
4. Monitoring

## 🔒 Sécurité Checklist
- [x] SSL/TLS
- [x] Secrets management
- [x] Database encryption
- [x] DDoS protection
- [x] WAF rules

Sois PRATIQUE et ACTIONNABLE - prêt à copier-coller!"""


def generate_deployment_architecture(
    project_name: str,
    service: str = "AWS",
    usage_level: str = "small",
    top_k: int = 20
) -> str:
    """
    Agent intelligent qui génère une architecture de déploiement optimale.
    
    Args:
        project_name: Nom du projet
        service: "AWS", "Azure", ou "Private"
        usage_level: "small" ou "huge"
        top_k: Nombre de chunks à récupérer
    
    Returns:
        Architecture de déploiement complète et paramétrisée
    """
    
    # Valide les paramètres
    services = ["AWS", "Azure", "Private"]
    usage_levels = ["small", "huge"]
    
    if service not in services:
        return f"❌ Service invalide. Choisir: {', '.join(services)}"
    
    if usage_level not in usage_levels:
        return f"❌ Usage level invalide. Choisir: {', '.join(usage_levels)}"
    
    # Détermine l'estimation de charges
    load_mapping = {
        "small": "< 1000 req/day, < 100 concurrent users, < 100 GB data",
        "huge": "> 100k req/day, > 10k concurrent users, > 10 TB data"
    }
    load_estimation = load_mapping[usage_level]
    
    # Service-specific configurations
    service_info = {
        "AWS": {
            "backend_service": "EC2/ECS/Lambda",
            "db_service": "RDS PostgreSQL / DynamoDB",
            "cache": "ElastiCache (Redis)",
            "cdn": "CloudFront",
            "messaging": "SQS / SNS"
        },
        "Azure": {
            "backend_service": "App Service / Container Instances",
            "db_service": "Azure Database for PostgreSQL / Cosmos DB",
            "cache": "Azure Cache for Redis",
            "cdn": "Azure Front Door / CDN",
            "messaging": "Service Bus / Event Hubs"
        },
        "Private": {
            "backend_service": "Kubernetes / Docker Swarm",
            "db_service": "PostgreSQL self-hosted",
            "cache": "Redis self-hosted",
            "cdn": "Nginx reverse proxy",
            "messaging": "RabbitMQ / Kafka"
        }
    }
    
    services_desc = service_info.get(service, {})
    
    # Récupère le contexte du projet
    question = f"architecture technologie stack dépendances framework {project_name}"
    matches = retrieve_context(question, top_k=top_k)
    
    if matches:
        context = format_context(matches)
    else:
        context = f"Projet: {project_name}\n(Contexte: voir overview pour structure)"
    
    # Crée le system prompt spécifique
    system_prompt = _SYSTEM_PROMPT_TEMPLATE.format(
        service=service,
        usage_level=usage_level,
        load_estimation=load_estimation
    )
    
    prompt = f"""Génère une architecture PRODUCTION-READY complète pour ce projet:

**PROJECT**: {project_name}
**CLOUD SERVICE**: {service}
**USAGE LEVEL**: {usage_level} ({load_estimation})

**SERVICES À UTILISER**:
- Backend: {services_desc.get('backend_service')}
- Database: {services_desc.get('db_service')}
- Cache: {services_desc.get('cache')}
- CDN: {services_desc.get('cdn')}
- Messaging: {services_desc.get('messaging')}

**CONTEXTE DU CODE**:
{context}

**IMPORTANT**:
1. OPTIMISE pour {usage_level} usage ({load_estimation})
2. Fournis du CODE PRÊT À UTILISER (Terraform/CloudFormation/YAML)
3. Inclus les coûts estimés mensuels
4. Explique le scaling (horizontal/vertical)
5. Sois spécifique au service ({service})

Génère une architecture DE A À Z actionnable!
"""
    
    response = call_llm(system_prompt, prompt, temperature=0.1)
    return response


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python -m backend.assistant.deployment <project_name> [service] [usage_level]")
        print("  service: AWS, Azure, Private (default: AWS)")
        print("  usage_level: small, huge (default: small)")
        sys.exit(1)
    
    project_name = sys.argv[1]
    service = sys.argv[2] if len(sys.argv) > 2 else "AWS"
    usage_level = sys.argv[3] if len(sys.argv) > 3 else "small"
    
    print(generate_deployment_architecture(project_name, service, usage_level))

