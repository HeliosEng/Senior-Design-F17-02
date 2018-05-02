#------------------------------------------------------------------------------------------------------------------------------------------
# Version 01.03                                                                                                                            
#------------------------------------------------------------------------------------------------------------------------------------------

#This Code was written by Keaton Scheffler on Jan. 8th, 2018 and is designed to make zaber stages integrated for senior design team F17-02 
#This was written using the Python API documentation provided by Zaber Technologies this documentation can be found at                     
#https://www.zaber.com/support/docs/api/core-python/0.8.1/index.html#

#------------------------------------------------------------------------------------------------------------------------------------------
#Changelog: For documenting changes follow this format: Version xx.xx date initials: Changes to code including line number/function changed
#------------------------------------------------------------------------------------------------------------------------------------------
#Version 01.00 Jan. 8, 2018 KJS: Original Release                                                                                          
#Version 01.01 Jan 17, 2018 KJS: Added a baud rate of 115200 to the Connection Function as well as added new function called N_step_motion
#Version 01.02 Jan 18, 2018 HJW: Added single device home command called Home_Single_Device , descovered error in vel_motion commands,
#   found bug in single_device_status and fixed.
#Version 01.03 Jan 26, 2018 KCM: Added function mount setting for single and multiple stages under section II. 
#   Changed abs_move_position function to convert POSITION variable to accept multiple types. Converts variable to type int.   
#------------------------------------------------------------------------------------------------------------------------------------------
##                                                                      
#------------------------------------------------------------------------------------------------------------------------------------------

from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import Stage_Constants as Const
import Stage_Safety as SF
import time
import math
import sys
import numpy as np


'''
-------------------------------------------------------------------------------------------------------------------------------------------
I. Connecting Devices
-------------------------------------------------------------------------------------------------------------------------------------------
'''
#------------------------------------------------------------------------------------------------------------------------------------------
## There are no inputs to this function
## This function should be done once to initialize the stages to their respective devices
## The Home_All_Devices and mount command should be used to zero the system and to provide a good position to mount the part
#------------------------------------------------------------------------------------------------------------------------------------------

def init_system():

    portZ = ConnectionZ()
    portYXR = ConnectionYXR()
    deviceZ = Device_StageZ(portZ)
    deviceY, deviceX, deviceR = Device_StageYXR(portYXR)

    print("Intializing system.")
    return deviceX, deviceY, deviceZ, deviceR, portZ, portYXR

#------------------------------------------------------------------------------------------------------------------------------------------
## The input of this function are the devices of the gantry system
## The function will reset the stage to referenced positions
## BREADBOARD MUST BE REMOVED BEFOREHAND
#------------------------------------------------------------------------------------------------------------------------------------------


def stages_reset(deviceX, deviceY, deviceZ, deviceR):
    
    answer = input("Has the breadboard been removed? (Y/N): ")
       
    if answer.upper() in ["YES", "Y"]:
        print("Proceeding with Program")
    elif answer.upper() in ["NO", "N"]:
        print("Please mount the part. Program will exit")
        sys.exit()
    else:
        print("Please enter a valid answer (Y/N). Program will exit")
        sys.exit()

    Home_All_Devices(deviceY, deviceZ, deviceR)
    SF.X_Stage_Coll_SF("No Item","RESET")
    deviceX.send(AsciiCommand("home"))
    print("Resest 50% Complete")
    deviceX.poll_until_idle()
    abs_move(deviceX,2500000)
    print("Reset 100% Complete")
    
#------------------------------------------------------------------------------------------------------------------------------------------
## There are no inputs to this function however there could be if the user decided they wanted to choose which COM port to use
## A function that connects the stage controller to a computer as well as initalizing the stages for use in the code
#------------------------------------------------------------------------------------------------------------------------------------------

def ConnectionZ():
    
    port = AsciiSerial("COM10", baud = 115200,timeout=None)# Windows COM Port corresponding to the Zaber Controller
    return port

#------------------------------------------------------------------------------------------------------------------------------------------
## There are no inputs to this function however there could be if the user decided they wanted to choose which COM port to use
## A function that connects the stage controller to a computer as well as initalizing the stages for use in the code 
#------------------------------------------------------------------------------------------------------------------------------------------

