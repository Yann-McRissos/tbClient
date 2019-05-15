#!/usr/bin/python3
from string import Template
import multiprocessing
from operator import itemgetter
import requests
import time, socket, json, sys, os
import concurrent.futures

SERVER = "tfe.furest.be"
NB_PINGS = 3
TCP_TIMEOUT = 5
UDP_TIMEOUT = 2
PORTQUIZ_NOT_HTTP = [22,25,445]
REQ_TOT = 0
REQ_DONE = 0

def getTemplate(fileName):
    with open(fileName) as f:
        content = f.read()                        
        return Template(content)

def sendUDP(address):
    """
    address = address tuple (ip, port)
    returns true if the server answered a UDP null packer
    returns false otherwise
    """
    sock = socket.socket(socket.AF_INET, # Internet
                             socket.SOCK_DGRAM) # UDP
    sock.sendto("".encode(),address)
    sock.settimeout(UDP_TIMEOUT)
    try:
        answer, addr = sock.recvfrom(1024)
    except socket.timeout:
        return False
    return True
    
def pingTCP(port):
    start_time = time.time()
    if port in PORTQUIZ_NOT_HTTP:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(TCP_TIMEOUT)
        try:
            sock.connect(("portquiz.net", port))
            elapsed_time = time.time() - start_time
            notify()
            return {"port":port, "time":elapsed_time}
        except socket.timeout:
            notify()
            return {"port":port, "time":float("inf")}
    else:
        try:
            req = requests.get(url="http://portquiz.net:" +str(port), timeout=TCP_TIMEOUT)
            elapsed_time = time.time() - start_time
            notify()
            return {"port":port, "time":elapsed_time}
        except Exception as e:
            notify()
            return {"port":port, "time":float("inf")}
        

def pingUDP(port):
    success = 0
    for i in range(0,NB_PINGS):
        ret = sendUDP((SERVER, port))
        if ret == True:
            success +=1
        notify()
    success = ( success / NB_PINGS ) * 100 #Success in percents
    return {"success":success, "port": port}


def notify():
    l.acquire()
    try:
        global REQ_DONE
        REQ_DONE +=1
        progress = int((REQ_DONE/REQ_TOT)*100)
        msg={'type':'update', 'data':str(progress)}
        print(json.dumps(msg), end='\r\n')
        sys.stdout.flush()
    finally:
        l.release()

l = multiprocessing.Lock()
if __name__ == "__main__":
    req = " ".join(sys.argv[1:])
    jsonReq = json.loads(req)
    udp_ports = []
    tcp_ports = []
    pathname = os.path.dirname(sys.argv[0])
    dirname = os.path.abspath(pathname)
    os.chdir(dirname+"/..")
    for port in jsonReq['ports']:
        arr = port.split('/')
        if arr[1].lower() == "udp":
            udp_ports.append(int(arr[0]))
        else:
            tcp_ports.append(int(arr[0]))
    REQ_TOT = (len(udp_ports)*NB_PINGS)+len(tcp_ports)

    with concurrent.futures.ThreadPoolExecutor(max_workers=len(udp_ports)) as e:
        udpFuture = {e.submit(pingUDP, port): port for port in udp_ports}


    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tcp_ports)) as e:
        tcpFuture = {e.submit(pingTCP, port): port for port in tcp_ports}
    
    #Wait for udp results and sort them
    udpResults = []
    for future in concurrent.futures.as_completed(udpFuture):
        udpResults.append(future.result())
    sortedUdpResults = sorted(udpResults, key = itemgetter('success'), reverse=True)
    
    #Wait for tcp results and sort them
    tcpResults = []
    for future in concurrent.futures.as_completed(tcpFuture):
        tcpResults.append(future.result())
    sortedTcpResults = sorted(tcpResults, key = itemgetter('time'))

    remoteStr = ""
    for result in sortedUdpResults:
        if result['success'] > 50:
            remoteStr = "".join([remoteStr, "remote ", SERVER, " ", str(result['port']), " udp\n"])
    for result in sortedTcpResults:
        if result['time'] != float("inf"):
            remoteStr = "".join([remoteStr, "remote ", SERVER, " " ,  str(result['port']), " tcp\n"])
    ovpnTemplate = getTemplate("template.ovpn")
    
    finalOVPN = ovpnTemplate.safe_substitute(REMOTE_LIST=remoteStr,CONNECT_TIMEOUT=jsonReq['connect_timeout'],CONNECT_RETRY=jsonReq['connect_retry'])
    with open("/tmp/ovpndata", "w+") as clientvpn:
        clientvpn.write(finalOVPN)
    msg={'type':'done'}
    print(json.dumps(msg))
    sys.stdout.flush()
