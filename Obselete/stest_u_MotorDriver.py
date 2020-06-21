from opcua import Client
from opcua import ua
import py
import time
import pytest

MotorTestVars = ["Start",       #0
                 "OVLD",        #1 
                 "EMGC",        #2
                 "FeedBack",    #3
                 "Running",     #4
                 "Fault",       #5
                 "TimeOutWarn", #6
                 "Coil",        #7
                 "RESET"        #8
                 ]
MotorTestCalib = {'TimeOut' :  6000   #4
                       }


client = Client("opc.tcp://DESKTOP-G25O981:4840") 

tag_struct=MotorTestVars
delay_time=0.05

#Init_tags

    

def OPC_Disconnect():
    client.disconnect()
    
   
def OPC_Connect() :
    
    client.connect()

def getvar():
    root = client.get_root_node()
    objects = client.get_root_node()
 
    return objects

def end_test(tag_struct):
    time.sleep(delay_time)
    reset_tags(tag_struct)
    time.sleep(delay_time)
    u_reset_MotorDriver()
    time.sleep(delay_time)
    reset_tags(tag_struct)
    time.sleep(delay_time)
    assert 0==0
    
    
    
def read_opc_var (objects,var_name) :
    

    var_path=  objects.get_child(["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application" , "3:Programs","4:MotorTest",str("4:")+ str(var_name)])
    var_type= get_opc_var_type(var_path)
    
    return var_path.get_value()

def write_opc_var (objects, var_name, value):
    
    var_path=  objects.get_child(["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application" , "3:Programs","4:MotorTest",str("4:")+ str(var_name)])
    var_type= get_opc_var_type(var_path)
    
    return var_path.set_value(value, var_type)
    
def get_opc_var_type(var):
    
    return var.get_data_type_as_variant_type()

def reset_tags(tag_struct):
    
    objects=getvar()
    
    for i in range  (len(tag_struct)) :
        print(i)
        write_opc_var(objects, tag_struct[i], 0)
        time.sleep(delay_time)
     

def u_reset_MotorDriver():
    objects=getvar()
    write_opc_var(objects, MotorTestVars[8], True)
    
#Init test
def test_init():
    OPC_Connect()
    end_test(tag_struct)

def test_init_tags():
   
    objects=getvar()
    write_opc_var(objects , str(list(MotorTestCalib)[0]) ,int(MotorTestCalib['TimeOut']))
    time.sleep(delay_time)
    
#test_u_ovld
def test_u_md_000 ():
    #Initialize

    objects=getvar()
    
    
    #Activate OVLD
    write_opc_var(objects, MotorTestVars[1], True)
    time.sleep(delay_time)
    
    #Read Fault
    data=read_opc_var(objects, MotorTestVars[5])
    assert data == 1
    
    #End Test
    end_test(MotorTestVars)

#test_u_EMGC    
def test_u_md_001():
    
    #Initialize

    objects=getvar()
    
    #Activate OVLD
    write_opc_var(objects, MotorTestVars[2], True)
    time.sleep(delay_time)
    
    #Read Fault
    data=read_opc_var(objects, MotorTestVars[5])
    assert data == 1

    #End Test
    end_test(MotorTestVars)
    
#test_u_coil    
def test_u_md_002():
    #Initalize
    objects=getvar()
    
    #Activate Start
    write_opc_var(objects, MotorTestVars[0], True)
    time.sleep(delay_time)
    #Read Coil
    data=read_opc_var(objects, MotorTestVars[7])
    assert data == 1
    
    #End Test
    end_test(MotorTestVars)
    
    
    


#test_u_timeout
def test_u_md_003 ():

    #Initalize
    objects=getvar()
    
     
    #Activate start
    write_opc_var(objects, MotorTestVars[0], True)
    time.sleep((MotorTestCalib['TimeOut']+ MotorTestCalib['TimeOut']*0.1)/1000)
    
    #Read TimeoutWarn
    data=read_opc_var(objects, MotorTestVars[6])
    assert data == 1

    #End Test
    end_test(MotorTestVars)
    
#test_u_feedback
def test_u_md_004 ():
    
    #Initalize
    objects=getvar()
    
    #Activate Start
    write_opc_var(objects, MotorTestVars[0], True)
    time.sleep((MotorTestCalib['TimeOut']/2)/1000)
    
    #Activate Feedback
    write_opc_var(objects, MotorTestVars[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 1
    
    end_test(MotorTestVars)
    
#Fault while running
def test_u_md_005():
    
    #Initalize
    objects=getvar()
    
    #Activate Start
    write_opc_var(objects, MotorTestVars[0], True)
    time.sleep((MotorTestCalib['TimeOut']/2)/1000)
    
    #Activate Feedback
    write_opc_var(objects, MotorTestVars[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 1
    
    #Activate OVLD
    write_opc_var(objects, MotorTestVars[2], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 0
    
    #Read Coil
    data=read_opc_var(objects, MotorTestVars[7])
    assert data == 0
    
    #Read Fault Status
    data=read_opc_var(objects, MotorTestVars[5])
    assert data == 1
    
    end_test(MotorTestVars)

#Feedback disconnected while running        
def test_u_md_006():
    
    #Initalize
    objects=getvar()
    
    #Activate Start
    write_opc_var(objects, MotorTestVars[0], True)
    time.sleep((MotorTestCalib['TimeOut']/2)/1000)
    
    #Activate Feedback
    write_opc_var(objects, MotorTestVars[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 1
    
    #Dectivate Feedback
    write_opc_var(objects, MotorTestVars[3], False)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 0
    
    #Wait for Timeout
    time.sleep((MotorTestCalib['TimeOut']+ MotorTestCalib['TimeOut']*0.1)/1000)
    
    #Read TimeoutWarn
    data=read_opc_var(objects, MotorTestVars[6])
    assert data == 1
    
    end_test(MotorTestVars)
    
#Status RESET has no affect while running    
def test_u_md_007():  
    
    #Initalize
    objects=getvar()
    
    #Activate Start
    write_opc_var(objects, MotorTestVars[0], True)
    time.sleep((MotorTestCalib['TimeOut']/2)/1000)
    
    #Activate Feedback
    write_opc_var(objects, MotorTestVars[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 1
    
    #Activate Reset
    write_opc_var(objects, MotorTestVars[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=read_opc_var(objects, MotorTestVars[4])
    assert data == 1
    
    end_test(MotorTestVars)
    
def test_u_disconnect():
    OPC_Disconnect()
    assert 1==1
