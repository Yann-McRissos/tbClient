from config import *
from methods import *
import json
def createLab(invitedId):
    req = {"type":"create", "invited_id":invitedId}
    response = sendServer(json.dumps(req))
    try:
        dictResp = json.loads(response)
    except:
        return None
    return dictResp
