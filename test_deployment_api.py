#!/usr/bin/env python
"""
Script de test - Nouvelle API deployment COMPLÈTE

Teste tous les paramètres des recommandations de déploiement:
- service_type (web, job, worker, api, realtime, data_pipeline)
- ip_exposure (public, private, hybrid)
- data_type (public, confidential, mixed)
- service (AWS, Azure, Private)
- usage_level (small, huge)
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

# Couleurs pour le terminal
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'

def print_header(text: str):
    print(f"\n{BLUE}{'='*70}")
    print(f" {text}")
    print(f"{'='*70}{RESET}\n")

def print_success(text: str):
    print(f"{GREEN}✓ {text}{RESET}")

def print_info(text: str):
    print(f"{YELLOW}ℹ {text}{RESET}")

def test_deployment(params: Dict[str, Any]):
    """Teste un appel à l'endpoint /deployment"""
    print_header(f"Test: {params['service_type'].upper()} - {params['service']} - {params['ip_exposure'].upper()}")
    
    print(f"Paramètres:")
    for key, value in params.items():
        print(f"  • {key}: {value}")
    
    try:
        response = requests.post(f"{BASE_URL}/deployment", json=params)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Réponse reçue ({len(data['result'])} caractères)")
            
            # Affiche les paramètres confirmés
            print(f"\nParamètres confirmés par l'API:")
            for key, value in data['parameters'].items():
                print(f"  • {key}: {value}")
            
            # Affiche un aperçu de la réponse
            preview = data['result'][:300].replace('\n', ' ')
            print(f"\nAperçu de la réponse:")
            print(f"  {preview}...\n")
            
        else:
            print(f"{RED}✗ Erreur {response.status_code}: {response.text}{RESET}")
    
    except Exception as e:
        print(f"{RED}✗ Erreur de connexion: {e}{RESET}")
        print_info("Assure-toi que l'API est en train de tourner: python -m uvicorn backend.api.server:app --port 8000")

def main():
    print_header("🚀 Tests - Nouvelle API Deployment COMPLÈTE")
    
    # Définit les cas de test
    test_cases = [
        # Case 1: Web App Public AWS
        {
            "project_name": "app_web_demo",
            "service": "AWS",
            "usage_level": "small",
            "service_type": "web",
            "ip_exposure": "public",
            "data_type": "public"
        },
        
        # Case 2: Job Processing Azure Confidentiel
        {
            "project_name": "batch_processor",
            "service": "Azure",
            "usage_level": "huge",
            "service_type": "job",
            "ip_exposure": "private",
            "data_type": "confidential"
        },
        
        # Case 3: Worker SQS AWS
        {
            "project_name": "message_queue_workers",
            "service": "AWS",
            "usage_level": "small",
            "service_type": "worker",
            "ip_exposure": "private",
            "data_type": "public"
        },
        
        # Case 4: API Private Azure
        {
            "project_name": "api_backend",
            "service": "Azure",
            "usage_level": "small",
            "service_type": "api",
            "ip_exposure": "private",
            "data_type": "public"
        },
        
        # Case 5: Real-time AWS Hybrid
        {
            "project_name": "notifications_realtime",
            "service": "AWS",
            "usage_level": "small",
            "service_type": "realtime",
            "ip_exposure": "hybrid",
            "data_type": "mixed"
        },
        
        # Case 6: Data Pipeline Private Confidentiel
        {
            "project_name": "etl_pipeline",
            "service": "Private",
            "usage_level": "huge",
            "service_type": "data_pipeline",
            "ip_exposure": "private",
            "data_type": "confidential"
        },
    ]
    
    print_info(f"Exécution de {len(test_cases)} cas de test...\n")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n[{i}/{len(test_cases)}]", end=" ")
        test_deployment(test_case)
        
        if i < len(test_cases):
            input(f"{YELLOW}Appuie sur Entrée pour le prochain test...{RESET}")
    
    print_header("✅ Tous les tests terminés!")
    print(f"""
Résumé:
- 6 cas de test couvrant tous les paramètres
- Service types: web, job, worker, api, realtime, data_pipeline ✓
- IP exposure: public, private, hybrid ✓
- Data types: public, confidential, mixed ✓
- Cloud providers: AWS, Azure, Private ✓
- Usage levels: small, huge ✓

Prochaines étapes:
1. Vérifie les recommandations de backup pour chaque type de data
2. Valide les coûts estimés
3. Teste les recommandations de sécurité
4. Déploie sur ton cloud préféré!

Documentation complète: DEPLOYMENT_FEATURES.md
    """)

if __name__ == "__main__":
    main()
