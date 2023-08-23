import time
import math
import numpy as np

import odrive
from odrive.enums import *




odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))

