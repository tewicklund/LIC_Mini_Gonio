import serial
import time
import numpy as np
import serial.tools.list_ports



#dimming arduino functions-------------------------------------------------------------------------------------
def dimming_arduino_establish_serial_connection(com_port):
    try:
        # Set up the serial connection
        ser = serial.Serial(
            port=com_port,           # Serial port
            baudrate=115200,        # Baud rate
        )

        # Check if the serial port is open
        if ser.is_open:
            print(f"Serial connection established on {ser.port}")
        else:
            print("Failed to open serial port.")

        time.sleep(2)
        
        return ser

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def get_voltage_from_arduino(ser):
    # Send the character 'v'
    ser.write(b'v')
    
    # Read the response, expecting a newline-terminated string
    response = ser.readline()
    
    if not response:
        raise TimeoutError("No response received from the Arduino within the timeout period.")
    
    # Decode and clean the response
    response_str = response.decode('utf-8').strip()
    try:
        value = float(response_str)
    except ValueError:
        raise ValueError(f"Received data is not a valid float: {response_str}")
    
    return value



#PCL functions-------------------------------------------------------------------------------------
def PCL_establish_serial_connection(com_port):
    try:
        # Set up the serial connection
        ser = serial.Serial(
            port=com_port,           # Serial port
            baudrate=38400,        # Baud rate
            bytesize=serial.EIGHTBITS,  # Data bits
            parity=serial.PARITY_NONE,  # No parity
            stopbits=serial.STOPBITS_ONE,  # Stop bit
            xonxoff=True,          # Xon/Xoff flow control
            timeout=1              # Timeout for read
        )

        # Check if the serial port is open
        if ser.is_open:
            print(f"Serial connection established on {ser.port}")
        else:
            print("Failed to open serial port.")

        return ser

    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

def PCL_send_command_with_response(serial_object,command_string):
    command="@0X"+command_string+"\r\n"
    serial_object.write(command.encode())
    time.sleep(0.1)

    # Read the response
    response = serial_object.read(64)  # Adjust byte count as needed
    response_string=response.decode(errors='ignore')
    #print("Response:", response.decode(errors='ignore'))
    return response_string

def PCL_send_command_no_response(serial_object,command_string):
    command="@0X"+command_string+"\r\n"
    serial_object.write(command.encode())
    time.sleep(0.1)


def PCL_home_motor(serial_object):
    
    # set direction of travel toward the home switch
    PCL_send_command_no_response(serial_object,'-')
    time.sleep(0.1)
    PCL_send_command_no_response(serial_object,'H1')


    # wait till the motor is finished homing, check back every second
    homing_complete=False
    while not homing_complete:
        motor_busy_string=PCL_send_command_with_response(serial_object,'VF')
        #print(repr(motor_busy_string))
        if motor_busy_string=='0\r':
            homing_complete=True
        else:
            homing_complete=False
        time.sleep(1)
    

    # set the encoder and absolute positions to zero
    PCL_send_command_no_response(serial_object,'ET')
    PCL_send_command_no_response(serial_object,'Z0')

    # enable and set encoder autocorrect parameters
    PCL_send_command_no_response(serial_object,'EA1')
    PCL_send_command_no_response(serial_object,'ED1000')
    PCL_send_command_no_response(serial_object,'EM1')
    PCL_send_command_no_response(serial_object,'ER4')
    PCL_send_command_no_response(serial_object,'EW10')
    

def PCL_get_encoder_angle(serial_object):
    encoder_angle_string=PCL_send_command_with_response(serial_object,'VEP')
    tries=0
    while tries<10:
        try:
            encoder_angle_string=PCL_send_command_with_response(serial_object,'VEP')
            return int(encoder_angle_string)
        except:
            print("retrying encoder angle fetch")
            tries+=1
    return 0

def PCL_go_to_angle(serial_object, angle_steps):
    command_string='P'+str(angle_steps)
    PCL_send_command_no_response(serial_object,command_string)
    PCL_send_command_no_response(serial_object,'G')

    # wait till the motor is finished moving, check back every second
    moving_complete=False
    while not moving_complete:
        motor_busy_string=PCL_send_command_with_response(serial_object,'VF')
        if motor_busy_string=='0\r':
            moving_complete=True
        else:
            moving_complete=False
        #print(get_encoder_angle(serial_object))
        time.sleep(1)

