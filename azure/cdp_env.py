import subprocess as sp

from pkg_resources import safe_name

#Create CDP Environment

def create_env(env_name, credential_name, location, endpoint_access, ssh_key, log_container, sa_name, sub_id, rg_name, logger_name, vnet_name, *subnets):
    cdp_env = sp.getoutput(f""" cdp environments create-azure-environment \
        --environment-name {env_name} \
        --credential-name {credential_name} \
        --region \"{location}\" \
        --security-access cidr=0.0.0.0/0 \
        --endpoint-access-gateway-scheme {endpoint_access} \
        --enable-tunnel \
        --public-key \"{ssh_key}\" \
        --log-storage storageLocationBase=abfs://{log_container}@{sa_name}.dfs.core.        windows.net,managedIdentity=/subscriptions/{sub_id}/resourcegroups/{rg_name}/       providers/Microsoft.ManagedIdentity/userAssignedIdentities/{logger_name} \
        --no-use-public-ip \
        --existing-network-params networkId={vnet_name},resourceGroupName={rg_name},        subnetIds={subnets} \
        --free-ipa instanceCountByGroup=2 \
        --resource-group-name {rg_name}  """)
    print(cdp_env)
    return cdp_env

def create_id_broker(env_name, sub_id, rg_name, dataaccess_name, ranger_name, ranger_raz_name):
    cdp_idbroker = sp.getoutput(f""" cdp environments set-id-broker-mappings \
        --environment-name {env_name} \
        --data-access-role /subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/      Microsoft.ManagedIdentity/userAssignedIdentities/{dataaccess_name} \
        --ranger-audit-role /subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/     Microsoft.ManagedIdentity/userAssignedIdentities/{ranger_name} \
        --ranger-cloud-access-authorizer-role /subscriptions/{sub_id}/resourcegroups/       {rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/   {ranger_raz_name} \
        --set-empty-mappings """)
    print(cdp_idbroker)
    return cdp_idbroker

def create_datalake(dl_name, env_name, data_container, sa_name, scale, runtime):
    cdp_datalake = sp.getoutput(f""" cdp datalake create-azure-datalake \
        --datalake-name {dl_name} \
        --environment-name {env_name} \
        --cloud-provider-configuration managedIdentity=/subscriptions/      da35404a-2612-4419-baef-45fcdce6045e/resourcegroups/q2-mbo/providers/Microsoft.     ManagedIdentity/userAssignedIdentities/q2-mbo-AssumerIdentity,    storageLocation=abfs://{data_container}@{sa_name}.dfs.core.windows.net \
        --scale {scale} \
        --runtime {runtime} \
        --enable-ranger-raz """)

    print(cdp_datalake)
    return cdp_datalake
     