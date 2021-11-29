import time
from peeringAPI import *
from connect import *

# State vars
LAB = 0

if __name__ == "__main__":
    while true:
        while LAB == 0:
            peer = getPeering()
            if peer == -1:
                print("Error : Could not retrieve peer information. This issues seems to be with the server")
                time.sleep(300) # Sleep for 5 minutes
            else:
                LAB = 1
                connect(peer)
                labTime = datetime.datetime(peer.end_date)
                time.sleep() # Sleep for the duration of the lab
            

    