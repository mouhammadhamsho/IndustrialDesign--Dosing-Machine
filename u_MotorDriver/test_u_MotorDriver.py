from opcua import Client
import py
import time
import pytest
import Tags
import OPC as server
from importlib import reload
reload(Tags)

#///////////////////Initialize///////////////////
calibTag_struct=Tags.MotorCalibTags
tag_struct= Tags.MotorTestTags
varpath=  Tags.MotorTestpath

client = Client("opc.tcp://DESKTOP-G25O981:4840") 



reset_tag=tag_struct[8]
delay_time=0.05

#///////////////////////////////////////////////////    




#Init test
def test_init_prg():
    server.OPC_Connect(client)
    server.end_test(client,tag_struct,varpath, reset_tag)

def test_calib_tags():
   
    objects=server.getvar(client)
    for i,key in enumerate(calibTag_struct.keys()):
 
        server.write_opc_var(objects ,varpath, str(list(calibTag_struct)[i]) ,int(calibTag_struct[key]))
        time.sleep(delay_time)
    
#test_u_ovld
def test_u_md_000 ():
    #Initialize

    objects=server.getvar(client)
    
    
    #Activate OVLD
    server.write_opc_var(objects,varpath, tag_struct[1], True)
    time.sleep(delay_time)
    
    #Read Fault
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    #End Test
    server.end_test(client,tag_struct,varpath, reset_tag)

#test_u_EMGC    
def test_u_md_001():
    
    #Initialize

    objects=server.getvar(client)
    
    #Activate OVLD
    server.write_opc_var(objects,varpath, tag_struct[2], True)
    time.sleep(delay_time)
    
    #Read Fault
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1

    #End Test
    server.end_test(client,tag_struct,varpath, reset_tag)
    
#test_u_coil    
def test_u_md_002():
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[7])
    assert data == 1
    
    #End Test
    server.end_test(client,tag_struct,varpath, reset_tag)
    
    
    


#test_u_timeout
def test_u_md_003 ():

    #Initalize
    objects=server.getvar(client)
    
     
    #Activate start
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep((calibTag_struct['TimeOut']+ calibTag_struct['TimeOut']*0.1)/1000)
    
    #Read TimeoutWarn
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 1

    #End Test
    server.end_test(client,tag_struct,varpath, reset_tag)
    
#test_u_feedback
def test_u_md_004 ():
 
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath, tag_struct[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    server.end_test(client,tag_struct,varpath, reset_tag)
    
#Fault while running
def test_u_md_005():
    
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath, tag_struct[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #Activate OVLD
    server.write_opc_var(objects,varpath, tag_struct[2], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[7])
    assert data == 0
    
    #Read Fault Status
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    server.end_test(client,tag_struct,varpath, reset_tag)

#Feedback disconnected while running        
def test_u_md_006():
    
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath, tag_struct[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #Dectivate Feedback
    server.write_opc_var(objects,varpath, tag_struct[3], False)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    #Wait for Timeout
    time.sleep((calibTag_struct['TimeOut']+ calibTag_struct['TimeOut']*0.1)/1000)
    
    #Read TimeoutWarn
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 1
    
    server.end_test(client,tag_struct,varpath, reset_tag)
    
#Status RESET has no affect while running    
def test_u_md_007():  
    
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath, tag_struct[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #Activate Reset
    server.write_opc_var(objects,varpath, tag_struct[3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    server.end_test(client,tag_struct,varpath, reset_tag)

#end connection 
def test_u_disconnect():
    server.OPC_Disconnect(client)
    

 