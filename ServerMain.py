#!/usr/bin/env python3

# Import packages
from datetime import datetime  # to get today date
import PySimpleGUI as sg  # GUI window
import socket # for UDP

#setup gif for fun
g1 = r'C:\Users\dain\Documents\Github\Python_Andon_System\Resources\reisa-dance-blue-archive-resize.gif'
gifs = [g1]

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
    return local_ip

#setup for UDP
serverIP = getIP()
serverPort = 6000
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)   #create UDP socket
serverSock.bind((serverIP, serverPort)) #bind socket to server address

#main class
def main():
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
        [sg.Text("Dai's Andon Manager",font=("Arial Bold", 20),size=20,expand_x=True,justification="center"), sg.Image(key='gif', size=(5,1))],
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
            
            
            
  
# globalCD = 0
# def checkprint():
#     global globalCD
    
#     print("bruh" + str(globalCD))
#     globalCD = globalCD + 1
#     if globalCD == 200:
#         try:
#             #recieve data
#             if not serverSock.recvfrom(1024):
#                 return True
#         except TimeoutError:
#             print("nothing")
#         finally:
#             globalCD = 0

#to run the file lmao
if __name__ == "__main__":
    main()