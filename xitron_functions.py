import serial
import time

def xitron_establish_serial_connection(serial_port):
    xitron_serial = serial.Serial(port=serial_port, baudrate=115200,timeout=3,dsrdtr=True)
    # Check if the serial port is open
    if xitron_serial.is_open:
        print(f"Serial connection established on {xitron_serial.port}")
    else:
        print("Failed to open serial port.")

    return xitron_serial

def xitron_send_command(command_string,xitron_serial):
    xitron_serial.write(command_string.encode("ascii"))
    xitron_serial.write("READ?\n".encode("ascii"))
    received_string=xitron_serial.readline().decode()
    return received_string

# Configure the serial port for the XT2640
XT2640_PORT = '/dev/ttyUSB2'

try:
    xt_serial = serial.Serial(
        port=XT2640_PORT,
        baudrate=115200,       # Adjust to 115200 if your unit is configured that way
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1            # 1 second read timeout
    )

    if xt_serial.is_open:
        print(f"Connected to XT2640 on {XT2640_PORT}")
        
        # Send *IDN? command
        xt_serial.write(b'*IDN?\r')
        time.sleep(0.1)  # Wait for response

        response = xt_serial.read(128)  # Read response (increase buffer size if needed)
        print("XT2640 Response:", response.decode(errors='replace').strip())

        xt_serial.close()
    else:
        print(f"Failed to open port {XT2640_PORT}")

except serial.SerialException as e:
    print(f"Serial error: {e}")