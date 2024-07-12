# include
import RPi.GPIO as GPIO
import time
import board
import neopixel
import socket # UDP Client - Andon (Pi side)

serverIP = '10.1.29.6' #'10.1.29.6' # will report switch state to server
serverPort = 60000

# create UDP socket
clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send identifier
ID = "ID = Andon 2" #input("Enter message to send: ")
clientSock.sendto(ID.encode(), (serverIP, serverPort))

numLEDs=90

# Pin definitions
Green = 26
Yellow = 19
Red = 13
Blue = 6
YellowBlue = 5

pixels1 = neopixel.NeoPixel(board.D10, numLEDs, brightness=.5) # LED Data pin is on GPIO 10, SPI0 MOSI

# Setup switch pins
GPIO.setmode(GPIO.BCM)  # For Broadcom pin numbering  / GPIO.setmode(GPIO.BOARD)  # For pin numbering
GPIO.setup(Green, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # pulling up switch pin, wire switch to ground to pull down
GPIO.setup(Yellow, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Red, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(Blue, GPIO.IN, pull_up_down=GPIO.PUD_UP)  #testing udp
GPIO.setup(YellowBlue, GPIO.IN, pull_up_down=GPIO.PUD_UP)

t = 0
state = 0
lastColor = "" 
color = ""

while True:
    time.sleep(.1)
    if not GPIO.input(Green):
        while t<(numLEDs):
            pixels1[t] = (0,255,0)
            t=t+1        #Add 1 to the counter      
        t=0
        color = "Green"

    if not GPIO.input(Yellow):
        while t<(numLEDs):
            pixels1[t] = (255,255,0)
            t=t+1        #Add 1 to the counter      
        t=0
        color = "Yellow"

    if not GPIO.input(Red):
        while t<(numLEDs):
            pixels1[t] = (255,0,0)
            t=t+1        #Add 1 to the counter      
        t=0
        color = "Red"

    if not GPIO.input(Blue):
        while t<(numLEDs):
            pixels1[t] = (0,0,255)
            t=t+1        #Add 1 to the counter      
        t=0
        color = "Blue"
        
    if not GPIO.input(YellowBlue):
        while t<(numLEDs/2):
            pixels1[t] = (255, 255, 0)
            t=t+1        #Add 1 to the counter
        while t<(numLEDs):
            pixels1[t] = (0,0,255)
            t=t+1        #Add 1 to the counter      
        t=0
        color = "Yellow Blue"
    else:
        print("off\n")
    
    if color != lastColor:
        lastColor = color

        message = color #input("Enter message to send: ")
    
        clientSock.sendto(message.encode(), (serverIP, serverPort))
    
    #recieve
   # respond, serverAddress = clientSock.recvfrom(1024)
   # print(f"Got it from {serverAddress}: {respond.decode()}")
    
