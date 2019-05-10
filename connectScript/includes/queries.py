import socket
from includes.config import *
import json
from includes.interfaces import getTunGW

def sendServer(message):
    """
    Sends the string given in parameter to the server
    """
    if config['SRV_IP'] == None:
        ip = str(getTunGW())
    else:
        ip = config['SRV_IP']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, config['SRV_PORT']))
    message+="\n"
    s.send(message.encode())
    with s.makefile() as sockFile:
        response = sockFile.readline()
    return response.strip()

def createLab(invitedId):
    req = {"type":"create", "invited_id":invitedId}
    response = sendServer(json.dumps(req))
    try:
        dictResp = json.loads(response)
    except:
        return None
    return dictResp

def joinLab(pin):
    req = { "type": "join", "pin":pin}
    reqstr = json.dumps(req)
    response = sendServer(reqstr)
    try:
        dictResponse = json.loads(response)
    except:
        print("Response of the server is not JSON")
    if dictResponse["error"] == True:
        print(dictResponse["message"])
    else:
    	print("Labo rejoint!")
    	
def listTwinings():
    req = { "type":"list"}
    reqstr = json.dumps(req)
    response = sendServer(reqstr)
    try:
        dictResponse = json.loads(response)
        return dictResponse
    except:
        return None
