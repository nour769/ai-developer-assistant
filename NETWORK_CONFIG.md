# 🌐 Configuration Réseau - IP Publique vs IP Privée

## ⚠️ Remarque CRITIQUE pour le Déploiement

Le système écoute sur **`127.0.0.1` (localhost)** par défaut = **PERSONNE ne peut accéder depuis une autre machine!**

---

## 📍 Les 3 Types d'Adresses IP

### 1️⃣ **IP Privée (Locale) = `127.0.0.1`**

```
URL: http://127.0.0.1:8000
ou:  http://localhost:8000
```

**Accessibilité:**
- ✅ Depuis la MÊME machine seulement
- ❌ Pas accessible depuis d'autres machines
- ❌ Pas accessible depuis Internet

**Use Case:** Développement local uniquement

---

### 2️⃣ **IP Machine (Réseau Local) = `192.168.x.x`**

```
URL: http://192.168.1.50:8000  (exemple)
```

**Accessibilité:**
- ✅ Depuis la MÊME machine
- ✅ Depuis d'autres machines sur le MÊME réseau WiFi/Ethernet
- ❌ Pas accessible depuis Internet

**Use Case:** Équipe sur le même réseau, démo locale, tests

**Comment trouver ton IP machine:**
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Cherche une adresse `192.168.x.x` ou `10.0.x.x`

---

### 3️⃣ **IP Publique = `x.x.x.x` (Internet)**

```
URL: http://203.45.67.89:8000  (exemple)
```

**Accessibilité:**
- ✅ Depuis PARTOUT (Internet)
- ✅ Depuis le MÊME réseau
- ✅ Depuis d'autres machines

**Use Case:** Déploiement production, accès public

**Comment trouver ton IP publique:**
```bash
# Dans le terminal
curl ifconfig.me
```

**⚠️ ATTENTION:**
- Besoin d'un port ouvert côté routeur (port forwarding)
- Besoin d'HTTPS en production (pas HTTP)
- Sécurité critique!

---

## 🔧 Configuration Actuelle du Serveur

### Backend (Python FastAPI)

**Fichier:** `backend/api/server.py`

```python
# Actuellement (LOCALHOST SEULEMENT):
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

**Résultat:**
```
✅ Accessible: http://localhost:8000
✅ Accessible: http://127.0.0.1:8000
❌ Accessible: http://192.168.1.50:8000 (ERREUR!)
❌ Accessible: http://203.45.67.89:8000 (ERREUR!)
```

---

### Frontend (React/Vite)

**Fichier:** `frontend/src/api.js`

```javascript
// Actuellement:
const API_BASE = "http://localhost:8000"
```

**Résultat:**
```
✅ Fonctionne si frontend et backend sur MÊME machine
❌ Échoue si frontend sur 192.168.x.x et backend sur localhost
```

---

## 🚀 Solutions Pour Différents Scénarios

### Scénario 1: Développement Local (TU SEUL)
**Besoin:** Travailler sur ta machine

```bash
# Backend
python -m uvicorn backend.api.server:app --host 127.0.0.1 --port 8000

# Frontend
npm run dev  # Vite sur http://localhost:5173

# Accès
http://localhost:5173  ✅
```

**Rien à changer!** (Déjà configuré comme ça)

---

### Scénario 2: Équipe Locale (Même Réseau WiFi)
**Besoin:** Partager l'app avec des collègues sur le même réseau

#### Étape 1: Trouver ton IP machine
```bash
ipconfig
# Cherche: 192.168.1.XX ou 10.0.0.XX
# Exemple: 192.168.1.50
```

#### Étape 2: Modifier le Backend
**Fichier:** `backend/api/server.py`

```python
# À la fin du fichier:
if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0",  # ← CHANGE ICI: 127.0.0.1 → 0.0.0.0
        port=8000
    )
```

`0.0.0.0` = "écoute sur TOUTES les interfaces réseau"

#### Étape 3: Modifier le Frontend
**Fichier:** `frontend/src/api.js`

```javascript
// Récupère l'IP machine
const getBackendUrl = () => {
  if (window.location.hostname === "localhost") {
    return "http://localhost:8000"  // Dev local
  }
  return `http://${window.location.hostname}:8000`  // Réseau
}

const API_BASE = getBackendUrl()
```

#### Étape 4: Accès
```
Depuis ta machine: http://localhost:5173 ✅
Depuis collègue:   http://192.168.1.50:5173 ✅
```

---

### Scénario 3: Production (Internet Public)
**Besoin:** Accessible depuis Internet

#### Étape 1: Trouver IP Publique
```bash
curl ifconfig.me
# Résultat: 203.45.67.89 (exemple)
```

#### Étape 2: Port Forwarding
**Besoin:** Configurer ton routeur (Port Forwarding)
- Forward port 80/443 (HTTP/HTTPS) → port 8000 (backend)
- Forward port 80/443 → port 5173 (frontend) 

⚠️ **Complexe et hors de ce projet!**

#### Étape 3: HTTPS OBLIGATOIRE
```bash
# Générer certificat SSL
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365

