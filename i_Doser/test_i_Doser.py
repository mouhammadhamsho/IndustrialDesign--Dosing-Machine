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
Tags Read
                                "WeightAnalogSignal",           #0
                                "MotorOVLD",                    #1 
                                "MotorEMGC",                    #2
                                "MotorFeedback"                 #3
Tags virtualctrl

                                 "MotorStart",                  #0
                                 "MotorReset",                  #1                          
                                 "BunkerDose",                  #2
                                 "BunkerReset",                 #3
                                 "FreqScaledValue"              #4


Tags Send 
                                 "MotorCoil",                    #0
                                 "FreqAnalogSignal"              #1  
Tags Meas                                 
                                 "MotorsRunning",                #0
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
                                 "BunkerCurrentWeight",          #12
                 
CALIB calibTag_struct

             'MotorTimeOut'         :  7000 ,      #0 
             'FreqGain'             :  1310.7 ,    #1
             'FreqUpperLimit'       :  40 ,        #2
             'FreqLowerLimit'       :  10,         #3
             'BunkerTargetWeight'   :  100 ,       #4
             'BunkerMaxWeightLim'   :  5000 ,      #5
             'BunkerMinWeightLim'   :  10,         #6
             'WeightGain'           :  0.0007,     #7
             'WeightUpperLimit'     :  5000,       #8
             'WeightLowerLimit'     :  0           #9

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
def test_i_dsr_md_000():
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
def test_i_dsr_md_001():
    
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
def test_i_dsr_md_002():
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
def test_i_dsr_md_003():

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
def test_i_dsr_md_004():
 
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
def test_i_dsr_md_005():
    
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
def test_i_dsr_md_006():
    
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
def test_i_dsr_md_007():  
    
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
def test_i_dsr_freq_000():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4], 50)
    time.sleep(delay_time)
    
    #Read Output Value
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][1])
    assert data == pytest.approx(65534,1) 
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    

#Test Min Analog Signal
def test_i_dsr_freq_001():
    
    objects=server.getvar(client)
    
     #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4],0)
    time.sleep(delay_time)
    

    #Read Output Value
    data=server.read_opc_var(objects,varpath[3], tag_struct[3][1])
    assert data == pytest.approx(0,0) 
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Test Max Analog Signal Warn
def test_i_dsr_freq_002():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4], 50)
    time.sleep(delay_time)
    
    #Upper limit warn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][3])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Test Min Analog Signal Warn
def test_i_dsr_freq_003():
    
    objects=server.getvar(client)
    
    #Stimulate  Signal
    server.write_opc_var(objects,varpath[1], tag_struct[1][4], 0)
    time.sleep(delay_time)
    
    #lower limit warn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][4])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)


#Test Max Analog Signal
def test_i_dsr_ldcl_000():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], 65535)
    time.sleep(delay_time)
    
    #Read Scaled Value
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][12])
    assert data == pytest.approx(5000,20) 
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)     

#Test Min Analog Signal
def test_i_dsr_ldcl_001():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], 0)
    time.sleep(delay_time)
    
    #Read Scaled Value
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][12])
    assert data == pytest.approx(0,0) 
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
    
#Test Max Analog Signal Warn
def test_i_dsr_ldcl_002():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], 65535)
    time.sleep(delay_time)
    #Read Max Warn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][8])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)   
    
def test_i_dsr_ldcl_003():
    
    objects=server.getvar(client)
    
    #Activate Input Signal
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], 0)
    time.sleep(delay_time)
    
    #Read Max Warn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][7])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)  
 
 
#sMaxWeightWarn Test        
def test_i_dsr_prdchndl_000():
    
    objects=server.getvar(client) 
    RequiredWeight=5550
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    print(data)
    #set CurrentWeight>MaxWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Read sMaxWeightWarn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][8])
    assert data == 1
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 0

    server.end_Component_test(client, tag_struct, varpath, reset_tag)


