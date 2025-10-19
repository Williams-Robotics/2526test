# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       elenasore                                                    #
# 	Created:      10/19/2025, 3:17:13 PM                                       #
# 	Description:  V5 X-Drive Control                                           #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()
controller = Controller(PRIMARY)

# ==================== MOTOR CONFIGURATION ====================
# Configure your motor ports here
FRONT_LEFT_PORT = Ports.PORT10
FRONT_RIGHT_PORT = Ports.PORT20
BACK_LEFT_PORT = Ports.PORT1
BACK_RIGHT_PORT = Ports.PORT11

# Configure motor reverse settings (True = reversed, False = normal)
FRONT_LEFT_REVERSE = False
FRONT_RIGHT_REVERSE = True
BACK_LEFT_REVERSE = False
BACK_RIGHT_REVERSE = True

# ==================== MOTOR INITIALIZATION ====================
# Initialize motors with configured ports and reverse settings
front_left = Motor(FRONT_LEFT_PORT, GearSetting.RATIO_18_1, FRONT_LEFT_REVERSE)
front_right = Motor(FRONT_RIGHT_PORT, GearSetting.RATIO_18_1, FRONT_RIGHT_REVERSE)
back_left = Motor(BACK_LEFT_PORT, GearSetting.RATIO_18_1, BACK_LEFT_REVERSE)
back_right = Motor(BACK_RIGHT_PORT, GearSetting.RATIO_18_1, BACK_RIGHT_REVERSE)

# ==================== DRIVETRAIN FUNCTIONS ====================
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

# ==================== MAIN PROGRAM ====================
brain.screen.print("X-Drive Ready")
brain.screen.new_line()
brain.screen.print("Use controller to drive")

# Main control loop
while True:
    x_drive_control()
    wait(20, MSEC)  # Small delay to prevent CPU overload
