from arduino_functions import *

dimming_arduino_port_name='/dev/ttyACM0'

ser=dimming_arduino_establish_serial_connection(dimming_arduino_port_name)


while True:
    voltage=get_voltage_from_arduino(ser)
    print(voltage)
    time.sleep(1)