def ConnectionYXR():
    
    port = AsciiSerial("COM11", baud = 115200,timeout=None)# Windows COM Port corresponding to the second Zaber Controller
    return port

#------------------------------------------------------------------------------------------------------------------------------------------
## The input port is the return of the Connection Function and defines which COM port the controller is connected to
## Create a device An alternative would be to create a set of axis depends on how the controller works
#------------------------------------------------------------------------------------------------------------------------------------------

def Device_StageZ(port):

    deviceZ = AsciiDevice(port,1) #Device number 1 (Y axis). Singular Device on Controller
    return deviceZ

#------------------------------------------------------------------------------------------------------------------------------------------
## The input port is the return of the Connection Function and defines which COM port the controller is connected to
## Create a device An alternative would be to create a set of axis depends on how the controller works 
#------------------------------------------------------------------------------------------------------------------------------------------

def Device_StageYXR(port):

    deviceY = AsciiDevice(port,1)
    deviceX = AsciiDevice(port,2)
    deviceR = AsciiDevice(port,3)

    return deviceY, deviceX, deviceR

#------------------------------------------------------------------------------------------------------------------------------------------
## A function that verifys that the command that was issued to the controller succeeded
## ccs = check command succeded
#------------------------------------------------------------------------------------------------------------------------------------------
 
def ccs(reply):

    if reply.reply_flag != "OK": # If command not accepted (received "RJ")
        print ("Danger! Command rejected because: {}".format(reply.data))
        return False
    else: # Command was accepted
        print(str(reply), end="")
        print("Successfull Command!")
        print("=============================== \n")
        return True

'''
#-------------------------------------------------------------------------------------------------------------------------------------------
##II. Stage Movement Commands: Distance and Velocity
#-------------------------------------------------------------------------------------------------------------------------------------------
'''

#------------------------------------------------------------------------------------------------------------------------------------------
## The Inputs for this function are the returns of the Devices_Stage which represent the stages/axis of the zaber stages
## A function that will return all of the stages back to their home position
#------------------------------------------------------------------------------------------------------------------------------------------

def Home_All_Devices(deviceY, deviceZ, deviceR):

    command2 = deviceY.send(AsciiCommand("01 lockstep 1 home"))
    command3 = deviceZ.send(AsciiCommand("01 lockstep 1 home"))  
    command4 = deviceR.send(AsciiCommand("home"))

    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()
    
    print("Device Y")
    ccs(command2)
    print("Device Z")
    ccs(command3)
    print("Device R")
    ccs(command4)    

#------------------------------------------------------------------------------------------------------------------------------------------
## The Input for this function is the device that needs to be homed
## A function that will return a selected stage to it's home position 
#------------------------------------------------------------------------------------------------------------------------------------------

def Home_Single_Device(DEVICE):
    
    serial = int(str(DEVICE.send(AsciiCommand("get system.serial"))).split(" ")[5])

    # Note that the X stage is not provided here
    # X stage should be homed manually, accidently homing the X_stage could damage the system
    # X stage should not be homed in any case, because of the tools parking and unparking features
    if serial == Const.Yserial:
        reply = DEVICE.send(AsciiCommand("01 lockstep 1 home"))
    elif serial == Const.Zserial:
        reply = DEVICE.send(AsciiCommand("01 lockstep 1 home"))
    elif serial == Const.Rserial:
        reply = DEVICE.send(AsciiCommand("home"))
    else:
        print("nothing matched")

#------------------------------------------------------------------------------------------------------------------------------------------
## The inputs of this function all zager devices
## Mount Status is the position the stage should be in, in order to mount a part
## A function that will return all stages to their mount position 
#------------------------------------------------------------------------------------------------------------------------------------------

def Mount_All_Devices(deviceX, deviceY, deviceZ, deviceR):
   

    answer = input("Has the breadboard and/or part been mounted? (Y/N): ")
       
    if answer.upper() in ["YES", "Y"]:
        abs_move(deviceY, Const.YZstagemax)
        abs_move(deviceZ, 0)
        abs_move(deviceR, 0)
        abs_move(deviceX, Const.Xstagehalf)
        deviceY.poll_until_idle()
        deviceZ.poll_until_idle()
        deviceR.poll_until_idle()
        print("Proceeding with Program")
    else:
        print("Please mount the part. Program will exit")


