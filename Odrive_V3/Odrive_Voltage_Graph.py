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



n_samples = 300 # Number of samples
t_sample = 0.01 # Time to wait between each sample

vbus_voltages = []
timestamps = []

t0 = time.monotonic()

for i in range(n_samples):
    v_bus = odrv0.vbus_voltage
    t_meas = time.monotonic()-t0
    timestamps.append(t_meas)
    vbus_voltages.append(v_bus)    
    time.sleep(t_sample)

plt.plot(timestamps, vbus_voltages)
plt.xlabel("Time (s)")
plt.ylabel("ODrive VBus Voltage (V)")
plt.ylim([min(vbus_voltages)-1, max(vbus_voltages)+1])
plt.title("Continuous sampling of ODrive vbus_voltage property")
plt.show()
