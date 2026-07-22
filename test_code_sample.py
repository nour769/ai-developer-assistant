"""
Exemple de code simple pour tester les endpoints.
Contient intentionnellement quelques problèmes pour les recommandations.
"""

import hashlib
import subprocess


def authenticate(username: str, password: str) -> bool:
    """
    Authentifie un utilisateur (CONTIENT UNE VULNÉRABILITÉ INTENTIONNELLE).
    
    Args:
        username: Nom d'utilisateur
        password: Mot de passe en CLAIR (DANGER!)
        
    Returns:
        bool: True si authentifié, False sinon
    """
    # 🔴 VULNÉRABILITÉ: Mot de passe stocké en dur
    HARDCODED_PASSWORD = "admin123"
    
    # 🟠 VULNÉRABILITÉ: Comparaison non-timing-safe
    if username == "admin" and password == HARDCODED_PASSWORD:
        return True
    
    return False


def execute_user_command(cmd: str) -> str:
    """
    Exécute une commande shell (CONTIENT UNE VULNÉRABILITÉ INTENTIONNELLE).
    
    DANGEREUX: Permet l'injection de commande shell!
    
    Args:
        cmd: Commande à exécuter
        
    Returns:
        str: Résultat de la commande
    """
    # 🔴 VULNÉRABILITÉ: Injection de commande shell
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout


def calculate_hash(data: str) -> str:
    """
    Calcule un hash MD5 (NON-OPTIMISÉ et DANGÉREUX).
    
    Args:
        data: Donnée à hasher
        
    Returns:
        str: Hash MD5
    """
    # 🟠 PROBLÈME: MD5 est obsolète et insécurisé
    # 🟡 OPTIMISATION: Inutile de créer un hashlib à chaque fois
    md5_hash = hashlib.md5(data.encode()).hexdigest()
    
    # 🟡 OPTIMISATION: Boucle inefficace
    for i in range(1000):
        md5_hash = hashlib.md5(md5_hash.encode()).hexdigest()
    
    return md5_hash


class UserManager:
    """Gère les utilisateurs (CONTIENT PLUSIEURS PROBLÈMES)."""
    
    def __init__(self):
        self.users = {}  # 🟡 Best practice: Devrait être un dict avec ID numérique
    
    def add_user(self, name, email):
        """Ajoute un utilisateur (SANS VALIDATION)."""
        # 🟠 PROBLÈME: Pas de validation des emails
        # 🟠 PROBLÈME: Pas de gestion d'erreur pour doublons
        self.users[name] = email
    
    def get_user(self, name):
        """Récupère un utilisateur."""
        # 🟡 Best practice: Devrait retourner None au lieu de lever KeyError
        return self.users[name]
    
    def list_users(self):
        """Liste tous les utilisateurs."""
        # 🟡 Best practice: Nom ambigu (utiliser `get_all_users`)
        return list(self.users.values())


def process_data(items):
    """
    Traite une liste de données (MAUVAISES PRACTICES).
    
    Args:
        items: Liste de chaînes
        
    Returns:
        list: Données traitées
    """
    result = []
    
    # 🟡 OPTIMISATION: Concatenation de strings inefficace
    output = ""
    for item in items:
        output = output + item + ","  # ❌ O(n²) complexité
    
    # 🟡 Best practice: Variables avec noms peu clairs
    r = output.strip(",").split(",")
    for x in r:
        if x:
            result.append(x.upper())
    
    return result
