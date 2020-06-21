from opcua import Client
from opcua import ua
import py
import time
import pytest


def OPC_Disconnect(client):
    client.disconnect()
    
   
def OPC_Connect(client) :
    
    client.connect()

def getvar(client):
    root = client.get_root_node()
    objects = client.get_root_node()
 
    return objects


def get_opc_var_type(var):
    
    return var.get_data_type_as_variant_type()
    
def read_opc_var (objects,vpath,var_name) :
    
    vpath[len(vpath)-1]=str("4:")+ str(var_name)
    var_path=  objects.get_child(vpath)
    var_type= get_opc_var_type(var_path)
    
    return var_path.get_value()

def write_opc_var (objects,vpath, var_name, value):
    
    vpath[len(vpath)-1]=str("4:")+ str(var_name)
    var_path=  objects.get_child(vpath)
    var_type= get_opc_var_type(var_path)
    
    return var_path.set_value(value, var_type)


def reset_tags(client,tag_struct,varpath):
    
    objects=getvar(client)
    
    for i in range  (len(tag_struct)) :
        
        write_opc_var(objects,varpath, tag_struct[i], 0)
        time.sleep(0.05)
     

def u_reset(client,varpath,reset_tag):
    objects=getvar(client)
    write_opc_var(objects,varpath, reset_tag, True)
    

def end_test(client,tag_struct,varpath, reset_tag):
    time.sleep(0.05)
    reset_tags(client,tag_struct,varpath)
    time.sleep(0.05)
    u_reset(client,varpath,reset_tag)
    time.sleep(0.05)
    reset_tags(client,tag_struct,varpath)
    time.sleep(0.05)

    

    