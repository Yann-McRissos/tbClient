import time
import threading
import warnings
from subprocess import call
from peeringAPI import *
from connect import *

# State vars
LAB = 0

def thr_lab_timer(name, labDuration):
    global LAB
    print("Thread " + name + ": starting", )
    print("Duration of lab is " + labDuration + " seconds ("+labDuration/3600+" hours)")
    time.sleep(labDuration)
    LAB = 0
    print("Thread " + name + ": finishing")


if __name__ == "__main__":
    # Remove deprecation warnings coming from the pyroute2 module
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Make sure flush.sh is executable
    os.chmod("./flush.sh", 0o755)
    while True:
        while LAB == 0:
            try:
                peer = getPeering()
                if peer == -1 or peer == 404:
                    if peer == 404:
                        print("Error: Got 404 from the server, is the address correct ?")
                    else:
                        print("Error while retrieving peer information.")
                    print("Retrying in 5 minutes")
                    time.sleep(300) # Sleep for 5 minutes
                else:
                    connect(peer)
                    LAB = 1
                    # daemonize the thread so that it stops with the main program
                    thread = threading.Thread(target=thr_lab_timer, args=(1, peer["lab_duration"]), daemon=True)
                    thread.start()
                    # Wait for lab to finish
                    thread.join()
                    # Flush interfaces
                    rc = call("./flush.sh")
            except Exception as e:
                print("Error : Could not retrieve peer information. Retrying in 5 minutes.")
                print("Error message: " + str(e))
                time.sleep(300) # Sleep for 5 minutes