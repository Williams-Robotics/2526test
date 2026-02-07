# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Vincent, Xin, Elena                                          #
# 	Created:      10/19/2025, 3:17:13 PM                                       #
# 	Description:  V5 X-Drive Control & 2026 Code                               #
#                                                                              #
# ---------------------------------------------------------------------------- #

'''
Controls: 

Left Stick:Forwards and Back
Right Stick: Rotation

Down DPAD: Toggle Reverse Driving(flip which way is forward, useful for grabbing vs scoring)
A:Toggle Tounge
B: Toggle Wing
X: Toggle Butt(Big Robot Only)
Y: Hold to enable strafing with left stick
'''

#region Setup
# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
controller = Controller(PRIMARY)
import math
#endregion
#region  MOTOR & PNEUMATICS CONFIGURATION 
# Configure your motor ports here
FRONT_LEFT_PORT = Ports.PORT10
FRONT_RIGHT_PORT = Ports.PORT20
BACK_LEFT_PORT = Ports.PORT1
BACK_RIGHT_PORT = Ports.PORT11
INTAKE_PORT1=Ports.PORT3
INTAKE_PORT2=Ports.PORT5
OUTAKE_PORT=Ports.PORT4
BUTT_PORT=Ports.PORT14



# Configure motor reverse settings (True = reversed, False = normal)
FRONT_LEFT_REVERSE = False
FRONT_RIGHT_REVERSE = True
BACK_LEFT_REVERSE = False
BACK_RIGHT_REVERSE = True
INTAKE_REVERSE = False
OUTAKE_REVERSE = True
BUTT_REVERSE=False

strafeToggle=False
#endregion
#region  SENSOR CONFIG
AI_PORT=Ports.PORT13
D_PORT=Ports.PORT15
GPS_PORT=Ports.PORT9
INT_PORT=Ports.PORT21
#endregion
#region  DRIVE INIT
# Initialize motors with configured ports and reverse settings
front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)
front_right = Motor(FRONT_RIGHT_PORT, GearSetting.RATIO_18_1, FRONT_RIGHT_REVERSE)
back_left = Motor(BACK_LEFT_PORT, GearSetting.RATIO_18_1, BACK_LEFT_REVERSE)
back_right = Motor(BACK_RIGHT_PORT, GearSetting.RATIO_18_1, BACK_RIGHT_REVERSE)
gps=Gps(GPS_PORT,0,0)
#endregion
#region  INTAKE FUNCS
intake1  = Motor(INTAKE_PORT1, GearSetting.RATIO_18_1, INTAKE_REVERSE)
intake2  = Motor(INTAKE_PORT2, GearSetting.RATIO_18_1, not INTAKE_REVERSE)
intake=MotorGroup(intake1,intake2)
outake = Motor(OUTAKE_PORT, GearSetting.RATIO_18_1, OUTAKE_REVERSE)
butt=Motor(BUTT_PORT,GearSetting.RATIO_36_1,BUTT_REVERSE)
tongue_control=Pneumatics(brain.three_wire_port.h)
wing_control=Pneumatics(brain.three_wire_port.g)


#right and left relative to viewing from the front
def intake_forward_toggle():    
    global intake_forward, intake_reverse

    if intake_forward:
        # If already running forward, stop both motors concurrently
        intake.stop(HOLD)
        intake_forward = False
        
    else:
        intake_reverse = False
        intake_forward = True
        intake.stop(HOLD)
        intake.spin(FORWARD, 100, PERCENT)
    # Toggle the forward state
    

def intake_reverse_toggle():
    global intake_reverse, intake_forward

    if intake_reverse:
        # If already running reverse, stop both motors concurrently
        intake.stop(HOLD)
        intake_reverse = False
        
    else:
        intake_forward = False
        intake_reverse = True
        intake.stop(HOLD)
        intake.spin(REVERSE, 100, PERCENT)
    
