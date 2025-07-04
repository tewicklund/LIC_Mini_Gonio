import serial
import time

def xitron_establish_serial_connection(serial_port):
    xitron_serial = serial.Serial(
        port=serial_port,
        baudrate=115200,       # Adjust to 115200 if your unit is configured that way
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        timeout=1            # 1 second read timeout
    )
    # Check if the serial port is open
    if xitron_serial.is_open:
        #print(f"Serial connection established on {xitron_serial.port}")
        return xitron_serial
    else:
        #print("Failed to open serial port.")
        return None


def xitron_send_command(command_string,xitron_serial):
    xitron_serial.write(command_string.encode("ascii"))
    time.sleep(0.1)
    xitron_serial.write("READ?\n".encode("ascii"))
    time.sleep(0.1)
    received_string=xitron_serial.readline()#.decode()
    return received_string

# Configure the serial port for the XT2640
# XT2640_PORT = '/dev/ttyUSB2'

# try:
#     xt_serial = serial.Serial(
#         port=XT2640_PORT,
#         baudrate=115200,       # Adjust to 115200 if your unit is configured that way
#         bytesize=serial.EIGHTBITS,
#         parity=serial.PARITY_NONE,
#         stopbits=serial.STOPBITS_ONE,
#         timeout=1            # 1 second read timeout
#     )

#     response=xitron_send_command("*IDN?\n",xt_serial)
#     print(response)

# except serial.SerialException as e:
#     print(f"Serial error: {e}")