# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Vincent, Xin, Elena                                          #
# 	Created:      10/19/2025, 3:17:13 PM                                       #
# 	Description:  V5 X-Drive Control & 2026 Code                               #
#                                                                              #
# ---------------------------------------------------------------------------- #

#region Setup
# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
controller = Controller(PRIMARY)
import math
#endregion
#region ==================== MOTOR CONFIGURATION ====================
# Configure your motor ports here
FRONT_LEFT_PORT = Ports.PORT19
FRONT_RIGHT_PORT = Ports.PORT11
BACK_LEFT_PORT = Ports.PORT10
BACK_RIGHT_PORT = Ports.PORT1



# Configure motor reverse settings (True = reversed, False = normal)
FRONT_LEFT_REVERSE = False
FRONT_RIGHT_REVERSE = True
BACK_LEFT_REVERSE = False
BACK_RIGHT_REVERSE = True
#endregion
#region ==================== SENSOR CONFIGURATION ====================
AI_PORT=Ports.PORT13
D_PORT=Ports.PORT15
GPS_PORT=Ports.PORT9
#endregion
#region ==================== MOTOR INITIALIZATION ====================
# Initialize motors with configured ports and reverse settings
front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)
front_right = Motor(FRONT_RIGHT_PORT, GearSetting.RATIO_18_1, FRONT_RIGHT_REVERSE)
back_left = Motor(BACK_LEFT_PORT, GearSetting.RATIO_18_1, BACK_LEFT_REVERSE)
back_right = Motor(BACK_RIGHT_PORT, GearSetting.RATIO_18_1, BACK_RIGHT_REVERSE)
gps=Gps(GPS_PORT,0,0)
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
#region ==================== INTAKE MOTOR FUNCTIONS ====================
# Assume motors are already initialized somewhere:
intake_left  = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
intake_right = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)

#right and left relative to viewing from the front
def intake_forward_toggle():
    global intake_forward, intake_reverse

    if intake_forward:
        # If already running forward, stop both motors concurrently
        intake_left.stop(HOLD)
        intake_right.stop(HOLD)
    else:
        # If reverse is on, turn it off first
        if intake_reverse:
            intake_reverse = False
            intake_left.stop(HOLD)
            intake_right.stop(HOLD)

        # Spin both motors in forward intake direction concurrently
        intake_left.spin(FORWARD, 100, PERCENT)
        intake_right.spin(FORWARD, 100, PERCENT)

    # Toggle the forward state
    intake_forward = not intake_forward

def intake_reverse_toggle():
    global intake_reverse, intake_forward

    if intake_reverse:
        # If already running reverse, stop both motors concurrently
        intake_left.stop(HOLD)
        intake_right.stop(HOLD)
    else:
        # If forward is on, turn it off first
        if intake_forward:
            intake_forward = False
            intake_left.stop(HOLD)
            intake_right.stop(HOLD)

        # Spin both motors in reverse intake direction concurrently
        intake_left.spin(REVERSE, 100, PERCENT)
        intake_right.spin(REVERSE, 100, PERCENT)

spinny_thing = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)

def spin_toggle_fn():
    global spin_toggle
    if spin_toggle:
        spinny_thing.stop()
    else: 
        spinny_thing.spin(FORWARD, 100, PERCENT)
    spin_toggle = not spin_toggle

spin_toggle = False
controller.buttonA.pressed(spin_toggle_fn)

intake_forward = False
controller.buttonL1.pressed(intake_forward_toggle)

intake_reverse = False
controller.buttonL2.pressed(intake_reverse_toggle)
#endregion
#region ==================== DRIVETRAIN FUNCTIONS ====================
def x_drive_control():
    """
    Control the X-drive using controller joysticks.
    Left joystick: Forward/backward and strafing
    Right joystick (X-axis): Rotation
    """
    # Get controller inputs
    forward = controller.axis3.position()  # Left stick Y-axis
    strafe = controller.axis4.position()   # Left stick X-axis
    turn = controller.axis1.position()     # Right stick X-axis
    run_drive_motors(forward,strafe,turn)
    