def outake_forward_toggle():
    global outake_forward, outake_reverse

    if outake_forward:
        # If already runnoug forward, stop both motors concurrently
        outake.stop(HOLD)
        outake_forward=False
    else:
            outake_reverse = False
            outake_forward=True
            outake.stop(HOLD)
            outake.spin(FORWARD, 100, PERCENT)

def outake_reverse_toggle():
    global outake_reverse, outake_forward

    if outake_reverse:
        # If already runnoug reverse, stop both motors concurrently
        outake.stop(HOLD)
        outake_reverse=False
    else:
            outake_forward = False
            outake_reverse=True
            outake.stop(HOLD)
            outake.spin(REVERSE, 100, PERCENT)
            # outake.stop(HOLD)
        # Spou both motors ou reverse outake direction concurrently

def tongue_toggle_fn():
    global tongue_toggle
    tongue_toggle = not tongue_toggle
    if tongue_toggle:tongue_control.open()
    else:tongue_control.close()
def wing_toggle_fn():
    global wing_toggle
    wing_toggle = not wing_toggle
    if wing_toggle:wing_control.open()
    else:wing_control.close()
def butt_toggle_fn():
    global butt_toggle
    butt_toggle = not butt_toggle
    if butt_toggle:butt.spin_to_position(0,DEGREES)
    else:butt.spin_to_position(180,DEGREES)
    
def rev_drive_toggle_fn():
    global reverseDriveToggle
    reverseDriveToggle = not reverseDriveToggle


tongue_toggle = False
controller.buttonA.pressed(tongue_toggle_fn)

wing_toggle = False
controller.buttonB.pressed(wing_toggle_fn)

# outake_toggle = False
# controller.buttonX.pressed(outake_toggle_fn)

intake_forward = False
controller.buttonL1.pressed(intake_forward_toggle)

intake_reverse = False
controller.buttonL2.pressed(intake_reverse_toggle)

outake_forward = False
controller.buttonR1.pressed(outake_forward_toggle)

outake_reverse = False
controller.buttonR2.pressed(outake_reverse_toggle)

butt_toggle=True
controller.buttonX.pressed(butt_toggle_fn)

reverseDriveToggle=False
controller.buttonUp.pressed(rev_drive_toggle_fn)




#endregion'

#region  SENSOR INIT

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
int=Inertial(INT_PORT)
timer = Timer()

#endregion

#region DRIVETRAIN FUNCS
goal_head=999
last_head=999
getH=False
prev_head_error=0
total_head_error=0
def x_drive_control(ignore=False):
    """
    Control the X-drive using controller joysticks.
    Left joystick: Forward/backward and strafing
    Right joystick (X-axis): Rotation
    """
    # Get controller inputs
    forward = controller.axis3.position()  # Left stick Y-axis
    strafe = controller.axis4.position() 
    # strafe=0# Left stick X-axis
    turn_val = controller.axis1.position() 
    if abs(turn_val)<10:turn=2*abs(turn_val)
    elif abs(turn_val)<60: turn=.006*((abs(turn_val)-10)**2)+20
    else: turn=40+((60/(math.exp(2)-1))*(math.exp(.05*(abs(turn_val)-60))-1))
    if turn_val<0: turn*=-1
    # turn=.75*turn_val if turn_val<50 else 39.4*math.exp(.019*(turn_val-50))-1.9# Right stick X-axis
    # print("val: "+str(turn_val)+"turn: "+str(turn))
    run_drive_motors(forward,strafe,turn,ignore)
    
def run_drive_motors(forward,strafe,turn, ignore=False):
    if forward==strafe==turn==0:
        stop_drive()
        return
    if not strafeToggle: strafe=0
    if reverseDriveToggle: 
        forward*=-1
        strafe*=-1
    if not ignore: turn=newgps_heading_control(turn)
    
    # if not ignore: turn = gps_drive_assist(forward, strafe, turn)
       
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
#Gets the heading of the robot after a slight delay, so it gets the heading when it is stopped
def activate_heading():
    global getH
    global goal_head
    goal_head=(gps.orientation(OrientationType.YAW))
    getH=True
