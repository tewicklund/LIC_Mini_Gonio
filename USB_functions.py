import serial.tools.list_ports
import time

# Get a list of available ports
COM_ports = serial.tools.list_ports.comports()

for COM_port in COM_ports:
    # Check if port is PCL
    try:
        #Open PCL serial port
        PCL_serial = serial.Serial(
            port=COM_port.device,  # or COMx on Windows
            baudrate=38400,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1  # seconds
        )
        identify_command="@0$\r"
        PCL_serial.write(identify_command.encode())

        # Read the response
        response = PCL_serial.read(64)  # Adjust byte count as needed
        time.sleep(0.1)
        print("Response:", response.decode())

        print(f"PCL found on {COM_port.device}")

    except:
        print(f"PCL not found on {COM_port.device}")