def run_drive_motors(forward,strafe,turn):    
    # Calculate motor speeds for X-drive kinematics
    # X-drive formula accounts for diagonal motor placement
    front_left_speed = forward + strafe + turn
    front_right_speed = forward - strafe - turn
    back_left_speed = forward - strafe + turn
    back_right_speed = forward + strafe - turn
    
    # Set motor velocities
    front_left.spin(FORWARD, front_left_speed, PERCENT)
    front_right.spin(FORWARD, front_right_speed, PERCENT)
    back_left.spin(FORWARD, back_left_speed, PERCENT)
    back_right.spin(FORWARD, back_right_speed, PERCENT)

def stop_drive():
    """Stop all drive motors."""
    front_left.stop()
    front_right.stop()
    back_left.stop()
    back_right.stop()
#endregion
#region ==================== SENSOR FUNCTIONS ====================
#region GPS Functions
def reset_gps():
    #If we want, we can find a fixed reference points, find its setting, then calibrate the gps to it. 
    gps.calibrate()
    while gps.is_calibrating():
        continue
    gps.set_location(0,0) #inital x and y pos of robot, for calibrations 
    gps.set_origin(0,0) 
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
    error=20
    mx=abs(x-tx)
    my=abs(y-ty)
    if mx>error or my>error: return False
    else: return True
def int_margin(x,y,tx,ty):
    mx=abs(x-tx)
    my=abs(y-ty)
    return math.sqrt(mx**2+my**2)
def gps_gohead(heading):
    arrived=False
    c1=False
    turn=0
    while not arrived:
        if gps.quality()<90: continue
        head=gps.heading()
        diff=heading-head
        if diff<-180:diff+=360
        elif diff>180:diff-=360
        print("diff is" +str(diff)+"and head is"+str(head))
        if abs(diff)<1:
            stop_drive()
            if c1:
                arrived=True 
            c1=True
            continue 
        else:
            c1=False 
            if (diff>0 and diff<180):
                 if diff>150:turn=80               
                 elif diff>120:turn=60               
                 elif diff>90:turn=60               
                 elif diff>60:turn=40               
                 elif diff>30:turn=30               
                 elif diff>15:turn=20               
                 elif diff>5:turn=10               
                 else:turn=5              
            else:
                if diff<-150:turn=-800               
                elif diff<-120:turn=-60               
                elif diff<-90:turn=-50               
                elif diff<-60:turn=-40               
                elif diff<-30:turn=-30               
                elif diff<-15:turn=-20               
                elif diff<-5:turn=-10               
                else:turn=-5 
            run_drive_motors(0,0,turn)
            wait(5, MSEC)
    print("arrived")        
def gps_goto(x,y):
    arrived=False
    heading_set=False
    while not arrived:
        if gps.quality()<100: continue
        xc=gps.x_position()
        yc=gps.y_position()
        if bool_margin(xc,yc,x,y):
            arrived=True
            stop_drive()
        else:
            if not heading_set:
                mx=x-xc
                my=y-yc
                angle=math.degrees(math.atan2(my,mx))
                gps_gohead(angle)
                heading_set=True
            dis=int_margin(xc,yc,x,y)
            print("dis"+str(dis))
            if dis>200:f=100               
            elif dis>150:f=80               
            elif dis>120:f=60               
            elif dis>90:f=60               
            elif dis>60:f=40               
            elif dis>30:f=30               
            elif dis>15:f=20               
            elif dis>5:f=10               
            else:f=5 
            run_drive_motors(f,0,0)
            wait(5, MSEC)
    print("arrived")               
#endregion
#other funcs here
#endregion 
#region ==================== MAIN PROGRAM ====================
brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")

# GPS TESTING
# gps_goto(-800,-100)
# wait(1000, MSEC)
# gps_goto(-800,-100)
# wait(1000, MSEC)

# gps_gohead(0)
# wait(3000, MSEC)
# gps_gohead(120)
# wait(3000, MSEC)
# gps_gohead(240)
# wait(3000, MSEC)
# gps_gohead(0)
# wait(3000, MSEC)
# Main control loop

while True:
    gps_funcs()
    x_drive_control()
    wait(100, MSEC)  # Small delay to prevent CPU overload
#endregion