def PCL_set_motor_speed(serial_object, max_speed, base_speed):
    command_string='M'+str(max_speed)
    PCL_send_command_no_response(serial_object,command_string)
    command_string='B'+str(base_speed)
    PCL_send_command_no_response(serial_object,command_string)
    time.sleep(0.1)

def PCL_turn_light_on(serial_object,light_number):
    if (light_number>=1 or light_number<=5):
        light_byte_value=pow(2,light_number)
    PCL_send_command_no_response(serial_object,'OR'+str(light_byte_value))

def PCL_turn_lights_off(serial_object):
    PCL_send_command_no_response(serial_object,'OR0')



#T10A functions-------------------------------------------------------------------------------------
def T10A_establish_serial_connection(port):
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    ser.setRTS(False)
    ser.setDTR(False)
    return ser

def t10a_translate_response(response):
    # Check for error information
    # print("Checking for error information...")
    error_code = response[6]  # Indexing starts from 0 in Python, so 7th position is index 6
    if error_code == 32:  # space
        #print("Normal Operation: no errors detected")
        pass
    elif error_code == 49:  # 1
        print("Error: Receptor head power is switched off")
    elif error_code == 50:  # 2
        print("Error: EEPROM error 1")
    elif error_code == 51:  # 3
        print("Error: EEPROM error 2")
    elif error_code == 53:  # 5
        print("Error: Measurement value over error")
    elif error_code == 55:  # 7
        print("Normal Operation: no errors detected")

    # Figure out measurement range
    range_code = response[7]
    # print("\nChecking measurement range...")
    # if range_code == 49:  # 1
    #     print("Range 0.00 to 29.99 lx")
    # elif range_code == 50:  # 2
    #     print("Range 0.0 to 299.9 lx")
    # elif range_code == 51:  # 3
    #     print("Range 0 to 2,999 lx")
    # elif range_code == 52:  # 4
    #     print("Range 00 to 29,990 lx")
    # elif range_code == 53:  # 5
    #     print("Range 000 to 299,900 lx")

    # Format the measurement data
    sym = response[9]  # find the +, -, or =
    if sym == 43:  # +
        flag = 1
    elif sym == 45:  # -
        flag = -1
    elif sym == 61:  # = (means +/-)
        flag = 1

    # Handle potential leading space in the data
    if response[10] == 32:  # if the data starts with a space
        measurement_str = ''.join(chr(response[i]) for i in range(11, 15) if response[i] != 32)
        measurement = int(measurement_str)
    else:  # it's just a normal number
        measurement_str = ''.join(chr(response[i]) for i in range(10, 14))
        measurement = int(measurement_str)

    # Handle the exponent
    exponent_code = response[14]
    exponent_number=int(chr(exponent_code))-4
    exponent=pow(10,exponent_number)
    

    # Calculate the final measurement
    measurement = measurement * exponent * flag
    #print(measurement,exponent,flag)
    return measurement

def t10a_bcc_calc(km_head, command, param):
    # Concatenate the inputs
    input_str = km_head + command + param
    
    # Convert each character to binary and store in a list
    bin_input = []
    for char in input_str:
        # Convert the character to its ASCII value, then to binary, and ensure it's 8 bits long
        bin_char = bin(ord(char))[2:].zfill(8)
        bin_input.append([int(bit) for bit in bin_char])
    
    # Add the ETX (End of Text) binary value [00000011]
    etx = [0, 0, 0, 0, 0, 0, 1, 1]
    bin_input.append(etx)
    
    # Sum the columns and take modulo 2 (sum each column, if odd -> 1, if even -> 0)
    p = [sum(col) % 2 for col in zip(*bin_input)]
    
    # Convert binary list to a decimal value
    p_decimal = int("".join(map(str, p)), 2)
    
    # Convert decimal to hexadecimal
    bcc = format(p_decimal, '02X')  # Format as 2-digit hexadecimal

    return bcc

def t10a_send_command(ser, head, command, params):
    bcc = t10a_bcc_calc(head, command, params)
    full_command = f"\x02{head}{command}{params}\x03{bcc}\r\n"
    encoded_command=full_command.encode()
    ser.write(encoded_command)
    raw_data=[ord(char) for char in full_command]
    #print(raw_data)
    time.sleep(0.5)
    response = ser.read(ser.in_waiting)#.decode()
    return response

