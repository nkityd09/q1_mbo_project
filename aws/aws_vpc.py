import boto3
import time

ec2 = boto3.client('ec2')

def create_aws_vpc():
    create_aws_vpc = ec2.create_vpc(
        CidrBlock='10.0.0.0/16',
    )
    print(create_aws_vpc)
    return create_aws_vpc

#TODO CIDR to be passed by User
#TODO Add tags
def create_aws_subnet(vpc_id,az, cidr):
    create_aws_subnet = ec2.create_subnet(
        CidrBlock=cidr,
        VpcId=vpc_id,
        AvailabilityZone=az,
    )
    print(create_aws_subnet)
    return create_aws_subnet

def create_ig():
    create_ig = ec2.create_internet_gateway(
    )
    print(create_ig)
    return create_ig

def attach_ig(vpc_id, ig_id):
    attach_ig = ec2.attach_internet_gateway(
    InternetGatewayId=ig_id,
    VpcId=vpc_id,
    )
    print(attach_ig)
    return attach_ig

#takes subnet ID from create_aws_subnet
def create_nat_gateway(sub_id):
    nat_gateway = ec2.create_nat_gateway(
        SubnetId=sub_id,
    )
    print(nat_gateway)
    return nat_gateway



def delete_aws_vpc(vpc_id):
    delete_aws_vpc = ec2.delete_vpc(
        VpcId=vpc_id
    )
    return delete_aws_vpc

def delete_aws_subnet(subnet_id):
    delete_aws_subnet = ec2.delete_subnet(
    SubnetId=subnet_id
    )
    return delete_aws_subnet

#add tags
def create_private_subnets(num_of_subnets, vpc_id, azs, cidrs):
    private_subnet_list = []
    for i in range(int(num_of_subnets)):
        private_subnet = create_aws_subnet(vpc_id, azs[i], cidrs[i])
        private_subnet_list.append(private_subnet["Subnet"]["SubnetId"])
        i =+ 1
    return private_subnet_list


test_create_vpc = create_aws_vpc()
test_create_subnet = create_private_subnets(2,test_create_vpc["Vpc"]["VpcId"],['us-east-2a','us-east-2b'], ['10.0.1.0/24','10.0.2.0/24'])
# test_delete_subnet = delete_aws_subnet(test_create_subnet["Subnet"]["SubnetId"])
# test_delete_vpc = delete_aws_vpc(test_create_vpc["Vpc"]["VpcId"])


# for subnets in private_subnet_list:
        # create_nat_gateway(subnets)