#------------------------------------------------------------------------------------------------------------------------------------------
## The inputs are the device which are inteded to be moved and the respective position
## A function that moves the devices to the desired settup position while pausing the main code
#------------------------------------------------------------------------------------------------------------------------------------------

def Settup_Move(deviceX, deviceY, deviceZ, deviceR, X_pos, Y_pos, Z_pos, R_pos):

    abs_move(deviceX, X_pos)
    abs_move(deviceY, Y_pos)
    abs_move(deviceZ, Z_pos)
    abs_move(deviceR, R_pos)
    
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()
    
#------------------------------------------------------------------------------------------------------------------------------------------
#DEVICE is the device to undergo the motion, SPEED is the speed of that motion in microsteps/sec, TIME is the duration of the motion
#DOES NOT WORK, TIME IS NOT CHECKED DURING WHILE LOOP
#------------------------------------------------------------------------------------------------------------------------------------------

def vel_motion_timed(DEVICE, SPEED, TIME):
    
#------------------------------------------------------------------------------------------------------------------------------------------
##this function moves the stage as a certain speed for a certain amount of time                                                            
#------------------------------------------------------------------------------------------------------------------------------------------

    start_time = time.time()
    while (time.time() - start_time) < TIME :   
        DEVICE.move_vel(SPEED)
        DEVICE.poll_until_idle()
        DEVICE.stop()


#------------------------------------------------------------------------------------------------------------------------------------------
#DEVICE is the device to undergo the motion, SPEED is the speed of that motion in mu-steps/sec, POSITION is the desired postion of da stage
#DOES NOT WORK
#------------------------------------------------------------------------------------------------------------------------------------------

def vel_move_position(DEVICE, SPEED, POSITION):
    
#------------------------------------------------------------------------------------------------------------------------------------------
##This function will move the stage at a certain speed until the stage reaches a defined postion                                           
#------------------------------------------------------------------------------------------------------------------------------------------

    #Determine the position of the stage
    pos_int = DEVICE.send("get pos")
    print(pos_int)
    type(pos_int)
    #find the difference between the desired position and the current position as well as the direction that the stage must move to get to that pos
    pos_difference = pos_int - POSITION
    #Create the start time variable
    start_time = time.time()
    #an if statement that determines how the stage must move
    #Case 1 if pos_int = pos_desired there is no movement
    #Case 2 if pos_int is more positive than pos_desired move the stage in the negative direction
    #Case 3 if pos_int is less positive than pos_desired move stage in positive direction
    if pos_int == POSITION:
        DEVICE.stop() 
    elif POSITION < pos_int:
        abs_pos = abs(pos_difference) #pos in units of microsteps and speed in units of microsteps/second pos/speed is units of seconds
        move_time = abs_pos / SPEED
           
        while (time.time() - start_time) < move_time:
            speed = SPEED * (-1) #makes the stage go backwards
            DEVICE.move_vel(speed)
            DEVICE.poll_until_idle()
            DEVICE.stop()   
    else:
        start_time = time.time()
        move_time = POSITION / SPEED
        while time.time() - start_time < move_time:
            DEVICE.move_vel(SPEED)
            DEVICE.poll_until_idle()
            DEVICE.stop()
            
            
#------------------------------------------------------------------------------------------------------------------------------------------
## DEVICE is the device to undergo the motion, POSITION is the desired position of the stage
## Moves the devices to the specified position 
#------------------------------------------------------------------------------------------------------------------------------------------

