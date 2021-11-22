import requests
import json
from config import *

# setting the main function is not necessary if the file will be run directly
def getPeering():
    address = config['API_IP'] + ":" + str(config['API_PORT']) + "/nextPeering"
    timeout = 10 # timeout before cancelling the request
    attempts=3
    i = 0
    while i < attemps:
        print(f"Requesting data, time-out is {timeout}, attempt {i} out of {attemps}")
        response = requests.get(address, timeout=timeout)
        if response.status_code == 200 or response.status_code == 404:
            break
        print("Retrying...")
        i += 1
    # get response
    if i < 3:
        if response.status_code == 200:
            print(f"Got response from server.")
            peer = json.loads(response.text)
            print("\tName: ", peer["Name"])
            print("\tEmail: ", peer["Email"])
            return peer
        else:
            print("Server returned 404. Make sure the address is correct.")
    else:
        return 0

    # feed to connect.py (well actually modify connect.py to be a service)