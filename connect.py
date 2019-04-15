from config import *
from buildTopology import * #buildTopology(configFile, username, password)
from methods import * #getTunGW()
from listTwinings import * #listTwinings(ip, port)
from createLab import *
import getpass
import sys
def getNumber(minimum = None, maximum = None, force=True):
    choix = None
    while choix == None:
        strin = input()
        try:
            choix = int(strin)
            if (minimum != None and choix < minimum) or\
              (maximum != None and choix > maximum):
                choix = None
                print("Choix incorrect")
        except ValueError:
            print("Choix incorrect")
        if(force == False):
            break
    return choix

def joinLab(pin):
    req = { "ype": "join", "pin":pin}
    reqstr = json.dumps(req)
    response = sendServer(reqstr)
    try:
        dictResponse = json.loads(response)
    except:
        print("Response of the server is not JSON")
    if dictResponse["status"] == False:
        print(dictResponse["message"])
    print("Labo rejoint!")
    
        

   

if __name__ == "__main__":
    username = input("Username: ")
    password = getpass.getpass("Password: ")
    ret = buildTopology("client.ovpn", username, password)
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
        choice = getNumber(1, len(twlist))
        ret = createLab(twlist['response'][choice-1]['academy_id'])
        if ret['error'] == True:
            print("Error!", ret['message'])
            sys.exit(1)
        print("Lab created! PIN: ", ret['response']['pin'])
            
    elif action == 2:
        pin = input("Veuillez saisir le code PIN du labo à rejoindre: ")
        ret = joinLab(pin)
        
        
