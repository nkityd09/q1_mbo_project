from email.policy import default
import subprocess as sp


def create_nsg(nsg_name, rg_name):
    nsg_create = sp.getoutput(f""" az network nsg create --name {nsg_name} --resource-group {rg_name} """)
    print(nsg_create)
    return nsg_create

def create_nsg_rule_knox(rg_name, nsg_name, vnet_cidr):
    allow_cdp = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name AllowCDPControlPlane --priority 101 --source-address-prefixes {vnet_cidr} 52.36.110.208/32 52.40.165.49/32 35.166.86.177/32 --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 443 9443 """)

    ssh = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name SSH --priority 102 --source-address-prefixes {vnet_cidr} --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 22 """)

    internal_comm = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name InternalCommunication --priority 103 --source-address-prefixes {vnet_cidr} --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 0-65535 """)

    internal_comm_icmp = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name InternalCommunicationICMP --priority 104 --source-address-prefixes {vnet_cidr} --protocol Icmp --destination-port-ranges '*' """)
    
    print(allow_cdp, ssh, internal_comm, internal_comm_icmp)

    return allow_cdp, ssh, internal_comm, internal_comm_icmp

def create_nsg_rule_default(rg_name, nsg_name, vnet_cidr):
    allow_cdp = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name AllowCDPControlPlane --priority 101 --source-address-prefixes 35.80.24.128/27 35.166.86.177/32 52.36.110.208/32 52.40.165.49/32 --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 9443 """)
    
    experiences = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name Experiences --priority 102 --source-address-prefixes {vnet_cidr} --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 443 """)
    
    ssh = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name SSH --priority 103 --source-address-prefixes {vnet_cidr} --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 22 """)
    
    internal_comm = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name InternalCommunication --priority 104 --source-address-prefixes {vnet_cidr} --source-port-ranges '*' --destination-address-prefixes '*' --destination-port-ranges 0-65535 """)
    
    internal_comm_icmp = sp.getoutput(f""" az network nsg rule create --resource-group {rg_name} --nsg-name {nsg_name} --name InternalCommunicationICMP --priority 105 --source-address-prefixes {vnet_cidr} --protocol Icmp --destination-port-ranges '*' """)

    print(allow_cdp, experiences, ssh, internal_comm, internal_comm_icmp)

    return allow_cdp, experiences, ssh, internal_comm, internal_comm_icmp




 



 

