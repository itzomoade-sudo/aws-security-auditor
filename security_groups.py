print("Security Groups Auditor started")
import boto3
from botocore.exceptions import ClientError

session = boto3.Session(profile_name="security-auditor")
ec2 = session.client("ec2", region_name="eu-north-1")

SENSITIVE_PORTS = {
    22: "SSH",
    3389: "RDP",
    3306: "MySQL",
    5432: "PostgreSQL",
}

def audit_security_groups():
    print("\nEC2 SECURITY GROUP AUDIT")
    print("=" * 45)

    try:
        paginator = ec2.get_paginator("describe_security_groups")

        findings = 0

        for page in paginator.paginate():
            for group in page["SecurityGroups"]:
                group_name = group["GroupName"]
                group_id = group["GroupId"]

                for permission in group.get("IpPermissions", []):
                    protocol = permission.get("IpProtocol")
                    from_port = permission.get("FromPort")
                    to_port = permission.get("ToPort")

                    for ip_range in permission.get("IpRanges", []):
                        if ip_range.get("CidrIp") != "0.0.0.0/0":
                            continue

                        # -1 means all protocols and ports
                        if protocol == "-1":
                            print(
                                f"[WARNING] {group_name} ({group_id}): "
                                "All protocols open to the internet"
                            )
                            findings += 1
                            continue

                        if from_port is None or to_port is None:
                            continue

                        for port, service in SENSITIVE_PORTS.items():
                            if from_port <= port <= to_port:
                                print(
                                    f"[WARNING] {group_name} ({group_id}): "
                                    f"{service} port {port} is publicly accessible"
                                )
                                findings += 1

        if findings == 0:
            print("[PASS] No matching public inbound rules found.")

        print(f"\nAudit completed. Findings: {findings}")

    except ClientError as error:
        code = error.response["Error"]["Code"]
        print(f"[ERROR] AWS request failed: {code}")

if __name__ == "__main__":
    audit_security_groups()