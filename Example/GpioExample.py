#!/usr/bin/env python

from gpiozero import LED, Button
import neopixel
from board import *

# Addressable LED Pins
led5V = LED("GPIO5") # pin 29
ledData = LED("GPIO5") # pin 31
ledGND = LED("GPIO5") # pin 32

# Switch pins
switchRed = Button("GPIO19")    #pin 35
switchYellow = Button("GPIO16") #pin 36
switchGreen = Button("GPIO26")  #pin 37
switchBlue = Button("GPIO20")   #pin 38

while True:
    if switchRed.is_pressed(): #could be is_held too
        print("Red is activated")
        RED = (255, 0, 0)
        pixels = neopixel.NeoPixel(board.D18, 10)
        for i in range(len(pixels)):
            pixels[i] = RED
    
    if switchYellow.is_pressed(): #could be is_held too
        print("Yellow is activated")
        YELLOW = (255, 255, 0)
        pixels = neopixel.NeoPixel(board.D18, 10)
        for i in range(len(pixels)):
            pixels[i] = YELLOW
    
    if switchGreen.is_pressed(): #could be is_held too
        print("Green is activated")
        GREEN = (0, 255, 0)
        GREEN = neopixel.NeoPixel(board.D18, 10)
        for i in range(len(pixels)):
            pixels[i] = GREEN
        
    if switchBlue.is_pressed(): #could be is_held too
        print("Blue is activated")
        BLUE = (0, 0, 255)
        pixels = neopixel.NeoPixel(board.D18, 10)
        for i in range(len(pixels)):
            pixels[i] = BLUE