def newgps_heading_control(turn):
    global goal_head
    global getH
    global prev_head_error
    global total_head_error
    #When Turning
    if turn!=0:
        getH=False
        prev_head_error=0
        total_head_error=0
        return turn
    
    #When Done turning, get heading
    elif turn==0 and not getH:
        if abs(gps.gyro_rate(AxisType.XAXIS))<2000:
            timer.event(activate_heading,100)
            print("got: "+str(gps.gyro_rate(AxisType.XAXIS)))
        else: print("BAD: "+str(gps.gyro_rate(AxisType.XAXIS)))
        # timer.event(get_heading,500)
        return turn
        
    #runs the heading correction after it has the heading, which also means it only kicks in for longer drives
    elif turn==0 and getH:
        chead=(gps.orientation(OrientationType.YAW))
        # turn=(goal_head-chead)/4 

        heading_error = goal_head - chead
        if heading_error > 180:
            heading_error -= 360
        elif heading_error < -180:
            heading_error += 360

        turn,prev_head_error,total_head_error=PID(0,-heading_error,.7,.15,0.5,prev_head_error,total_head_error)  #THIS IS PID! please tune the values, the .25 is just from what i used before. 
        if turn>50: turn=50
        elif turn < -50:
            turn = -50
        # print("chead: "+str(chead)+"-goal: "+str(goal_head))
        return turn

    else: 
        print("Unexpexted Issue With Heading Control")
        return turn
    

  
def stop_drive():
    """Stop all drive motors."""
    front_left.stop(HOLD)
    front_right.stop(HOLD)
    back_left.stop(HOLD)
    back_right.stop(HOLD)

def raw_drive_test():
    f = controller.axis3.position()
    front_left.spin(FORWARD, f, PERCENT)
    front_right.spin(FORWARD, f, PERCENT)
    back_left.spin(FORWARD, f, PERCENT)
    back_right.spin(FORWARD, f, PERCENT)
hold_heading = None
prev_error = 0

def wrap_angle(a):
    if a > 180: a -= 360
    if a < -180: a += 360
    return a


def gps_drive_assist(forward, strafe, driver_turn):
    global hold_heading, prev_error

    #off when turning
    if abs(driver_turn) > 5:
        hold_heading = None
        prev_error = 0
        return driver_turn

    # off when still
    if abs(forward) < 15:
        hold_heading = None
        prev_error = 0
        return driver_turn

    if gps.quality() < 90:
        return driver_turn

    # startiing heading
    if hold_heading is None:
        hold_heading = gps.heading()
        return driver_turn

    # calculate heading error
    error = wrap_angle(hold_heading - gps.heading())

    Kp = 1.1
    Kd = 0.25

    correction = Kp * error + Kd * (error - prev_error)
    prev_error = error

    # Limit correction so it doesn't feel "grabby"
    correction = max(-20, min(20, correction))

    return driver_turn + correction
#endregion

#region SENSOR FUNCS

def PID(desired_state,current_state,Kp,Ki,Kd,prev_error,total_error):
    #Blank PID Function, so we can use it everywhere
    '''
    ### PID Function
   
    desired_state-- What we want
    
    current_state-- where we are
    
    Kp,Ki,Kd: Tuning variables
    
    Prev_error: previous error
    
    total_error: total error
    '''
    
    '''## Desired position (adjust number based on what we need the robot to do)
    desired_state = 0

    ## Variables used in PID algo (adjust numbers based on what we need the robot to do)
    Kp = 0
    Ki = 0
    Kd = 0
    ## Remember to test each constants one at a time, this affects output of PID controller

    Ki_total = 0 # sum from integral
    prev_error = 0

    while True():'''
    ## get error
    error = desired_state - current_state
    ## Kp : proportional correction
    proportional = Kp * error
    ## Ki : integral correction
    total_error += error ## add current error to summation
    integral = Ki * total_error ## get Ki Result by applying tuning constant to total
    ## consider limits on Ki perchance?
    ## Kd : derivative
    derivative = Kd * (error - prev_error)
    prev_error = error
    ## sum P, I, and D
    PID_result = proportional + integral + derivative
    return PID_result, prev_error,total_error
    ## apply PID_result (sum) to the bot depending on which component we want it to adjust

