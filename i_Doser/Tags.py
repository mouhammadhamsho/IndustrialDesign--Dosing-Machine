TestTags_readport =       [  "WeightAnalogSignal",        #0
                             "MotorOVLD",                 #1 
                             "MotorEMGC",                 #2
                             "MotorFeedback"              #3
                             
                                                     
                                         ]

TestTags_virtctrlport =       [
                                 "MotorStart",                #0
                                 "MotorReset",                #1                          
                                 "BunkerDose",                #2
                                 "BunkerReset",               #3
                                 "FreqScaledValue"            #4
                             
                                         ]


TestTags_sendport =       [
                                 "MotorCoil",                #0
                                 "FreqAnalogSignal"          #1                          
                             
                                         ]
 
TestTags_measport =       [
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
                             
                                         ]

 

CalibTags = {'MotorTimeOut'         :  7000 ,      #0 
             'FreqGain'             :  1310.7 ,    #1
             'FreqUpperLimit'       :  40 ,        #2
             'FreqLowerLimit'       :  10,         #3
             'BunkerTargetWeight'   :  100 ,       #4
             'BunkerMaxWeightLim'   :  5500 ,      #5
             'BunkerMinWeightLim'   :  10,         #6
             'WeightGain'           :  0.76295,     #7
             'WeightUpperLimit'     :  5000,       #8
             'WeightLowerLimit'     :  0           #9
             
             }  

Testpath_readport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Doser_IntegrationTest", "4:ReadPort","var"]


Testpath_virtctrlport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Doser_IntegrationTest", "4:VirtualCtrlPort","var"]


Testpath_calibport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Doser_IntegrationTest", "4:CalibPort","var"]


Testpath_measport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Doser_IntegrationTest", "4:MeasPort","var"]

Testpath_sendport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Doser_IntegrationTest", "4:SendPort","var"]