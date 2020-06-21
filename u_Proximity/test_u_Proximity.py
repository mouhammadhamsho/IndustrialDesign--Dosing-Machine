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

                  "InputSignal",    #0
                  "Latch"           #1 
                 
CALIB calibTag_struct
             
                  'ONdelay'  :  5000 ,   #0 
                  'OFFdelay' :  3000     #1

"""
#////////////////////////////////////////////////////
#Init test
def test_init_prg():
    server.OPC_Connect(client)
    server.reset_tags(client, tag_struct, varpath)
    time.sleep((calibTag_struct['OFFdelay']+0.1*calibTag_struct['OFFdelay'])/1000)

def test_calib_tags():
   
    objects=server.getvar(client)
    for i,key in enumerate(calibTag_struct.keys()):
 
        server.write_opc_var(objects ,varpath, str(list(calibTag_struct)[i]) ,int(calibTag_struct[key]))
        time.sleep(delay_time)

#Test ONdelay
def test_u_px_000():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
        
    #Read Latch
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 0
    
    #Wait for TON delay
    time.sleep((calibTag_struct['ONdelay']+0.1*calibTag_struct['ONdelay'])/1000)
    
    #Read Latch
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 1
    
    server.reset_tags(client, tag_struct, varpath)
    time.sleep((calibTag_struct['OFFdelay']+0.1*calibTag_struct['OFFdelay'])/1000)

#Test OFFdelay
def test_u_px_001():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
        
    #Read Latch
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 0
    
    #Wait for TON delay
    time.sleep((calibTag_struct['ONdelay']+0.1*calibTag_struct['ONdelay'])/1000)
    
    #Read Latch
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 1
    
    #Deactivate Input Signal
    server.write_opc_var(objects,varpath, tag_struct[0], False)
    time.sleep(delay_time)
  
    #Wait for Toff delay
    time.sleep((calibTag_struct['ONdelay']+0.1*calibTag_struct['ONdelay'])/1000)
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 0
    
    server.reset_tags(client, tag_struct, varpath)
    time.sleep((calibTag_struct['OFFdelay']+0.1*calibTag_struct['OFFdelay'])/1000)

#end connection 
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    

 