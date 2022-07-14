import subprocess as sp

# Assign roles to Assumer Identity


def assign_assumer(assumer_id, subscription_id, storage_account_name, log_container, rg_name):
    # Assign Managed Identity Operator role to the assumerIdentity principal at subscription scope
    assumer_subscription = sp.getoutput(f""" az role assignment create --assignee {assumer_id} --role 'f1a07417-d97a-45cb-824c-7a7467783830' --scope "/subscriptions/{subscription_id}" """)

    # Assign Virtual Machine Contributor role to the assumerIdentity principal at subscription scope
    assumer_mc = sp.getoutput(f""" az role assignment create --assignee {assumer_id} --role '9980e02c-c2be-4d73-94e8-173b1dc7cf3c' --scope "/subscriptions/{subscription_id}" """)

    # Assign Storage Blob Data Contributor role to the Assumer Identity principal at logs filesystem scope
    assumer_log_contributor = sp.getoutput(f""" az role assignment create --assignee {assumer_id} --role 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}/blobServices/default/containers/{log_container}" """)
    print(assumer_subscription, assumer_mc, assumer_log_contributor)

    return assumer_subscription, assumer_mc, assumer_log_contributor


def assing_ranger_raz(ranger_id, subscription_id, storage_account_name, rg_name):
    # Assign Storage Blob Data Owner role to the Ranger RAZ principal at Storage Account scope
    ranger_raz_owner_sa = sp.getoutput(f""" az role assignment create --assignee {ranger_id} --role 'b7e6dc6d-f1e8-4753-8033-0f276bb0955b' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}" """)

    ranger_raz_delegator_sa = sp.getoutput(f""" az role assignment create --assignee {ranger_id} --role 'db58b8e5-c6ad-4a2a-8342-4190687cbf4a' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}" """)

    print(ranger_raz_owner_sa, ranger_raz_delegator_sa)
    return ranger_raz_owner_sa, ranger_raz_delegator_sa

def assign_dataaccess(data_id, subscription_id, storage_account_name, log_container, data_container, rg_name):
    # Assign Storage Blob Data Owner role to the dataAccessIdentity principal at data filesystem scope
    dataaccess_owner_data = sp.getoutput(f""" az role assignment create --assignee {data_id} --role 'b7e6dc6d-f1e8-4753-8033-0f276bb0955b' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}/blobServices/default/containers/{data_container}" """)

    # Assign Storage Blob Data Owner role to the dataAccessIdentity principal at logs filesystem scope
    dataaccess_owner_data = sp.getoutput(f""" az role assignment create --assignee {data_id} --role 'b7e6dc6d-f1e8-4753-8033-0f276bb0955b' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}/blobServices/default/containers/{log_container}" """)
    
    print(dataaccess_owner_data, dataaccess_owner_data)
    return dataaccess_owner_data, dataaccess_owner_data

def assign_ranger(ranger_id, subscription_id, storage_account_name, data_container, rg_name):
    # Assign Storage Blob Data Contributor role to the rangerIdentity principal at data filesystem scope
    ranger_contributor_data = sp.getoutput(f""" az role assignment create --assignee {ranger_id} --role 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}/blobServices/default/containers/{data_container}" """)

    print(ranger_contributor_data)
    return ranger_contributor_data


def assign_logger(logger_id, subscription_id, storage_account_name, log_container, rg_name):
    # Assign Storage Blob Data Contributor role to the loggerIdentity principal at logs filesystem scope
    logger_contributor_log = sp.getoutput(f""" az role assignment create --assignee {logger_id} --role 'ba92f5b4-2d11-453d-a403-e96b0029c9fe' --scope "/subscriptions/{subscription_id}/resourceGroups/{rg_name}/providers/Microsoft.Storage/storageAccounts/{storage_account_name}/blobServices/default/containers/{log_container}" """)

    print(logger_contributor_log)
    return logger_contributor_log




    