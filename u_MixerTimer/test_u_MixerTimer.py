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
                 "Start",           #0
                 "TimerDone"        #1 
   

              

CALIB calibTag_struct

                 'PresetTime' :  7000   #0 

"""
#////////////////////////////////////////////////////
#Init test
def test_init_prg():
    server.OPC_Connect(client)
    server.reset_tags(client, tag_struct, varpath)

def test_calib_tags():
   
    objects=server.getvar(client)
    for i,key in enumerate(calibTag_struct.keys()):
 
        server.write_opc_var(objects ,varpath, str(list(calibTag_struct)[i]) ,int(calibTag_struct[key]))
        time.sleep(delay_time)

#Test EMGC
def test_u_mxt_000():
    
    objects=server.getvar(client)
    
    #Activate Start Timer
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read TimerDone
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 0
    
    #Wait for PresetTime
    time.sleep((calibTag_struct['PresetTime']+0.1*calibTag_struct['PresetTime'])/1000)
        
    #Read TimerDone
    data=server.read_opc_var(objects,varpath, tag_struct[1])
    assert data == 1
    
    server.reset_tags(client, tag_struct, varpath)


#end connection 
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    

 