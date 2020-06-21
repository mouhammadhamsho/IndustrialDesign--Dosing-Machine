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
tag_struct= [Tags.TestTags_Mixermeasport,       #0
             Tags.TestTags_UserInput,           #1
             Tags.TestTags_Mixervirtctrlport,   #2
             Tags.TestTags_Dosermeasport,       #3
             Tags.TestTags_Doservirtctrlport,   #4
             Tags.TestTags_Dosermeasport,       #5
             Tags.TestTags_Doservirtctrlport,   #6
             Tags.TestTags_Status                #7
             ]           


varpath=  [Tags.Testpath_Mixermeasport,         #0
           Tags.Testpath_UserInput,             #1
           Tags.Testpath_Mixervirtctrlport,     #2
           Tags.Testpath_Doser1measport,        #3
           Tags.Testpath_Doser1virtctrlport,    #4
           Tags.Testpath_Doser2measport,        #5
           Tags.Testpath_Doser2virtctrlport,    #6
           Tags.Testpath_Status                 #7
           ]             


client = Client("opc.tcp://DESKTOP-G25O981:4840") 


#Virtual Control Port
reset_tag=[tag_struct[1][2]]

delay_time=0.5

#///////////////////////////////////////////////////    
"""

2
TestTags_Mixervirtctrlport =     ["MotorStart",               #0
                                 "MotorReset",                #1                          
                                 "GateActuate",               #2
                                 "GateReset",                 #3
                                 "FreqScaledValue" ,          #4
                                 "MixerStartTimer"]         #5
                             


4 6
TestTags_Doservirtctrlport =    ["MotorStart",               #0
                                 "MotorReset",                #1                          
                                 "BunkerDose",                #2
                                 "BunkerReset",               #3
                                 "FreqScaledValue"]           #4
                             
         
                                         
                                         
0
TestTags_Mixermeasport =        ["MotorsRunning",               #0
                                 "MotorsFault",                  #1                          
                                 "MotorsTimeOutWarn",            #2
                                 "FreqUpperLimitWarn",           #3
                                 "FreqLowerLimitWarn",           #4
                                 "MixersGateFault",              #5
                                 "MixersGateOpen",               #6
                                 "MixerTimerDone",               #7
                                 "MixerElapsedTime" ]            #8
                           
3 5                             
TestTags_Dosermeasport =        ["MotorsRunning",                #0
                                 "MotorsFault",                  #1                          
                                 "MotorsTimeOutWarn",            #2
                                 "FreqUpperLimitWarn",           #3
                                 "FreqLowerLimitWarn",           #4
                                 "BunkersDone",                  #5
                                 "BunkersDosing",                #6
                                 "BunkersMinWeightWarn",         #7
                                 "BunkersMaxWeightWarn",         #8
                                 "BunkersNotEnough",             #9
                                 "BunkerExtractedWeight",        #10
                                 "BunkerExtraWeight",            #11
                                 "BunkerCurrentWeight"]          #12
                             
                                         
1
TestTags_serInput = ["Start",  #0
                      "Stop",   #1
                      "Reset"   #2
                      ]
7

TestTags_Status =      ["State",                #0
                        "StatusDosing",         #1
                        "StatusDosingDone",     #2
                        "StatusFault",          #3
                        "StatusMixingDone"      #4
                         ]





 

"""
#////////////////////////////////////////////////////
def test_init_prg():
    server.OPC_Connect(client)
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
#Testing FSM reset

def test_i_fsm_000():
        #Initialize

    objects=server.getvar(client)
    
    #Activate RESET
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    

    #Read MixerMotor Reset
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][3])
    assert data == 1
    
    #Read DoserMotor 1 Reset
    data=server.read_opc_var(objects,varpath[4], tag_struct[4][1])
    assert data == 1
    
      
    
    #Read DoserMotor 2 Reset
    data=server.read_opc_var(objects,varpath[6], tag_struct[6][1])
    assert data == 1
    
    time.sleep(1.1)  
    
    #Read MixerMotor Reset
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][3])
    assert data == 0
    
    #Read DoserMotor 1 Reset
    data=server.read_opc_var(objects,varpath[4], tag_struct[4][1])
    assert data == 0
    
      
    
    #Read DoserMotor 2 Reset
    data=server.read_opc_var(objects,varpath[6], tag_struct[6][1])
    assert data == 0
    
    
    #Read Status
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 0

    #End Test
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
# Testing Start lock on Fault
def test_i_fsm_001():
     
    objects=server.getvar(client)
    
    #Activate Mixer Motor Fault
    server.write_opc_var(objects,varpath[0], tag_struct[0][1], True)
    time.sleep(delay_time)
    
    #Read MixerMotor Reset
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][3])
    assert data == 1
     
    #De-activate Mixer Motor Fault
    server.write_opc_var(objects,varpath[0], tag_struct[0][1], False)
    time.sleep(delay_time)
