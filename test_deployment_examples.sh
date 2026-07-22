#!/bin/bash
# ============================================================================
# 🚀 EXAMPLES - Deployment API Advanced
# 
# Copie/colle les commandes curl ci-dessous pour tester l'API deployment
# avec tous les nouveaux paramètres (8 paramètres avancés)
# ============================================================================

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8000"

echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Deployment API - Advanced Examples${NC}"
echo -e "${BLUE}==================================${NC}\n"

# ============================================================================
# EXEMPLE 1: Web App AWS Public (Small)
# ============================================================================
echo -e "${YELLOW}[1/6] Web App AWS Public${NC}"
echo "curl -X POST $BASE_URL/deployment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"project_name\": \"ecommerce_app\",
    \"service\": \"AWS\",
    \"usage_level\": \"small\",
    \"service_type\": \"web\",
    \"ip_exposure\": \"public\",
    \"data_type\": \"public\",
    \"top_k\": 20
  }'"
echo -e "\n${GREEN}Expected Cost: ~\$70/month${NC}\n"

# ============================================================================
# EXEMPLE 2: Job Processing Azure (Huge, Confidential)
# ============================================================================
echo -e "${YELLOW}[2/6] Job Processing Azure Confidential${NC}"
echo "curl -X POST $BASE_URL/deployment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"project_name\": \"medical_data_processor\",
    \"service\": \"Azure\",
    \"usage_level\": \"huge\",
    \"service_type\": \"job\",
    \"ip_exposure\": \"private\",
    \"data_type\": \"confidential\",
    \"top_k\": 20
  }'"
echo -e "\n${GREEN}Expected Features:${NC}"
echo "  - Backup: Geo-redundant + immutable + customer-managed keys"
echo "  - Security: AES-256 + audit trail + SOC 2"
echo "  - Cost: ~\$450/month"
echo ""

# ============================================================================
# EXEMPLE 3: Worker Queue AWS (Small, Mixed)
# ============================================================================
echo -e "${YELLOW}[3/6] Message Queue Workers AWS${NC}"
echo "curl -X POST $BASE_URL/deployment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"project_name\": \"email_notification_workers\",
    \"service\": \"AWS\",
    \"usage_level\": \"small\",
    \"service_type\": \"worker\",
    \"ip_exposure\": \"private\",
    \"data_type\": \"mixed\",
    \"top_k\": 20
  }'"
echo -e "\n${GREEN}Expected Features:${NC}"
echo "  - Architecture: SQS + Lambda / EC2 workers"
echo "  - Backup: Mixed (partitioned) strategy"
echo "  - Cost: ~\$50-100/month"
echo ""

# ============================================================================
# EXEMPLE 4: REST API Azure (Small, Private)
# ============================================================================
echo -e "${YELLOW}[4/6] REST API Azure Private${NC}"
echo "curl -X POST $BASE_URL/deployment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"project_name\": \"internal_api\",
    \"service\": \"Azure\",
    \"usage_level\": \"small\",
    \"service_type\": \"api\",
    \"ip_exposure\": \"private\",
    \"data_type\": \"public\",
    \"top_k\": 20
  }'"
echo -e "\n${GREEN}Expected Features:${NC}"
echo "  - Network: Private VPC + Security Groups"
echo "  - DDoS: Not exposed (internal only)"
echo "  - SSL: Optional (internal mTLS)"
echo "  - Cost: ~\$75/month"
echo ""

# ============================================================================
# EXEMPLE 5: Real-time Notifications AWS (Hybrid)
# ============================================================================
echo -e "${YELLOW}[5/6] Real-time Notifications AWS Hybrid${NC}"
echo "curl -X POST $BASE_URL/deployment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"project_name\": \"collaborative_editor\",
    \"service\": \"AWS\",
    \"usage_level\": \"small\",
    \"service_type\": \"realtime\",
    \"ip_exposure\": \"hybrid\",
    \"data_type\": \"mixed\",
    \"top_k\": 20
  }'"
