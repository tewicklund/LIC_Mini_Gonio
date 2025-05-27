import serial

# Get a list of available ports
ports = serial.tools.list_ports.comports()

# Iterate and print port info
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}, HWID: {port.hwid}")