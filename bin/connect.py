from includes.config import *
from includes.interfaces import *
from includes.queries import *
import getpass
import sys


FORBIDDEN_INTERFACES = ['eth0', 'vxlan0', 'br0', 'tun0']

def getNumber(minimum = None, maximum = None, force=True):
    choice = None
    print("Enter a number between", minimum, "and",maximum)
    while choice == None:
        strin = input()
        try:
            choice = int(strin)
            if (minimum != None and choice < minimum) or\
              (maximum != None and choice > maximum):
                choice = None
                print("Invalid choice")
        except ValueError:
            print("Please enter a number")
        if(force == False):
            break
    return choice


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
            print("An error occurred while setting up the tunnel")
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
    print("What to do?")
    print("1. Create a lab")
    print("2. Join an existing lab")
    action = getNumber(1, 2) 
    print("Choice : ",action)
    if action == 1:
        twlist = listTwinings()
        print("Academies list:")
        if twlist["error"] == True:
            print("Error!", twlist["reason"])
            sys.exit(1)
        for index, tw in enumerate(twlist["response"], start=1):
            print('%d. %s (contact %s)' % (index,tw["login"], tw["email"]) )
        print("Invite which academy?")
        choice = getNumber(1, len(twlist['response']))
        ret = createLab(twlist['response'][choice-1]['academy_id'])
        if ret['error'] == True:
            print("Error!", ret['reason'])
            sys.exit(1)
        print("Lab created! PIN: ", ret['response']['pin'])
            
    elif action == 2:
        pin = input("Please enter the PIN code of the lab to join: ")
        ret = joinLab(pin)
        
        
