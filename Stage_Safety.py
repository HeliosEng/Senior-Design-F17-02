#------------------------------------------------------------------------------------------------------------------------------------------
## Version 13.2.5
#------------------------------------------------------------------------------------------------------------------------------------------

#This Code was written by Keith Mody on Jan. 26th, 2018 and is designed to create safety check for zaber stage movements
#Reference .txt file labeled "Stage_Safety_Log.txt" for Changelog
#Changelog: For documenting changes follow this format: Version xx.xx date intitials: Changes to code

#------------------------------------------------------------------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------------------------------------------------------------------

from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import Stage_Constants as Const
import sys


#------------------------------------------------------------------------------------------------------------------------------------------
#The inputs are the device to "check" and the position that the user wants to move the device                                                                                         
#------------------------------------------------------------------------------------------------------------------------------------------

def check(DEVICE, POSITION):

#------------------------------------------------------------------------------------------------------------------------------------------
##Function will references the maximum and minimum limits of the stages and if POSITION excedes either
##of those limits then the function will produce an error.
##This function should be used before each movement command in order to ensure the stage will not
##trigger any of the limits. Limits triggers will automatically stop the program from running accordding
##to zaber.serial code which should not be changed at any point. 
#------------------------------------------------------------------------------------------------------------------------------------------

    SERIAL = int(str(DEVICE.send(AsciiCommand("get system.serial"))).split(" ")[5]) #Check the UNIQUE serial
    #of the DEVICE. This allows any DEVICE to be inputed into the function.

    #X stage serial 
    if SERIAL == Const.Xserial:
        mini = int(str(DEVICE.send(AsciiCommand("get limit.min"))).split(" ")[5])
        maxi = int(str(DEVICE.send(AsciiCommand("get limit.max"))).split(" ")[5])
        if POSITION < mini or POSITION > maxi:
            print("X Stage cannot move to desired location. Limit will be triggered.")
            print("Limits of X Stage are:",mini,"<===>",maxi,"microsteps.")
            print("The desired Position was: ",POSITION," microsteps")
            print("============================ \n")
            sys.exit()
            
    #Y stage serial     
    elif SERIAL == Const.Yserial:
        mini = int(str(DEVICE.send(AsciiCommand("get limit.min"))).split(" ")[5])
        maxi = int(str(DEVICE.send(AsciiCommand("get limit.max"))).split(" ")[5])
        if POSITION < mini or POSITION > maxi:
            print("Y Stage cannot move to desired location. Limit will be triggered.")
            print("Limits of Y Stage are: ",mini,"<===>",maxi," microsteps.")
            print("The desired Position was: ",POSITION, " microsteps.")
            print("============================ \n")
            sys.exit()
            
    #Z stage serial
    elif SERIAL == Const.Zserial:
        mini = int(str(DEVICE.send(AsciiCommand("get limit.min"))).split(" ")[5])
        maxi = int(str(DEVICE.send(AsciiCommand("get limit.max"))).split(" ")[5])
        if POSITION < mini or POSITION > maxi:
            print("Z Stage cannot move to desired location. Limit will be triggered.")
            print("Limits of Z Stage are: ",mini,"<===>",maxi," microsteps.")
            print("The desired Position was: ",POSITION," microsteps.")
            print("============================ \n")
            sys.exit()
            
    #R stage serial
    elif SERIAL == Const.Rserial:
        mini = int(str(DEVICE.send(AsciiCommand("get limit.min"))).split(" ")[5])
        maxi = int(str(DEVICE.send(AsciiCommand("get limit.max"))).split(" ")[5])
        if POSITION < mini or POSITION > maxi:
            print("R Stage cannot move to desired location. Limit will be triggered.")
            print("Limits of R Stage are: ",mini,"<===>",maxi," microsteps.")
            print("The desired Position was: ",POSITION)
            print("============================ \n")
            sys.exit()
    else:
        print("nothing matched")

def X_Stage_Coll_SF(r_action,w_action):

    file = open("X_Stage_Safety_Check.txt","r")
    status = 1
    status = int(status)

    if r_action.upper() == "R":
        if status == 1:
            pass
        elif status == 0:
            print("Unexpected power cycle has occurred during X_Stage movement.")
            print("X_stage will now try to home to 0 position.")
            print("Ensure that the BREADBOARD has been dismounted now.")
            sys.exit()
        else:
            print("The status of the stage X_Stage safety protocol could not be determined.")
            print("Please refer to .txt \"X_Stage_Safety_Check.txt\" to ensure that it either says 1 or 0")
            print("System will exit program now")
            sys.exit()
        file.close()
            
    if w_action.upper() == "W":
        file = open("X_Stage_Safety_Check.txt","w")
        if status == 1:
            file.write("0")
        elif status == 0:
            file.write("1")
        else:
            print("Write action could not be performed.")
            print("Closing Program.")
            sys.exit()
        file.close()

    if w_action.upper() == "RESET":
        file = open("X_Stage_Safety_Check.txt","w")
        if status == 1:
            pass
        elif status == 0:
            file.write("1")
        file.close()
            