def initialize():
    gps.set_origin(0,5,MM)
    gpsh=gps.heading()
    int.calibrate
    # while int.is_calibrating:
    # print("calibrating")
    int.set_heading(gpsh)
    wait(1500,MSEC)
    butt.set_position(0, DEGREES)
    # gpsavg=[]
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
    error=25
    mx=abs(x-tx)
    my=abs(y-ty)
    if mx>error or my>error: return False
    else: return True
def int_margin(x,y,tx,ty):
    mx=abs(x-tx)
    my=abs(y-ty)
    return math.sqrt(mx**2+my**2)
def gps_gohead_old(heading):
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
                 if diff>150:turn=50               
                 elif diff>120:turn=40               
                 elif diff>90:turn=20               
                 elif diff>60:turn=20               
                 elif diff>30:turn=10               
                 elif diff>15:turn=5               
                 elif diff>5:turn=5               
                 else:turn=3             
            else:
                if diff<-150:turn=-50               
                elif diff<-120:turn=-40               
                elif diff<-90:turn=-20               
                elif diff<-60:turn=-20               
                elif diff<-30:turn=-10               
                elif diff<-15:turn=-5               
                elif diff<-5:turn=-5               
                else:turn=-3
            run_drive_motors(0,0,turn)
            wait(5, MSEC)
    print("arrived")
def gps_gohead(heading):
    if reverseDriveToggle: 
        heading+=180
    arrived=False
    c1=False
    turn,prev_head_error,total_head_error=0,0,0
    while not arrived:
        if gps.quality()<90: continue
        head=gps.heading()
        diff=heading-head
        while diff<-180:diff+=360
        while diff>180:diff-=360
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
                turn,prev_head_error,total_head_error=PID(0,diff,.6,.0001,0.1,prev_head_error,total_head_error)  
                turn*=-1 
                # print("turnR: {}".format(turn))
                        
            else:
                turn,prev_head_error,total_head_error=PID(0,diff,.6,.0001,0.1,prev_head_error,total_head_error)
                turn*=-1 
                # print("turnL: {}".format(turn))
                
            run_drive_motors(0,0,turn)
            wait(5, MSEC)
    print("arrived")                
def goto_arr():
    global arrived
    while not arrived:
        if bool_margin(gps.x_position(),gps.y_position(),goalx,goaly):
            arrived=True
            stop_drive()
def gps_goto(x,y):
    global arrived
    global goalx
    global goaly
    goalx=x
    goaly=y
    arrived=False
    counter=3000
    heading_set=False
    prev_gps_error=0
    total_gps_error=0
    # arr_thread=Thread(goto_arr)
    while not arrived:
        # if gps.quality()<100:
        #     stop_drive()
        #     print("NO GPS")
        xc=gps.x_position()
        yc=gps.y_position()
        if bool_margin(xc,yc,x,y):
            arrived=True
            stop_drive()
            continue
        if counter%3000==0 and int_margin(xc,yc,x,y)>150:
            counter=0
            mx=x-xc
            my=y-yc
            print("Pos: (",xc,",",yc,")")
            print("dis: (",mx,",",my,")")
            
            angle=math.degrees(math.atan2(mx, my))

            print("ANGLE: "+str(angle))
            gps_gohead(angle)
            heading_set=True
            # wait(1500,MSEC)
        dis=int_margin(xc,yc,x,y)
        print("dis"+str(dis))
        counter+=1
        # if dis>200:f=10              
        # elif dis>150:f=10               
        # elif dis>120:f=10               
        # elif dis>90:f=10               
        # elif dis>60:f=5               
        # elif dis>30:f=4               
        # elif dis>15:f=3               
        # elif dis>5:f=2              
        # else:f=1
        f,prev_gps_error,total_gps_error=PID(dis,0,.1,.005,.01,prev_gps_error,total_gps_error)
        if f>35: f=35
        # if reverseDriveToggle: 
        #     f*=-1
        run_drive_motors(f,0,0,True)
        print("Pos: (",xc,",",yc,"), HEAD: "+str(gps.heading()) +"Counter: "+str(counter)+"f: "+str(f))
        
        # wait(100, MSEC)
    print("arrived")    
