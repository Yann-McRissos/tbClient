from includes.config import *
from includes.buildTopology import * #buildTopology(configFile, username, password)
from includes.methods import * #getTunGW()
from includes.listTwinings import * #listTwinings(ip, port)
from includes.createLab import *
from includes.joinLab import *
import getpass
import sys
import psutil

if __name__ == "__main__":
    if not tunnelExists():
        if len(sys.argv) < 3:
            username = input("Username: ")
            password = getpass.getpass("Password: ")
        else:
            username = sys.argv[1]
            password = sys.argv[2]
        #Start openvpn    
        connectOVPN("connectScript/client.ovpn", username, password)
    
        #Wait until the tunnel is up or until the process dies
        ret = waitForTunnelUp()
        if ret == False:
            print("Erreur durant la creation du tunnel")
            with open(config['PIDFILE'], "r") as pidfile:
                pid = pidfile.read()
            pid = int(pid.strip())
            try:
                os.kill(pid, psutil.signal.SIGINT)
            except ProcessLookupError:
                print("No openvpn process to be killed")
            os.remove(config['PIDFILE'])
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
        pin = input("Veuillez saisir le code PIN du labo a rejoindre: ")
        ret = joinLab(pin)
        
        
