# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "..")
from opcua import ua

from opcua import Client
"""
Created on Tue May  5 01:32:14 2020

@author: Hamsho
"""

client = Client("opc.tcp://DESKTOP-G25O981:4840") 
client.connect()
root = client.get_root_node()
#print("Root node is: {:s} ".format(str(root)))

def browse_recursive(node):
    for childId in node.get_children():
        ch = client.get_node(childId)
       
        if ch.get_node_class() == ua.NodeClass.Object:
            browse_recursive(ch)
        elif ch.get_node_class() == ua.NodeClass.Variable:
            try:
                print(str(ch.get_value()) )
            except ua.uaerrors._auto.BadWaitingForInitialData:
                pass

browse_recursive(root)

 #print("{bn} has value {val}".format(bn=ch.get_browse_name(), val=str(ch.get_value()))  )