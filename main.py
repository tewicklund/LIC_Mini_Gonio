from functions import *

#set tungsten halogen lamp warm-up time
#warm_up_time_minutes=5
#warm_up_time_seconds=warm_up_time_minutes*60
warm_up_time_seconds=5

user_input_bool=False

demo_mode=True

if not demo_mode:
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

    #get file name to store the logs, stored in local directory
    log_file_name=input("Enter log file name (ex. mini_gonio_log.csv): ")
    if log_file_name=='':
        log_file_name='mini_gonio_log.csv'
else:
    light_voltage=12
    num_angles=2
    log_file_name='mini_gonio_demo_log.csv'

#COM port names: plug in PCL first, then T10A, then arduino
PCL_port_name='/dev/ttyUSB0'
T10A_port_name='/dev/ttyUSB1'
dimming_arduino_port_name='/dev/ttyUSB2'


#run test
run_test(light_voltage,PCL_port_name,T10A_port_name,dimming_arduino_port_name,warm_up_time_seconds,num_angles,log_file_name,user_input_bool,demo_mode)

