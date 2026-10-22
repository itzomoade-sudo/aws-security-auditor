import subprocess
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
REPORT_DIR = PROJECT_DIR / "reports"


def run_audit(script_name):
    """Run an existing audit and capture its output."""
    print(f"\nRunning {script_name}...")

    result = subprocess.run(
        [sys.executable, "-u", str(PROJECT_DIR / script_name)],
        capture_output=True,
        text=True,
        timeout=120,
    )

    output = result.stdout.strip()
    errors = result.stderr.strip()

    if output:
        print(output)

    if errors:
        print(errors, file=sys.stderr)

    if result.returncode != 0:
        return f"ERROR: {script_name} exited with code {result.returncode}\n{output}\n{errors}"

    return output or "No output returned."


def main():
    REPORT_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    print("=" * 55)
    print("AWS CLOUD SECURITY AUDITOR")
    print("=" * 55)
    print(f"Started: {timestamp}")

    iam_results = run_audit("auditor.py")
    ec2_results = run_audit("security_groups.py")

    report = f"""AWS CLOUD SECURITY AUDIT REPORT
=======================================
Audit time: {timestamp}

IAM MFA AUDIT
---------------------------------------
{iam_results}

EC2 SECURITY GROUP AUDIT
---------------------------------------
{ec2_results}

=======================================
End of report
"""

    report_file = REPORT_DIR / (
        f"security-audit-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    )
    report_file.write_text(report, encoding="utf-8")

    print("\n" + "=" * 55)
    print(f"Report saved to: {report_file}")
    print("=" * 55)


if __name__ == "__main__":
    main()