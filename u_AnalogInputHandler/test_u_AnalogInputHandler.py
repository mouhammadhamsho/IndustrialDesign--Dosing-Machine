from opcua import Client
import py
import time
import pytest
import Tags
import OPC as server


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
                 
                 'Gain'       :  0.076 ,  #0 
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
def test_u_ai_000():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], 65535)
    time.sleep(delay_time)
    
    #Read Scaled Value
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == pytest.approx(50,0.01) 
    
    server.reset_tags(client, tag_struct, varpath)


#Test Min Analog Signal
def test_u_ai_001():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], 0)
    time.sleep(delay_time)
    
    #Read Scaled Value
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == pytest.approx(0,0) 
    
    server.reset_tags(client, tag_struct, varpath)

#Test Max Analog Signal Warn
def test_u_ai_002():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], 65535)
    time.sleep(delay_time)
    
    #Read Scaled Value
    data=server.read_opc_var(objects,varpath, tag_struct[2])
    assert data == 1
    
    server.reset_tags(client, tag_struct, varpath)
    
#Test Min Analog Signal Warn
def test_u_ai_003():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], 0)
    time.sleep(delay_time)
    
    #Read Scaled Value
    data=server.read_opc_var(objects,varpath, tag_struct[3])
    assert data == 1
    
    server.reset_tags(client, tag_struct, varpath)

#end connection 
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    

 