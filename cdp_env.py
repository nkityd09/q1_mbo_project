import os

#Creating env
#Create CDP Environment 
def create_env(env_name, cred_name, region, keypair, storage_base, inst_prof, cidr):
    os.system(f'cdp environments create-aws-environment --environment-name {env_name} --credential-name {cred_name} --region "{region}" --security-access cidr=0.0.0.0/0 --enable-tunnel --authentication publicKeyId="{keypair}" --log-storage storageLocationBase=s3a://{storage_base}/my-data,instanceProfile={inst_prof} --network-cidr {cidr} --free-ipa instanceCountByGroup=1')

#Create ID Broker 
def create_id_broker(env_name, data_role, ranger_role):
    os.system(f'cdp environments set-id-broker-mappings --environment-name {env_name} --data-access-role {data_role} --ranger-audit-role {ranger_role} --set-empty-mappings')

#Create DataLake 
def create_datalake(dl_name, env_name, id_inst_prof, storage_base, dl_size, dl_runtime):
    os.system(f'cdp datalake create-aws-datalake --datalake-name {dl_name} --environment-name {env_name} --cloud-provider-configuration instanceProfile={id_inst_prof},storageBucketLocation=s3a://{storage_base}/my-data --scale {dl_size} --runtime {dl_runtime}')
