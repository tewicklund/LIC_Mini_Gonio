import serial

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