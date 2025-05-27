def get_demo_mode():
    choice=input("Enter 1 for demo mode or hit enter for normal mode: ")
    if choice=='1':
        return True
    else:
        return False

def get_user_lux_mode():
    choice=input("Enter 1 if manually entering lux values, hit enter for auto mode: ")
    if choice=='1':
        return True
    else:
        return False

def get_light_voltage():
    #get light voltage from user and check that it is in range
    light_voltage_valid=False
    while not light_voltage_valid:
        light_voltage_input=input("What voltage are you running the lamps at? (V) (0-24): ")
        try:
            light_voltage=float(light_voltage_input)
            if light_voltage>=0 and light_voltage<=24:
                light_voltage_valid=True
            else:
                print("Invalid light voltage, try again")
        except:
            print("Invalid light voltage, try again")
    print(f"Lights running at {light_voltage} volts.")
    return light_voltage

def get_num_angles():
    #get number of angles btwn 0 and 180 to test at, for example a value of 3 would mean test at 0, 90, and 180
    num_angles_valid=False
    while not num_angles_valid:
        num_angles_input=input("How many angles will you test at? (2-180): ")
        try:
            num_angles=int(num_angles_input)
            if num_angles>=2 and num_angles<=180:
                num_angles_valid=True
            else:
                print("Invalid number of angles, try again")
        except:
            print("Invalid number of angles, try again")
    print(f"Will test at {num_angles} angles.")
    return num_angles

def get_log_file_name():
    """
    Prompt the user to enter a CSV file name without forbidden characters.
    Returns the validated file name.
    """
    # Define characters that are not allowed in file names
    forbidden = set('<>:"/\\|?*')
    while True:
        name = input("Enter log file name (must end with .csv): ").strip()
        # Identify any forbidden characters in the input
        invalid = [c for c in name if c in forbidden]
        if invalid:
            print(f"Invalid character(s) found: {''.join(sorted(set(invalid)))}")
            continue
        # Ensure the file name ends with .csv (case-insensitive)
        if not name.lower().endswith('.csv'):
            print("File name must end with .csv")
            continue
        return name

def get_uut_lx_value_from_user():
    #get number of angles btwn 0 and 180 to test at, for example a value of 3 would mean test at 0, 90, and 180
    uut_lux_value_valid=False
    while not uut_lux_value_valid:
        uut_lux_value_input=input("Enter UUT lux value integer: ")
        try:
            uut_lux_value=int(uut_lux_value_input)
            if uut_lux_value>=0:
                uut_lux_value_valid=True
            else:
                print("Invalid number of angles, try again")
        except:
            print("Invalid number of angles, try again")
    return uut_lux_value