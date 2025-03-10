import time
import serial

# Open the serial port
ser = serial.Serial(port='COM19', baudrate=115200, timeout=1)
time.sleep(2)  # Allow the Arduino time to reset

def send_v_and_get_value(ser):
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

# Example usage
try:
    result = send_v_and_get_value(ser)
    print("Received float:", result)
except Exception as e:
    print("Error:", e)
