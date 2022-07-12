import subprocess as sp

# Create Azure Storage Account

def create_sa(rg_name, sa_name, location):
    storage_account = sp.getoutput(f'az storage account create --name {sa_name} --resource-group {rg_name} --location {location} --enable-hierarchical-namespace true --sku Standard_RAGRS --kind StorageV2')
    print(storage_account)
    return storage_account

# Create Azure Storage Container

def create_container(sa_name, container_name):
    container = sp.getoutput(f'az storage container create --name {container_name} --account-name {sa_name}')
    print(container)
    return container



    