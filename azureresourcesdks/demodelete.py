from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql.models import ServerForCreate, ServerPropertiesForDefaultCreate, ServerVersion
import os
import random

credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = "3cc010e2-0a53-40f5-a317-f9d7c9233f09"
# Obtain the management object for resources, using the credentials from the CLI login.
resource_client = ResourceManagementClient(credential, subscription_id)

network_client = NetworkManagementClient(credential, subscription_id)

compute_client = ComputeManagementClient(credential, subscription_id)

LOCATION = "centralus "
RESOURCE_GROUP_NAME='PythonAzureExample-VM-rg'

# Delete the Virtual Machine
print("===============================================\n")
print("I am deleting the First virtual Machine")
print("===============================================\n")
virtual_machine_name='ExampleVM'
delete_virtual_machine=compute_client.virtual_machines.begin_delete(
      RESOURCE_GROUP_NAME,
      virtual_machine_name,
).result()
print("Finally Deleted the First virtual machine.\n")
# Delete the second virtual Machine
print("===============================================\n")
print("I am deleting the second virtual Machine")
print("===============================================\n")
virtual_machine_name='ExampleVM-1'
delete_virtual_machine=compute_client.virtual_machines.begin_delete(
      RESOURCE_GROUP_NAME,
      virtual_machine_name,
).result()
print("Finally Deleted the Second virtual machine.\n")
# Delete the First NIC
print("==============================================\n")
print("I am deleting the first NIC")
print("==============================================\n")
NIC_NAME="python-example-nic-1"
nic_delete=network_client.network_interfaces.begin_delete(
    RESOURCE_GROUP_NAME,
    NIC_NAME,

).result()
print("Finally Deleted the first NIC")
# Delete the First NIC
print("==============================================\n")
print("I am deleting the Second NIC")
print("==============================================\n")
NIC_NAME="python-example-nic-2"
nic_delete=network_client.network_interfaces.begin_delete(
    RESOURCE_GROUP_NAME,
    NIC_NAME,

).result()
print("Finally Deleted the Second NIC")

#Delete First Public IP Address
print("============================================\n")
print("I am deleting the first public ip")
print("============================================\n")
PUBLIC_IP_ADDRESS='python-example-ip'
public_ip_address = network_client.public_ip_addresses.begin_delete(
    RESOURCE_GROUP_NAME,
    PUBLIC_IP_ADDRESS,
).result()
print("Finally Deleted the first Public IP Address.\n")
# Delete the Second Public IP Address
print("============================================\n")
print("I am deleting the second public ip")
print("============================================\n")
PUBLIC_IP_ADDRESS='python-example-ip-2'
public_ip_address = network_client.public_ip_addresses.begin_delete(
    RESOURCE_GROUP_NAME,
    PUBLIC_IP_ADDRESS,
).result()
print("Finally Deleted the second Public IP Address.\n")
# Delete the First Subnet
print("============================================\n")
print("I am deleting the first Subnet")
print("============================================\n")
SUBNET_NAME="python-example-subnet-1"
virtual_network_name="python-example-vnet"
delete_vnet=network_client.subnets.begin_delete(
    RESOURCE_GROUP_NAME,
    virtual_network_name,
    SUBNET_NAME,
).result()
print("Finally Deleted the first subnet")
# Delete the second Subnet
print("============================================\n")
print("I am deleting the second Subnet")
print("============================================\n")
SUBNET_NAME="python-example-subnet-2"
virtual_network_name="python-example-vnet"
delete_vnet=network_client.subnets.begin_delete(
    RESOURCE_GROUP_NAME,
    virtual_network_name,
    SUBNET_NAME,
).result()
print("Finally Deleted the second subnet")
# Delete the Virtual Network
print("===========================================\n")
print("I am deleting the virtual Network")
print("===========================================\n")
VNET_NAME = "python-example-vnet"
delete_vnet=network_client.virtual_networks.begin_delete(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
).result()
print("Finally  Deleted the virtual Network")
mysql_client = MySQLManagementClient(credential, subscription_id)
SERVER_NAME=os.environ.get("DB_SERVER_NAME", f"PythonAzureExample-MySQL-{random.randint(1,100000):05}")
# print("============================================\n")
# print("I am deleting the firewell rule on seerver")
# print("========================================\n")
# RULE_NAME = "allow_ip"
# delete_firewell_rule = mysql_client.firewall_rules.begin_delete(
#     RESOURCE_GROUP_NAME,
#     SERVER_NAME,
#     RULE_NAME,
# ).result()
# print("Finally deleted the firewell rules")
# print(" I am deleting the sql data bases")
# db_name='example-db1'
# delete_db=mysql_client.databases.begin_delete(
#     RESOURCE_GROUP_NAME,
#     SERVER_NAME,
#     db_name,
# ).result()
# print("Finally deleted the sql data bases")
print("==========================================\n")
print("I am deleting the sql server")
print("==========================================\n")
delete_server=mysql_client.servers.begin_delete(
    RESOURCE_GROUP_NAME,
    SERVER_NAME,
).result()
print("Finally deleted the server")
# Delete the Resource Group
print("============================================\n")
print("I am deleting in Resource Group")
print("============================================\n")
delete_resource_group = resource_client.resource_groups.begin_delete(
    RESOURCE_GROUP_NAME,
    
).result()
print("Finally Deleted the resource group.\n")
# delete the Network Security Group

 
