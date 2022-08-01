import subprocess as sp

#Create CDP Environment

def create_env(env_name, credential_name, location, endpoint_access, ssh_key, log_container, sa_name, sub_id, rg_name, logger_name, vnet_name, subnets, default_nsg, knox_nsg):
    cdp_env = sp.getoutput(f' cdp environments create-azure-environment --environment-name {env_name} --credential-name {credential_name} --region {location} --security-access defaultSecurityGroupId=/subscriptions/{sub_id}/resourceGroups/{rg_name}/providers/Microsoft.Network/networkSecurityGroups/{default_nsg},securityGroupIdForKnox=/subscriptions/{sub_id}/resourceGroups/{rg_name}/providers/Microsoft.Network/networkSecurityGroups/{knox_nsg} --tags key="App",value="Cloudera Data Platform" key="Confidentiality",value="Clearsense Internal"  key="Criticality",value="Moderate" key="Ticket",value="J123" key="Data Classification",value="PHI" --endpoint-access-gateway-scheme {endpoint_access}  --enable-tunnel --public-key {ssh_key} --log-storage storageLocationBase=abfs://{log_container}@{sa_name}.dfs.core.windows.net,managedIdentity=/subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{logger_name} --no-use-public-ip --existing-network-params networkId={vnet_name},resourceGroupName={rg_name},subnetIds={subnets} --free-ipa instanceCountByGroup=2 --resource-group-name {rg_name}')
    print(cdp_env)
    return cdp_env

def create_id_broker(env_name, sub_id, rg_name, dataaccess_name, ranger_name, ranger_raz_name):
    cdp_idbroker = sp.getoutput(f""" cdp environments set-id-broker-mappings \
        --environment-name {env_name} \
        --data-access-role /subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{dataaccess_name} \
        --ranger-audit-role /subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{ranger_name} \
        --ranger-cloud-access-authorizer-role /subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{ranger_raz_name} \
        --set-empty-mappings """)
    print(cdp_idbroker)
    return cdp_idbroker

def create_datalake(dl_name,sub_id, rg_name, env_name, data_container, sa_name, scale, runtime, assumer_name):
    cdp_datalake = sp.getoutput(f""" cdp datalake create-azure-datalake \
        --datalake-name {dl_name} \
        --environment-name {env_name} \
        --cloud-provider-configuration managedIdentity=/subscriptions/{sub_id}/resourcegroups/{rg_name}/providers/Microsoft.ManagedIdentity/userAssignedIdentities/{assumer_name},storageLocation=abfs://{data_container}@{sa_name}.dfs.core.windows.net \
        --scale {scale} \
        --runtime {runtime} \
        --enable-ranger-raz """)

    print(cdp_datalake)
    return cdp_datalake
     