import subprocess as sp
import configparser

import az_rg as rg
import az_storage_account as sa
import az_network as nw
import az_managed_identity as mi
import az_assign_identities as ai
import cdp_env as ce
import time



config = configparser.ConfigParser()
config.read('config.ini')

SUBSCRIPTION_ID = config.get('AZURE', 'SUBSCRIPTION_ID')
RG_NAME = config.get('AZURE', 'RGNAME')
LOCATION = config.get('AZURE', 'LOCATION')

ASSUMER_ROLE_NAME = config.get('AZURE', 'ASSUMER_ROLE_NAME')
DATAACCESS_ROLE_NAME = config.get('AZURE', 'DATALAKE_ADMIN_ROLE_NAME')
LOGGER_ROLE_NAME = config.get('AZURE', 'LOG_ROLE_NAME')
RANGER_ROLE_NAME = config.get('AZURE', 'RANGER_AUDIT_ROLE_NAME')
RANGER_RAZ_ROLE_NAME = config.get('AZURE', 'RANGER_RAZ')

MI_LIST = [ASSUMER_ROLE_NAME, DATAACCESS_ROLE_NAME, LOGGER_ROLE_NAME, RANGER_ROLE_NAME, RANGER_RAZ_ROLE_NAME]

STORAGEACCOUNTNAME = config.get('AZURE', 'STORAGE_ACCOUNT')
LOG_CONTAINER = config.get('AZURE', 'LOGS_CONTAINER')
DL_CONTAINER = config.get('AZURE', 'DATALAKE_CONTAINER')

VNET_NAME = config.get('AZURE', 'VNET_NAME')
VNET_CIDR = config.get('AZURE', 'VNET_CIDR')
NUMBER_OF_SUBNETS = int(config.get('AZURE', 'NUMBER_OF_SUBNETS'))
SUBNET_NAMES = str(config.get('AZURE', 'SUBNET_NAMES'))
SUBNET_NAME_LIST = SUBNET_NAMES.split(',')
DL_SUBNET = config.get('AZURE', 'DL_SUBNET_NAME')
SUBNET_PREFIXES = str(config.get('AZURE', 'SUBNET_PREFIXES'))
SUBNET_PREFIX_LIST = SUBNET_PREFIXES.split(',')
KEYPAIR = config.get('CDP_NAMES', 'KEYPAIR')

ENV_NAME = config.get('CDP_NAMES', 'ENV_NAME')
CREDENTIAL_NAME = config.get('CDP_NAMES', 'CREDENTIAL_NAME')
ENDPOINT_ACCESS = config.get('CDP_NAMES', 'ENDPOINT_ACCESS')
DL_NAME = config.get('CDP_NAMES', 'DATALAKE_NAME')
DL_SIZE = config.get('CDP_NAMES', 'DATALAKE_SIZE')
DL_RUNTIME = config.get('CDP_NAMES', 'DATALAKE_RUNTIME') 



ASSUMER_OBJECTID = str(sp.getoutput(f"az identity show -g {RG_NAME} -n {ASSUMER_ROLE_NAME} | jq -r '.principalId'"))
DATAACCESS_OBJECTID = str(sp.getoutput(f"az identity show -g {RG_NAME} -n {DATAACCESS_ROLE_NAME} | jq -r '.principalId'"))
LOGGER_OBJECTID = str(sp.getoutput(f"az identity show -g {RG_NAME} -n {LOGGER_ROLE_NAME} | jq -r '.principalId'"))
RANGER_OBJECTID = str(sp.getoutput(f"az identity show -g {RG_NAME} -n {RANGER_ROLE_NAME} | jq -r '.principalId'"))
RANGER_RAZ_OBJECTID = str(sp.getoutput(f"az identity show -g {RG_NAME} -n {RANGER_RAZ_ROLE_NAME} | jq -r '.principalId'"))

def main():
    #Create RG in Azure
    print('#####')
    print("Creating Azure Resource Group")
    rg.create_rg(RG_NAME, LOCATION)
    #Create Storage Account
    print('#####')
    print("Creating Azure Storage Account")
    sa.create_sa(RG_NAME, STORAGEACCOUNTNAME, LOCATION)
    #Create Storage Containers for Data Lake and Logs
    print('#####')
    print("Creating Azure Storage Containers")
    sa.create_container(STORAGEACCOUNTNAME, DL_CONTAINER)
    sa.create_container(STORAGEACCOUNTNAME, LOG_CONTAINER)
    #Create Azure Vnet
    print('#####')
    print("Creating Azure VNet")
    nw.create_vnet(RG_NAME, VNET_NAME, VNET_CIDR, LOCATION)
    #Create Azure Subnets
    print('#####')
    print("Creating Azure Subnets")
    for n in range(NUMBER_OF_SUBNETS):
        nw.create_subnet(RG_NAME, VNET_NAME, SUBNET_NAME_LIST[n], SUBNET_PREFIX_LIST[n])
    #Update Data Lake Subnet
    print('#####')
    print("Updating DataLake Subnets")
    nw.update_datalake_subnet(RG_NAME, VNET_NAME, DL_SUBNET)
    #Create Azure Managed Identities
    print('#####')
    print("Createing Azure Managed Identity")
    for identities in MI_LIST:
        mi.create_identity(RG_NAME, identities)
    #Inducing Sleep for consistency
    time.sleep(300)
    #Assign Azure Managed Identities
    print('#####')
    print("Assigning Assumer Managed Identity")
    ai.assign_assumer(ASSUMER_OBJECTID, SUBSCRIPTION_ID, STORAGEACCOUNTNAME, LOG_CONTAINER, RG_NAME)
    print('#####')
    print("Assigning Ranger RAZ Managed Identity")
    ai.assing_ranger_raz(RANGER_RAZ_OBJECTID, SUBSCRIPTION_ID, STORAGEACCOUNTNAME, RG_NAME)
    print('#####')
    print("Assigning Data Access Managed Identity")
    ai.assign_dataaccess(DATAACCESS_OBJECTID, SUBSCRIPTION_ID, STORAGEACCOUNTNAME, LOG_CONTAINER, DL_CONTAINER, RG_NAME)
    print('#####')
    print("Assigning Ranger Managed Identity")
    ai.assign_ranger(RANGER_OBJECTID, SUBSCRIPTION_ID, STORAGEACCOUNTNAME, DL_CONTAINER, RG_NAME)
    print('#####')
    print("Assigning Logger Managed Identity")
    ai.assign_logger(LOGGER_OBJECTID, SUBSCRIPTION_ID, STORAGEACCOUNTNAME, LOG_CONTAINER, RG_NAME)
    #Create CDP Environment
    # print('#####')
    # print("Creating CDP Environment")
    # ce.create_env(ENV_NAME, CREDENTIAL_NAME, LOCATION, ENDPOINT_ACCESS, KEYPAIR, LOG_CONTAINER, STORAGEACCOUNTNAME, RG_NAME, LOGGER_ROLE_NAME, VNET_NAME, SUBNET_NAME_LIST)
    # print('#####')
    # print("Creating CDP ID Broker")
    # ce.create_id_broker(ENV_NAME, SUBSCRIPTION_ID, RG_NAME, DATAACCESS_ROLE_NAME, RANGER_ROLE_NAME, RANGER_RAZ_ROLE_NAME)
    # time.sleep(30)
    # print('#####')
    # print("Creating CDP DataLake")
    # ce.create_datalake(DL_NAME, ENV_NAME, DL_CONTAINER, STORAGEACCOUNTNAME, DL_SIZE, DL_RUNTIME)


if __name__ == "__main__":
    main()


    



    
