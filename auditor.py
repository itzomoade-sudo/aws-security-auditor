import boto3

session = boto3.Session(profile_name="security-auditor")

iam = session.client("iam")

print("AWS CLOUD SECURITY AUDITOR")
print("=" * 40)

# Retrieve IAM Users
response = iam.list_users()

for user in response["Users"]:

    username = user["UserName"]

    mfa= iam.list_mfa_devices(
        UserName=username
    )

    if mfa["MFADevices"]:
        print(f"[PASS] {username}: MFA enabled")
    else:
        print(f"[WARNING] {username}: No IAM MFA device assigned")
print("\nAudit completed!")