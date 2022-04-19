- # Automating CDP Environment Registration On AWS

- [Introduction](#introduction)
- [Using the Script](#using-the-script)
  - [Prerequisite](#prerequisite)
  - [Running the Script](#running-the-script)
- [Execution Flow Diagram](#execution-flow-diagram)
  
## Introduction
CDP currently requires certain AWS resources to be created manually before an Environment can be registered. The initial setup of Credentials, SSH Keypair along with the required [minimal setup for cloud storage](https://docs.cloudera.com/cdp/latest/requirements-aws/topics/mc-idbroker-minimum-setup.html#mc-idbroker-minimum-setup) are steps that need to be taken for each individual CDP user. 

Our project aims at reducing the manual steps of creating resources on AWS and registering an Environment on CDP using the CDP CLI and Boto3 library. 
## Using the Script

### Prerequisite

1. Install required Python packages
   The script utilizes the below Python 3 packages
   - boto3
   - json
   - configparser
   - halo
   - time 
   - os
2. Install and configure [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
3. Install and configure [CDP CLI](https://docs.cloudera.com/cdp/latest/cli/topics/mc-installing-cdp-client.html)
4. Create [CDP Credential for AWS](https://docs.cloudera.com/management-console/cloud/credentials-aws/topics/mc-create-role-based-credential.html)
5. Clone the repository
### Running the Script

1. Edit the config.ini file 
   The config.ini file acts as the central repository for all configurations which will be used to create the resources and environment. 
2. Use python3 to execute the main.py file
## Execution Flow Diagram 

![Execution Flow Diagram](images/Q1_MBO_Project_Execution_Flow_Graph.jpeg)

The main.py script imports other scripts and configurations. Once imported, the main.py file calls individual functions to create resources with the configurations as the parameters for them.
