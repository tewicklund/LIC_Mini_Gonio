import serial

# Open the serial port
ser = serial.Serial(
    port='/dev/ttyUSB0',  # or COMx on Windows
    baudrate=38400,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1  # seconds
)

# Send a known-good command (e.g., read inputs)
command = '@0VEP\r\n'
ser.write(command.encode())

# Read the response
response = ser.read(64)  # Adjust byte count as needed
print("Response:", response.decode(errors='ignore'))

ser.close()