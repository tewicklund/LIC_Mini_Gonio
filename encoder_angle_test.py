from functions import *

PCL_serial=PCL_establish_serial_connection('/dev/ttyUSB0')

PCL_send_other_command(PCL_serial,'VEP')