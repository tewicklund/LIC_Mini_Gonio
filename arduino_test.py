from arduino_functions import *

ser=dimming_arduino_establish_serial_connection('/dev/ttyUSB2')

while True:
    voltage=get_voltage_from_arduino(ser)
    print(voltage)
    time.sleep(1)