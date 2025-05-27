from functions import *

PCL_serial=PCL_establish_serial_connection('/dev/ttyUSB0')

PCL_get_encoder_angle(PCL_serial)