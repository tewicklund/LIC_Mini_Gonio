from functions import *


# variables set by the user
warm_up_time=5     # warm up time of each lamp in seconds
num_angles=9        # number of angles to test at, linspace from 0 to 180 degrees
output_csv_location="test_output.csv"
PCL_serial_port='COM11'
t10a_serial_port='COM12'
arduino_serial_port='COM19'


# run the test
run_test(PCL_serial_port,t10a_serial_port,arduino_serial_port,warm_up_time,num_angles,output_csv_location)