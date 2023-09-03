#!/usr/bin/env python
from getch import getch
import can
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0'
can.rc['bitrate'] = 500000
from can.interface import Bus

def send_one():
    """Sends a single message."""
    with can.Bus() as bus:
        bus = Bus()
        msg = can.Message(
            arbitration_id=0xC0FFEE, data=[0, 25, 0, 1, 3, 1, 4, 1], is_extended_id=True
        )

        try:
            bus.send(msg)
            print(f"Message sent on {bus.channel_info}")
        except can.CanError:
            print("Message NOT sent")


if __name__ == "__main__":
    while True:
        print("\nPress 's' to send a menssage to CAN BUS or press 'q' to Quit\n")
        pressedKey = getch()
        if pressedKey == 's': 
            send_one()   
        elif pressedKey == 'q':    
            systems.exit()
        else:
            print ("\nKey Pressed:" + str(pressedKey))
    