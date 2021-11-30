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
    print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Thread " + name + ": starting", )
    print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Duration of lab is " + labDuration + " seconds ("+labDuration/3600+" hours)")
    time.sleep(labDuration)
    LAB = 0
    print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Thread " + name + ": finishing")


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
                        print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Error: Got 404 from the server, is the address correct ?")
                    else:
                        print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Error while retrieving peer information.")
                    print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Retrying in 5 minutes")
                    time.sleep(300) # Sleep for 5 minutes
                else:
                    print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Lab starts on " + peer["start_date"].strftime("%d/%m/%Y @ %H:%M:%S"))
                    while(datetime.now() < peer["start_date"]):
                        sleep(60)
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
                print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Error : Could not retrieve peer information. Retrying in 5 minutes.")
                print(datetime.now().strftime("%m/%d-%H:%M:%S") + ": Error message: " + str(e))
                time.sleep(300) # Sleep for 5 minutes