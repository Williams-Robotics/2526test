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
#region ==================== MOTOR & PNEUMATICS CONFIGURATION ====================
# Configure your motor ports here
FRONT_LEFT_PORT = Ports.PORT5
FRONT_RIGHT_PORT = Ports.PORT2
BACK_LEFT_PORT = Ports.PORT3
BACK_RIGHT_PORT = Ports.PORT4
INTAKE_PORT=Ports.PORT9
OUTAKE_PORT=Ports.PORT1
WING_PORT=Ports.PORT20



# Configure motor reverse settings (True = reversed, False = normal)
FRONT_LEFT_REVERSE = False
FRONT_RIGHT_REVERSE = True
BACK_LEFT_REVERSE = False
BACK_RIGHT_REVERSE = True
INTAKE_REVERSE = False
OUTAKE_REVERSE = True
WING_REVERSE=False
#endregion
#region ==================== SENSOR CONFIGURATION ====================
AI_PORT=Ports.PORT13
D_PORT=Ports.PORT15
GPS_PORT=Ports.PORT10
INT_PORT=Ports.PORT21
#endregion
#region ==================== DRIVE MOTOR INITIALIZATION ====================
# Initialize motors with configured ports and reverse settings
front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)
front_right = Motor(FRONT_RIGHT_PORT, GearSetting.RATIO_18_1, FRONT_RIGHT_REVERSE)
back_left = Motor(BACK_LEFT_PORT, GearSetting.RATIO_18_1, BACK_LEFT_REVERSE)
back_right = Motor(BACK_RIGHT_PORT, GearSetting.RATIO_18_1, BACK_RIGHT_REVERSE)
#endregion
#region ==================== INTAKE FUNCTIONS ====================
intake  = Motor(INTAKE_PORT, GearSetting.RATIO_18_1, INTAKE_REVERSE)
wing  = Motor(WING_PORT, GearSetting.RATIO_36_1, WING_REVERSE)
outake = Motor(OUTAKE_PORT, GearSetting.RATIO_18_1, OUTAKE_REVERSE)
tongue_control=Pneumatics(brain.three_wire_port.h)


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
        intake.spin(REVERSE, 60, PERCENT)
    
def outake_forward_toggle(speed=65):
    global outake_forward, outake_reverse

    if outake_forward:
        # If already runnoug forward, stop both motors concurrently
        outake.stop(HOLD)
        outake_forward=False
    else:
            outake_reverse = False
            outake_forward=True
            outake.stop(HOLD)
            outake.spin(FORWARD, speed, PERCENT)

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
            outake.spin(REVERSE, 65, PERCENT)
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
    if (wing.position())==(0.0):wing.spin_to_position(-173.0)
    if wing_toggle:
        wing.spin_to_position(-125.4)
        # wing.spin_for(REVERSE, 280, MSEC, 80, PERCENT)
        print("wing up")
    else:
        wing.spin_to_position(-173.0)
        # wing.spin_for(FORWARD, 240, MSEC, 80, PERCENT)
        print("wing down")
    
    # global med_state
    # if wing_toggle == False and med_state == False:
    #     # Wing UP
    #     med_state = True
    #     wing_toggle = True
    #     wing.spin_for(REVERSE, 200, MSEC, 80, PERCENT)
    #     print("wing med")
    # elif wing_toggle == True and med_state ==True:
    #     med_state = False
    #     wing_toggle = True
    #     wing.spin_for(REVERSE,100, MSEC, 80, PERCENT)
    #     print("wing highest position")
    # elif wing_toggle == True and med_state == False:
    #     med_state = True
    #     wing_toggle = False
    #     wing.spin_for(FORWARD, 100, MSEC, 80, PERCENT)
    #     print("wing highest position")

    # else:
    #     # Wing DOWN
    #     wing_toggle = False
    #     med_state = False
    #     wing.spin_for(FORWARD, 200 , MSEC, 80, PERCENT)
    #     print("wing down")
     
def rev_drive_toggle_fn():
    global reverseDriveToggle
    reverseDriveToggle = not reverseDriveToggle



tongue_toggle = False
controller.buttonA.pressed(tongue_toggle_fn)

