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


# ===================================
# BRAIN AND CONTROLLER SETUP
# ===================================
brain = Brain()  # Should be defined by default
controller = Controller(PRIMARY)
import math

# ===================================
# MOTOR CONFIGURATION
# ===================================
FRONT_LEFT_PORT = Ports.PORT10
FRONT_RIGHT_PORT = Ports.PORT20
BACK_LEFT_PORT = Ports.PORT1
BACK_RIGHT_PORT = Ports.PORT11

FRONT_LEFT_REVERSE = False
FRONT_RIGHT_REVERSE = True
BACK_LEFT_REVERSE = False
BACK_RIGHT_REVERSE = True

# ===================================
# SENSOR CONFIGURATION
# ===================================
AI_PORT = Ports.PORT13
D_PORT = Ports.PORT15
GPS_PORT = Ports.PORT9
INT_PORT = Ports.PORT21

# ===================================
# MOTOR INITIALIZATION
# ===================================
front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)
front_right = Motor(FRONT_RIGHT_PORT, GearSetting.RATIO_18_1, FRONT_RIGHT_REVERSE)
back_left = Motor(BACK_LEFT_PORT, GearSetting.RATIO_18_1, BACK_LEFT_REVERSE)
back_right = Motor(BACK_RIGHT_PORT, GearSetting.RATIO_18_1, BACK_RIGHT_REVERSE)

gps = Gps(GPS_PORT, 0, 0)

# ===================================
# SENSOR INITIALIZATION
# ===================================
# AI Vision
class GameElementsPushBack:
    BLUE_BLOCK = 0
    RED_BLOCK = 1

ai__BBLUE = Colordesc(1, 32, 154, 226, 10, 0.2)
ai__BRED = Colordesc(2, 231, 42, 92, 10, 0.2)

distance = Distance(D_PORT)
gps = Gps(GPS_PORT, 0, 0)  # GPS offset from center
ai = AiVision(AI_PORT, ai__BBLUE, ai__BRED, AiVision.ALL_AIOBJS)
int = Inertial(INT_PORT)
timer = Timer()

# ===================================
# INTAKE MOTOR FUNCTIONS
# ===================================
intake_left = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
intake_right = Motor(Ports.PORT16, GearSetting.RATIO_18_1, True)
spinny_thing = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)

intake_forward = False
intake_reverse = False
spin_toggle = False

def intake_forward_toggle():
    global intake_forward, intake_reverse
    if intake_forward:
        intake_left.stop(HOLD)
        intake_right.stop(HOLD)
    else:
        if intake_reverse:
            intake_reverse = False
            intake_left.stop(HOLD)
            intake_right.stop(HOLD)
        intake_left.spin(FORWARD, 100, PERCENT)
        intake_right.spin(FORWARD, 100, PERCENT)
    intake_forward = not intake_forward

def intake_reverse_toggle():
    global intake_reverse, intake_forward
    if intake_reverse:
        intake_left.stop(HOLD)
        intake_right.stop(HOLD)
    else:
        if intake_forward:
            intake_forward = False
            intake_left.stop(HOLD)
            intake_right.stop(HOLD)
        intake_left.spin(REVERSE, 100, PERCENT)
        intake_right.spin(REVERSE, 100, PERCENT)
    intake_reverse = not intake_reverse

def spin_toggle_fn():
    global spin_toggle
    if spin_toggle:
        spinny_thing.stop()
    else:
        spinny_thing.spin(FORWARD, 100, PERCENT)
    spin_toggle = not spin_toggle

controller.buttonA.pressed(spin_toggle_fn)
controller.buttonL1.pressed(intake_forward_toggle)
controller.buttonL2.pressed(intake_reverse_toggle)

# ===================================
# DRIVETRAIN FUNCTIONS
# ===================================
goal_head = 999
last_head = 999
getH = False
prev_head_error = 0
total_head_error = 0

def x_drive_control():
    """Control X-drive using controller joysticks."""
    forward = controller.axis3.position() / 2  # Left stick Y-axis
    strafe = 0  # Left stick X-axis disabled
    turn = controller.axis1.position() / 2  # Right stick X-axis
    run_drive_motors(forward, strafe, turn)

def run_drive_motors(forward, strafe, turn):
    turn = newgps_heading_control(turn)
    # X-drive kinematics
    front_left_speed = forward + strafe + turn
    front_right_speed = forward - strafe - turn
    back_left_speed = forward - strafe + turn
    back_right_speed = forward + strafe - turn
    front_left.spin(FORWARD, front_left_speed, PERCENT)
    front_right.spin(FORWARD, front_right_speed, PERCENT)
    back_left.spin(FORWARD, back_left_speed, PERCENT)
    back_right.spin(FORWARD, back_right_speed, PERCENT)

