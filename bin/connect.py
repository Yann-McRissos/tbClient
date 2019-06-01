from includes.config import *
from includes.interfaces import *
from includes.queries import *
import getpass
import sys


FORBIDDEN_INTERFACES = ['eth0', 'vxlan0', 'br0', 'tun0']

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
    #Move current dir to script's parent
    pathname = os.path.dirname(sys.argv[0])
    dirname = os.path.abspath(pathname)
    os.chdir(dirname+"/..")
    gwInterfaces = getGWInterfaces()
    if len(gwInterfaces) == 0:
        print("It appears you have no default route. Please make sure you are connected to the internet")
        sys.exit(1)
    for interface in gwInterfaces:
        if interface in FORBIDDEN_INTERFACES:
            print("It appears", interface, "is configured with a default route!\nPlease make sur that interface is not configured before going further")
            sys.exit(1)

    if not tunnelExists():
        if len(sys.argv) < 3:
            username = input("Username: ")
            password = getpass.getpass("Password: ")
        else:
            username = sys.argv[1]
            password = sys.argv[2]

        #Start openvpn    
        startOVPN("client.ovpn", username, password)
    
        #Wait until the tunnel is up or until the process dies
        ret = waitForTunnelUp()
        if ret == False:
            print("Erreur durant la creation du tunnel")
            killOpenvpn()
            sys.exit(1)
    else:
        print("Tunnel already set up. Skipping Openvpn connection")


    #Create the interfaces
    ret = vxlanExists()
    if ret < 2:
        if ret == 1:
            print("Error : VXLAN partially set up or incorrectly set up. Please erase config")
            sys.exit(1)
        createInterfaces()
    print("Que faire?")
    print("1. Initier un labo")
    print("2. Joindre un labo")
    action = getNumber(1, 2) 
    print("action choisie",action)
    if action == 1:
        twlist = listTwinings()
        print("liste des academies")
        if twlist["error"] == True:
            print("Error!", twlist["reason"])
            sys.exit(1)
        for index, tw in enumerate(twlist["response"], start=1):
            print('%d. %s (contact %s)' % (index,tw["login"], tw["email"]) )
        print("Quelle academie choisir?")
        choice = getNumber(1, len(twlist['response']))
        ret = createLab(twlist['response'][choice-1]['academy_id'])
        if ret['error'] == True:
            print("Error!", ret['reason'])
            sys.exit(1)
        print("Lab created! PIN: ", ret['response']['pin'])
            
    elif action == 2:
        pin = input("Veuillez saisir le code PIN du labo a rejoindre: ")
        ret = joinLab(pin)
        
        
