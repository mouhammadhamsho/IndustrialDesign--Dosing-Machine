TestTags_readport =       [  "GateEMGC",                  #0
                             "MotorOVLD",                 #1 
                             "MotorEMGC",                 #2
                             "MotorFeedBack",             #3
                             "GateOpenSensor"             #4
                                                     
                                         ]




TestTags_virtctrlport =       [
                                 "MotorStart",                #0
                                 "MotorReset",                #1                          
                                 "GateActuate",               #2
                                 "GateReset",                 #3
                                 "FreqScaledValue" ,           #4
                                 "MixerStartTimer"           #5
                                 
                             
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
                                 "MixerElapsedTime"            #8

                             
                                         ]





CalibTags = {'MotorTimeOut'         :  7000 ,      #0 
             'FreqGain'             :  1310.7 ,    #1
             'FreqUpperLimit'       :  40 ,        #2
             'FreqLowerLimit'       :  10,         #3
             'GateOpenTime'         :  3000 ,       #4
             'GateTimeOut'          :  3000 ,      #5
             'MixerPreSetTime'      :  5000        #6
 
             
             }  

 
 
 

Testpath_readport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Mixer_IntegrationTest", "4:ReadPort","var"]


Testpath_virtctrlport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Mixer_IntegrationTest", "4:VirtualCtrlPort","var"]


Testpath_calibport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Mixer_IntegrationTest", "4:CalibPort","var"]


Testpath_measport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Mixer_IntegrationTest", "4:MeasPort","var"]

Testpath_sendport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Mixer_IntegrationTest", "4:SendPort","var"]