# Lancer avec HTTPS
uvicorn backend.api.server:app --host 0.0.0.0 --port 443 --ssl-keyfile key.pem --ssl-certfile cert.pem
```

#### Étape 4: Accès Public
```
https://mondomaine.com ✅
```

---

## 📊 Tableau Récapitulatif

| Adresse | Local | Réseau | Internet | Cas d'Usage |
|---------|-------|--------|----------|------------|
| `127.0.0.1` | ✅ | ❌ | ❌ | Dev solo |
| `0.0.0.0` | ✅ | ✅ | ❌* | Démo équipe |
| IP Public | ✅ | ✅ | ✅ | Production |

*Besoin du port forwarding du routeur

---

## ✅ Checklist pour Différents Déploiements

### ✅ Dev Local (Actuellement)
- [x] Backend: `host="127.0.0.1"`
- [x] Frontend: `API_BASE="http://localhost:8000"`
- [x] Port: 8000
- [x] Accès: `http://localhost:5173`

### ✅ Démo Équipe (À Faire)
- [ ] Backend: `host="0.0.0.0"` (Changer!)
- [ ] Frontend: `API_BASE = getBackendUrl()` (Changer!)
- [ ] Port: 8000
- [ ] Accès: `http://192.168.1.50:5173`

### ✅ Production (Hors Scope)
- [ ] Backend: HTTPS + `host="0.0.0.0"`
- [ ] Frontend: Domaine custom
- [ ] Port: 443 (HTTPS)
- [ ] Certificat SSL
- [ ] Port Forwarding routeur

---

## 💻 Commandes Utiles

### Vérifier quel port écoute
```bash
# Windows
netstat -ano | findstr :8000

# Linux
netstat -tuln | grep 8000

# macOS
lsof -i :8000
```

### Tester l'accès depuis autre machine
```bash
# Depuis collègue, remplace 192.168.1.50 par TON IP
curl http://192.168.1.50:8000/health
# Devrait retourner: {"status": "ok"}
```

### Désactiver le firewall localement (test rapide)
```bash
# Windows (administrateur)
netsh advfirewall set allprofiles state off

# À réactiver après test!
netsh advfirewall set allprofiles state on
```

---

## 🎯 À Dire à l'Encadrant

> "L'application écoute actuellement sur **127.0.0.1 (localhost)**, ce qui signifie qu'elle n'est accessible que depuis la même machine. 
>
> Pour une démo en équipe, il faut changer `host="0.0.0.0"` dans le backend, ce qui permettra d'accéder via l'IP machine (192.168.1.x).
>
> Pour la production publique, il faudrait:
> 1. Utiliser une IP publique
> 2. Configurer le port forwarding du routeur  
> 3. Activer HTTPS
>
> Actuellement, l'app est en mode **développement local 100% sécurisé** mais non-distribué."

---

## 🔐 Sécurité Note

### Development (127.0.0.1)
✅ Aucun risque - personne ne peut accéder

### Local Network (0.0.0.0)
⚠️ Tout le monde sur ton WiFi peut accéder
- Risque faible si réseau personnel
- Ajouter authentification si production interne

### Internet Public
🚨 CRITIQUE
- HTTPS obligatoire
- Authentification/API key obligatoire
- Rate limiting obligatoire
- Firewall/DDoS protection

---

## Code Snippet: Configuration Paramétrisée

**Si tu veux faire une config facile à changer:**

```python
# backend/config.py
import os

HOST = os.getenv("BACKEND_HOST", "127.0.0.1")  # Par défaut: local
PORT = int(os.getenv("BACKEND_PORT", 8000))

# backend/api/server.py
from backend.config import HOST, PORT

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
```

**Utilisation:**
```bash
# Dev local (défaut)
python -m uvicorn backend.api.server:app --port 8000

# Démo équipe
set BACKEND_HOST=0.0.0.0 && python -m uvicorn backend.api.server:app --port 8000

# Production
set BACKEND_HOST=0.0.0.0 && set BACKEND_PORT=443 && python -m uvicorn ...
```

---

## ❓ FAQ

**Q: Pourquoi 127.0.0.1 et pas 0.0.0.0 par défaut?**
A: Pour la sécurité! En dev, tu ne veux pas exposer par accident ton app au réseau.

**Q: Qu'est-ce que 0.0.0.0?**
A: "Écoute sur TOUTES les interfaces réseau" (127.0.0.1, 192.168.1.x, etc)

**Q: Port forwarding c'est quoi?**
A: Dire au routeur: "Si quelqu'un frappe à la porte 80/443, redirige vers port 8000"

**Q: Pourquoi HTTPS en production?**
A: Chiffre les données. Sans HTTPS, on voit tous les passwords/tokens en clair!

**Q: Puis-je utiliser un domaine DNS?**
A: Oui! Pointe le domaine vers ton IP publique + port forwarding
