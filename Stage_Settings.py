from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import Stage_Controls as SC
import Stage_Constants as Const
import Stage_Safety as SF
import time

def Stage_set(deviceX,deviceY,deviceZ,deviceR):
    command  = AsciiCommand("get system.serial")
    command1 = AsciiCommand("get maxspeed")
    command2 = AsciiCommand("get limit.min")
    command3 = AsciiCommand("get limit.max")
    command4 = AsciiCommand("get limit.start.pos")
    command5 = AsciiCommand("get pos")
    
    # Device X
    print("Device X Settings")
    reply  = deviceX.send(command)
    reply1 = deviceX.send(command1)
    reply2 = deviceX.send(command2)
    reply3 = deviceX.send(command3)
    reply4 = deviceX.send(command4)
    reply5 = deviceX.send(command5)

    print("Device Serial number:", str(reply).split(" ")[5], end="")
    print("Maxspeed:", str(reply1).split(" ")[5], end="")
    print("Minimum Limit (microsteps):", str(reply2).split(" ")[5], end="")
    print("Maximum Limit (microsteps):", str(reply3).split(" ")[5], end="")
    print("Limit Start Position:", str(reply4).split(" ")[5], end="")
    print("Current Position (microsteps):", str(reply5).split(" ")[5], end="")
    print("============================ \n")
    
    # Device Y
    print("Device Y Settings")
    reply  = deviceY.send(command)
    reply1 = deviceY.send(command1)
    reply2 = deviceY.send(command2)
    reply3 = deviceY.send(command3)
    reply4 = deviceY.send(command4)
    reply5 = deviceY.send(command5)

    print("Device Serial number:", str(reply).split(" ")[5], end="")
    print("Maxspeed:", str(reply1).split(" ")[5], str(reply1).split(" ")[6], end="")
    print("Minimum Limit (microsteps):", str(reply2).split(" ")[5],
          str(reply2).split(" ")[6], end="")
    print("Maximum Limit (microsteps):", str(reply3).split(" ")[5],
          str(reply3).split(" ")[6], end="")
    print("Limit Start Position:", str(reply4).split(" ")[5],
          str(reply4).split(" ")[6], end="")
    print("Current Position (microsteps):", str(reply5).split(" ")[5],
          str(reply5).split(" ")[6], end="")
    print("============================ \n")
    
    # Device Z
    print("Device Z Settings")
    reply  = deviceZ.send(command)
    reply1 = deviceZ.send(command1)
    reply2 = deviceZ.send(command2)
    reply3 = deviceZ.send(command3)
    reply4 = deviceZ.send(command4)
    reply5 = deviceZ.send(command5)

    print("Device Serial number:", str(reply).split(" ")[5], end="")
    print("Maxspeed:", str(reply1).split(" ")[5], str(reply1).split(" ")[6], end="")
    print("Minimum Limit (microsteps):", str(reply2).split(" ")[5],
          str(reply2).split(" ")[6], end="")
    print("Maximum Limit (microsteps):", str(reply3).split(" ")[5],
          str(reply3).split(" ")[6], end="")
    print("Limit Start Position:", str(reply4).split(" ")[5],
          str(reply4).split(" ")[6], end="")
    print("Current Position (microsteps):", str(reply5).split(" ")[5],
          str(reply5).split(" ")[6], end="")
    print("============================ \n")
    
    # Device R
    print("Ddevice R Settings")
    reply  = deviceR.send(command)
    reply1 = deviceR.send(command1)
    reply2 = deviceR.send(command2)
    reply3 = deviceR.send(command3)
    reply4 = deviceR.send(command4)
    reply5 = deviceR.send(command5)
    
    print("Device Serial number:", str(reply).split(" ")[5], end="")
    print("Maxspeed:", str(reply1).split(" ")[5], end="")
    print("Minimum Limit (microsteps):", str(reply2).split(" ")[5], end="")
    print("Maximum Limit (microsteps):", str(reply3).split(" ")[5], end="")
    print("Limit Start Position:", str(reply4).split(" ")[5], end="")
    print("Current Position (microsteps):", str(reply5).split(" ")[5], end="")
    print("============================ \n")