#endregion

#other funcs here
#endregion 
#region  MAIN PROGRAM 
initialize()

brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")

# GPS TESTING
# gps_goto(-800,-100)
# wait(1000, MSEC)
# gps_goto(-500,500)
# wait(1000, MSEC)
# gps_goto(500,500)
# gps_gohead(0)
# wait(1000, MSEC)


# gps_gohead(0)
# wait(3000, MSEC)
# gps_gohead(120)
# wait(3000, MSEC)
# gps_gohead(240)
# wait(3000, MSEC)
# gps_gohead(0)
# wait(3000, MSEC)
# gps_gohead(0)

#Main control loop
# gps_goto(365,440)
# wait(3000, MSEC)

#region Auton
# def autonomous0():
#     initialize()
#     brain.screen.clear_screen()
#     brain.screen.print("autonomous code")
#     #AUTON
#     tongue_toggle_fn()
#     butt_toggle_fn()
#     wait(150,MSEC)
#     intake_forward_toggle()
#     timer.clear()
#     while timer.time(MSEC) < 1500:
#         run_drive_motors(-80, 0, 0)   # forward
#         wait(10, MSEC)
#     stop_drive()
#     outake_forward_toggle()
   

# def autonomous2():
#     tongue_toggle_fn()
#     wait(150,MSEC)
#     intake_forward_toggle()
#     run_drive_motors(100,0,0)
#     wait(3000,MSEC)
#     run_drive_motors(0,0,0)
#     # wait(1500,MSEC)
#     intake_forward_toggle()
#     run_drive_motors(-50,0,0)
#     butt_toggle_fn()
#     wait(1500,MSEC)
#     stop_drive()
def autonomous_v1():
    # gps_goto(894,-1241)
    # gps_gohead(87)
    # tongue_toggle_fn()
    # gps_goto(1363,-1174)
    # intake_forward_toggle()
    # gps_goto(0,406)
    # gps_gohead(270)
    # gps_goto(-1162,542)
    # gps_gohead(0)
    gps_goto(1162,-1235)
    gps_gohead(90)
    intake_forward_toggle()
    butt_toggle_fn()
    run_drive_motors(-50,0,0)
    wait(2000,MSEC)
    outake_forward_toggle()
    wait(5000,MSEC)
    run_drive_motors(50,0,0)
    outake_forward_toggle()
    tongue_toggle_fn()
    wait(3000,MSEC)
    run_drive_motors(-50,0,0)
    outake_forward_toggle()
    wait(5000,MSEC)
    
def autonomous_v2_red():
    initialize()
    while True: 
        # goto spot 
        gps_goto(-1220,-1200)
        gps_gohead(270)
        
        #grab balls
        print("grab balls")
        intake_forward_toggle()
        tongue_toggle_fn()
        wait(100,MSEC)
        run_drive_motors(25,0,0)
        wait(800,MSEC)
        run_drive_motors(100,0,0)
        wait(2200,MSEC)
        print("Stoop moter")
        tongue_toggle_fn()
        wait(50,MSEC)
        tongue_toggle_fn()
        run_drive_motors(0,0,0)
        wait(1200,MSEC)
        intake_forward_toggle()

        
        #go to drop spot
        print("godrop")
        # butt_toggle_fn()
        print("f1")
        rev_drive_toggle_fn()
        print("greoooo")
        run_drive_motors(50,0,0)
        wait(500,MSEC)
        print("f2")
        # gps_goto(-1000,-1250)
        tongue_toggle_fn()
        print("grat")   
        # gps_gohead(90)
        run_drive_motors(50,0,0)
        wait(2000,MSEC)
        
        #drop balls
        print("drop")
        intake_forward_toggle()
        outake_forward_toggle()
        wait(3500,MSEC)
        intake_forward_toggle()
        outake_forward_toggle()
        rev_drive_toggle_fn()
        

