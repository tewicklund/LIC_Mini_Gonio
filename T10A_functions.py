import time
import serial

def T10A_establish_serial_connection(port):
    ser = serial.Serial(
        port=port,
        baudrate=9600,
        bytesize=serial.SEVENBITS,
        parity=serial.PARITY_EVEN,
        stopbits=serial.STOPBITS_ONE,
        timeout=1
    )
    ser.setRTS(False)
    ser.setDTR(False)
    return ser

def t10a_translate_response(response):
    # Check for error information
    # print("Checking for error information...")
    error_code = response[6]  # Indexing starts from 0 in Python, so 7th position is index 6
    if error_code == 32:  # space
        #print("Normal Operation: no errors detected")
        pass
    elif error_code == 49:  # 1
        print("Error: Receptor head power is switched off")
    elif error_code == 50:  # 2
        print("Error: EEPROM error 1")
    elif error_code == 51:  # 3
        print("Error: EEPROM error 2")
    elif error_code == 53:  # 5
        print("Error: Measurement value over error")
    elif error_code == 55:  # 7
        #print("Normal Operation: no errors detected")
        pass

    # Figure out measurement range
    range_code = response[7]
    # print("\nChecking measurement range...")
    # if range_code == 49:  # 1
    #     print("Range 0.00 to 29.99 lx")
    # elif range_code == 50:  # 2
    #     print("Range 0.0 to 299.9 lx")
    # elif range_code == 51:  # 3
    #     print("Range 0 to 2,999 lx")
    # elif range_code == 52:  # 4
    #     print("Range 00 to 29,990 lx")
    # elif range_code == 53:  # 5
    #     print("Range 000 to 299,900 lx")

    # Format the measurement data
    sym = response[9]  # find the +, -, or =
    if sym == 43:  # +
        flag = 1
    elif sym == 45:  # -
        flag = -1
    elif sym == 61:  # = (means +/-)
        flag = 1

    # Handle potential leading space in the data
    if response[10] == 32:  # if the data starts with a space
        measurement_str = ''.join(chr(response[i]) for i in range(11, 14) if response[i] != 32)
        measurement = int(measurement_str)
    else:  # it's just a normal number
        measurement_str = ''.join(chr(response[i]) for i in range(10, 14))
        measurement = int(measurement_str)

    # Handle the exponent
    exponent_code = response[14]
    exponent_number=int(chr(exponent_code))-4
    exponent=pow(10,exponent_number)
    

    # Calculate the final measurement
    #print(measurement,exponent,flag)
    measurement = measurement * exponent * flag
    #print(measurement,exponent,flag)
    return measurement

def t10a_bcc_calc(km_head, command, param):
    # Concatenate the inputs
    input_str = km_head + command + param
    
    # Convert each character to binary and store in a list
    bin_input = []
    for char in input_str:
        # Convert the character to its ASCII value, then to binary, and ensure it's 8 bits long
        bin_char = bin(ord(char))[2:].zfill(8)
        bin_input.append([int(bit) for bit in bin_char])
    
    # Add the ETX (End of Text) binary value [00000011]
    etx = [0, 0, 0, 0, 0, 0, 1, 1]
    bin_input.append(etx)
    
    # Sum the columns and take modulo 2 (sum each column, if odd -> 1, if even -> 0)
    p = [sum(col) % 2 for col in zip(*bin_input)]
    
    # Convert binary list to a decimal value
    p_decimal = int("".join(map(str, p)), 2)
    
    # Convert decimal to hexadecimal
    bcc = format(p_decimal, '02X')  # Format as 2-digit hexadecimal

    return bcc

def t10a_send_command(ser, head, command, params):
    bcc = t10a_bcc_calc(head, command, params)
    full_command = f"\x02{head}{command}{params}\x03{bcc}\r\n"
    encoded_command=full_command.encode()
    ser.write(encoded_command)
    raw_data=[ord(char) for char in full_command]
    #print(raw_data)
    time.sleep(0.5)
    response = ser.read(ser.in_waiting)#.decode()
    return response

def t10a_get_fcd_measurement(serial_object):
    head = '00'
    command = '10'
    params = '0200'
    response = t10a_send_command(serial_object, head, command, params)
    translated_response=t10a_translate_response(response)
    reading_lx=float(translated_response)
    reading_fcd=round(reading_lx/10.7639,2)
    return reading_fcd

def t10a_get_lx_measurement(serial_object):
    head = '00'
    command = '10'
    params = '0200'
    response = t10a_send_command(serial_object, head, command, params)
    translated_response=t10a_translate_response(response)
    reading_lx=float(translated_response)
    #reading_fcd=round(reading_lx/10.7639,2)
    return reading_lx

def t10a_init(serial_object):
    head = '00'  # Receptor head number
    command = '54'
    params = '1   '
    response = t10a_send_command(serial_object, head, command, params)
    #print("PC connection mode response:", response.decode())
    return response
    