import serial
import time

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
        value = int(response_str)
    except ValueError:
        raise ValueError(f"Received data is not a valid int: {response_str}")
    
    return value
