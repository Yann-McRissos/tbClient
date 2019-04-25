from includes.methods import *
from includes.config import *
import json
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

