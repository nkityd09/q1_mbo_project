import subprocess as sp

# Create managed identities

def create_identity(rg_name, identity_name):
    managed_identities = sp.getoutput(f'az identity create -g {rg_name} -n {identity_name}')
    print(managed_identities)
    return managed_identities