echo -e "\n${GREEN}Expected Features:${NC}"
echo "  - Compute: AppSync + DynamoDB Streams"
echo "  - Network: Public LB + Private backend"
echo "  - Firewall: WAF + Network segmentation"
echo "  - Cost: ~\$150-200/month"
echo ""

# ============================================================================
# EXEMPLE 6: Data Pipeline Private (Huge, Confidential)
# ============================================================================
echo -e "${YELLOW}[6/6] Data Pipeline Private Confidential${NC}"
echo "curl -X POST $BASE_URL/deployment \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{
    \"project_name\": \"etl_financial_data\",
    \"service\": \"Private\",
    \"usage_level\": \"huge\",
    \"service_type\": \"data_pipeline\",
    \"ip_exposure\": \"private\",
    \"data_type\": \"confidential\",
    \"top_k\": 20
  }'"
echo -e "\n${GREEN}Expected Features:${NC}"
echo "  - Compute: Kubernetes Jobs + PVC"
echo "  - Backup: On-site encrypted + air-gapped + 24/7 monitoring"
echo "  - Security: Full immutable audit trail"
echo "  - Compliance: SOC 2 Type II / ISO 27001"
echo "  - Cost: \$1300+/month (hardware + licensing)"
echo ""

# ============================================================================
# PARAMÈTRES DISPONIBLES
# ============================================================================
echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Paramètres Disponibles${NC}"
echo -e "${BLUE}==================================${NC}\n"

echo -e "${GREEN}service:${NC}"
echo "  - AWS (E.U./US supported)"
echo "  - Azure (Europe + US)"
echo "  - Private (On-premises)\n"

echo -e "${GREEN}usage_level:${NC}"
echo "  - small  (<1000 req/day, <100 concurrent users)"
echo "  - huge   (>100k req/day, >10k concurrent users)\n"

echo -e "${GREEN}service_type:${NC}"
echo "  - web           (Full-stack web application)"
echo "  - job           (Batch processing / ETL)"
echo "  - worker        (Queue-based workers)"
echo "  - api           (REST/GraphQL backend)"
echo "  - realtime      (WebSocket / SSE)"
echo "  - data_pipeline (Data lake / ML pipeline)\n"

echo -e "${GREEN}ip_exposure:${NC}"
echo "  - public  (Internet accessible)"
echo "  - private (Internal only)"
echo "  - hybrid  (Public API + private backend)\n"

echo -e "${GREEN}data_type:${NC}"
echo "  - public        (No restrictions)"
echo "  - confidential   (PII, medical, financial)"
echo "  - mixed         (Partitioned data)\n"

# ============================================================================
# TESTER AVEC PYTHON
# ============================================================================
echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Test Automatisé (Python)${NC}"
echo -e "${BLUE}==================================${NC}\n"

echo "Exécute le script de test complet:"
echo -e "${GREEN}python test_deployment_api.py${NC}\n"

# ============================================================================
# TESTER AVEC CURL (Interactive)
# ============================================================================
echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Test avec curl (Interactive)${NC}"
echo -e "${BLUE}==================================${NC}\n"

echo "Copie l'un des exemples ci-dessus et exécute:"
echo -e "${GREEN}curl -X POST $BASE_URL/deployment ...${NC}\n"

# ============================================================================
# VÉRIFIER L'API
# ============================================================================
echo -e "${BLUE}==================================${NC}"
echo -e "${BLUE}Vérifier que l'API Fonctionne${NC}"
echo -e "${BLUE}==================================${NC}\n"

echo "Teste la connectivité:"
echo -e "${GREEN}curl $BASE_URL/health${NC}\n"

echo "Ou lance l'API:"
echo -e "${GREEN}python -m uvicorn backend.api.server:app --port 8000 --reload${NC}\n"
