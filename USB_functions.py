import serial.tools.list_ports
import time
from PCL_functions import *
from T10A_functions import *

# Get a list of available ports
COM_ports = serial.tools.list_ports.comports()

for COM_port in COM_ports:
    # Check if port is PCL
    try:
        #Open PCL serial port
        PCL_serial = PCL_establish_serial_connection(COM_port.device)
        identify_command="@0$\r"
        PCL_serial.write(identify_command.encode())

        # Read the response
        response = PCL_serial.read(64)  # Adjust byte count as needed
        time.sleep(0.1)
        print("Raw response:", response)

        #If the response is not blank, the device is PCL
        if response != b'':
            PCL_port=COM_port.device
            print(f"PCL found on {PCL_port}")
        else:
            print(f"PCL not found on {COM_port.device}")
            
    except:
        print(f"PCL not found on {COM_port.device}")

    PCL_serial.close()

    # Check if port is T10A
    try:
        T10A_serial = T10A_establish_serial_connection(COM_port.device)
        response=t10a_init(COM_port.device)
        print(response)
        print(f"T10A found on {COM_port.device}")
    
    except:
        print(f"T10A not found on {COM_port.device}")

    T10A_serial.close()
