# Reverse Shell — Python TCP

> Projet réalisé dans un cadre éducatif en cybersécurité offensive.  
> Environnement : Kali Linux (attaquant) ↔ Windows 7 (cible) en réseau local isolé.

---

##  Objectif

Ce projet implémente un **reverse shell** en Python, c'est-à-dire un mécanisme par lequel une machine cible (Windows 7) initie elle-même une connexion TCP vers la machine de l'attaquant (Kali Linux), lui donnant un accès shell à distance.

Contrairement à un shell classique où l'attaquant se connecte à la cible, le reverse shell **inverse ce flux**. Cela permet de contourner les pare-feux qui bloquent les connexions entrantes mais autorisent les connexions sortantes.

---

##  Architecture

```
┌─────────────────────┐         TCP:8000          ┌─────────────────────┐
│   Kali Linux        │ ◄─────────────────────── │   Windows 7         │
│   (Attaquant)       │                            │   (Cible)           │
│   tcp_server.py     │ ──── commandes ──────────► │   client.py         │
│   192.168.191.148   │ ◄─── résultats ─────────── │   192.168.191.162   │
└─────────────────────┘                            └─────────────────────┘
```

- **`tcp_server.py`** tourne sur Kali : ouvre un port d'écoute et attend la connexion de la cible. Une fois connecté, l'attaquant tape des commandes exécutées à distance sur Windows.
- **`client.py`** tourne sur Windows : se connecte automatiquement au serveur, exécute les commandes reçues via `subprocess` et renvoie les résultats. Intègre un mécanisme de persistance.

---

##  Fonctionnalités implémentées

### Côté serveur — Kali Linux (`tcp_server.py`)
- Écoute TCP sur un port défini
- Interface shell interactive pour envoyer des commandes
- Réception et affichage des résultats en temps réel
- Fermeture propre de la session via la commande `quit`

### Côté client — Windows 7 (`client.py`)
- Connexion automatique vers le serveur attaquant au démarrage
- Exécution de commandes système Windows via `subprocess`
- Gestion des commandes de navigation (`cd`, `pwd`)
- Reconnexion automatique toutes les 5 secondes si la connexion est perdue
- **Persistance via Registry Run Key** : inscription dans la clé de registre `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run` sous le nom `WindowsUpdate` pour survivre aux redémarrages

---

##  Concepts cybersécurité illustrés

| Concept | Description |
|---------|-------------|
| **Reverse Shell** | La cible initie la connexion vers l'attaquant, contournant les pare-feux sur les connexions entrantes |
| **Persistance — Registry Run Key** | Le malware se relance automatiquement à chaque démarrage Windows via les clés de registre |
| **Command & Control (C2)** | Architecture où l'attaquant envoie des instructions à une machine compromise et reçoit les résultats |
| **Reconnexion automatique** | Résilience de l'implant face aux interruptions réseau |

---

##  Stack technique

| Élément | Détail |
|---------|--------|
| Langage | Python 3 |
| Librairies | `socket`, `subprocess`, `winreg`, `os`, `sys`, `time` |
| Attaquant | Kali Linux |
| Cible | Windows 7 |
| Protocole | TCP |
| Port utilisé | 8000 |

---

##  Mise en place

**Prérequis** : les deux machines doivent être sur le même réseau local. Python 3 installé sur les deux machines.

**Étape 1 — Lancer le serveur sur Kali**

Modifier l'IP dans `tcp_server.py` avec l'IP de la machine Kali, puis lancer :

```bash
python3 tcp_server.py
```

**Étape 2 — Lancer le client sur Windows**

Modifier `HOST` dans `client.py` avec l'IP de Kali, puis lancer :

```bash
python client.py
```

**Étape 3**

La connexion s'établit automatiquement. Le shell interactif apparaît sur Kali :

```
[+] yipee!! Connexion reussit vers la cible ('192.168.191.162', 8000)
Shell> whoami
windows7\user
Shell> ipconfig
...
```

---

##  Références MITRE ATT&CK

- [T1059 — Command and Scripting Interpreter](https://attack.mitre.org/techniques/T1059/)
- [T1547.001 — Registry Run Keys / Startup Folder](https://attack.mitre.org/techniques/T1547/001/)
- [T1571 — Non-Standard Port](https://attack.mitre.org/techniques/T1571/)

---

##  Ce que ce projet m'a appris

- Comprendre le fonctionnement bas niveau des sockets TCP en Python
- Maîtriser la différence entre bind shell et reverse shell
- Appréhender les mécanismes de persistance Windows via le registre
- Comprendre l'architecture C2 utilisée dans les malwares réels
- Manipuler Kali Linux et Windows en environnement de lab virtuel

---

## ⚠️ Avertissement légal

Ce projet est réalisé **uniquement à des fins éducatives** dans un environnement isolé et contrôlé (machines virtuelles sans accès à Internet).  
L'utilisation de ces techniques sur des systèmes sans autorisation explicite est **illégale**.  
Ce projet vise à comprendre les mécanismes d'attaque pour mieux s'en défendre.
