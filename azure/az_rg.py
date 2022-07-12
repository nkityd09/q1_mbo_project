import subprocess as sp

#Create Azure Resource Group
def create_rg(rg_name, location):
    rg = sp.getoutput(f'az group create --name {rg_name} --location {location}')
    print(rg)
    return rg