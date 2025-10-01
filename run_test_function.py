from PCL_functions import *
from T10A_functions import *
from parameters_from_user_functions import *
from xitron_functions import *
import numpy as np

def run_test(PCL_serial_port,t10a_serial_port,xitron_serial_port,output_csv_location,demo_mode):

    # start serial connection
    PCL_serial=PCL_establish_serial_connection(PCL_serial_port)
    t10a_serial=T10A_establish_serial_connection(t10a_serial_port)
    xitron_serial=xitron_establish_serial_connection(xitron_serial_port)
    t10a_init(t10a_serial)


    # setup lists used during test
    if demo_mode:
        num_angles=3
        warm_up_time=0
    else:
        num_angles=37
        warm_up_time=180
    angles=np.linspace(0,180,num_angles,endpoint=True,dtype=int)
    lights=[1,2,3,4,5]

    # record ambient light reading
    PCL_turn_lights_off(PCL_serial)
    lx_value=t10a_get_lx_measurement(t10a_serial)

    #xitron prep
    #query_string="read=volts[a],amps[a],watts[a],freq[a],PF[a],V-CF[a],A-CF[a],V-HARMS[a,1,13],volts[b],amps[b],watts[b],freq[b],PF[b],V-CF[b],A-CF[b],V-HARMS[b,1,13]\n"
    #column_label_string=query_string.removeprefix("read=").replace("V-HARMS[a,1,13],","FUNDA,HARM2A,HARM3A,HARM4A,HARM5A,HARM6A,HARM7A,HARM8A,HARM9A,HARM10A,HARM11A,HARM12A,HARM13A,").replace("V-HARMS[b,1,13]","FUNDB,HARM2B,HARM3B,HARM4B,HARM5B,HARM6B,HARM7B,HARM8B,HARM9B,HARM10B,HARM11B,HARM12B,HARM13B")

    #get query string from file
    f=open('query_string.txt','r')
    query_string=f.readline()
    f.close()
    print(f'Found query string {query_string}')

    column_label_string=query_string.removeprefix('READ?,')



    # format output file with ambient light and column labels
    f=open(output_csv_location,"w")
    f.write('Ambient Lux: '+str(lx_value)+'\n')
    f.write('Target Angle,Encoder Reading,Lux Value,'+column_label_string)
    f.close()

    #set motor base speed and max speed
    if demo_mode:
        PCL_set_motor_speed(PCL_serial,1500,250)
    else:
        PCL_set_motor_speed(PCL_serial,750,250)


    # run test for each light and each angle
    for light in lights:
        PCL_turn_light_on(PCL_serial,light)
        PCL_home_motor(PCL_serial)
        if not demo_mode:
            print(f"warming up light {light}")
            time.sleep(warm_up_time)
            

        f=open(output_csv_location,"a")
        f.write("Light "+str(light)+'\n')
        f.close()

        for angle in angles:
            angle_steps=int(angle/0.009)
            PCL_go_to_angle(PCL_serial,angle_steps)
            print(f"Light {light} now at position {angle}")
            if not demo_mode:
                time.sleep(5) #5 seconds for settling, letting the dimming wires adjust to the new light position
            lx_value=t10a_get_lx_measurement(t10a_serial)
            lx_value_rounded=round(lx_value,2)
            print(f"got lx value {lx_value_rounded}")
            encoder_value=PCL_get_encoder_angle(PCL_serial)
            xitron_response=xitron_send_command(query_string,xitron_serial)
            f=open(output_csv_location,"a")
            f.write(str(angle)+','+str(encoder_value)+','+str(lx_value_rounded)+','+xitron_response.decode())
            f.close()
        
        f=open(output_csv_location,"a")
        f.write('\n')
        f.close()


    PCL_turn_lights_off(PCL_serial)