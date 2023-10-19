%matplotlib inline

import time
import math
import numpy as np

import odrive
from odrive.enums import *

from matplotlib import pyplot as plt

# Start motor calibration
odrv.axis0.requested_state = AxisState.MOTOR_CALIBRATION

# Wait until the ODrive is finished calibrating
while AxisState(odrv.axis0.current_state) != AxisState.IDLE:
    time.sleep(0.1)
    
time.sleep(2)
    
# Make sure that the calibration procedure was successful
assert odrv.axis0.config.motor.phase_inductance_valid
assert odrv.axis0.config.motor.phase_resistance_valid
assert ProcedureResult(odrv.axis0.procedure_result) == ProcedureResult.SUCCESS
assert AxisError(odrv.axis0.active_errors) == AxisError.NONE

# Finally, save configuration 
try: odrv.save_configuration()
except: pass 
odrv = odrive.find_any()  # Blocks until ODrive comes back online
time.sleep(2) # Additional wait time for ODrive to initialize the inverter

bus_voltage = odrv.vbus_voltage
print(f"ODrive bus voltage: {bus_voltage:.3f}V")

n_samples = 300 # Number of samples
t_sample = 0.01 # Time to wait between each sample

vbus_voltages = []
timestamps = []

t0 = time.monotonic()

for i in range(n_samples):
    v_bus = odrv.vbus_voltage
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