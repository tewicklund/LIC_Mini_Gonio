from xitron_functions import *

xitron_serial=xitron_establish_serial_connection('/dev/ttyUSB2')

response = xitron_send_command("*IDN?\n",xitron_serial)

print(response)