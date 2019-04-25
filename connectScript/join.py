from includes.config import *
from includes.buildTopology import * #buildTopology(configFile, username, password)
from includes.methods import * #getTunGW()
from includes.listTwinings import * #listTwinings(ip, port)
from includes.createLab import *
from includes.joinLab import *
import getpass
import sys

if __name__ == "__main__":
    pin = input("Veuillez saisir le code PIN du labo a rejoindre: ")
    ret = joinLab(pin)