#sMaxWeightWarn Test        
def test_i_dsr_prdchndl_001():
    
    objects=server.getvar(client) 
    RequiredWeight=0
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight<=mineightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Read sMinWeightWarn
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][7])
    assert data == 1
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 0

    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
    
#Not Enough Product Test        
def  test_i_dsr_prdchndl_002():
    
    objects=server.getvar(client)
    RequiredWeight=99.9
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight<TargetWeight
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][9])
    assert data == 1
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 0

    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
#Testing sDosing        
def test_i_dsr_prdchndl_003():
    
    objects=server.getvar(client)
    
    RequiredWeight=4000
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)

    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    #Read sMaxWieghtLim
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][8])
    assert data == 0
    
    #Read sMinWieghtLim
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][7])
    assert data == 0
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][9])
    assert data == 0
    
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Testing Extracted Weight        
def test_i_dsr_prdchndl_004():
    
    objects=server.getvar(client)
    
    RequiredWeight=4000
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=RequiredWeight
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    # Drop CurrentWeight so that ExtractedWeight=TargetWeight 
    RequiredWeight=3950
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Read ExtractedWeight
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][10])
    assert data == pytest.approx(50,5)
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Testing sDosing        
def test_i_dsr_prdchndl_005():
    
    objects=server.getvar(client)
    
    RequiredWeight=4000
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=RequiredWeight
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    
    # Drop CurrentWeight so that ExtractedWeight=TargetWeight 
    RequiredWeight=3870
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 0
    
    #Read sDone
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 1
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)

#Testing Extra Weight        
def test_i_dsr_prdchndl_006():
    
    objects=server.getvar(client)
    
    
    RequiredWeight=4000
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=RequiredWeight
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    
    # Drop CurrentWeight so that ExtractedWeight=TargetWeight 
    RequiredWeight=3880
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Read ExtractedWeight
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][10])
    assert data == pytest.approx(120,3)
    
     #Read Extra Weight
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][11])
    assert data == pytest.approx(20,3)
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
    
#Testing sNotEnough during Operation        
def test_i_dsr_prdchndl_007():
    
    objects=server.getvar(client)
    
    
    RequiredWeight=110
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=RequiredWeight
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    # Drop CurrentWeight so thatCurrentWeight<TargetWeight 
    RequiredWeight=60
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][9])
    assert data == 0
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    #Read sDone
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 0
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)


#Testing Resetn        
def test_i_dsr_prdchndl_008():
    
    objects=server.getvar(client)
   
    RequiredWeight=110
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    #Store CurrentWeight before starting the Dose Operation
    Init_CurrentWeight=RequiredWeight
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], True)
    time.sleep(delay_time)
    
    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 1
    
    # Drop CurrentWeight so thatCurrentWeight<TargetWeight 
    RequiredWeight=60
    data=int(RequiredWeight/calibTag_struct['WeightGain'])
    #set CurrentWeight>TargetWeight AND <MaxWeightLim AND >MinWeightLim
    server.write_opc_var(objects,varpath[0], tag_struct[0][0], data)
    time.sleep(delay_time)
    
    
    #Activate Dose
    server.write_opc_var(objects,varpath[1], tag_struct[1][2], False)
    time.sleep(delay_time)
    
    #Activate Reset
    server.write_opc_var(objects,varpath[1], tag_struct[1][3], True)
    time.sleep(delay_time) 
    
    #Read sDone
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][5])
    assert data == 0
    

    #Read sDosing
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][6])
    assert data == 0
    
    #Read sNotEnough
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][9])
    assert data == 1
    
    #Read ExtractedWeight
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][10])
    assert data == 0
    
     #Read Extra Weight
    data=server.read_opc_var(objects,varpath[2], tag_struct[2][11])
    assert data == 0
    
    server.end_Component_test(client, tag_struct, varpath, reset_tag)
def test_u_disconnect():
    
    server.OPC_Disconnect(client)
    
