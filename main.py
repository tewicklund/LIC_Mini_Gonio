from parameters_from_user_functions import *
from run_test_function import *
from USB_functions import *
from log_file_naming_function import *

demo_mode=False

log_file_name=generate_unique_csv_filename()

#COM port names: plug in PCL first, then T10A, then arduino
[PCL_port_name,T10A_port_name,xitron_serial_port_name]=get_port_names()


#run test
run_test(PCL_port_name,T10A_port_name,xitron_serial_port_name,log_file_name,demo_mode)