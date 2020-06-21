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



delay_time=0.05

#///////////////////////////////////////////////////    
"""
TAGS tag_struct

                  "AnalogSignal",    #0
                  "ScaledValue" ,    #1 
                  "UpperLimitWarn" , #2 
                  "LowerLimitWarn"   #3  
                 
CALIB calibTag_struct
                 
                 'Gain'       :  1310.7 ,  #0 
                 'UpperLimit' :  40 ,      #1 
                 'LowerLimit' :  10        #2 

"""
#////////////////////////////////////////////////////
#Init test
def test_init_prg():
    server.OPC_Connect(client)
    server.reset_tags(client, tag_struct, varpath)
    

def test_calib_tags():
   
    objects=server.getvar(client)
    for i,key in enumerate(calibTag_struct.keys()):
 
        server.write_opc_var(objects ,varpath, str(list(calibTag_struct)[i]) ,(calibTag_struct[key]))
        time.sleep(delay_time)

#Test Max Analog Signal
def test_u_ao_000():
    
    objects=server.getvar(client)
    
    #Stimulate signal
    server.write_opc_var(objects,varpath, tag_struct[1], 50)
    time.sleep(delay_time)
    
    #Read Output value
    data=server.read_opc_var(objects,varpath, tag_struct[0])
    assert data == pytest.approx(65535,1) 
    
    server.reset_tags(client, tag_struct, varpath)


#Test Min Analog Signal
def test_u_ao_001():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath, tag_struct[1], 0)
    time.sleep(delay_time)
    
    #Read Output value
    data=server.read_opc_var(objects,varpath, tag_struct[0])
    assert data == pytest.approx(0,0) 
    
    server.reset_tags(client, tag_struct, varpath)

#Test Max Analog Signal Warn
def test_u_ao_002():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[1],50)
    time.sleep(delay_time)
    
    #Read Upperlimit warn
    data=server.read_opc_var(objects,varpath, tag_struct[2])
    assert data == 1
    
    server.reset_tags(client, tag_struct, varpath)
    
#Test Min Analog Signal Warn
def test_u_ao_003():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[1], 0)
    time.sleep(delay_time)
    
    #Read Lower limit warning
    data=server.read_opc_var(objects,varpath, tag_struct[3])
    assert data == 1
    
    server.reset_tags(client, tag_struct, varpath)

#end connection 
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    

 