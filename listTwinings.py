import socket
import json


SRV_IP = "172.16.100.1"
SRV_PORT = 1500
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SRV_IP, SRV_PORT))

req = { "type":"list"}
reqstr = json.dumps(req)+"\n"
s.send(reqstr.encode())
response = s.recv(1024)
print(response.strip())