def t10a_get_fcd_measurement(serial_object):
    head = '00'
    command = '10'
    params = '0200'
    response = t10a_send_command(serial_object, head, command, params)
    translated_response=t10a_translate_response(response)
    reading_lx=float(translated_response)
    reading_fcd=round(reading_lx/10.7639,2)
    return reading_fcd

def t10a_get_lx_measurement(serial_object):
    head = '00'
    command = '10'
    params = '0200'
    response = t10a_send_command(serial_object, head, command, params)
    translated_response=t10a_translate_response(response)
    reading_lx=float(translated_response)
    #reading_fcd=round(reading_lx/10.7639,2)
    return reading_lx

def t10a_init(serial_object):
    head = '00'  # Receptor head number
    command = '54'
    params = '1   '
    response = t10a_send_command(serial_object, head, command, params)
    print("PC connection mode response:", response.decode())


def get_uut_lx_value_from_user():
    #get number of angles btwn 0 and 180 to test at, for example a value of 3 would mean test at 0, 90, and 180
    uut_lux_value_valid=False
    while not uut_lux_value_valid:
        uut_lux_value_input=input("Enter UUT lux value integer: ")
        try:
            uut_lux_value=int(uut_lux_value_input)
            if uut_lux_value>=0:
                uut_lux_value_valid=True
            else:
                print("Invalid number of angles, try again")
        except:
            print("Invalid number of angles, try again")
    return uut_lux_value
    


#misc functions-------------------------------------------------------------------------------------
def get_serial_port_list():
    ports = serial.tools.list_ports.comports()
    com_ports = [port.device for port in ports]
    return com_ports

def get_detailed_serial_ports_list():
    # Get a list of available ports
    ports = serial.tools.list_ports.comports()

    # Iterate and print port info
    for port in ports:
        print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")

def run_test(light_voltage,PCL_serial_port,t10a_serial_port,arduino_serial_port,warm_up_time,num_angles,output_csv_location,user_input_lux_bool,demo_mode):

    # start serial connection
    PCL_serial=PCL_establish_serial_connection(PCL_serial_port)
    t10a_serial=T10A_establish_serial_connection(t10a_serial_port)
    arduino_serial=dimming_arduino_establish_serial_connection(arduino_serial_port)
    t10a_init(t10a_serial)


    # setup lists used during test
    angles=np.linspace(0,180,num_angles,endpoint=True,dtype=int)
    lights=[1,2,3,4,5]

    # record ambient light reading
    PCL_turn_lights_off(PCL_serial)
    lx_value=t10a_get_lx_measurement(t10a_serial)


    # format output file with ambient light and column labels
    f=open(output_csv_location,"w")
    f.write('Ambient Lux: '+str(lx_value)+'\n')
    f.write('Voltage: '+str(light_voltage)+'\n')
    f.write('Target Angle,Encoder Reading,Lux Value,Dimming Voltage,UUT Lux Value\n')
    f.close()

    #set motor base speed and max speed
    if demo_mode:
        PCL_set_motor_speed(PCL_serial,1500,250)
    else:
        PCL_set_motor_speed(PCL_serial,750,250)


    # run test for each light and each angle
    for light in lights:
        PCL_turn_light_on(PCL_serial,light)
        PCL_home_motor(PCL_serial)
        if not demo_mode:
            time.sleep(warm_up_time)

        f=open(output_csv_location,"a")
        f.write("Light "+str(light)+'\n')
        f.close()

        for angle in angles:
            angle_steps=int(angle/0.009)
            PCL_go_to_angle(PCL_serial,angle_steps)
            if not demo_mode:
                time.sleep(5) #5 seconds for settling, letting the dimming wires adjust to the new light position
            lx_value=t10a_get_lx_measurement(t10a_serial)
            lx_value_rounded=round(lx_value,2)
            encoder_value=PCL_get_encoder_angle(PCL_serial)
            dimming_voltage_value=get_voltage_from_arduino(arduino_serial)
            if user_input_lux_bool:
                uut_lx_value=get_uut_lx_value_from_user()
            else:
                uut_lx_value='0'
            # put code here to get the reading from the UUT's daylight sensor
            f=open(output_csv_location,"a")
            f.write(str(angle)+','+str(encoder_value)+','+str(lx_value_rounded)+','+str(dimming_voltage_value)+','+str(uut_lx_value)+'\n')
            f.close()
        
        f=open(output_csv_location,"a")
        f.write('\n')
        f.close()


    PCL_turn_lights_off(PCL_serial)