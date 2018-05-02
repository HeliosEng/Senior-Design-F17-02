from zaber.serial import AsciiSerial, AsciiDevice, AsciiCommand, AsciiReply
import Stage_Controls as SC
import Stage_Settings as SS
import math
import Stage_Constants as Const
import Stage_Safety as SF


deviceX, deviceY, deviceZ, deviceR, portZ, portYXR = SC.init_system()
#portZ = SC.ConnectionZ()
#portYXR = SC.ConnectionYXR()
#deviceZ = SC.Device_StageZ(portZ)
#deviceY, deviceX, deviceR = SC.Device_StageYXR(portYXR)

#SC.Home_All_Devices(deviceY, deviceZ, deviceR)
#deviceX.send(AsciiCommand("home"))
#SC.stage_dance(deviceX, deviceY, deviceZ, deviceR)
#SS.adjust_stage_set(deviceX, deviceY, deviceZ, deviceR)
#SC.stage_dance(deviceX, deviceY, deviceZ, deviceR)
#SS.adjust_stage_set(deviceX, deviceY, deviceZ, deviceR)

#reply = deviceX.send(AsciiCommand("get pos"))
#SC.ccs(reply)

#SC.abs_move(deviceX, int((2500000+4200000)/2))
#SC.abs_move(deviceX, 3160000)       #Range: 2,500,000 ---> 4,200,000
SC.abs_move(deviceY, 1905000)
SC.abs_move(deviceZ, 31496)
#SC.abs_move(deviceR, 1000000)

#SC.abs_move(deviceZ, 2000000)

#SC.stages_reset(deviceX, deviceY, deviceZ, deviceR)







'''
deviceY. send(AsciiCommand("set maxspeed 10000"))
SS.Stage_set(deviceX, deviceY, deviceZ, deviceR)

check = SC.all_devices_status(deviceX, deviceY, deviceZ, deviceR)
deviceY.send(AsciiCommand("01 lockstep 1 move abs 500000"))
positions = SC.cont_read_all_pos(deviceX, deviceY, deviceZ, deviceR)

SC.write_pos_to_file("Max_speed_10000.txt", positions)
'''


#SS.Stage_set(deviceX,deviceY,deviceZ,deviceR)


#SC.shutdown_system(deviceX, deviceY, deviceZ, deviceR, portZ, portYXR)




#reply = deviceY.send(AsciiCommand("01 lockstep 1 move abs 0"))
#SC.ccs(reply)
#reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs", Const.YZstagemax))

#data = []

#data = SC.abs_move_cont_X(1000000, data, deviceX, deviceY, deviceZ, deviceR)

#data = SC.cont_read_all_pos(deviceX, deviceY, deviceZ, deviceR)
#print(data)

