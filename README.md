- # Automating CDP Environment Registration On AWS

- [Introduction](#introduction)
- [Using the Script](#using-the-script)
  - [Prerequisite](#prerequisite)
- [](#)
- [Execution Flow Diagram](#execution-flow-diagram)
  
## Introduction
CDP currently requires certain AWS resources to be created manually before an Environment can be registered. The initial setup of Credentials, SSH Keypair along with the required [minimal setup for cloud storage](https://docs.cloudera.com/cdp/latest/requirements-aws/topics/mc-idbroker-minimum-setup.html#mc-idbroker-minimum-setup) are steps that need to be taken for each individual CDP user. 

Our project aims at reducing the manual steps of creating resources on AWS and registering an Environment on CDP using the CDP CLI and Boto3 library. 
## Using the Script

### Prerequisite

1. Install AWS CLI
2. Install CDP CLI
3. CREATE CDP Credential
4. 
## 

## Execution Flow Diagram 

![Execution Flow Diagram](images/Q1_MBO_Project_Execution_Flow_Graph.jpeg)

The main.py script imports other scripts and configurations. 