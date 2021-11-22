from includes.config import *
from includes.interfaces import *
from includes.queries import *
from peeringAPI import *
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
        username = config["USERNAME"]
        password = config["PASSWORD"]

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
    print("Creating new lab...")
    print("Getting next peer...")
    # Add a timeout
    peer = getPeering()
    if peer == 0:
        print("Error : Could not retrieve peer information.")
        sys.exit(1)
    print(f"Peer: {peer.Name}:{peer.Email}")
    print("\tDone .\nGetting list of users...")
    twlist = listTwinings()
    print("User list:")
    if twlist["error"] == True:
        print("Error!", twlist["reason"])
        sys.exit(1)
    choice = -1
    for index, tw in enumerate(twlist["response"], start=1):
        print('%d. %s (contact %s)' % (index,tw["login"], tw["email"]) )
        # in current for loop, compare login & email for every user to nextPeering
        # if match, set choice variable
        if peer.Name == tw["login"] and peer.Email == tw["email"]:
            print(f"Match! + {index} {tw['login']}:{tw['email']}")
            # record index
            choice = index
            break
    print("out of loop")
    ret = createLab(twlist['response'][choice-1]['academy_id'])
    if ret['error'] == True:
        print("Error!", ret['reason'])
        sys.exit(1)
    print("Lab created! PIN: ", ret['response']['pin'])
        
        
