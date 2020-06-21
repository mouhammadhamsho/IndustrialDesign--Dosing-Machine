from opcua import Client
import py
import time
import pytest
import Tags
import OPC as server
from importlib import reload
reload(Tags)
reload(server)

#///////////////////Initialize///////////////////
calibTag_struct=Tags.CalibTags
calibTag_path= Tags.Testpath_calibport
tag_struct= [Tags.TestTags_readport, Tags.TestTags_virtctrlport, Tags.TestTags_measport, Tags.TestTags_sendport]
varpath=  [Tags.Testpath_readport, Tags.Testpath_virtctrlport, Tags.Testpath_measport, Tags.Testpath_sendport]

client = Client("opc.tcp://DESKTOP-G25O981:4840") 


#Virtual Control Port
reset_tag=[tag_struct[1][1],tag_struct[1][3]]

delay_time=0.05

#///////////////////////////////////////////////////    
"""
TestTags_readport =       [  "GateEMGC",                  #0
                             "MotorOVLD",                 #1 
                             "MotorEMGC",                 #2
                             "MotorFeedback",             #3
                             "GateOpenSensor"             #4
                                                     
                                         ]




TestTags_virtctrlport =       [
                                 "MotorStart",                #0
                                 "MotorReset",                #1                          
                                 "GateActuate",               #2
                                 "GateReset",                 #3
                                 "FreqScaledValue"            #4
                                 "MixerStartTimer",           #5
                                 
                             
                                         ]



TestTags_sendport =       [
                                 "MotorCoil",                 #0
                                 "FreqAnalogSignal" ,         #1   
                                 "GateCoil"                   #2 
                             
                                         ]
 
TestTags_measport =       [
                                 "MotorsRunning",                #0
                                 "MotorsFault",                  #1                          
                                 "MotorsTimeOutWarn",            #2
                                 "FreqUpperLimitWarn",           #3
                                 "FreqLowerLimitWarn",           #4
                                 "MixersGateFault",              #5
                                 "MixersGateOpen",               #6
                                 "MixerTimerDone",               #7
                                 "MixerElapsedTime"              #8

                             
                                         ]





CalibTags = {'MotorTimeOut'         :  7000 ,      #0 
             'FreqGain'             :  1310.7 ,    #1
             'FreqUpperLimit'       :  40 ,        #2
             'FreqLowerLimit'       :  10,         #3
             'GateOpenTime'         :  3000 ,      #4
             'GateTimeOut'          :  3000 ,      #5
             'MixerPreSetTime'      :  5000        #6
 
             
             }  

"""
#////////////////////////////////////////////////////
def test_init_prg():
    server.OPC_Connect(client)
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
  
def test_calib_tags():
   
    objects=server.getvar(client)
    for i,key in enumerate(calibTag_struct.keys()):
        
        server.write_opc_var(objects ,calibTag_path, str(list(calibTag_struct)[i]) ,calibTag_struct[key])
        time.sleep(delay_time)

 #test_i_OVLD
def test_i_mxr_md_000():
    objects=server.getvar(client)
    
    
    #Activate OVLD
    server.write_opc_var(objects,varpath[0], tag_struct[0][1], True)
    time.sleep(delay_time)
    
    #Read Fault
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][1])
    assert data == 1
    
    #End Test
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
#test_i_EMGC    
def test_i_mxr_md_001():
    
    #Initialize

    objects=server.getvar(client)
    
    #Activate OVLD
    server.write_opc_var(objects,varpath[0], tag_struct[0][1], True)
    time.sleep(delay_time)
    
    #Read Fault
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][1])
    assert data == 1

    #End Test
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#test_i_coil    
def test_i_mxr_md_002():
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time)
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][0])
    assert data == 1
    
    #End Test
    server.end_Component_test(client,tag_struct,varpath, reset_tag)
    
# Test running Status   
def test_i_mxr_md_003():

    #Initalize
    objects=server.getvar(client)
    
     
    #Activate start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep((calibTag_struct['MotorTimeOut']+ calibTag_struct['MotorTimeOut']*0.1)/1000)
    
    #Read TimeoutWarn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][2])
    assert data == 1

    #End Test
    server.end_Component_test(client,tag_struct,varpath, reset_tag)    

