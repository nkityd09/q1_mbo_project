import subprocess as sp

#Create VNet in Azure

def create_vnet(rg_name, vnet_name, cidr, location):
    vnet = sp.getoutput(f'az network vnet create --name {vnet_name} --resource-group {rg_name} --location {location} --address-prefix {cidr}')
    print(vnet)
    return vnet

#Create Subnet Azure
def create_subnet(rg_name, vnet_name, subnet_name, cidr):
    subnet = sp.getoutput(f'az network vnet subnet create --resource-group {rg_name} --vnet-name {vnet_name} --name {subnet_name} --address-prefixes {cidr}')
    print(subnet)
    return subnet

#Disable private endpoint and add sql and storage endpoints in Datalake subnet
def update_datalake_subnet(rg_name, vnet_name, subnet_name):
    disable_private_endpoint = sp.getoutput(f'az network vnet subnet update --name {subnet_name} --resource-group {rg_name} --vnet-name {vnet_name} --disable-private-endpoint-network-policies true')

    sql_service_endpoint = sp.getoutput(f'az network vnet subnet update --resource-group {rg_name} --name {subnet_name} --vnet-name {vnet_name} --service-endpoints Microsoft.Sql')

    storage_service_endpoint = sp.getoutput(f'az network vnet subnet update --resource-group {rg_name} --name {subnet_name} --vnet-name {vnet_name} --service-endpoints Microsoft.Storage')

    print(disable_private_endpoint, sql_service_endpoint, storage_service_endpoint)
    return disable_private_endpoint, sql_service_endpoint, storage_service_endpoint

