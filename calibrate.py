from run_test_function import *
from USB_functions import *

#serial port names
[PCL_port_name,T10A_port_name,xitron_serial_port_name]=get_port_names()

#establish serial comms
PCL_serial=PCL_establish_serial_connection(PCL_port_name)
t10a_serial=T10A_establish_serial_connection(T10A_port_name)
t10a_init(t10a_serial)

#turn on center light
PCL_turn_light_on(PCL_serial,3)

#move to center position
angle=90
angle_steps=int(angle/0.009)
PCL_home_motor(PCL_serial)
PCL_go_to_angle(PCL_serial,angle_steps)


while True:
    lx_value=t10a_get_lx_measurement(t10a_serial)
    lx_value_rounded=round(lx_value,2)
    print(f"Lux Value: {lx_value_rounded}")
    time.sleep(1)

