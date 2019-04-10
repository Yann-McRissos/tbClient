from buildTopology import * #buildTopology(configFile, username, password)
from gwUtils import * #getTunGW()
from listTwinings import * #listTwinings(ip, port)
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


SRV_IP = None #If set to none, uses the vpn GW ip
SRV_PORT = 1500
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
        ip = SRV_IP if SRV_IP != None else str(getTunGW())
        twlist = listTwinings(ip, SRV_PORT)
        print("liste des academies")
        for index, tw in enumerate(twlist, start=1):
            print('%d. %s (contact %s)' % (index,tw["login"], tw["email"]) )
        print("Quelle academie choisir?")
        getNumber(1, len(twlist))

