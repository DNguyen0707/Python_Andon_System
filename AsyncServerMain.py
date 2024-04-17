#!/usr/bin/env python3
# Asyncronous UDP Server for Qualitel Andon system, there are two threads, 
#   * Main thread: spins off the following threads: 
#   * UDP thread: polls for measeges comming from the individual Andon lights.
#   * GUI thread: shows current status of the Qualtiel Andon lights.
#   * HTML thread: posts andon light status to webpage - Not implemented yet.


######   Import packages   ######   
from datetime import datetime   # to get today date
import PySimpleGUI as sg        # GUI window
import socket                   # for UDP
import time                     # time.sleep(seconds)
import asyncio                  # for threads

#setup gif for fun
g1 = r'C:\Projects\000_QDev\Test Engineering\ANDON\Software\reisa-dance-blue-archive-resize.gif'
gifs = [g1]

andonDictonary = {              # dictionary data type to hold data for each andon
    "IP": "xxx.xxx.xxx.xxx",
    "Name": "Andon XX",
    "Status": "Color",
    "Down Time": 0
}

listOfAndons = [] # Array of andon dictionaries
listOfAndons.append(andonDictonary) 

# get IP address automatically
def getIP():
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

serverIP = getIP()    # getIP doesn't work over VPN... gets wrong adapter's IP
serverPort = 60000
print(serverIP)

######   UDP Thread is always waiting for messages   ######    
def UDP_thread():
    #setup for UDP

    serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #create UDP socket
    serverSock.bind((serverIP, serverPort)) #bind socket to server address
    
    while True:
        # recieve data
        data, clientAddress = serverSock.recvfrom(1024)
        print(f"Got it from {clientAddress}: {data.decode()}")

        if data.decode()[0:5] == "ID = ":        # "ID =" is a token that the Andon's send when powering on, will get added to the list: listOfAndons
            andonDictonary = {                   # todo: check if this Andon's IP address is already in the array
                "IP": clientAddress[0],
                "Name": data.decode()[5:100],
                "Status": "Color",
                "Down Time": 0
            }
            listOfAndons.append(andonDictonary)
            print(listOfAndons)
        else:
            for i in range (0,len(listOfAndons)):
                if clientAddress[0] == listOfAndons[i]["IP"]:
                    listOfAndons[i]["Status"] = data.decode()
                    print(listOfAndons[i])
                    break


######   UI Thread displays the current state of the andons   ######     
def UI_thread():
    sg.set_options(font=('Arial Bold', 14))
    
    rpiName = [
        [sg.Text("Name/Location", size=(20,1),justification="center")],
    ]
    
    rpiIPAddress = [
        [sg.Text("IP Address", size=(15,1),justification="center")],
    ]
    
    rpiStatus = [
        [sg.Text("Status", size=(5,1),justification="center")],
    ]
    
    rpiRunTime = [
        [sg.Text("Run Time", size=(10,1),justification="center")],
    ]
    
    headerInfo = [[
        sg.Text("Date:"), 
        sg.Text(datetime.now().strftime("%m/%d/%y %H:%M:%S"), key="date"),
        sg.VSeperator(),
        sg.Text("IP Address: "),
        sg.InputText(serverIP + ':' + str(serverPort), size=(15,1), use_readonly_for_disable=True, disabled=True),
        sg.VSeperator(),
        #might add button here or something
        sg.Button("Prev", size=(7,1)),
        sg.Button("Next", size=(7,1)),
        sg.Button("Refresh", size=(7,1)),
        
    ]]
    
    layout = [
        [sg.Text("Qualitel Andon Manager",font=("Arial Bold", 20),size=20,expand_x=True,justification="center"), sg.Image(key='gif', size=(5,1))],
        [sg.HSeparator()],
        [sg.Column(headerInfo)],
        [sg.HSeparator()],
        [sg.Column(rpiName, key='rpiName'), sg.VSeperator(), 
         sg.Column(rpiIPAddress, key ='rpiIP'), sg.VSeperator(), 
         sg.Column(rpiStatus, key='rpiStatus'), sg.VSeparator(), 
         sg.Column(rpiRunTime, key='rpiRunTime')],

    ]
    

    window = sg.Window('Andon Manager', layout, size=(900,500), enable_close_attempted_event=True)
    image =  window['gif']
        
    while True:
        event, values = window.read(timeout=30)
        
        if event == sg.WIN_CLOSED:
            return False
        elif event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            return False
        elif event == 'Prev':
            print("test for now")
        elif event == 'Next':
            print("test for now")
        elif event == 'Refresh':
            print("test for now")
        elif event == sg.TIMEOUT_EVENT: #meat and potato of the code
            #update time every second
            window["date"].update(datetime.now().strftime("%m/%d/%y %H:%M:%S"))
            image.update_animation(g1, 0)
            

######   Main function spins off the threads   ######           
async def main():
    print("starting main")

    await asyncio.gather(
        asyncio.to_thread(UI_thread),
        asyncio.to_thread(UDP_thread))

asyncio.run(main())