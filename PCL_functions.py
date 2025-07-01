import time
import serial

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
            #print(f"Serial connection established on {ser.port}")
            return ser
        else:
            #print("Failed to open serial port.")
            return None

    except serial.SerialException as e:
        #print(f"Error opening serial port: {e}")
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