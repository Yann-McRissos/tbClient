import socket
import json


def listTwinings(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, port))
    req = { "type":"list"}
    reqstr = json.dumps(req)+"\n"
    s.send(reqstr.encode())
    with s.makefile() as sockFile:
        response = sockFile.readline()
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