#test_i_feedback
def test_i_mxr_md_004():
 
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep((calibTag_struct['MotorTimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath[0], tag_struct[0][3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 1
    
    server.end_Component_test(client,tag_struct,varpath, reset_tag)
    
#Fault while running
def test_i_mxr_md_005():
    
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep((calibTag_struct['MotorTimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath[0], tag_struct[0][3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 1
    
    #Activate OVLD
    server.write_opc_var(objects,varpath[0], tag_struct[0][1], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 0
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][0])
    assert data == 0
    
    #Read Fault Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][1])
    assert data == 1
    
    server.end_Component_test(client,tag_struct,varpath, reset_tag)


#Feedback disconnected while running        
def test_i_mxr_md_006():
    
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep((calibTag_struct['MotorTimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath[0], tag_struct[0][3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 1
    
    #Dectivate Feedback
    server.write_opc_var(objects,varpath[0], tag_struct[0][3], False)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 0
    
    #Wait for Timeout
    time.sleep((calibTag_struct['MotorTimeOut']+ calibTag_struct['MotorTimeOut']*0.1)/1000)
    
    #Read TimeoutWarn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][2])
    assert data == 1
    
    server.end_Component_test(client,tag_struct,varpath, reset_tag)
    
#Status RESET has no affect while running    
def test_i_mxr_md_007():  
    
    #Initalize
    objects=server.getvar(client)
    
    #Activate Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep((calibTag_struct['MotorTimeOut']/2)/1000)
    
    #Activate Feedback
    server.write_opc_var(objects,varpath[0], tag_struct[0][3], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 1
    
    #Activate Reset
    server.write_opc_var(objects,varpath[1], tag_struct[1][1], True)
    time.sleep(delay_time)
    
    #Read Running Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 1
    
    server.end_Component_test(client,tag_struct,varpath, reset_tag)




#Test Max Analog Signal
def test_i_mxr_freq_000():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4], 49.9)
    time.sleep(delay_time)
    
    #Read Output Value
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][1])
    assert data == pytest.approx(65534,1) 
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    

#Test Min Analog Signal
def test_i_mxr_freq_001():
    
    objects=server.getvar(client)
    
     #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4],0)
    time.sleep(delay_time)
    

    #Read Output Value
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][1])
    assert data == pytest.approx(0,0) 
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Test Max Analog Signal Warn
def test_i_mxr_freq_002():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4], 50)
    time.sleep(delay_time)
    
    #Upper limit warn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][3])
    assert data == 1

    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Test Min Analog Signal Warn
def test_i_mxr_freq_003():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4], 0)
    time.sleep(delay_time)
    
    #lower limit warn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][4])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)


#Test EMGC
def test_i_mxr_gd_000():
    
    objects=server.getvar(client)
    
    #Activate EMGC
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], True)
    time.sleep(delay_time)
    
        
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 1
    
    #Activate Actuate
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 0
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)


#Fault Reset
def test_i_mxr_gd_001():
    
    objects=server.getvar(client)
    
    #Activate EMGC
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], True)
    time.sleep(delay_time)
    
       
        
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 1
    
    
    #Activate EMGC
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], False)
    time.sleep(delay_time)
    
    #Reset Fault
    server.write_opc_var(objects,varpath[1], tag_struct[1][3], True)
    time.sleep(delay_time)
    
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 0
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Actuate Coil Test
def test_i_mxr_gd_002():
    
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)


#Timeout Fault test
def test_i_mxr_gd_003():
    
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['GateTimeOut']+0.1*calibTag_struct['GateTimeOut'])/1000)
    
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Open Sensor Test    
def test_i_mxr_gd_004():
    
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['GateTimeOut']+0.1*calibTag_struct['GateTimeOut'])/1000)
    
    #Activate GateSensor
    server.write_opc_var(objects,varpath[0], tag_struct[0][4], True)
    time.sleep(delay_time)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
#OpenTime Test
def test_i_mxr_gd_005():
     
    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['GateTimeOut']+0.1*calibTag_struct['GateTimeOut'])/1000)
    
    #Activate GateSensor
    server.write_opc_var(objects,varpath[0], tag_struct[0][4], True)
    time.sleep(delay_time)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    #Wait for Open Time
    time.sleep((calibTag_struct['GateOpenTime']-0.1*calibTag_struct['GateOpenTime'])/1000)
    
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    #Wait for Open Time elapse
    time.sleep((0.2*calibTag_struct['GateOpenTime'])/1000)
   
    #Read sGateOpen Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 0
    
    #Read coil Status
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 0
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#in Operation EMGC
def test_i_mxr_gd_00():

    objects=server.getvar(client)
    
    #Activate Actuate
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read Coil
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][2])
    assert data == 1
    
    #wait for Timeout
    time.sleep((calibTag_struct['GateTimeOut']+0.1*calibTag_struct['GateTimeOut'])/1000)
    
    #Activate GateSensor
    server.write_opc_var(objects,varpath[0], tag_struct[0][4], True)
    time.sleep(delay_time) 
    
    
    #Activate EMGC
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], True)
    time.sleep(delay_time)
    
        
    #Read sGateFault Status
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

def test_i_mxr_tm_000():
    
    objects=server.getvar(client)
    
    #Activate Start Timer
    server.write_opc_var(objects,varpath[1], tag_struct[1][5], True)
    time.sleep(delay_time)
    
    #Read TimerDone
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][7])
    assert data == 0
    
    #Wait for PresetTime
    time.sleep((calibTag_struct['MixerPreSetTime']+0.1*calibTag_struct['MixerPreSetTime'])/1000)
        
    #Read TimerDone
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][7])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
   
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    
