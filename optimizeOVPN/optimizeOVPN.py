from string import Template
import multiprocessing
from pingUDP import pingUDP 
from operator import itemgetter
import requests
import time

SERVER = "tfe.furest.be"
NB_PINGS = 10

def getTemplate(fileName):
    with open(fileName) as f:
        content = f.read()                        
        return Template(content)

def pingUDP(address):
    """
    address = address tuple (ip, port)
    returns true if the server answered a UDP null packer
    returns false otherwise
    """
    sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
    sock.sendto("".encode(),address)
    sock.settimeout(5)
    try:
        answer, addr = sock.recvfrom(1024)
    except socket.timeout:
        return False
    return True
    
def pingTCP(port):
    try:
        start_time = time.time()
        req = requests.get(url="http://portquiz.net:" +str(port))
        elapsed_time = time.time() - start_time
        return {"port":port, "time":elapsed_time}
    except Exception as e:
        print(e)
        return {"port":port, "time":float("inf")}
        

def testUDPPort(port):
    success = 0
    for i in range(0,NB_PINGS):
        ret = pingUDP((SERVER, port))
        if ret == True:
            success +=1
    success = ( success / NB_PINGS ) * 100 #Success in percents
    return {"success":success, "port": port}

if __name__ == "__main__":
    UDP_PORTS = [22,443,1194,8080]
    TCP_PORTS = [22,443,1194,8080]
    with multiprocessing.Pool(len(UDP_PORTS)) as p:
        udpResults = p.map(testUDPPort, UDP_PORTS)
    sortedUdpResults = sorted(udpResults, key = itemgetter('success'), reverse=True)


    with multiprocessing.Pool(len(TCP_PORTS)) as p:
        tcpResults = p.map(pingTCP, TCP_PORTS)
    sortedTcpResults = sorted(tcpResults, key = itemgetter('time'))
    print(sortedUdpResults)
    print(sortedTcpResults)
    remoteStr = ""
    for result in sortedUdpResults:
        if result['success'] > 50:
            remoteStr = "".join([remoteStr, "remote tfe.furest.be ", str(result['port']), " udp\n"])
    for result in sortedTcpResults:
        if result['time'] != float("inf"):
            remoteStr = "".join([remoteStr, "remote tfe.furest.be ", str(result['port']), " tcp\n"])
    ovpnTemplate = getTemplate("template.ovpn")
    finalOVPN = ovpnTemplate.safe_substitute(REMOTE_LIST=remoteStr,CONNECT_TIMEOUT=30,CONNECT_RETRY=1)
    with open("../connectScript/client.ovpn", "w+") as clientvpn:
        clientvpn.write(finalOVPN)
    print("OVPN connection file optimized and replaced!")
