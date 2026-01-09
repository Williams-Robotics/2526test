# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       vincent                                                      #
# 	Created:      11/23/2025, 3:28:20 PM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# NOTE: Distance Sensor and GPS work great, AI vision cannot detect objects...yet!


# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
# controller = Controller(PRIMARY)

# ==================== MOTOR CONFIGURATION ====================
# Configure your motor ports here
# FRONT_LEFT_PORT = Ports.PORT10
GPS_PORT=Ports.PORT11
AI_PORT=Ports.PORT13
D_PORT=Ports.PORT15

# Configure motor reverse settings (True = reversed, False = normal)
# FRONT_LEFT_REVERSE = False


# ==================== SENSOR INITIALIZATION ====================
# Initialize motors with configured ports and reverse settings
# front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)

distance = Distance(D_PORT)
gps=Gps(GPS_PORT,0,0)# set to be the offset from the center of robot
ai=AiVision(AI_PORT)

# ==================== SENSOR FUNCTIONS ====================
def initialize():
    gps.calibrate()
    while gps.is_calibrating():
        continue
    gps.set_location(0,0) #inital x and y pos of robot, for calibrations 
    gps.set_origin(0,0) 
def dis_funcs():
    obj= distance.is_object_detected()
    if obj:
        dis = distance.object_distance()
        size = distance.object_size()
        print("Distance: ",dis,"Size: ",size)
def gps_funcs():
    xc=gps.x_position()
    yc=gps.y_position()
    head=gps.heading()
    if gps.quality()==100:
        qual="Good"
    elif gps.quality()>=90:
        qual="Ok"
    elif gps.quality()>=80:
        qual="Bad"
    else: 
        qual="Awful"
    print("Pos: (",xc,",",yc,") Heading: ",head,"Quality: ",qual)
def ai_funcs():
    objs=ai.take_snapshot(AiVision.ALL_AIOBJS)
    if objs[0].exists: 
        print("yes")
        objs_names=""
        for x in objs:
            if x.id==0 or GameElementsPushBack.BLUE_BLOCK:
                objs_names+=("Blue: "+str(x.score)+", ")
            elif x.id==1:
                objs_names+=("Red: "+str(x.score)+", ")
            else:
                objs_names+=("Unknown: "+str(x.score)+", ")
        print("Objects Detected: ",objs_names)
    else: print ("no")
        
    
    '''ai_vision_13_objects = []
screen_precision = 0
console_precision = 0
ai_vision_13_index = 0
myVariable = 0

def when_started1():
    global myVariable, ai_vision_13_objects, screen_precision, console_precision, ai_vision_13_index
    while True:
        ai_vision_13_objects = ai_vision_13.take_snapshot(AiVision.ALL_AIOBJS)
        if ai_vision_13_objects and len(ai_vision_13_objects) > 0:
            brain.screen.set_cursor(1, 1)
            if ai_vision_13_objects[ai_vision_13_index].id == GameElementsPushBack.BLUE_BLOCK:
                brain.screen.print("VLUE")
            else:
                brain.screen.print("BAD")
        else:
            brain.screen.print("SUPERBADBAD")
        wait(0.25, SECONDS)
        brain.screen.clear_screen()
        wait(5, MSEC)

when_started1()'''


        

# ==================== MAIN PROGRAM ====================
brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")
initialize()

# Main control loop
while True:
    #dis_funcs()
    gps_funcs()
    #ai_funcs()
    wait(200, MSEC)  # Small delay to prevent CPU overload


        