def abs_move(DEVICE, POSITION):
    
    serial = int(str(DEVICE.send(AsciiCommand("get system.serial"))).split(" ")[5])
    SF.check(DEVICE, POSITION)

    if serial == Const.Xserial:
        DEVICE.send(AsciiCommand("tools parking unpark"))
        SF.X_Stage_Coll_SF("R","W")
        reply = DEVICE.send(AsciiCommand("move abs",POSITION))
        DEVICE.poll_until_idle()
        DEVICE.send(AsciiCommand("tools parking park"))
        SF.X_Stage_Coll_SF("","W")
    elif serial == Const.Yserial:
        reply = DEVICE.send(AsciiCommand("01 lockstep 1 move abs",POSITION))
    elif serial == Const.Zserial:
        reply = DEVICE.send(AsciiCommand("01 lockstep 1 move abs",POSITION))
    elif serial == Const.Rserial:
        reply = DEVICE.send(AsciiCommand("move abs", POSITION))
    else:
        print("nothing matched")
  
#------------------------------------------------------------------------------------------------------------------------------------------
## The inputs are:
        # POSITION: desired position of the Xstage
        # data: previous position data of all stages in the system
        # deviceX, deviceY, deviceZ, deviceR: All devices in system
## Continously record positional data while the XSTAGE is in motion
## The X stage needs seperate code to record position because of how the "tools parking" and "tools unparking" safety feature is settup
#------------------------------------------------------------------------------------------------------------------------------------------

def abs_move_cont_X(POSITION, data, deviceX, deviceY, deviceZ, deviceR):

    SF.check(deviceX, POSITION)                                     #safety check for the desired positoin of Xstage

    deviceX.send(AsciiCommand("tools parking unpark"))              #unparks the Xstage so it can move
    SF.X_Stage_Coll_SF("R","W")                                     #writes to X_Stage_Safety_Check.txt
    deviceX.send(AsciiCommand("move abs",POSITION))
    positions = cont_read_all_pos(deviceX,deviceY,deviceZ,deviceR)  #records all positions
    data = combine_data(positions,data)                             #combines all positional data with prvious data
    deviceX.poll_until_idle()                                       
    deviceX.send(AsciiCommand("tools parking park"))                #parks the Xstage so it can't move
    SF.X_Stage_Coll_SF("","W")                                      #writes to and resets X_Stage_Safety_Check.txt

    return data
'''
#-------------------------------------------------------------------------------------------------------------------------------------------
##III. Stage Status and Location Commands
#-------------------------------------------------------------------------------------------------------------------------------------------
'''

#------------------------------------------------------------------------------------------------------------------------------------------
## The Input for this function is the device whose position [step] is to be returned
## Get the theoretical position of the stage
## Any device ID can be entered and the function will check the serial number on the device
#------------------------------------------------------------------------------------------------------------------------------------------

def read_single_pos(DEVICE):

    serial = int(str(DEVICE.send(AsciiCommand("get system.serial"))).split(" ")[5])

    if serial == Const.Xserial:
        pos = int(str(DEVICE.send(AsciiCommand("get pos"))).split(" ")[5])
    elif serial == Const.Yserial:
        pos = int(str(DEVICE.send(AsciiCommand("get pos"))).split(" ")[5])
        pos = int(str(DEVICE.send(AsciiCommand("get pos"))).split(" ")[6])
    elif serial == Const.Zserial:
        pos = int(str(DEVICE.send(AsciiCommand("get pos"))).split(" ")[5])
        pos = int(str(DEVICE.send(AsciiCommand("get pos"))).split(" ")[6])
    elif serial == Const.Rserial:
        pos = int(str(DEVICE.send(AsciiCommand("get pos"))).split(" ")[5])

    return pos

#------------------------------------------------------------------------------------------------------------------------------------------
## The Inputs for this function are the returns of the Devices_Stage which represent the stages/axis of the zaber stages
## Get the theoretical position of all the stages 
#------------------------------------------------------------------------------------------------------------------------------------------
                    
def read_all_pos(deviceX, deviceY, deviceZ, deviceR):
    
    check = all_devices_status(deviceX, deviceY, deviceZ, deviceR)
    while check == 0: #BUSY
        check = all_devices_status(deviceX,deviceY, deviceZ, deviceR)

    posX = [int(str(deviceX.send(AsciiCommand("get pos"))).split(" ")[5])]
    posY1 = [int(str(deviceY.send(AsciiCommand("get pos"))).split(" ")[5])]
    posY2 = [int(str(deviceY.send(AsciiCommand("get pos"))).split(" ")[6])]
    posZ1 = [int(str(deviceZ.send(AsciiCommand("get pos"))).split(" ")[5])]
    posZ2 = [int(str(deviceZ.send(AsciiCommand("get pos"))).split(" ")[6])]
    posR = [int(str(deviceR.send(AsciiCommand("get pos"))).split(" ")[5])]

    data = [posX,posY1,posY2,posZ1,posZ2,posR]
    
    return data

