import boto3

ec2 = boto3.client('ec2')

#Create EC2 Keypair
def create_ssh_key_pair(key_pair_name):
    key_pair = ec2.create_key_pair(
        KeyName = key_pair_name
    )
    print(" ")
    print("Created KeyPair -> ", key_pair["KeyName"])
    print(" ")
    return key_pair

##### Rough Code #####