import boto3
def check_iam_users():
    iam = boto3.client("iam")
    users = iam.list_users()["Users"]
    for user in users:
        name = user["UserName"]
        key = iam.list_access_keys(UserName=name)["AccessKeyMetadata"]
        if key:
            print(f"RISK | {name} has {len(key)} access key(s)")
        else:
                print(name, "| NO KEY")


def check_s3_buckets():
     s3 = boto3.client("s3")
     buckets = s3.list_buckets()["Buckets"]
     for bucket in  buckets:
         name = bucket["Name"]
         try:
               PABC= s3.get_public_access_block(Bucket=name)
               print("Bucket name:     ", name, PABC["PublicAccessBlockConfiguration"])
         except:
               print("Bucket name:", name, "NO PABC")



def check_security_groups():
     ec2 = boto3.client("ec2")
     securitygroups = ec2.describe_security_groups()["SecurityGroups"]
     found = False
     
     for securitygroup in securitygroups:
        securitygroup_id = securitygroup["GroupId"]
        for permission in securitygroup.get("IpPermissions", []):
             from_port = permission.get("FromPort")
             to_port = permission.get("ToPort")
             for r in permission.get("IpRanges", []):
                  if r.get("CidrIp") == "0.0.0.0/0":
                       found = True
                       print("RISK: | security group", securitygroup_id, "is open", from_port, "-", to_port, "to the internet")
     if not found:
      print("OK | no security groups are open to 0.0.0.0/0")

check_iam_users()
check_s3_buckets()           
check_security_groups()