#------------------------------------------------------------------------------------------------------------------------------------------
## The Inputs for this function are the returns of the Devices_Stage which represent the stages/axis of the zaber stages
## Continuously get the position of the stages while in movement
## "abs_move_cont_X" will need to be used to continously record data for Xstage in movment
#------------------------------------------------------------------------------------------------------------------------------------------

def cont_read_all_pos(deviceX, deviceY, deviceZ, deviceR):

    data = []
    check = all_devices_status(deviceX, deviceY, deviceZ, deviceR)

    while check == 0:
        posX = [int(str(deviceX.send(AsciiCommand("get pos"))).split(" ")[5])]
        posY1 = [int(str(deviceY.send(AsciiCommand("get pos"))).split(" ")[5])]
        posY2 = [int(str(deviceY.send(AsciiCommand("get pos"))).split(" ")[6])]
        posZ1 = [int(str(deviceZ.send(AsciiCommand("get pos"))).split(" ")[5])]
        posZ2 = [int(str(deviceZ.send(AsciiCommand("get pos"))).split(" ")[6])]
        posR = [int(str(deviceR.send(AsciiCommand("get pos"))).split(" ")[5])]
        positions = [posX,posY1,posY2,posZ1,posZ2,posR]
        data = combine_data(positions, data)
        check = all_devices_status(deviceX, deviceY, deviceZ, deviceR)

    positions = read_all_pos(deviceX, deviceY, deviceZ, deviceR)
    data = combine_data(positions, data)

    return data


#------------------------------------------------------------------------------------------------------------------------------------------
#The inputs of the function are the desired text file save name, and the data which is needed to be saved
#Data is positional data
#Positional data should be formatted as follows
#------------------------------------------------------------------------------------------------------------------------------------------

def write_pos_to_file(filename,data):

    if len(data) != 6:
        print("Data length is not 6. Missing Compoenent. Exiting Program")
        sys.exit()

    header = [["X", "Y1", "Y2", "Z1", "Z2", "R"]]
    newdata = list(map(list,zip(*data)))
    newdata = header + newdata
    with open(filename, "w") as out_file:
        for i in range(0,len(newdata)):
            for item in newdata[i]:
                out_file.write("%s\t" %item)
            out_file.write("\n")
        
#------------------------------------------------------------------------------------------------------------------------------------------
## The inputs are the new POSITIONS and the old DATA that the POSITIONS will be appended to
## Combines the positional data of the stages 
#------------------------------------------------------------------------------------------------------------------------------------------

def combine_data(POSITIONS, DATA):

    if DATA == []:
        DATA = POSITIONS
    else:
        for items in range(0, len(DATA)):
            for j in range(0, len(POSITIONS[0])):
                DATA[items] += POSITIONS[items]

    return DATA
     

#------------------------------------------------------------------------------------------------------------------------------------------
## The input is all the devices that are a part of the zaber stage
## Determines the status of all of the stages
#------------------------------------------------------------------------------------------------------------------------------------------

def all_devices_status(deviceX, deviceY, deviceZ, deviceR):

    Status = {'Status 1': deviceX.get_status(),'Status 2': deviceY.get_status(),'Status 3': deviceZ.get_status(),'Status 4': deviceR.get_status()}
    BUSY = 0
    IDLE = 1
    if 'BUSY' in Status.values():
        return BUSY 
    else:
        return IDLE
    
  
#------------------------------------------------------------------------------------------------------------------------------------------
## The input is the device that is being tested
## determines the status of a singular stage 
#------------------------------------------------------------------------------------------------------------------------------------------

