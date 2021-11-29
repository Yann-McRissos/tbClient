import time
import threading
from subprocess import call
from peeringAPI import *
from connect import *

# State vars
LAB = 0

def thr_lab_timer(name, labDuration):
    global LAB
    logging.info("Thread %s: starting", name)
    logging.info("Duration of lab is %s seconds (%s hours)", labDuration, labDuration/3600)
    time.sleep(labDuration)
    LAB = 0
    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    # Make sure flush.sh is executable
    os.chmod("./flush.sh", 0o755)
    while true:
        while LAB == 0:
            try:
                peer = getPeering()
                if peer == -1 or peer == 404:
                    print("Error : Could not retrieve peer information. This issues seems to be with the server")
                    time.sleep(300) # Sleep for 5 minutes
                else:
                    LAB = 1
                    # daemonize the thread so that it stops with the main program
                    thread = threading.Thread(target=thr_lab_timer, args=(1, peer["lab_duration"]), daemon=True)
                    thread.start()
                    #connect(peer)
                    i = 0
                    while i < 1000:
                        print(i)
                    # Wait for lab to finish
                    thread.join()
                    # Flush interfaces
                    rc = call("./flush.sh")
            except:
                print("Error : Could not retrieve peer information. Verify connection information")
                time.sleep(300) # Sleep for 5 minutes