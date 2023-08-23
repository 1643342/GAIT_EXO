import time
import math
import numpy as np

import odrive
from odrive.enums import *

from matplotlib import pyplot as plt


odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

odrv0.axis0.motor.config.current_lim = 20
odrv0.axis0.controller.config.vel_limit = 10
odrv0.config.enable_brake_resistor = True
odrv0.config.brake_resistance = 2
odrv0.axis0.motor.config.pole_pairs = 20
odrv0.axis0.motor.config.torque_constant =.091
odrv0.axis0.motor.config.motor_type = 0
odrv0.axis0.encoder.config.cpr = 4000



# Start motor calibration
odrv0.clear_errors()
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
    
# Wait until the ODrive is finished calibrating
while AxisState(odrv0.axis0.current_state) != AxisState.IDLE:
    time.sleep(0.1)
    print('wait or else')
    calibration = True


if calibration == True:
    # Configure velocity control mode and enable the ramp input filter
	odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
	odrv0.axis0.controller.config.input_mode = INPUT_MODE_VEL_RAMP

# Set velocity ramp rate to 2 turn/s^2
	odrv0.axis0.controller.config.vel_ramp_rate = 2
	odrv0.axis0.controller.input_vel = 0

# Put ODrive into closed-loop velocity control mode
	odrv0.axis0.requested_state = AxisState_CLOSED_LOOP_CONTROL


	sample_ts = 0.01 # Sample velocity at 100Hz-ish
	sample_vel_array = []
	sample_time_array = []

	vel_ramp_max = 10
	timeout = 12 # It shouldn't take more than 12 seconds to complete the ramp up-down

	t0 = time.monotonic()
	odrv0.axis0.controller.input_vel = vel_ramp_max

while (t_now := time.monotonic() - t0) < timeout:
    vel = odrv0.axis0.pos_vel_mapper.vel
    
    
    if (odrv0.axis0.controller.vel_setpoint == odrv.axis0.controller.input_vel):
        if odrv0.axis0.controller.input_vel == vel_ramp_max:
            odrv0.axis0.controller.input_vel = 0
            print("Velocity ramp up complete!")
        else:
            print("Velocity ramp down complete!")
            odrv0.axis0.requested_state = AxisState.IDLE
            break
            
    
    sample_vel_array.append(vel)
    sample_time_array.append(t_now)
    
    time.sleep(sample_ts)
    
else: # Only reach here if the while loop timed out
    odrv0.axis0.requested_state = AxisState.IDLE
    print("Error! Timeout on reaching velocity target.")
    assert False
