import pytest
import sys
sys.path.insert(0, "..")
from opcua import ua
from opcua import Client

def readVAR(x,expected):
    assert x == expected ,"Test Failed"
    
def OPC_Connect() :
    client = Client("opc.tcp://DESKTOP-G25O981:4840") 
    client.connect()
    root = client.get_root_node()
    objects = client.get_root_node()
     
    return objects

def getMeasDoser0 (var) :
    return    objects.get_child(["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application" , "3:GlobalVars" , "4:Measurement","4:DoserMeas",
                                          "4:DoserMeas[0]",str("4:")+ str(var)])
def getMeasDoser1 (var) :
    return    objects.get_child(["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application" , "3:GlobalVars" , "4:Measurement","4:DoserMeas",
                                          "4:DoserMeas[1]",str("4:")+ str(var)])
    
def getMeasMixer (var) :
    return    objects.get_child(["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application" , "3:GlobalVars" , "4:Measurement","4:MixerMeas",
                                          str("4:")+ str(var)])
def setCalibDoser0(var) :
    return    objects.get_child(["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                 "3:Resources" , "4:Application" , "3:GlobalVars" , "4:Calibration","4:DoserCalib",
                                   "4:DoserCalib[0]",str("4:")+ str(var)])

if __name__ == "__main__":


    objects=OPC_Connect()

        
                                             
     #   print(myval.get_value())
      #  myval.set_value(True)

   
    MixerMeas= ["MotorsRunning",      #0
                "MotorsFault",        #1
                "MotorsTimeOutWarn",  #2
                "MixersGateFault",    #3
                "MixersGateOpen",     #4
                "MixerTimerDone",     #5
                "MixerElapsedTime",   #6
                "FreqUpperLimitWarn" ,#7
                "FreqLowerLimitWarn" ,#8
                "FreqScaledValue"     #9
                ]
    
    
    DoserMeas= ["MotorsRunning",        #0			 
	            "MotorsFault",          #1				 
	            "MotorsTimeOutWarn",    #2		 
	            "FreqUpperLimitWarn",   #3		 
	            "FreqLowerLimitWarn",   #4		 
	            "BunkersDone",          #5  
	            "BunkersDosing",        #6
				"BunkersMinWeightWarn", #7 
	            "BunkersMaxWeightWarn", #8	 
                "BunkersNotEnough",	    #9
                "BunkerExtractedWeight",#10	
                "BunkerExtraWeight",	#11
                "BunkerCurrentWeight",	#12
                 ]
    
	
    DoserCalib= [ "MotorTimeOut",           #0
                  "FreqGain",               #1
                  "FreqUpperLimit",         #2
                  "FreqLowerLimit",         #3
                  "BunkerTargetWeight",     #4
                  "BunkerMaxWeightLim",     #5
                  "BunkerMinWeightLim",     #6
                  "WeightGain",             #7
                  "WeightUpperLimit",       #8
                  "WeightLowerLimit"        #9
              
                ]



 
		 
  #  for i in range (0,12):
  #      print(getMeasDoser0(DoserMeas[i]).get_value())
        
  #  for i in range (0,12):
  #      print(getMeasDoser1(DoserMeas[i]).get_value())
    
  #  for i in range (0,9):
  #      print(getMeasMixer(MixerMeas[i]).get_value())
    
    print(setCalibDoser0(DoserCalib[1]).set_value(200,ua.VariantType.Float))
    
    