#Testing Dosing Done Status    
def test_i_fsm_002():
    
    objects=server.getvar(client)
    
    #Activate BunkersDone 1,2
    server.write_opc_var(objects,varpath[3], tag_struct[3][5], True)
    server.write_opc_var(objects,varpath[5], tag_struct[5][5], True)
    time.sleep(delay_time) 
    
    #Read StatusDosingDone
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][2])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
#Testing Dosing Status
def test_i_fsm_003():
    
    objects=server.getvar(client)
    
    #Activate BunkersDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], True)
    time.sleep(delay_time) 
    
    #Read StatusDosing
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][1])
    assert data == 1
    
    #De-Activate BunkersDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], False)
    time.sleep(delay_time)
    #Read StatusDosing
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][1])
    assert data == 0
    
    #Activate BunkerDosing 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][6], True)
    time.sleep(delay_time)
    
    #Read StatusDosing
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][1])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
def test_i_fsm_004():
    
    objects=server.getvar(client)
    
    #Activate MixerTimerDone
    server.write_opc_var(objects,varpath[0], tag_struct[0][7], True)
    time.sleep(delay_time) 
    
    
    #Read StatusMixer
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][4])
    assert data == 1

    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
# Testing Start 
def test_i_fsm_005():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 1

    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
    
#Testing state 1 transition
def test_i_fsm_006():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 1
    
    #Read Mixer Start
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][0])
    assert data == 1
    
    #Read Doser 1 Start
    data=server.read_opc_var(objects,varpath[4], tag_struct[4][0])
    assert data == 1
    
    #Read Doser 2 Start
    data=server.read_opc_var(objects,varpath[6], tag_struct[6][0])
    assert data == 1
    
    #Read BunkerDose 1 
    data=server.read_opc_var(objects,varpath[4], tag_struct[4][2])
    assert data == 1
    
    #Read BunkerDose 2 
    data=server.read_opc_var(objects,varpath[6], tag_struct[6][2])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
#Testing State 2 Transition
def test_i_fsm_007():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 1
    
    #Activate BunkerDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], True)
    time.sleep(delay_time)
    
    #Activate BunkerDosing 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][6], True)
    time.sleep(delay_time)
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 2
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
#Transit to State 3,4
def test_i_fsm_008():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 1
    
    #Activate BunkerDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], True)
    time.sleep(delay_time)
    
    #Activate BunkerDosing 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][6], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][5], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][5], True)
    time.sleep(delay_time)
    

    
    #Read MotorStart 1
    data=server.read_opc_var(objects,varpath[4], tag_struct[4][0])
    assert data == 0
  
    #Read MotorStart 2
    data=server.read_opc_var(objects,varpath[6], tag_struct[6][0])
    assert data == 0
    
    #Read MixerStart Timer
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 1    
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 4
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
# Testing Transition to state 6
def test_i_fsm_009():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    
    #Activate BunkerDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], True)
    time.sleep(delay_time)
    
    #Activate BunkerDosing 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][6], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][5], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][5], True)
    time.sleep(delay_time)
    
    #Activate MixerTimingDone 
    server.write_opc_var(objects,varpath[0], tag_struct[0][7], True)
    time.sleep(delay_time)
    
    #Read GateActuate
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][2])
    assert data == 1
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 6
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
#Testing Transition to state 7
def test_i_fsm_010():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    
    #Activate BunkerDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], True)
    time.sleep(delay_time)
    
    #Activate BunkerDosing 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][6], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][5], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][5], True)
    time.sleep(delay_time)
    
    #Activate MixerTimingDone 
    server.write_opc_var(objects,varpath[0], tag_struct[0][7], True)
    time.sleep(delay_time)
    
    #Activate MixerGateOpen
    server.write_opc_var(objects,varpath[0], tag_struct[0][6], True)
    time.sleep(delay_time)
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 7
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
 
def test_i_fsm_011():

    objects=server.getvar(client)
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], True)
    time.sleep(delay_time) 
    
    #Activate FSM Start
    server.write_opc_var(objects,varpath[1], tag_struct[1][0], False)
    time.sleep(delay_time) 
    
    
    #Activate BunkerDosing 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][6], True)
    time.sleep(delay_time)
    
    #Activate BunkerDosing 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][6], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 1
    server.write_opc_var(objects,varpath[3], tag_struct[3][5], True)
    time.sleep(delay_time)
    
    #Activate DoserDone 2
    server.write_opc_var(objects,varpath[5], tag_struct[5][5], True)
    time.sleep(delay_time)
    
    #Activate MixerTimingDone 
    server.write_opc_var(objects,varpath[0], tag_struct[0][7], True)
    time.sleep(delay_time)
    
    #Activate MixerGateOpen
    server.write_opc_var(objects,varpath[0], tag_struct[0][6], True)
    time.sleep(10)
    
    #De-Activate MixerGateOpen
    server.write_opc_var(objects,varpath[0], tag_struct[0][6], False)
    time.sleep(delay_time)
    
    #Read GateActuate
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][2])
    assert data == 0
    
    #Read State
    data=server.read_opc_var(objects,varpath[7], tag_struct[7][0])
    assert data == 0

    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
    
def test_u_disconnect():
    
    server.OPC_Disconnect(client)


