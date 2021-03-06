import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import neopixel
import time
import sys
import board
import threading


Location = sys.argv[1]
NumPixels = int(sys.argv[2])
print ('Number of Pixels : {0}'.format(NumPixels))
Duration = int(sys.argv[3])
pixels = neopixel.NeoPixel(board.D18, NumPixels)

StartTime = 0



def on_connect(client, userdata, flags, rc):
     print("Connected with result code "+str(rc))
     client.subscribe(Location)

try:
    import urandom as random
except ImportError:
    import random



def flash_off():
    global goingOn
    goingOn = False
    j=0
    amount = []
    while len(set(amount)) != 15 and goingOn == False:
        amount.append(random.randint(0, NumPixels - 1)) # Choose random pixel
        pixels[amount[j]] = [0,0,0]
        j += 1
        print(goingOn)
        time.sleep(0.01)

def flash_random(wait, howmany):
    global goingOn
    goingOn = True
    amount = []
    j=0
    while len(set(amount)) != 15:
        amount.append(random.randint(0, NumPixels - 1)) # Choose random pixel
        pixels[amount[j]] = [255,255,255]  # Set pixel to color
        j += 1
        print(goingOn)
        time.sleep(0.01)
def set_timer(): 
     global startTime
     startTime = time.perf_counter()
     endTime = startTime

     while endTime - startTime < Duration:
          endTime += 1
          print(endTime, startTime)
          time.sleep(1)
          if endTime - startTime >= Duration:
               flash_off()
               time.sleep(5)

def on_message(client, userdata, msg):

    if msg.payload.decode() == "ON":

   # first number is 'wait' delay, shorter num == shorter twinkle
        flash_random(0.1,1)
        x = threading.Thread(target=set_timer)
        x.start()

    # second number is how many neopixels to simultaneously light up


client = mqtt.Client()
client.connect("192.168.0.160",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()