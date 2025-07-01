import serial.tools.list_ports
import time
from PCL_functions import *
from T10A_functions import *
from xitron_functions import *

PCL_port_found=False
t10a_port_found=False
xitron_port_found=False

# Get a list of available ports
COM_ports = serial.tools.list_ports.comports()

for COM_port in COM_ports:
    # Check if port is PCL
    if not PCL_port_found:
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
                PCL_port_found=True
                print(f"PCL found on {PCL_port}")

            else:
                print(f"PCL not found on {COM_port.device}")
            PCL_serial.close()
                
        except:
            print(f"PCL not found on {COM_port.device}")

    

    # Check if port is T10A
    if not t10a_port_found:
        try:
            T10A_serial = T10A_establish_serial_connection(COM_port.device)
            response=t10a_init(T10A_serial)
            print(response)
            if response != b'':
                t10a_port=COM_port.device
                t10a_port_found=True
                print(f"T10A found on {t10a_port}")
            else:
                print(f"T10A not found on {COM_port.device}")
            T10A_serial.close()
        
        except:
            print(f"T10A not found on {COM_port.device}")

    

    #Check if port is xitron
    if not xitron_port_found:
        try:
            xitron_serial=xitron_establish_serial_connection(COM_port.device)
            response=xitron_send_command("*IDN?\n",xitron_serial)
            print("XT2640 Response:", response)
            if response != b'':
                xitron_port=COM_port.device
                xitron_port_found=True
                print(f"Xitron found on {xitron_port}")
            else:
                print(f"Xitron not found on {COM_port.device}")
            xitron_serial.close()
        
        except:
            print(f"Xitron not found on {COM_port.device}")

print(f"PCL Port: {PCL_port}")
print(f"T10A Port: {t10a_port}")
print(f"Xitron Port: {xitron_port}")
