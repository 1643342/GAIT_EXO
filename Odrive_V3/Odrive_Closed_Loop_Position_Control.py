import time
import math
import numpy as np

import odrive
from odrive.enums import *

from matplotlib import pyplot as plt


odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

odrv0.axis0.motor.config.current_lim = 20
odrv0.axis0.controller.config.vel_limit = 6
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
    print('wait for tune value to be set')
    time.sleep(1)
    odrv0.axis0.controller.config.pos_gain = 20.0
    odrv0.axis0.controller.config.vel_gain = 0.21
    odrv0.axis0.controller.config.vel_integrator_gain = 0
    time.sleep(1)
    print('now the fun starts')
    calibration = True


if calibration == True:
    print('now the fun starts')
    odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
    odrv0.axis0.controller.input_pos = 250
    
