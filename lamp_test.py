from parameters_from_user_functions import *
from run_test_function import *

PCL_port_name='/dev/ttyUSB1'
PCL_serial=PCL_establish_serial_connection(PCL_port_name)

try:
    while True:
        for i in range(1,6):
            print(f"testing light {i}")
            PCL_turn_light_on(PCL_serial,i)
            time.sleep(1)
except:
    PCL_turn_lights_off(PCL_serial)