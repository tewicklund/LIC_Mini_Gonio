from parameters_from_user_functions import *
from run_test_function import *


warm_up_time_seconds=180

demo_mode=get_demo_mode()

if not demo_mode:
    user_input_lux_bool=get_user_lux_mode()
    light_voltage=get_light_voltage()
    num_angles=get_num_angles()
    log_file_name=get_log_file_name()
else:
    user_input_lux_bool=False
    light_voltage=12
    num_angles=2
    log_file_name='mini_gonio_demo_log.csv'

#COM port names: plug in PCL first, then T10A, then arduino
PCL_port_name='/dev/ttyUSB1'
T10A_port_name='/dev/ttyUSB0'
#dimming_arduino_port_name='/dev/ttyACM0'
xitron_serial_port_name='/dev/ttyUSB2'



#run test
run_test(light_voltage,PCL_port_name,T10A_port_name,xitron_serial_port_name,warm_up_time_seconds,num_angles,log_file_name,user_input_lux_bool,demo_mode)