def newgps_heading_control(turn):
    global goal_head, getH, prev_head_error, total_head_error
    # When turning
    if turn != 0:
        getH = False
        prev_head_error = 0
        total_head_error = 0
        return turn
    # When done turning, capture heading
    elif turn == 0 and not getH:
        if abs(gps.gyro_rate(AxisType.XAXIS)) < 1:
            goal_head = gps.orientation(OrientationType.YAW)
            getH = True
            print("got: " + str(gps.gyro_rate(AxisType.XAXIS)))
        return turn
    # Heading correction
    elif turn == 0 and getH:
        chead = gps.orientation(OrientationType.YAW)
        heading_error = goal_head - chead
        if heading_error > 180: heading_error -= 360
        elif heading_error < -180: heading_error += 360
        turn, prev_head_error, total_head_error = PID(0, -heading_error, .8, 0, 0.15, prev_head_error, total_head_error)
        turn = max(min(turn, 50), -50)
        print("chead: " + str(chead) + " - goal: " + str(goal_head))
        return turn
    else:
        print("Unexpected Issue With Heading Control")
        return turn

def stop_drive():
    front_left.stop()
    front_right.stop()
    back_left.stop()
    back_right.stop()

def raw_drive_test():
    f = controller.axis3.position()
    front_left.spin(FORWARD, f, PERCENT)
    front_right.spin(FORWARD, f, PERCENT)
    back_left.spin(FORWARD, f, PERCENT)
    back_right.spin(FORWARD, f, PERCENT)

# ===================================
# SENSOR / PID FUNCTIONS
# ===================================
def PID(desired_state, current_state, Kp, Ki, Kd, prev_error, total_error):
    error = desired_state - current_state
    proportional = Kp * error
    total_error += error
    integral = Ki * total_error
    derivative = Kd * (error - prev_error)
    prev_error = error
    PID_result = proportional + integral + derivative
    return PID_result, prev_error, total_error

def initialize():
    gps.set_origin(0, 5, MM)
    gpsh = gps.heading()
    int.calibrate()
    int.set_heading(gpsh)
    wait(1500, MSEC)

def bool_margin(x, y, tx, ty):
    error = 50
    mx = abs(x - tx)
    my = abs(y - ty)
    return mx <= error and my <= error

def int_margin(x, y, tx, ty):
    mx = abs(x - tx)
    my = abs(y - ty)
    return math.sqrt(mx**2 + my**2)

def gps_gohead(heading):
    arrived = False
    c1 = False
    turn = 0
    while not arrived:
        if gps.quality() < 90:
            continue
        head = gps.heading()
        diff = heading - head
        if diff < -180: diff += 360
        elif diff > 180: diff -= 360
        if abs(diff) < 1:
            stop_drive()
            if c1:
                arrived = True
            c1 = True
            continue
        else:
            c1 = False
        # Set turn speed based on diff
        if 0 < diff < 180:
            if diff > 150: turn = 50
            elif diff > 120: turn = 40
            elif diff > 90: turn = 20
            elif diff > 60: turn = 20
            elif diff > 30: turn = 10
            elif diff > 15: turn = 5
            else: turn = 3
        else:
            if diff < -150: turn = -50
            elif diff < -120: turn = -40
            elif diff < -90: turn = -20
            elif diff < -60: turn = -20
            elif diff < -30: turn = -10
            elif diff < -15: turn = -5
            else: turn = -3
        run_drive_motors(0, 0, turn)
        wait(5, MSEC)

def gps_goto(x, y):
    arrived = False
    goalx = x
    goaly = y
    counter = 2000
    prev_gps_error = 0
    total_gps_error = 0
    while not arrived:
        if gps.quality() < 100:
            stop_drive()
            print("NO GPS")
            continue
        xc = gps.x_position()
        yc = gps.y_position()
        if bool_margin(xc, yc, x, y):
            arrived = True
            stop_drive()
            continue
        if counter % 2000 == 0 and int_margin(xc, yc, x, y) > 150:
            counter = 0
            mx = x - xc
            my = y - yc
            angle = math.degrees(math.atan2(mx, my))
            gps_gohead(angle)
        dis = int_margin(xc, yc, x, y)
        f, prev_gps_error, total_gps_error = PID(dis, 0, .1, .005, .01, prev_gps_error, total_gps_error)
        f = min(f, 50)
        run_drive_motors(f, 0, 0)
        counter += 1

# ===================================
# MAIN PROGRAM
# ===================================
initialize()
brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")

# Example GPS Moves
# gps_goto(-800, -100)
# wait(1000, MSEC)
# gps_goto(500, 500)

gps_goto(365, 440)
wait(3000, MSEC)
gps_goto(440, 417)
xc = gps.x_position()
yc = gps.y_position()

while True:
    # x_drive_control()
    # raw_drive_test()
    print("Pos: (", xc, ",", yc, "), HEAD: " + str(gps.heading()))
    wait(100, MSEC)
