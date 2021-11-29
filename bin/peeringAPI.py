from datetime import datetime, timedelta
import requests
import json
from includes.config import *

# setting the main function is not necessary if the file will be run directly
def getPeering():
    """ Queries the API for the next peer. Returns object on success. 404 on no student, -1 on failure """
    address = config['API_IP'] + ":" + str(config['API_PORT']) + "/nextPeering"
    print("Server is at: " + address)
    timeout = 10 # timeout before cancelling the request
    attempts=3
    i = 0
    while i < attempts:
        print(f"Requesting data, time-out is {timeout}, attempt {i} out of {attempts}")
        response = requests.get(address, timeout=timeout)
        if response.status_code == 200 or response.status_code == 404:
            break
        print("Retrying...")
        i += 1
    # get response
    if i < 3:
        if response.status_code == 200:
            print(f"Got response from server.")
            peer = json.loads(response.text) # peer is now a dict
            # Convert dates from unclean strings to datetime
            peer["start_date"] = peer["start_date"].replace("T", " ").replace(".000Z", "")
            peer["start_date"] = datetime.strptime(peer["start_date"], "%Y-%m-%d %H:%M:%S")
            peer["end_date"] = peer["end_date"].replace("T", " ").replace(".000Z", "")
            peer["end_date"] = datetime.strptime(peer["end_date"], "%Y-%m-%d %H:%M:%S")
            peer["date_created"] = peer["date_created"].replace("T", " ").replace(".000Z", "")
            peer["date_created"] = datetime.strptime(peer["date_created"], "%Y-%m-%d %H:%M:%S")
            # Add lab_duration
            delta = peer["end_date"] - peer["start_date"]
            peer["lab_duration"] = delta.total_seconds() / 3600
            print("\tName:\t", peer["Name"])
            print("\tEmail:\t", peer["Email"])
            print("\tStart date:\t", peer["start_date"].strftime("%d/%m/%Y @ %H:%M"))
            print("\tEnd date:\t", peer["end_date"].strftime("%d/%m/%Y @ %H:%M"))
            print("\tDate created:\t", peer["date_created"].strftime("%d/%m/%Y @ %H:%M"))
            print("\tLab Duration:\t", peer["lab_duration"], "hours")
            return peer
        else:
            print("Server returned 404. Make sure the address is correct.")
            return 404
    else:
        return -1

    # feed to connect.py (well actually modify connect.py to be a service)