"""
Deployment Architecture Generator - Agent Intelligent

Analyse le code ET propose une architecture de déploiement optimale basée sur:
- Service cloud (AWS, Azure, Private Server)
- Volume d'usage (small: <1000 req/day, huge: >10k req/day)
- Type de service (Web App, Job, Worker, API, Real-time)
- Exposition d'IP (public, private, hybrid)
- Type de data (confidentiel, public, mixed)

Génère configuration production-ready avec:
- Infrastructure as Code (Terraform/CloudFormation)
- Docker et orchestration
- Database scaling et backup strategies
- Load balancing et HA/DR
- Monitoring et observabilité
- Cost estimation par provider
- Recommandations de sécurité
"""

from backend.assistant.llm_client import call_llm
from backend.rag.retriever import retrieve_context, format_context, AUCUN_CONTEXTE_PERTINENT


def generate_deployment_architecture(
    project_name: str,
    service: str = "AWS",
    usage_level: str = "small",
    service_type: str = "web",
    ip_exposure: str = "public",
    data_type: str = "public",
    top_k: int = 20
) -> str:
    """
    Agent intelligent qui génère une architecture de déploiement COMPLÈTE et optimale.
    
    Args:
        project_name: Nom du projet
        service: "AWS", "Azure", ou "Private"
        usage_level: "small" (<1k req/day) ou "huge" (>100k req/day)
        service_type: "web", "job", "worker", "api", "realtime", "data_pipeline"
        ip_exposure: "public", "private", "hybrid"
        data_type: "public", "confidential", "mixed"
        top_k: Nombre de chunks à récupérer
    
    Returns:
        Architecture PRODUCTION-READY avec backup, coûts, sécurité, etc.
    """
    
    # Validation des paramètres
    services = ["AWS", "Azure", "Private"]
    usage_levels = ["small", "huge"]
    service_types = ["web", "job", "worker", "api", "realtime", "data_pipeline"]
    ip_exposures = ["public", "private", "hybrid"]
    data_types = ["public", "confidential", "mixed"]
    
    if service not in services:
        return f"❌ Service invalide. Choisir: {', '.join(services)}"
    if usage_level not in usage_levels:
        return f"❌ Usage level invalide. Choisir: {', '.join(usage_levels)}"
    if service_type not in service_types:
        return f"❌ Service type invalide. Choisir: {', '.join(service_types)}"
    if ip_exposure not in ip_exposures:
        return f"❌ IP exposure invalide. Choisir: {', '.join(ip_exposures)}"
    if data_type not in data_types:
        return f"❌ Data type invalide. Choisir: {', '.join(data_types)}"
    
    # Détermine l'estimation de charges
    load_mapping = {
        "small": "< 1000 req/day, < 100 concurrent users, < 100 GB data",
        "huge": "> 100k req/day, > 10k concurrent users, > 10 TB data"
    }
    load_estimation = load_mapping[usage_level]
    
    # Service-specific configurations DÉTAILLÉES
    service_configs = {
        "AWS": {
            "web": {"compute": "ALB + Auto Scaling Group + EC2/ECS", "default_instance": "t3.medium"},
            "job": {"compute": "Lambda / Glue / Batch", "default_instance": "batch_compute"},
            "worker": {"compute": "SQS + Lambda / EC2 workers", "default_instance": "t3.small"},
            "api": {"compute": "API Gateway + Lambda / ALB + ECS", "default_instance": "t3.medium"},
            "realtime": {"compute": "AppSync + DynamoDB Streams / ALB + WebSocket", "default_instance": "m5.large"},
            "data_pipeline": {"compute": "Glue / EMR / Data Pipeline", "default_instance": "m5.xlarge"}
        },
        "Azure": {
            "web": {"compute": "App Service / Container Instances", "default_instance": "B2"},
            "job": {"compute": "Batch / Functions / Logic Apps", "default_instance": "batch_compute"},
            "worker": {"compute": "Service Bus + Functions / VMs", "default_instance": "B1s"},
            "api": {"compute": "API Management + App Service", "default_instance": "B2"},
            "realtime": {"compute": "SignalR Service + App Service", "default_instance": "S1"},
            "data_pipeline": {"compute": "Data Factory / Synapse", "default_instance": "pay_per_use"}
        },
        "Private": {
            "web": {"compute": "Kubernetes Deployment + Ingress / Docker Swarm", "default_instance": "2vCPU 4GB"},
            "job": {"compute": "Kubernetes CronJob / Celery + Redis", "default_instance": "1vCPU 2GB"},
            "worker": {"compute": "Kubernetes StatefulSet / Worker Pods", "default_instance": "2vCPU 4GB"},
            "api": {"compute": "Kubernetes Service + Ingress", "default_instance": "2vCPU 4GB"},
            "realtime": {"compute": "Kubernetes with message broker", "default_instance": "4vCPU 8GB"},
            "data_pipeline": {"compute": "Kubernetes Jobs + PVC", "default_instance": "4vCPU 8GB"}
        }
    }
    
    # Stratégies de backup par service
    backup_strategies = {
        "AWS": {
            "confidential": "AWS Backup + encrypted snapshots + cross-region replication + vault lock",
            "mixed": "AWS Backup + daily snapshots + 7-day retention",
            "public": "Daily snapshots + 3-day retention"
        },
        "Azure": {
            "confidential": "Azure Backup + customer-managed keys + geo-redundant storage + immutable backups",
            "mixed": "Azure Backup + locally redundant storage + 30-day retention",
            "public": "Managed backup + 7-day retention"
        },
        "Private": {
            "confidential": "On-site backup + encrypted storage + air-gapped backup + 24/7 monitoring",
            "mixed": "Incremental backups + nightly full backup + 30-day retention",
            "public": "Backup to NAS + 7-day retention"
        }
    }
    
    # Coûts estimés mensuels (fourchette USD)
    cost_estimation = {
        "AWS": {
            ("web", "small", "public"): {"compute": 50, "db": 15, "cdn": 5, "total": 70},
            ("web", "small", "confidential"): {"compute": 100, "db": 50, "cdn": 10, "total": 160},
            ("web", "huge", "public"): {"compute": 500, "db": 200, "cdn": 100, "total": 800},
            ("web", "huge", "confidential"): {"compute": 1000, "db": 500, "cdn": 150, "total": 1650},
            ("job", "small", "public"): {"compute": 20, "db": 10, "storage": 5, "total": 35},
            ("job", "huge", "confidential"): {"compute": 300, "db": 100, "storage": 50, "total": 450},
            ("worker", "small", "public"): {"compute": 30, "queue": 5, "total": 35},
            ("worker", "huge", "public"): {"compute": 200, "queue": 50, "total": 250},
            ("api", "small", "public"): {"compute": 40, "db": 20, "total": 60},
            ("api", "huge", "confidential"): {"compute": 800, "db": 400, "total": 1200},
            ("realtime", "small", "public"): {"compute": 80, "db": 50, "total": 130},
            ("realtime", "huge", "confidential"): {"compute": 1500, "db": 800, "total": 2300},
            ("data_pipeline", "huge", "confidential"): {"compute": 1000, "storage": 200, "total": 1200}
        },
        "Azure": {
            ("web", "small", "public"): {"compute": 60, "db": 15, "total": 75},
            ("web", "small", "confidential"): {"compute": 120, "db": 60, "total": 180},
            ("web", "huge", "public"): {"compute": 550, "db": 220, "total": 770},
            ("api", "small", "public"): {"compute": 50, "db": 25, "total": 75},
            ("realtime", "small", "public"): {"compute": 100, "signalr": 50, "total": 150},
        },
        "Private": {
            ("web", "small", "public"): {"compute": 100, "db": 50, "storage": 20, "total": 170},
            ("web", "huge", "public"): {"compute": 800, "db": 300, "storage": 200, "total": 1300},
        }
    }
    
    # Configuration par IP exposure
    network_configs = {
        "public": {
            "ingress": "Public Load Balancer + DNS",
            "firewall": "WAF (Web Application Firewall)",
            "ddos": "DDoS Protection (AWS Shield / Azure DDoS)",
            "ssl": "Auto-renewing SSL/TLS (Let's Encrypt ou managed)"
        },
        "private": {
            "ingress": "Private VPC / Private Kubernetes Service",
            "firewall": "Network ACL + Security Groups",
            "ddos": "Not exposed (internal only)",
            "ssl": "Optional - internal mTLS"
        },
        "hybrid": {
            "ingress": "Public Load Balancer + Private backend",
            "firewall": "WAF + Network segmentation",
            "ddos": "DDoS Protection on public layer",
            "ssl": "SSL termination on LB + mTLS to backend"
        }
    }
    
    # Récupère le contexte du code
    question = f"architecture technologie stack dépendances framework {project_name}"
    matches = retrieve_context(question, top_k=top_k)
    
    if matches and matches != AUCUN_CONTEXTE_PERTINENT:
        context = format_context(matches)
    else:
        context = f"Projet: {project_name}\n(Analyse: voir overview pour structure complète)"
    
    # Détermine les coûts
    cost_key = (service_type, usage_level, data_type if data_type != "mixed" else "public")
    if service in cost_estimation and cost_key in cost_estimation[service]:
        costs = cost_estimation[service][cost_key]
        cost_str = " | ".join([f"{k}: ${v}" for k, v in costs.items() if k != "total"])
        cost_monthly = costs.get("total", "N/A")
    else:
        cost_str = "See service pricing"
        cost_monthly = "Variable"
    
    # Configuration réseau
    network_info = network_configs.get(ip_exposure, {})
    
    # Configuration spécifique au service
    service_conf = service_configs.get(service, {}).get(service_type, {})
    compute_type = service_conf.get("compute", "TBD")
    
    # Stratégie de backup
    backup_strategy = backup_strategies.get(service, {}).get(data_type, "Standard backup")
    
    # System prompt amélioré
    system_prompt = f"""Tu es un expert en architecture cloud et déploiement production.

CONTEXTE DE DÉPLOIEMENT:
- **Service Cloud**: {service}
- **Volume d'Usage**: {usage_level} ({load_estimation})
- **Type de Service**: {service_type} (compute: {compute_type})
- **Exposition**: {ip_exposure} network
- **Type de Data**: {data_type}
- **Coûts Estimés**: {cost_monthly}/mois ({cost_str})
- **Backup Strategy**: {backup_strategy}

Tu dois générer une architecture COMPLÈTE et ACTIONABLE:
1. OPTIMISÉE pour {service}
2. DIMENSIONNÉE pour {usage_level} usage
3. SÉCURISÉE pour data de type {data_type}
4. BACKUP compatible: {backup_strategy}
5. COÛTS: environ ${cost_monthly}/mois
6. PRÊTE À DÉPLOYER du jour 1

STRUCTURE DE RÉPONSE (OBLIGATOIRE):

## 📋 Vue d'ensemble
[Diagramme ASCII]

## 🏗️ Architecture Spécifique à {service}
- Compute: {compute_type}
- Database: [managed/self-hosted selon service]
- Network: {ip_exposure} exposure config

## 💾 Stratégie Backup Recommandée
{backup_strategy}
- RPO (Recovery Point Objective): [heure/jour]
- RTO (Recovery Time Objective): [minutes/heures]
- Test de recovery: Tous les [30/90 jours]

## 🛡️ Sécurité pour {data_type} Data
[Encryption, access control, audit logging]

## 💵 Coûts Détaillés
Estimé: ${cost_monthly}/mois ({cost_str})
[Breakdown par composant]

## 🚀 Déploiement (blue-green recommended)
1. Dev local
2. Staging
3. Production canary (5% traffic)
4. Production full

## 📊 Monitoring & Observabilité
[Metrics clés, logs, alertes]"""
    
    prompt = f"""Génère une architecture PRODUCTION-READY COMPLÈTE pour:

**PROJECT**: {project_name}
**CLOUD SERVICE**: {service}
**SERVICE TYPE**: {service_type}
**IP EXPOSURE**: {ip_exposure}
**DATA TYPE**: {data_type}
**USAGE LEVEL**: {usage_level} ({load_estimation})

**CONTEXTE DU CODE**:
{context}

REQUIREMENTS ABSOLUS:
1. ✓ Recommandations de BACKUP détaillées (RPO/RTO)
2. ✓ IP exposure config ({ip_exposure})
3. ✓ Adapté à type de service: {service_type}
4. ✓ Sécurité pour data: {data_type}
5. ✓ Coûts estimés: ${cost_monthly}/mois
6. ✓ Infrastructure as Code (prêt à copier-coller)
7. ✓ HA/DR strategy
8. ✓ Monitoring et alertes

Génère l'architecture COMPLÈTE ET ACTIONABLE!
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

