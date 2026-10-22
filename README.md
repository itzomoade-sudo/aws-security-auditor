AWS Cloud Security Auditor

A Python-based AWS security auditing tool built with Boto3 to identify potential cloud security misconfigurations. The project checks IAM user MFA enrollment and EC2 security group ingress rules, then generates a timestamped audit report.

Features

- IAM MFA Audit: Identifies IAM users with and without assigned MFA devices.
- EC2 Security Group Audit: Checks for public IPv4 access ("0.0.0.0/0") to sensitive ports:
  - SSH — "22"
  - RDP — "3389"
  - MySQL — "3306"
  - PostgreSQL — "5432"
- Broad Ingress Detection: Flags security group rules that allow all protocols from the public IPv4 internet.
- Automated Reporting: Runs both audits and saves their output to a timestamped text file.
- AWS Role-Based Access: Uses a dedicated IAM role and temporary credentials for read-only auditing.

Technologies

- Python
- AWS SDK for Python (Boto3)
- AWS Identity and Access Management (IAM)
- Amazon EC2
- AWS Security Groups
- AWS Security Token Service (STS)
- Visual Studio Code

Project Structure

aws-security-auditor/
├── auditor.py
├── security_groups.py
├── main.py
├── README.md
├── .gitignore
├── requirements.txt
└── reports/                 # Local reports; not committed

Prerequisites

- Python 3.10 or later
- AWS CLI configured locally
- An AWS account with permission to assume the audit role
- An MFA device configured for the source IAM identity

Setup

1. Clone the repository

git clone https://github.com/itzomade-sudo/aws-security-auditor.git
cd aws-security-auditor

2. Create and activate a virtual environment

Windows PowerShell:

python -m venv .venv
.\.venv\Scripts\Activate.ps1

3. Install dependencies

pip install boto3
pip freeze > requirements.txt

4. Configure AWS access

Configure the AWS CLI locally and set up the "security-auditor" profile to assume the dedicated audit role using temporary credentials and MFA.

Do not commit AWS credentials, MFA codes, account-specific ARNs, or local AWS configuration files.

5. Run the audit

python main.py

The tool runs the IAM and EC2 security group checks and saves a timestamped report in the local "reports/" directory.

Security Findings

During testing, the auditor identified these potential exposures:

Resource label| Finding| Risk
"launch-wizard-1"| SSH (22) allowed from "0.0.0.0/0"| Unwanted login attempts
"aurora-lab-sg"| PostgreSQL (5432) allowed from "0.0.0.0/0"| Unwanted database connection attempts

Both security groups were investigated, confirmed to have no associated resources, and deleted after verification.

These findings reflect the lab environment at the time of testing. They do not indicate that a resource was compromised.

Security Design

- Uses a dedicated audit role rather than routine administrator access.
- Uses temporary role credentials and MFA for access.
- Uses read-only AWS API actions for the audit.
- Keeps generated reports and local configuration out of version control by default.

Limitations

- The tool checks only the configured AWS region for EC2 security groups.
- Public IPv4 ingress is checked; equivalent IPv6 exposure is not currently included.
- The IAM check reports MFA device enrollment, not every possible MFA or sign-in security control.
- Findings require human review before remediation.

Future Improvements

- Add IPv6 ingress checks for "::/0".
- Export findings as JSON or CSV.
- Add severity ratings and a summary of findings.
- Add automated tests and structured logging.
- Expand checks to other AWS security configurations.

## Screenshots

### IAM MFA Audit
![IAM MFA audit results](image1.png)

### EC2 Security Group Audit
![Security group audit findings](image2.png)

### Generated Audit Report
![Generated audit report](image3.png)

### Project Structure
![Project structure in VS Code](image4.png)

Disclaimer

This project is intended for educational use and authorized security auditing of AWS environments. Review findings before making changes to cloud resources.

Author

Yusuf Tajudeen

Cybersecurity Student | AWS Certified Cloud Practitioner | Aspiring Cloud Security Engineer

- GitHub: https://github.com/itzomoade-sudo