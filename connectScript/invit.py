from includes.config import *
from includes.config import *
from includes.buildTopology import * #buildTopology(configFile, username, password)
from includes.methods import * #getTunGW()
from includes.listTwinings import * #listTwinings(ip, port)
from includes.createLab import *
from includes.joinLab import *
import getpass

if __name__ == "__main__":
        twlist = listTwinings()
        print("liste des academies")
        if twlist["error"] == True:
            print("Error!", twlist["message"])
            sys.exit(1)
        for index, tw in enumerate(twlist["response"], start=1):
            print('%d. %s (contact %s)' % (index,tw["login"], tw["email"]) )
        print("Quelle academie choisir?")
        choice = getNumber(1, len(twlist['response']))
        ret = createLab(twlist['response'][choice-1]['academy_id'])
        if ret['error'] == True:
            print("Error!", ret['message'])
            sys.exit(1)
        print("Lab created! PIN: ", ret['response']['pin'])
