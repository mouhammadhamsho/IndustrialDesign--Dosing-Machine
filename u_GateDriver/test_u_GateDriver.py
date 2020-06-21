from opcua import Client
import py
import time
import pytest
import Tags
import OPC as server
from importlib import reload
reload(Tags)

#///////////////////Initialize///////////////////
calibTag_struct=Tags.CalibTags
tag_struct= Tags.TestTags
varpath=  Tags.Testpath

client = Client("opc.tcp://DESKTOP-G25O981:4840") 



reset_tag=tag_struct[3]
delay_time=0.05

#///////////////////////////////////////////////////    
"""
TAGS tag_struct

                 "Actuate",     #0
                 "EMGC",        #1 
                 "GateSensor",  #2
                 "Reset",       #3
                 "Coil",        #4
                 "sGateFault",  #5
                 "sGateOpen",   #6
                 
CALIB calibTag_struct

                 'OpenTime' :  7000 ,  #0 
                 'TimeOut' :  6000     #1 

"""
#////////////////////////////////////////////////////
#Init test
def test_init_prg():
    server.OPC_Connect(client)
    server.end_test(client,tag_struct,varpath, reset_tag)

def test_calib_tags():
   
    objects=server.getvar(client)
    for i,key in enumerate(calibTag_struct.keys()):
 
        server.write_opc_var(objects ,varpath, str(list(calibTag_struct)[i]) ,int(calibTag_struct[key]))
        time.sleep(delay_time)

#Test EMGC
def test_u_gd_000():
    
    objects=server.getvar(client)
    
    #Activate EMGC
    server.write_opc_var(objects,varpath, tag_struct[1], True)
    time.sleep(delay_time)
    
        
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    #Activate Actuate
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#Fault Reset
def test_u_gd_001():
    
    objects=server.getvar(client)
    
    #Activate EMGC
    server.write_opc_var(objects,varpath, tag_struct[1], True)
    time.sleep(delay_time)
    
        
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    #Deactivate EMGC
    server.write_opc_var(objects,varpath, tag_struct[1], False)
    time.sleep(delay_time)
    
    #Reset Fault
    server.write_opc_var(objects,varpath, tag_struct[3], True)
    time.sleep(delay_time)
    
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#Actuate Coil Test
def test_u_gd_002():
    
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#Timeout Fault test
def test_u_gd_003():
    
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['TimeOut']+0.1*calibTag_struct['TimeOut'])/1000)
    
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#Open Sensor Test    
def test_u_gd_004():
    
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate GateSensor
    server.write_opc_var(objects,varpath, tag_struct[2], True)
    time.sleep(delay_time)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 1
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#OpenTime Test
def test_u_gd_005():
     
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate GateSensor
    server.write_opc_var(objects,varpath, tag_struct[2], True)
    time.sleep(delay_time)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 1
    
    #Wait for Open Time
    time.sleep((calibTag_struct['OpenTime']-0.1*calibTag_struct['OpenTime'])/1000)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 1
    
    #Wait for Open Time elapse
    time.sleep((0.2*calibTag_struct['OpenTime'])/1000)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 0
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#Operation EMGC
def test_u_gd_006():

    objects=server.getvar(client) 
    
    #Activate Actuate
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['TimeOut']/2)/1000)
    
    #Activate GateSensor
    server.write_opc_var(objects,varpath, tag_struct[2], True)
    time.sleep(delay_time)    
    
    #Activate EMGC
    server.write_opc_var(objects,varpath, tag_struct[1], True)
    time.sleep(delay_time)
    
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    #Read Coil
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#end connection 
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    

 