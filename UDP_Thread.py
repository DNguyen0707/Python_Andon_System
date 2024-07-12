import socket                   # for UDP
from datetime import datetime   # to get today date
import time                     # time.sleep(seconds)
import asyncio                  # for threads and queues
from webui import webui         # for HTML

andonDictonary = {              # dictionary data type to hold data for each andon
    "IP": "xxx.xxx.xxx.xxx",
    "Name": "Andon XX",
    "Status": "Color",
    "Date Time": "01.01.01"
}


listOfAndons = []               # Array of andon dictionaries
listOfAndons.append(andonDictonary) 

def getIP():                    # get IP address automatically
    # The IP address of the local machine is found by creating a socket connection.
    # The socket connects to an external address, but does not send any data.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    except Exception:
        # Failed, return 'localhost'
        local_ip = 'localhost'
    finally:
        s.close()
        # print(local_ip)
    return local_ip


serverIP = "10.100.100.102" #getIP()    # getIP doesn't work over VPN... gets wrong adapter's IP
serverPort = 60000
print(serverIP)


######   UDP Thread is always waiting for messages   ######    
async def UDP_Thread(queue: asyncio.Queue):
    print("starting UDP Thread")        #setup for UDP
    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #create UDP socket
    serverSock.bind((serverIP, serverPort)) #bind socket to server address
    
    while True:                         # recieve data
        data, clientAddress = serverSock.recvfrom(1024)
        print(f"Got it from {clientAddress}: {data.decode()}")
        ipInList = False
        if data.decode()[0:5] == "ID = ":        # "ID =" is a token that the Andon's send when powering on, will get added to the list: listOfAndons
            for i in range (0,len(listOfAndons)):
                if clientAddress[0] == listOfAndons[i]["IP"]:
                    ipInList = True     # IP is already in list of Andons
                    break
            if ipInList == False:       # IP is not in list of Andons
                if(len(listOfAndons) == 1): # list of Andons is empty (1 entry = initialized)
                        andonDictonary = {                   
                            "IP": clientAddress[0],
                            "Name": data.decode()[5:100],
                            "Status": "Color",
                            "Date Time": datetime.now()}
                        listOfAndons.append(andonDictonary)
                        listOfAndons.pop(0)
                        print(listOfAndons)
                        # queue.put(andonDictonary)
                else:                   # IP is not in list of Andons, append it. 
                    andonDictonary = {                   
                        "IP": clientAddress[0],
                        "Name": data.decode()[5:100],
                        "Status": "Color",
                        "Date Time": datetime.now()}
                    listOfAndons.append(andonDictonary)
                    # queue.put(andonDictonary)
                    print(listOfAndons)
        else:
            for i in range (0,len(listOfAndons)):
                if clientAddress[0] == listOfAndons[i]["IP"]:
                    listOfAndons[i]["Status"] = data.decode()
                    listOfAndons[i]["Date Time"] = datetime.now()
                    print(listOfAndons[i])
                    await queue.put(listOfAndons[i])
                    break
       # queue.put(andonDictonary)
        

