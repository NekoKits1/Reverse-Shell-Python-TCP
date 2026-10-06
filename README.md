# Reverse Shell — Python TCP

> Projet réalisé dans un cadre éducatif en cybersécurité offensive **et défensive**.
> Environnement : Kali Linux (attaquant) ↔ Windows 7 (cible), réseau local isolé, sans accès Internet.

---

## Objectif

Ce projet implémente un **reverse shell** en Python : la machine cible (Windows 7) initie elle-même une connexion TCP vers la machine attaquante (Kali Linux), qui obtient ainsi un accès shell à distance.

Contrairement à un shell classique où l'attaquant se connecte à la cible, le flux est inversé — ce qui permet de contourner les pare-feux qui bloquent les connexions entrantes mais autorisent les connexions sortantes.

L'objectif n'est pas seulement de faire fonctionner l'attaque, mais de comprendre **ce qu'elle laisse comme traces**, pour savoir la repérer.

---

## Architecture

```
┌─────────────────────┐         TCP:8000           ┌─────────────────────┐
│   Kali Linux         │ ◄─────────────────────── │   Windows 7          │
│   (Attaquant)         │                           │   (Cible)             │
│   tcp_server.py       │ ──── commandes ─────────► │   client.py           │
│   192.168.191.148     │ ◄─── résultats ─────────── │   192.168.191.162     │
└─────────────────────┘                             └─────────────────────┘
```

- **`tcp_server.py`** (Kali) : ouvre un port d'écoute, attend la connexion de la cible, puis envoie des commandes exécutées à distance.
- **`client.py`** (Windows) : se connecte automatiquement au serveur, exécute les commandes via `subprocess`, renvoie les résultats, et intègre un mécanisme de persistance.

---

## Fonctionnalités implémentées

**Côté serveur — Kali Linux (`tcp_server.py`)**
- Écoute TCP sur un port défini
- Interface shell interactive
- Réception et affichage des résultats en temps réel
- Fermeture propre de la session via `quit`

**Côté client — Windows 7 (`client.py`)**
- Connexion automatique au démarrage
- Exécution de commandes système via `subprocess`
- Navigation (`cd`, `pwd`)
- Reconnexion automatique toutes les 5 s si la connexion est perdue
- **Persistance via Registry Run Key** : inscription dans `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run` sous le nom `WindowsUpdate`

---

## Côté défense : comment ce comportement se détecte

Chaque fonctionnalité offensive ci-dessus laisse un signal exploitable côté défense.

| Comportement offensif | Signal de détection |
|---|---|
| Connexion sortante persistante vers un port inhabituel (8000) | Surveillance des connexions sortantes rares/non standard (firewall, Sysmon Event ID 3) |
| Persistance via clé de registre `Run` | Audit des clés `Run`/`RunOnce` ; une entrée nommée `WindowsUpdate` qui ne correspond à aucun processus Microsoft signé est un indicateur fort |
| Reconnexion automatique toutes les 5 s | Pattern de trafic périodique et régulier, typique d'un beacon C2 — détectable par analyse de fréquence sur les logs réseau |
| Exécution de commandes via `subprocess` depuis un process inattendu | Journalisation des créations de process (Sysmon Event ID 1) et de leur arborescence parent/enfant |

**Pistes pour aller plus loin** (prochaine itération du projet) :
- Capturer le trafic avec Wireshark et identifier la signature du beacon.
- Écrire une règle Sysmon/Sigma qui détecte la création de la clé de registre.
- Tester la détection avec un EDR gratuit (ex. Wazuh) en environnement isolé.

---

## Stack technique

| Élément | Détail |
|---|---|
| Langage | Python 3 |
| Librairies | `socket`, `subprocess`, `winreg`, `os`, `sys`, `time` |
| Attaquant | Kali Linux |
| Cible | Windows 7 |
| Protocole | TCP |
| Port utilisé | 8000 |

---

## Mise en place

**Prérequis** : les deux machines sur le même réseau local, Python 3 installé sur les deux.

**1 — Lancer le serveur sur Kali**
```
python3 tcp_server.py
```

**2 — Lancer le client sur Windows**
```
python client.py
```

**3 — Résultat attendu**
```
[+] Connexion réussie vers la cible ('192.168.191.162', 8000)
Shell> whoami
windows7\user
Shell> ipconfig
...
```

---

## Références MITRE ATT&CK

- [T1059 — Command and Scripting Interpreter](https://attack.mitre.org/techniques/T1059/)
- [T1547.001 — Registry Run Keys / Startup Folder](https://attack.mitre.org/techniques/T1547/001/)
- [T1571 — Non-Standard Port](https://attack.mitre.org/techniques/T1571/)

---

## Ce que ce projet m'a appris

- Le fonctionnement bas niveau des sockets TCP en Python
- La différence entre bind shell et reverse shell
- Les mécanismes de persistance Windows via le registre
- L'architecture C2 utilisée dans les malwares réels
- **Que chaque technique offensive a une contrepartie détectable** — et que c'est cette contrepartie qui m'intéresse le plus

---

## ⚠️ Avertissement légal

Ce projet est réalisé **uniquement à des fins éducatives**, dans un environnement isolé et contrôlé (machines virtuelles sans accès à Internet). L'utilisation de ces techniques sur des systèmes sans autorisation explicite est **illégale**. Ce projet vise à comprendre les mécanismes d'attaque pour mieux s'en défendre.
