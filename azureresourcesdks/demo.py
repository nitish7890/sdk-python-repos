import random
from azure.identity import AzureCliCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql.models import ServerForCreate, ServerPropertiesForDefaultCreate, ServerVersion
from azure.mgmt.network.v2017_03_01.models import NetworkSecurityGroup
from azure.mgmt.network.v2017_03_01.models import SecurityRule
import os
import json
import requests



credential = AzureCliCredential()

# Retrieve subscription ID from environment variable.
subscription_id = "3cc010e2-0a53-40f5-a317-f9d7c9233f09"

# Obtain the management object for resources, using the credentials from the CLI login.
resource_client = ResourceManagementClient(credential, subscription_id)
# create a resource group
RESOURCE_GROUP_NAME = "PythonAzureExample-VM-rg"
LOCATION = "centralus "

# Provision the resource group.
rg_result = resource_client.resource_groups.create_or_update(RESOURCE_GROUP_NAME,
    {
         "location": LOCATION
    }
)
print(f"resource group {rg_result.name} in the {rg_result.location}")
# Network and IP address names
VNET_NAME = "python-example-vnet"
# Obtain the management object for networks
network_client = NetworkManagementClient(credential, subscription_id)
# # # Provision the virtual network and wait for completion
print("I am creating the virtual Network")
poller = network_client.virtual_networks.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    VNET_NAME,
    {
        "location": LOCATION,
        "address_space": {
            "address_prefixes": ["10.0.0.0/16"]
        }
    }
)
vnet_result = poller.result()
print(f" virtual network {vnet_result.name} with address prefixes {vnet_result.address_space.address_prefixes}")
# # Step 3: Provision the subnet and wait for completion
print("I am creating the first subnet")
SUBNET_NAME = "python-example-subnet-1"
poller = network_client.subnets.begin_create_or_update(
    RESOURCE_GROUP_NAME, 
    VNET_NAME, 
    SUBNET_NAME,
    { 
        "address_prefix": "10.0.0.0/24" 
    }
)
subnet_result = poller.result()
print(f"virtual subnet {subnet_result.name} with address prefix {subnet_result.address_prefix}")
# # create the second subnet
print("I am creating the second subnet")
SUBNET_NAME = "python-example-subnet-2"
poller1 = network_client.subnets.begin_create_or_update(
    RESOURCE_GROUP_NAME, 
    VNET_NAME, 
    SUBNET_NAME,
    {
        "address_prefix": "10.0.1.0/24"
    }
)
subnet_result1 = poller1.result()
print(f" virtual subnet {subnet_result1.name} with address prefix {subnet_result1.address_prefix}")


# # Step 4: Provision an IP address and wait for completion
print("I am creating the first public ip address")
IP_NAME = "python-example-ip"
poller = network_client.public_ip_addresses.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    IP_NAME,
     {
         "location": LOCATION,
         "sku": { "name": "Standard" },
         "public_ip_allocation_method": "Static",
         "public_ip_address_version" : "IPV4"
      }
 )

ip_address_result = poller.result()
print(f" public IP address {ip_address_result.name} with address {ip_address_result.ip_address}")


# # create the first NIC
print("I am creating the first NIC")
NIC_NAME = "python-example-nic-1"
IP_CONFIG_NAME = "python-example-ip-config"
poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
    NIC_NAME, 
     {
         "location": LOCATION,
         "ip_configurations": [ {
            "name": IP_CONFIG_NAME,
             "subnet": { "id": subnet_result.id },
             "public_ip_address": {"id": ip_address_result.id }
         }]
     }
)

nic_result = poller.result()
print(f" network interface client {nic_result.name}")



# # # create the second public ip address
print("I am creating the second public ip address")
IP_NAME = "python-example-ip-2"
poller = network_client.public_ip_addresses.begin_create_or_update(RESOURCE_GROUP_NAME,
    IP_NAME,
    {
        "location": LOCATION,
        "sku": { "name": "Standard" },
        "public_ip_allocation_method": "Static",
        "public_ip_address_version" : "IPV4"
    }
)

ip_address_result1 = poller.result()

print(f" public IP address {ip_address_result1.name} with address {ip_address_result1.ip_address}")



