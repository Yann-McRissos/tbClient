from includes.config import *
from includes.buildTopology import * #buildTopology(configFile, username, password)
from includes.methods import * #getTunGW()
from includes.listTwinings import * #listTwinings(ip, port)
from includes.createLab import *
from includes.joinLab import *
import getpass
import sys
def getNumber(minimum = None, maximum = None, force=True):
    choix = None
    print("selection d'un nombre entre", minimum, "et",maximum)
    while choix == None:
        strin = input()
        try:
            choix = int(strin)
            if (minimum != None and choix < minimum) or\
              (maximum != None and choix > maximum):
                choix = None
                print("Choix incorrect")
        except ValueError:
            print("Veuillez entrer un nombre")
        if(force == False):
            break
    return choix

if __name__ == "__main__":
    if len(sys.argv) < 3:
        username = input("Username: ")
        password = getpass.getpass("Password: ")
    else:
        username = sys.argv[1]
        password = sys.argv[2]
    ret = buildTopology("connectScript/client.ovpn", username, password)
    if ret != 0:
        print("Erreur durant la creation du tunnel")
        sys.exit(1)
    print("Que faire?")
    print("1. Initier un labo")
    print("2. Joindre un labo")
    action = getNumber(1, 2) 
    print("action choisie",action)
    if action == 1:
        twlist = listTwinings()
        print("liste des academies")
        if twlist["error"] == True:
            print("Error!", twlist["message"])
            sys.exit(1)
        for index, tw in enumerate(twlist["response"], start=1):
            print('%d. %s (contact %s)' % (index,tw["login"], tw["email"]) )
        print("Quelle academie choisir?")
        choice = getNumber(1, len(twlist['response']))
        ret = createLab(twlist['response'][choice-1]['academy_id'])
        if ret['error'] == True:
            print("Error!", ret['message'])
            sys.exit(1)
        print("Lab created! PIN: ", ret['response']['pin'])
            
    elif action == 2:
        pin = input("Veuillez saisir le code PIN du labo à rejoindre: ")
        ret = joinLab(pin)
        
        
