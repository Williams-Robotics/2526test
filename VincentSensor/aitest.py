#region VEXcode Generated Robot Configuration
from vex import *
# import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code


# # Make random actually random
# def initializeRandomSeed():
#     wait(100, MSEC)
#     random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
#     urandom.seed(int(random))
      
# # Set random seed 
# initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration
# region---------------------------------------------------------------------------- #
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
#endregion

#region ==================== MOTOR CONFIGURATION ====================
# Configure your motor ports here
# FRONT_LEFT_PORT = Ports.PORT10
GPS_PORT=Ports.PORT11
AI_PORT=Ports.PORT13
D_PORT=Ports.PORT15

# Configure motor reverse settings (True = reversed, False = normal)
# FRONT_LEFT_REVERSE = False
#endregion

#region ==================== SENSOR INITIALIZATION ====================

# AI Classification Competition Element IDs - Push Back
class GameElementsPushBack:
    BLUE_BLOCK = 0
    RED_BLOCK = 1
# AI Vision Color Descriptions
ai__BBLUE = Colordesc(1, 32, 154, 226, 10, 0.2)
ai__BRED = Colordesc(2, 231, 42, 92, 10, 0.2)


# Initialize motors with configured ports and reverse settings
# front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)

distance = Distance(D_PORT)
gps=Gps(GPS_PORT,0,0)# set to be the offset from the center of robot
ai = AiVision(AI_PORT, ai__BBLUE, ai__BRED, AiVision.ALL_AIOBJS)
#endregion

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
def bool_margin(x,y,tx,ty):
    mx=abs(x-tx)
    my=abs(y-ty)
    if mx>30 or my>30: return False
    else: return True
def int_margin(x,y,tx,ty):
    mx=abs(x-tx)
    my=abs(y-ty)
    return math.sqrt(mx**2+my**2)
def gps_gohead(heading):
    arrived=False
    while not arrived:
        if gps.quality()<100: continue
        head=gps.heading()
        diff=heading-head
        if abs(diff)>2:arrived=True
        else: 
            if diff<-180:diff+=360
            elif diff>180:dif-=360
            if (diff>0 and diff<180):
                                
            else:
                
            
def gps_goto(x,y):
    arrived=False
    while not arrived:
        if gps.quality()<100: continue
        xc=gps.x_position()
        yc=gps.y_position()
        if bool_margin(xc,yc,x,y):arrived=True
        else:
            
        
    
def ai_funcs():
    objs=ai.take_snapshot(AiVision.ALL_AIOBJS)
    #bobjs=ai.take_snapshot(ai__BBLUE)
    #robjs=ai.take_snapshot(ai__BRED)
    objs_names=""
    if objs[0].exists: 
        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        print("yes")
        for x in objs:
            if x.id==GameElementsPushBack.BLUE_BLOCK:
                objs_names+=("Blue: "+str(x.score)+", ")
            elif x.id==1:
                objs_names+=("Red: "+str(x.score)+", ")
            else:
                objs_names+=("Unknown: "+str(x.score)+", ")
    '''elif bobjs[0].exists:
        for x in bobjs:
            objs_names+=("BBlue: "+str(x.score)+", ")
    elif robjs[0].exists:
        for x in robjs:
            objs_names+=("BRed: "+str(x.score)+", ")
    else: print ("no")'''
    if objs_names: print("Objects Detected: ",objs_names)
    
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


        
