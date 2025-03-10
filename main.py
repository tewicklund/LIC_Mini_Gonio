from functions import *

#set tungsten halogen lamp warm-up time
#warm_up_time_minutes=5
#warm_up_time_seconds=warm_up_time_minutes*60
warm_up_time_seconds=5

#get light voltage from user and check that it is in range
light_voltage_valid=False
while not light_voltage_valid:
    light_voltage_input=input("What voltage are you running the lamps at? (V) (0-24): ")
    try:
        light_voltage=float(light_voltage_input)
        if light_voltage>=0 and light_voltage<=24:
            light_voltage_valid=True
        else:
            print("Invalid light voltage, try again")
    except:
        print("Invalid light voltage, try again")
print(f"Lights running at {light_voltage} volts.")

#get number of angles btwn 0 and 180 to test at, for example a value of 3 would mean test at 0, 90, and 180
num_angles_valid=False
while not num_angles_valid:
    num_angles_input=input("How many angles will you test at? (2-180): ")
    try:
        num_angles=int(num_angles_input)
        if num_angles>=2 and num_angles<=180:
            num_angles_valid=True
        else:
            print("Invalid number of angles, try again")
    except:
        print("Invalid number of angles, try again")
print(f"Will test at {num_angles} angles.")

#get COM port for PCL from user
PCL_port_name_valid=False
while not PCL_port_name_valid:
    serial_port_list=get_serial_port_list()
    print("Serial port list: ",serial_port_list)
    PCL_port_name_input=input("Type name of PCL COM port (COM#): ")
    if PCL_port_name_input in serial_port_list:
        PCL_port_name_valid=True
        PCL_port_name=PCL_port_name_input
        print(f"Confirmed port {PCL_port_name}")
    else:
        print("Invalid port name, try again")


#get COM port for T10A from user
T10A_port_name_valid=False
while not T10A_port_name_valid:
    serial_port_list=get_serial_port_list()
    print("Serial port list: ",serial_port_list)
    T10A_port_name_input=input("Type name of T10A COM port (COM#): ")
    if T10A_port_name_input in serial_port_list:
        T10A_port_name_valid=True
        T10A_port_name=T10A_port_name_input
        print(f"Confirmed port {T10A_port_name}")
    else:
        print("Invalid port name, try again")


#get COM port for dimming_arduino from user
dimming_arduino_port_name_valid=False
while not dimming_arduino_port_name_valid:
    serial_port_list=get_serial_port_list()
    print("Serial port list: ",serial_port_list)
    dimming_arduino_port_name_input=input("Type name of dimming_arduino COM port (COM#): ")
    if dimming_arduino_port_name_input in serial_port_list:
        dimming_arduino_port_name_valid=True
        dimming_arduino_port_name=dimming_arduino_port_name_input
        print(f"Confirmed port {dimming_arduino_port_name}")
    else:
        print("Invalid port name, try again")

#get file name to store the logs, stored in local directory
log_file_name=input("Enter log file name (ex. mini_gonio_log.csv): ")
if log_file_name=='':
    log_file_name='mini_gonio_log.csv'


#run test
run_test(PCL_port_name,T10A_port_name,dimming_arduino_port_name,warm_up_time_seconds,num_angles,log_file_name)