wing_toggle = False
med_state = False
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

reverseDriveToggle=False

controller.buttonUp.pressed(rev_drive_toggle_fn)
strafeToggle = False

#endregion'

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
gps=Gps(GPS_PORT)# set to be the offset from the center of robot
gps.set_origin(0,100,MM)
ai = AiVision(AI_PORT, ai__BBLUE, ai__BRED, AiVision.ALL_AIOBJS)
int=Inertial(INT_PORT)
timer = Timer()

#endregion

#region ==================== DRIVETRAIN FUNCTIONS ====================
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
    # turn=3*turn_val if turn_val<(20/3) else 39.4*math.exp(.019*(turn_val-50))-1.9# Right stick X-axis
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
#endregion
#region ==================== SENSOR FUNCTIONS ====================

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
    wing.set_position(0, DEGREES)
    
    wait(1500,MSEC)
    
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
    error=30
    mx=abs(x-tx)
    my=abs(y-ty)
    if mx>error or my>error: return False
    else: return True
def int_margin(x,y,tx,ty):
    mx=abs(x-tx)
    my=abs(y-ty)
    return math.sqrt(mx**2+my**2)
def gps_gohead(heading):
    Kp=1.1
    Ki=.0001
    Kd=.1
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
        if abs(diff)<1.7:
            stop_drive()
            if c1:
                arrived=True
                wait(50,MSEC) 
            c1=True
            continue 
        else:
            c1=False 
            if (diff>0 and diff<180):
                turn,prev_head_error,total_head_error=PID(0,diff,Kp,Ki,Kd,prev_head_error,total_head_error)  
                turn*=-1 
                # print("turnR: {}".format(turn))
                        
            else:
                turn,prev_head_error,total_head_error=PID(0,diff,Kp,Ki,Kd,prev_head_error,total_head_error)
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
def gps_goto(x,y,max_speed=40):
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
        if counter%3000==0 and int_margin(xc,yc,x,y)>120:
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
        f,prev_gps_error,total_gps_error=PID(dis,0,.1,.0003,.08,prev_gps_error,total_gps_error)
        if f>max_speed: f=max_speed
        run_drive_motors(f,0,0,True)
        print("Pos: (",xc,",",yc,"), HEAD: "+str(gps.heading()) +"Counter: "+str(counter)+"f: "+str(f))
        
        # wait(100, MSEC)
    print("arrived")    
#endregion

#other funcs here
#endregion 
#region ==================== MAIN PROGRAM ====================
initialize()

brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")

def autonomous():
    
    

    # AUTON

    # tongue_toggle_fn()
    # while timer.time(MSEC) < 3000:
    #         intake.spin(REVERSE, 100, PERCENT)
    #         run_drive_motors(80, 0, 0)   # forward
    #         wait(10, MSEC)

    # while timer.time(MSEC) < 1000:
    #             intake.spin(REVERSE, 100, PERCENT)
    #             run_drive_motors(80, 0, 0)   # forward
    #             wait(10, MSEC)

    # controller.screen.print("Auton Program Done.")

    # # screo the blue ones, then grab and spit out red

    # for i in range(5):  # repeat 5 times
    #     # back for 1 second
    #     timer.clear()
    #     while timer.time(MSEC) < 1000:
    #         intake.stop()
    #         run_drive_motors(-100, 0, 0)   # forward
    #         wait(10, MSEC)


    #     while timer.time(MSEC) < 1000:
    #         intake.spin(REVERSE, 100, PERCENT)
    #         run_drive_motors(80, 0, 0)   # forward
    #         wait(10, MSEC)

    # # makes angles unreliable
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
    print("s")

