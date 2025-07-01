from run_test_function import *

#serial port names
PCL_port_name='/dev/ttyUSB1'
T10A_port_name='/dev/ttyUSB0'

#establish serial comms
PCL_serial=PCL_establish_serial_connection(PCL_port_name)
t10a_serial=T10A_establish_serial_connection(T10A_port_name)
t10a_init(t10a_serial)

#turn on center light
PCL_turn_light_on(PCL_serial,3)

#move to center position
angle=90
angle_steps=int(angle/0.009)
PCL_home_motor(PCL_serial)
PCL_go_to_angle(PCL_serial,angle_steps)

#wait 3 minutes for lamp to warm up
# print("Lamp warming up")
# for second in range(180):
#     print(180-second)
#     time.sleep(1)

while True:
    #dimming_voltage_value=get_voltage_from_arduino(arduino_serial)
    #print(f"Arduino Voltage: {dimming_voltage_value}")
    lx_value=t10a_get_lx_measurement(t10a_serial)
    lx_value_rounded=round(lx_value,2)
    print(f"Lux Value: {lx_value_rounded}")
    time.sleep(1)