def single_device_status(device):

    Status = {'Status': device.get_status()}

    BUSY = 0
    IDLE = 1
    
    if 'BUSY' in Status.values() == True:
        return BUSY 
    
    else:
        return IDLE

#------------------------------------------------------------------------------------------------------------------------------------------
## There is no input for this function
## This functions sole purpose is to impress judges at trade fair 2018
#------------------------------------------------------------------------------------------------------------------------------------------

def stage_dance(deviceX, deviceY, deviceZ, deviceR):
    
    deviceX_lmax = int(6000000)
    deviceY_lmax = int(4031496)
    deviceZ_lmax = int(4031496)
    deviceR_lmax = int(1000000000)
    
    deviceX_lmin = int(0)
    deviceY_lmin = int(0)
    deviceZ_lmin = int(0)
    deviceR_lmin = int(-1000000000)

    #Adjusting stage settings
    deviceX.send(AsciiCommand("set limit.max", deviceX_lmax))
    deviceY.send(AsciiCommand("set limit.max", deviceY_lmax))
    deviceZ.send(AsciiCommand("set limit.max", deviceZ_lmax))
    deviceR.send(AsciiCommand("set limit.max", deviceR_lmax))

    deviceX.send(AsciiCommand("set limit.min", deviceX_lmin))
    deviceY.send(AsciiCommand("set limit.min", deviceY_lmin))
    deviceZ.send(AsciiCommand("set limit.min", deviceZ_lmin))
    deviceR.send(AsciiCommand("set limit.min", deviceR_lmin))

    deviceX.send(AsciiCommand("tools parking unpark"))
    
    deviceX.send(AsciiCommand("move abs 1000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 1000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 1000000"))
    deviceR.send(AsciiCommand("move abs 000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()

    print("14% Complete")
    
    deviceX.send(AsciiCommand("move abs 2000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 2000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 2000000"))
    deviceR.send(AsciiCommand("move abs 1000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()

    print("28% Complete")

    deviceX.send(AsciiCommand("move abs 1000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 3000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 1000000"))
    deviceR.send(AsciiCommand("move abs 000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()

    print("42% Complete")

    deviceX.send(AsciiCommand("move abs 4000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 4000000"))
    deviceR.send(AsciiCommand("move abs 3000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()

    print("56% Complete")

    deviceX.send(AsciiCommand("move abs 3000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 1000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 3000000"))
    deviceR.send(AsciiCommand("move abs 2000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()

    print("70% Complete")
    
    deviceX.send(AsciiCommand("move abs 4000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 0000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 2000000"))
    deviceR.send(AsciiCommand("move abs 1000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()

    print("85% Complete")

    deviceX.send(AsciiCommand("move abs 0000000"))
    deviceY.send(AsciiCommand("01 lockstep 1 move abs 4000000"))
    deviceZ.send(AsciiCommand("01 lockstep 1 move abs 00000"))
    deviceR.send(AsciiCommand("move abs -1000000"))
    deviceX.poll_until_idle()
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()
    
    print("100% Complete")

    deviceX.send(AsciiCommand("tools parking park"))
    
    
    
#------------------------------------------------------------------------------------------------------------------------------------------
## The inputs of this function are the devices ID's from Device_Stages and the Port ID's
## The stages will be moved to mount position and the ports will be closed until opend and connected
#------------------------------------------------------------------------------------------------------------------------------------------

def shutdown_system(deviceX, deviceY, deviceZ, deviceR, portZ, portYXR):

    abs_move(deviceY, Const.YZstagemax)
    abs_move(deviceZ, 0)
    abs_move(deviceR, 0)
    abs_move(deviceX, Const.Xstagehalf)
    deviceY.poll_until_idle()
    deviceZ.poll_until_idle()
    deviceR.poll_until_idle()
    
    close_port(portZ)
    close_port(portYXR)
    print("System can now be properly shut down.")


#-------------------------------------------------------------------------------------------------------------------------------------------
#End of Program
#-------------------------------------------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------------------------------------------
## The input port is defined by the Connection function and is used to disconnect the port
## A function that closes the port 
#------------------------------------------------------------------------------------------------------------------------------------------

def close_port(port):

    port.close()
    


    