def autonomous_v2():
    initialize()
      
    #goto spot 
    gps_goto(-1235,1200)
    gps_gohead(270)
    
    #grab balls
    print("grab balls")
    intake_forward_toggle()
    tongue_toggle_fn()
    wait(100,MSEC)
    run_drive_motors(60,0,0)
    wait(1000,MSEC)
    print("Stoop moter")
    run_drive_motors(0,0,0)
    wait(1000,MSEC)
    
    #go to drop spot
    print("godrop")
    rev_drive_toggle_fn()
    print("greoooo")
    run_drive_motors(50,0,0)
    wait(50,MSEC)
    print("f2")
    # gps_goto(-1200,1200)
    # run_drive_motors(50,0,0)

    tongue_toggle_fn()
    print("grat") 
    gps_goto(-520,390)
    print("breep")  
    gps_gohead(135)
    run_drive_motors(50,0,0)
    wait(2000,MSEC)
    
    #drop balls
    print("drop")
    outake_forward_toggle()
    wait(5000,MSEC)

def autonomous_v3_red():
    initialize()
    
    #goto goal
    rev_drive_toggle_fn()
    gps_goto(-501,440)
    gps_gohead(135)
    run_drive_motors(15,0,0,True)
    wait(1500,MSEC)
    
    #score
    outake_forward_toggle(40)
    wait(4000,MSEC)
    outake_forward_toggle(40)
    
    #goto spot 
    rev_drive_toggle_fn()
    run_drive_motors(25,0,0,True)
    wait(4500,MSEC)
    
    gps_goto(-1240,1230,25)
    gps_gohead(270)
    
    #grab balls
    print("grab balls")
    intake_forward_toggle()
    tongue_toggle_fn()
    wait(100,MSEC)
    run_drive_motors(25,0,0)
    wait(3000,MSEC)
    print("Stoop moter")
    run_drive_motors(0,0,0)
    wait(1000,MSEC)
    stop_drive()
    wait(2000,MSEC)
def autonomous_v3_blue():
    initialize()
    
    #goto goal
    rev_drive_toggle_fn()
    gps_goto(525,-440)
    gps_gohead(315)
    run_drive_motors(15,0,0,True)
    wait(1500,MSEC)
    
    #score
    outake_forward_toggle(40)
    wait(4000,MSEC)
    outake_forward_toggle(40)
    
    #goto spot 
    rev_drive_toggle_fn()
    run_drive_motors(25,0,0,True)
    wait(4500,MSEC)
    
    gps_goto(1394,-1149,20)
    # gps_goto(1240,-1230,20)
    gps_gohead(90)
    
    #grab balls
    print("grab balls")
    intake_forward_toggle()
    tongue_toggle_fn()
    wait(100,MSEC)
    run_drive_motors(25,0,0)
    wait(3000,MSEC)
    print("Stoop moter")
    run_drive_motors(0,0,0)
    wait(1000,MSEC)
    stop_drive()
    wait(2000,MSEC)   
def user_control():
    global strafeToggle
    # gps_gohead(0)
    # wait(1000, MSEC)
    # gps_gohead(90)
    # wait(1000, MSEC)
    # gps_gohead(240)
    # wait(1000, MSEC)
    # gps_gohead(265)
    # wait(1000, MSEC)
    # gps_gohead(255)
    # wait(1000, MSEC)
    # gps_gohead(250)
    # wait(1000, MSEC)
    # gps_gohead(252)
    # wait(1000, MSEC)
    # gps_gohead(0)
    while True:
        xc=gps.x_position()
        yc=gps.y_position()
        if controller.buttonY.pressing(): strafeToggle=True
        else:strafeToggle=False
        
        x_drive_control()
        controller.screen.clear_screen()
        # x=gps.x_position()
        # y=gps.y_position()
        # head=gps.heading()
        # print(x,y,head)
        controller.screen.set_cursor(1, 1)
        controller.screen.print("Score" if reverseDriveToggle else "Gather")
        # controller.screen.set_cursor(2, 1)
        # controller.screen.print(head)
        
        
        # print("heading: "+str(get_gps_avg()))
        # print("int: "+str(int.heading()))
        #raw_drive_test()
        # initialize()
        # print_gps_status()
        print("Pos: (",xc,",",yc,"), HEAD: "+str(gps.heading()))
        # print(strafeToggle)
        wait(100, MSEC)  # Small delay to prevent CPU overload
    #endregion


# create competition instance
comp = Competition(user_control, autonomous_v3_blue)

# actions to do when the program starts
brain.screen.clear_screen()
#user_control()
# autonomous_v3()