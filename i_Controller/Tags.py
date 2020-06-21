
TestTags_Mixervirtctrlport =     ["MotorStart",               #0
                                 "MotorReset",                #1                          
                                 "GateActuate",               #2
                                 "GateReset",                 #3
                                 "FreqScaledValue" ,          #4
                                 "MixerStartTimer"]         #5
                             



TestTags_Doservirtctrlport =    ["MotorStart",               #0
                                 "MotorReset",                #1                          
                                 "BunkerDose",                #2
                                 "BunkerReset",               #3
                                 "FreqScaledValue"]           #4
                             
         
                                         
                                         
 
TestTags_Mixermeasport =        ["MotorsRunning",               #0
                                 "MotorsFault",                  #1                          
                                 "MotorsTimeOutWarn",            #2
                                 "FreqUpperLimitWarn",           #3
                                 "FreqLowerLimitWarn",           #4
                                 "MixersGateFault",              #5
                                 "MixersGateOpen",               #6
                                 "MixerTimerDone",               #7
                                 "MixerElapsedTime" ]            #8
                           
                                 
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
                             
                                         

                             
                           


 
 
TestTags_UserInput = ["Start",  #0
                      "Stop",   #1
                      "Reset"   ]#2


TestTags_Status =       ["State",                #0
                        "StatusDosing",         #1
                        "StatusDosingDone",     #2
                        "StatusFault",          #3
                        "StatusMixingDone"      #4
                         ]


 


Testpath_Mixervirtctrlport=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:MixerCtrl","var"]

Testpath_Doser1virtctrlport=    ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:DoserCtrl","4:DoserCtrl[0]","var"]

Testpath_Doser2virtctrlport=    ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:DoserCtrl","4:DoserCtrl[1]","var"]



Testpath_Mixermeasport =       ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:MixerMeas","var"]
                       
Testpath_Doser1measport =       ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:DoserMeas", "4:DoserMeas[0]","var"]

Testpath_Doser2measport =       ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:DoserMeas", "4:DoserMeas[1]","var"]
                                       


Testpath_UserInput=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest", "4:UserInput","var"]

Testpath_Status=     ["0:Objects", "2:DeviceSet", "4:CODESYS Control Win V3 x64",
                                   "3:Resources" , "4:Application"  , "3:Programs","4:Controller_IntegrationTest","4:Status", "var"]