def autonomous_v2_blue():
    initialize()
    while True: 
        #goto spot 
        gps_goto(1220,1200)
        gps_gohead(90)
        
        #grab balls
        print("grab balls")
        intake_forward_toggle()
        tongue_toggle_fn()
        wait(100,MSEC)
        run_drive_motors(25,0,0)
        wait(800,MSEC)
        run_drive_motors(100,0,0)
        wait(2200,MSEC)
        print("Stoop moter")
        tongue_toggle_fn()
        wait(50,MSEC)
        tongue_toggle_fn()
        run_drive_motors(0,0,0)
        wait(1200,MSEC)
        intake_forward_toggle()

        
        #go to drop spot
        print("godrop")
        # butt_toggle_fn()
        print("f1")
        rev_drive_toggle_fn()
        print("greoooo")
        run_drive_motors(50,0,0)
        wait(500,MSEC)
        print("f2")
        # gps_goto(-1000,-1250)
        tongue_toggle_fn()
        print("grat")   
        # gps_gohead(90)
        run_drive_motors(50,0,0)
        wait(2000,MSEC)
        
        #drop balls
        print("drop")
        intake_forward_toggle()
        outake_forward_toggle()
        wait(3500,MSEC)
        intake_forward_toggle()
        outake_forward_toggle()
        
        rev_drive_toggle_fn()
    

   
   
def autonomou():
    initialize()
    print("Driving")
    intake_forward_toggle()
    run_drive_motors(60, 0, 0)   # forward
    wait(3000,MSEC)
    print("nodrive")
    stop_drive()
    wait(2500,MSEC)
    intake_forward_toggle()
    
    
    #makes angles unreliable
    # for i in range(5):  # repeat 5 times
    #     # rev for x msec
    #     timer.clear()
    #     while timer.time(MSEC) < 100:
    #         run_drive_motors(-100, 0, 0)   # forward
    #         wait(10, MSEC)

    #     stop_drive()
    #     wait(100, MSEC)  # small pause (optional)

    #     # fow for x msec
    #     timer.clear()
    #     while timer.time(MSEC) < 200:
    #         run_drive_motors(100, 0, 0)  # backward
    #         wait(10, MSEC)

    #     stop_drive()
    #     wait(100, MSEC)  # small pause (optional)


    


    #Drive forward
    #grab 3 Balls
    #drive to goal and drop flap
    #Hit goal and dispense 3 balls
    #drive back
    #grab 3 red. Spit. Grab 3 blue
    #do it
    #keep doing it
#endregion


def user_control():
    # COMMENT OUT FOR THE ACTUAL
    
    global strafeToggle
    while True:
        # gps_gohead(90)
        # wait(500,MSEC)
        # gps_gohead(190)
        # wait(500,MSEC)
        # gps_gohead(180)
        # wait(500,MSEC)
    
        xc=gps.x_position()
        yc=gps.y_position()
        if controller.buttonY.pressing(): strafeToggle=True
        else:strafeToggle=False
        
        x_drive_control(False)
        
        #Controller Screen
        
        controller.screen.clear_screen()
        # x=gps.x_position()
        # y=gps.y_position()
        # head=gps.heading()
        # print(x,y,head)
        # print(intake.torque(TorqueUnits.NM))
        controller.screen.set_cursor(1, 1)
        controller.screen.print("Score" if reverseDriveToggle else "Gather")
        controller.screen.set_cursor(2, 1)
        controller.screen.print("Butt Closed" if not butt_toggle else "Butt Open")

        
        
        # print("heading: "+str(get_gps_avg()))
        # print("int: "+str(int.heading()))
        #raw_drive_test()
        # initialize()
        # print_gps_status()
        
        print("Pos: (",xc,",",yc,"), HEAD: "+str(gps.heading()))
        wait(100, MSEC)  # Small delay to prevent CPU overload
#endregion

# create competition instance
comp = Competition(user_control, autonomous_v2_blue)

# actions to do when the program starts
brain.screen.clear_screen()
# user_control()
# autonomous()