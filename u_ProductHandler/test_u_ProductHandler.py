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



reset_tag=tag_struct[1]
delay_time=0.08

#///////////////////////////////////////////////////    
"""
TAGS tag_struct
                 "Dose",            #0
                 "CurrentWeight",    #1 
                 "Reset",            #2
                 "sDone",            #3
                 "sDosing",          #4
                 "sMinWeightWarn",   #5
                 "sMaxWeightWarn",   #6
                 "sNotEnough",       #7
                 "ExtractedWeight",  #8
                 "ExtraWeight",      #9
                 
CALIB calibTag_struct

             'TargetWeight' :  100 ,  #0 
             'MaxWeightLim' :  6000 , #1 
             'MinWeightLim' :  10     #2 

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
        
#sMaxWeightWarn Test        
def test_u_prdchndl_000():
    
    objects=server.getvar(client) 
    
    #set CurrentWeight>MaxWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 6000.1)
    time.sleep(delay_time)
    
    #Read sMaxWeightWarn
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 1
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0

    server.end_test(client, tag_struct, varpath, reset_tag)
    
#sMinWeightWarn Test        
def test_u_prdchndl_001():
    
    objects=server.getvar(client)
    
    #set CurrentWeight<MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 9.99)
    time.sleep(delay_time)
    
    #Read sMinWeightWarn
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 1
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)
    
#Not Enough Product Test        
def test_u_prdchndl_002():
    
    objects=server.getvar(client)
    
    #set CurrentWeight<TargetWeight
    server.write_opc_var(objects,varpath, tag_struct[1], 99.99)
    time.sleep(delay_time)
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath, tag_struct[7])
    assert data == 1
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)

#Testing sDosing        
def test_u_prdchndl_003():
    
    objects=server.getvar(client)
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 4000)
    time.sleep(delay_time)
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #Read sMaxWieghtLim
    data=server.read_opc_var(objects,varpath, tag_struct[5])
    assert data == 0
    
    #Read sMinWieghtLim
    data=server.read_opc_var(objects,varpath, tag_struct[6])
    assert data == 0
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath, tag_struct[7])
    assert data == 0
    
    
    server.end_test(client, tag_struct, varpath, reset_tag)
 
    
#Testing Extracted Weight        
def test_u_prdchndl_004():
    
    objects=server.getvar(client)
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 4000)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=4000
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time) 
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    # Drop CurrentWeight so that ExtractedWeight=TargetWeight 
    server.write_opc_var(objects,varpath, tag_struct[1], 3950)
    time.sleep(delay_time)
    
    #Read ExtractedWeight
    data=server.read_opc_var(objects,varpath, tag_struct[8])
    assert data == 50
    
    server.end_test(client, tag_struct, varpath, reset_tag)
    
    
#Testing sDone       
def test_u_prdchndl_005():
    
    objects=server.getvar(client)
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 4000)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=4000
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time) 
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    
    # Drop CurrentWeight so that ExtractedWeight=TargetWeight 
    server.write_opc_var(objects,varpath, tag_struct[1], 3900)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    #Read sDone
    data=server.read_opc_var(objects,varpath, tag_struct[3])
    assert data == 1
    
    server.end_test(client, tag_struct, varpath, reset_tag)
    
#Testing Extra Weight        
def test_u_prdchndl_006():
    
    objects=server.getvar(client)
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 4000)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=4000
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time) 
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    # Drop CurrentWeight so that ExtractedWeight=TargetWeight 
    server.write_opc_var(objects,varpath, tag_struct[1], 3890)
    time.sleep(delay_time)
    
    #Read ExtractedWeight
    data=server.read_opc_var(objects,varpath, tag_struct[8])
    assert data == 110
    
     #Read ExtractedWeight
    data=server.read_opc_var(objects,varpath, tag_struct[9])
    assert data == 10
    
    server.end_test(client, tag_struct, varpath, reset_tag)
#end connection 

#Testing sNotEnough during Operation        
def test_u_prdchndl_007():
    
    objects=server.getvar(client)
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 110)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
 
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time) 
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    # Drop CurrentWeight so thatCurrentWeight<TargetWeight 
    server.write_opc_var(objects,varpath, tag_struct[1], 50)
    time.sleep(delay_time)
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath, tag_struct[7])
    assert data == 0
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    #Read sDone
    data=server.read_opc_var(objects,varpath, tag_struct[3])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)


#Testing Resetn        
def test_u_prdchndl_008():
    
    objects=server.getvar(client)
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath, tag_struct[1], 110)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
 
    
    #Activate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], True)
    time.sleep(delay_time) 
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 1
    
    # Drop CurrentWeight so that sDone is activated 
    server.write_opc_var(objects,varpath, tag_struct[1], 5)
    time.sleep(delay_time)
    
    #Deactivate Dose
    server.write_opc_var(objects,varpath, tag_struct[0], False)
    time.sleep(delay_time) 
    
    #Activate Reset
    server.write_opc_var(objects,varpath, tag_struct[2], True)
    time.sleep(delay_time) 
    
    #Read sDone
    data=server.read_opc_var(objects,varpath, tag_struct[3])
    assert data == 0
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath, tag_struct[4])
    assert data == 0
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath, tag_struct[7])
    assert data == 1
    
    #Read sExtractedWeight
    data=server.read_opc_var(objects,varpath, tag_struct[8])
    assert data == 0
    
    #Read sExtraWeight
    data=server.read_opc_var(objects,varpath, tag_struct[9])
    assert data == 0
    
    server.end_test(client, tag_struct, varpath, reset_tag)
    
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    

 