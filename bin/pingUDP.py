import socket

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
    
if __name__ == "__main__":
    UDP_IP = "51.77.222.239"
    port = input("Please enter target port: ")
    if pingUDP((UDP_IP, int(port))):
        print("ping successful")
    else:
        print("ping failed!")
