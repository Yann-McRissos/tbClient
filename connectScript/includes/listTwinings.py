import socket
import json
from methods import *
from config import *
def listTwinings():
    req = { "type":"list"}
    reqstr = json.dumps(req)
    response = sendServer(reqstr)
    try:
        dictResponse = json.loads(response)
        return dictResponse
    except:
        return None

if __name__ == "__main__":
    SRV_IP = "172.16.100.1"
    SRV_PORT = 1500
    twinings = listTwinings(SRV_IP, SRV_PORT)
    print(twinings)