'''
DATA = [[1],[1],[1],[1]]
x = [[5,5,43,6],[3,23,4,5],[6,8,6,3],[4,2,56,2]]


for i in range(0,len(DATA)):
    for j in range(0,len(x[0])):
        DATA[i].append(x[i][j])

print(DATA)
#reply = deviceX.send(AsciiCommand("system reset"))
#SC.ccs(reply)
#SC.Home_All_Devices(deviceY, deviceZ, deviceR)
SS.Stage_set(deviceX, deviceY, deviceZ, deviceR)

reply = deviceX.send(AsciiCommand("move abs 2000000"))
print(reply)

reply = deviceX.send(AsciiCommand("get pos"))
print(reply)

reply = deviceX.send(AsciiCommand("home"))
print(reply)

#reply = deviceX.send(AsciiCommand("home"))








#deviceX.send(AsciiCommand("tools parking unpark"))
#deviceX.send(AsciiCommand("move abs 4000000"))
#data = []

#while deviceX.get_status() == "BUSY":
#    data.append(int(str(deviceX.send(AsciiCommand("get pos"))).split(" ")[5]))

#data2 = []
#print(len(data))
#print(data)
#print(len(data2))
#print("here")
#for i in range(0,len(data)-2):
    
#    data2.append(data[i+1] - data[i])
#print(data2)
#print(max(data2))

    



#deviceX.send(AsciiCommand("tools parking unpark"))
#reply = deviceX.send(AsciiCommand("move abs 2000000"))
#SC.ccs(reply)
#deviceX.poll_until_idle()
#reply = deviceX.send(AsciiCommand("tools parking park"))
#SC.ccs(reply)

#SC.write_pos_to_file("test.txt", data)

#device = SC.Single_Device_Stage(port)

#SC.Home_Single_Device(device)

#SC.abs_move_position(device, 100010)
#SC.abs_move_position(device, 5000)

Status=SC.single_device_status(device)
#print(Status)

#SC.vel_move_position(device,200,1000000)

#------------------------------------------------------------
def read_single_pos(device):

    pos1 = device.send("get pos")

    return pos1
#-----------------------------------------------------------

pos = int(str(read_single_pos(device)).split(" ")[5])
print(pos)

#pos3 = pos.split(" ")
#print(pos3)
#print(pos3[5])

#pos4 = int(pos[5])

L = len(pos)
print(L)


#Movement for the Y-Stage Controls
#--------------------------------------
def Devices_stages(port):
    deviceXOne = AsciiDevice(port,1)

    return deviceY
#--------------------------------------
deviceY = Devices_stages(port)
print(deviceY,'\n')

command = AsciiCommand("01 lockstep 1 move abs 0")
port.write(command)
deviceY.poll_until_idle(0)

command = AsciiCommand("get maxspeed")
reply = deviceY.send(command)
print("maxspeed for Y Device")
print(reply)

command = AsciiCommand("01 lockstep 1 move abs 1500000")
reply = deviceY.send(command)
deviceY.send(AsciiCommand("01 lockstep 1 move abs 1000000"))
print(reply)
deviceY.poll_until_idle(0)


command1 = AsciiCommand("01 lockstep 1 info")
port.write(command1)

reply = port.read()
print("Lockstep info")
print(reply)

command = AsciiCommand("01 get limit.max")
port.write(command)

reply = port.read()
print(reply)

deviceXOne.poll_until_idle(0)

command = AsciiCommand("get pos")
port.write(command)

reply = port.read()
print(reply)

if reply.reply_flag == "RJ":
    print("A command was rejected! Reason: {}".format(reply.data))
elif reply.reply_flag == "OK":
    print("Command successful")

#Movement for the X,Z,Rotation stage controls
print("Entering commands for Stage Section 2")
#--------------------------------------
def Devices_stages_2(port):
    deviceZ = AsciiDevice(port,1)
    deviceX = AsciiDevice(port,2)
    deviceR = AsciiDevice(port,3)

    return deviceZ,deviceX,deviceR
#--------------------------------------

deviceZ,deviceX,deviceR = Devices_stages_2(port2)

reply = deviceX.send(AsciiCommand("set maxspeed 153600"))
print("setting new max speed")
print(reply)

reply = deviceX.send(AsciiCommand("get maxspeed"))
print("maxspeed for deviceX")
print(reply)

deviceX.send(AsciiCommand("move abs 3000000"))

command = AsciiCommand("01 lockstep 1 info")
port2.write(command)
reply = port2.read()
print(reply)

command = AsciiCommand("get pos")
port2.write(command)

reply = port2.read()
print(reply)

if reply.reply_flag == "RJ":
    print("A command was rejected! Reason: {}".format(reply.data))
elif reply.reply_flag == "OK":
    print("Command successful")

deviceX.send(AsciiCommand("move abs 300000"))
deviceR.send(AsciiCommand("move abs 100000"))
deviceZ.send(AsciiCommand("01 lockstep 1 move abs 300000"))
deviceY.send(AsciiCommand("01 lockstep 1 move abs 300000"))
deviceX.poll_until_idle()
deviceY.poll_until_idle()
deviceZ.poll_until_idle()
deviceR.poll_until_idle()

SC.Home_All_Devices(deviceX, deviceY, deviceZ, deviceR)



print("Debugging Z axis")

command = AsciiCommand("01 lockstep 1 info")
reply = deviceZ.send(command)
SC.ccs(reply)

command = AsciiCommand("01 get limit.min")
reply = deviceZ.send(command)
SC.ccs(reply)

command = AsciiCommand("01 get limit.max")
reply = deviceZ.send(command)
SC.ccs(reply)

reply = deviceZ.send(AsciiCommand("01 lockstep 1 home"))

reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 1000000"))
SC.ccs(reply)
deviceZ.poll_until_idle()

command = AsciiCommand("01 get encoder.pos")
reply = deviceZ.send(command)
SC.ccs(reply)

command = AsciiCommand("01 get pos")
reply = deviceZ.send(command)
SC.ccs(reply)

print("new code")

reply = deviceZ.send(AsciiCommand("set limit.start.pos 2"))
SC.ccs(reply)

print("here")
reply = deviceZ.send(AsciiCommand("get limit.start.pos"))
SC.ccs(reply)

reply = deviceZ.send(AsciiCommand("get system.access"))
SC.ccs(reply)

reply = deviceZ.send(AsciiCommand("01 lockstep 1 home"))
SC.ccs(reply)
deviceZ.poll_until_idle()


reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 1500000"))
SC.ccs(reply)


#deviceZ.send(AsciiCommand("warnings clear"))
reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 8"))
SC.ccs(reply)
reply = deviceY.send(AsciiCommand("01 lockstep 1 home"))
SC.ccs(reply)
deviceY.poll_until_idle()
deviceZ.poll_until_idle()
reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 200000"))
SC.ccs(reply)
reply = deviceY.send(AsciiCommand("01 lockstep 1 move abs 200000"))
SC.ccs(reply)

reply = deviceZ.send(AsciiCommand("01 lockstep 1 home"))
SC.ccs(reply)
reply = deviceZ.send(AsciiCommand("get pos"))
SC.ccs(reply)

reply = deviceZ.send(AsciiCommand("get encoder.pos"))
SC.ccs(reply)
deviceZ.poll_until_idle()
reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 100000"))
SC.ccs(reply)
deviceZ.poll_until_idle()
reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 700000"))
SC.ccs(reply)
deviceZ.poll_until_idle()
reply = deviceZ.send(AsciiCommand("01 lockstep 1 move abs 400000"))
SC.ccs(reply)
deviceZ.poll_until_idle()

reply = deviceZ.send(AsciiCommand("01 lockstep 1 info"))
SC.ccs(reply)
deviceZ.send(AsciiCommand("warnings clear"))
'''






SC.close_port(portZ)
SC.close_port(portYXR)
