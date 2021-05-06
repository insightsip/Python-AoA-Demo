import aoa_locator as locator
import aoa_gui as gui
import time
import math
import tkinter as tk



#Constants
COM_PORT = 13
METER_TO_PIXEL_RATIO = 75
SCENE_SIZE_M = 10
ANC_HEIGHT_M = 1.1
INVALID_VAL = -999

AZIMUTH_INDEX = 0
ELEVATION_INDEX = 1

#variables
tag1 = [0,0] #[azimuth, elevation]
anchor_height = ANC_HEIGHT_M #Height of the anchor in meter, anchor is supposed to be on the ceilling


        
#Implement all uartTransport events
def onErrorReceived(fatal, data):
    print('Error:', data)
    if fatal == 1:
        exit()

def onIQReceived(data):
    pass

def onSWReceived(data):
    pass

def onRRReceived(data):
    pass

def onSSReceived(data):
    pass

def onFRReceived(data):
    pass

def onMEReceived(data):
    pass

def onMAReceived(data):
    pass

def onKEReceived(data):
    global tag1
    
    try:
        elevation = int(data)
        tag1[ELEVATION_INDEX] = elevation
        compute_position(tag1)
    except ValueError:
        print("not valid number")    

def onKAReceived(data):
    global tag1
    
    try:
        azimuth = int(data)
        tag1[AZIMUTH_INDEX] = azimuth
        compute_position(tag1)
    except ValueError:
        print("not valid number")

#Implement all gui events
def onGuiNotifEvent(NotifType, NotifData):
    global anchor_height
    
    if NotifType == "OpenPort":
        locator.set_port_config(115200, NotifData, 1)
        locator.open_port()
    elif NotifType == "closePort":
        locator.close_port()
    elif NotifType == "LocatorHeightChanged":
        try:
            anchor_height = float(NotifData)
        except (ValueError, TypeError):
            pass

def onGuiRequestEvent(RequestType, RequestData):
    if RequestType == "ListPortRequest":
        port_list = locator.get_port_list()
        gui.set_list_port(port_list)
        

#Implement methods
def compute_position(tag):
    if tag[AZIMUTH_INDEX] != INVALID_VAL and tag[ELEVATION_INDEX] != INVALID_VAL:
        #update  position
        x = anchor_height*math.tan(tag[ELEVATION_INDEX]*math.pi/180)*math.cos(tag1[AZIMUTH_INDEX]*math.pi/180)
        y = anchor_height*math.tan(tag[ELEVATION_INDEX]*math.pi/180)*math.sin(tag1[AZIMUTH_INDEX]*math.pi/180)
        print("(x, y) =", "{:.2f}".format(x), "{:.2f}".format(y))
        gui.set_tag_coords(x, y, tag[AZIMUTH_INDEX], tag[ELEVATION_INDEX])
        
        #invalidate angles
        tag[AZIMUTH_INDEX] = INVALID_VAL
        tag[ELEVATION_INDEX] = INVALID_VAL
       
            
#Setup locator
locator = locator.Locator(COM_PORT, 115200, 1, onErrorReceived)
locator.subscribe_event('KE', onKEReceived)
locator.subscribe_event('KA', onKAReceived)
locator.get_port_config()

#Setup graphical interface
root = tk.Tk()
gui = gui.Gui2D(master=root, scene_size=SCENE_SIZE_M, ratio=METER_TO_PIXEL_RATIO, locator_height=anchor_height, request_subscriber=onGuiRequestEvent, notif_subscriber=onGuiNotifEvent)
gui.master.title("AoA Demo")
#display.master.maxsize(1000, 400)

#main loop
gui.mainloop()

print("Close locator port")
locator.close_port()



