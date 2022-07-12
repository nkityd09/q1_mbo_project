##Steps for running script

1. Setup (Azure CLI)[https://docs.microsoft.com/en-us/cli/azure/install-azure-cli-macos]
2. (Sign in to Azure CLI)[https://docs.microsoft.com/en-us/cli/azure/get-started-with-azure-cli#how-to-sign-into-the-azure-cli]
3. Setup CDP CLI
4. (Install jq)[https://stedolan.github.io/jq/download/]
5. Create Azure Subscription
6. Create Azure App
7. Create CDP Credential
   ```
   az ad sp create-for-rbac \
>     --name http://q2-mbo \
>     --role Contributor \
>     --scopes /subscriptions/da35404a-2612-4419-baef-45fcdce6045e
```

```
cdp environments create-azure-credential \
--credential-name <credential_name?> \
--subscription-id  <subscription_id>\
--tenant-id <tenant_id> \
--app-based applicationId=<applicaiton_id>, \
secretKey=<app_password>
```