# # Step 5: Provision the network interface client
print("I am creating the Second NIC")
NIC_NAME = "python-example-nic-2"
IP_CONFIG_NAME = "python-example-ip-config"
poller = network_client.network_interfaces.begin_create_or_update(RESOURCE_GROUP_NAME,
    NIC_NAME, 
    {
        "location": LOCATION,
         "ip_configurations": [ {
             "name": IP_CONFIG_NAME,
             "subnet": { "id": subnet_result1.id },
             "public_ip_address": {"id": ip_address_result1.id }
         }]
     }
 )

nic_result1 = poller.result()
print(f" network interface client {nic_result1.name}")




# # # Obtain the management object for virtual machines
compute_client = ComputeManagementClient(credential, subscription_id)
print("I am creating the first virtual Machine")
VM_NAME = "ExampleVM"
USERNAME = "azureuser"
PASSWORD = "ChangePa$$w0rd24"
print(f" virtual machine {VM_NAME}; this operation might take a few minutes.")
poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": 'Canonical',
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest"
            }
        },
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD
        },
        "network_profile": {
            "network_interfaces": [{
                "id": nic_result.id,
            }]
        }        
    }
)
vm_result = poller.result()
print(f" virtual machine {vm_result.name}")


print("I am creating the second virtual Machine")
VM_NAME = "ExampleVM-1"
USERNAME = "azureuser1"
PASSWORD = "Nitish@1997"
print(f" virtual machine {VM_NAME}; this operation might take a few minutes.")
poller = compute_client.virtual_machines.begin_create_or_update(RESOURCE_GROUP_NAME, VM_NAME,
    {
        "location": LOCATION,
        "storage_profile": {
            "image_reference": {
                "publisher": 'Canonical',
                "offer": "UbuntuServer",
                "sku": "16.04.0-LTS",
                "version": "latest"
            }
        },
        "hardware_profile": {
            "vm_size": "Standard_DS1_v2"
        },
        "os_profile": {
            "computer_name": VM_NAME,
            "admin_username": USERNAME,
            "admin_password": PASSWORD
        },
        "network_profile": {
            "network_interfaces": [{
                "id": nic_result1.id,
            }]
        }        
    }
)
vm_result = poller.result()
print(f" virtual machine {vm_result.name}")


# # # create a sql server
mysql_client = MySQLManagementClient(credential, subscription_id)
db_server_name = os.environ.get("DB_SERVER_NAME", f"PythonAzureExample-MySQL-{random.randint(1,100000):05}")
db_admin_name = os.environ.get("DB_ADMIN_NAME", "azureuser")
db_admin_password = os.environ.get("DB_ADMIN_PASSWORD", "ChangePa$$w0rd24")
print("=======================================\n")
print("I am creating the sql server")
poller = mysql_client.servers.begin_create(
    RESOURCE_GROUP_NAME,
    db_server_name, 
    ServerForCreate(
        location=LOCATION,
        properties=ServerPropertiesForDefaultCreate(
            administrator_login=db_admin_name,            
            administrator_login_password=db_admin_password,
            version=ServerVersion.FIVE7
        )
    )
)
server = poller.result()
print(f"Provisioned MySQL server {server.name}")
print("Finally created the sql server")
# # Step 4: Provision a database on the server
db_name = os.environ.get("DB_NAME", "example-db1")
print("====================================\n")
print("I am creating the data bases")
print("=====================================\n")
poller = mysql_client.databases.begin_create_or_update(
    RESOURCE_GROUP_NAME,
    db_server_name, 
    db_name, {})

db_result = poller.result()
print(f"Provisioned MySQL database {db_result.name} with ID {db_result.id}")
print("Finally created the data base")
# create a firewell Rule
print("=========================================\n")
print("I am creating the firewell Rule")
print("=========================================\n")
RULE_NAME = "allow_ip"
ip_address = ip_address_result.ip_address
poller = mysql_client.firewall_rules.begin_create_or_update(RESOURCE_GROUP_NAME,
    db_server_name, RULE_NAME, 
    { "start_ip_address": ip_address, "end_ip_address": ip_address }  
)
firewall_rule = poller.result()
print(f"Provisioned firewall rule {firewall_rule.name}")
     
  


     
