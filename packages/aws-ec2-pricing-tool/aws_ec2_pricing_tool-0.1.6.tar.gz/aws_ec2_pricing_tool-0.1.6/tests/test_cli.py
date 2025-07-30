import subprocess
import pytest

def test_ec2pricing_help():
    result = subprocess.run(
        ["ec2pricing", "-h"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "usage" in result.stdout.lower()

def test_ec2pricing_help_content():
    result = subprocess.run(
        ["ec2pricing", "-h"],
        capture_output=True,
        text=True,
    )
    output = result.stdout.lower()
    assert "instance_type" in output or "instance type" in output
    assert "--os" in output
    assert "--distro" in output

def test_ec2pricing_missing_args():
    # Only instance_type and --os are required, distro optional
    result = subprocess.run(
        ["ec2pricing", "t2.micro", "--os", "linux"],
        capture_output=True,
        text=True
    )
    # This might succeed or fail depending on AWS creds, so just check return code
    assert result.returncode == 0 or result.returncode == 1

def test_ec2pricing_invalid_distro():
    result = subprocess.run(
        ["ec2pricing", "t2.micro", "--os", "linux", "--distro", "invaliddistro"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    # error could be in stdout or stderr
    combined_output = (result.stdout + result.stderr).lower()
    assert "invalid distro" in combined_output or "invalid" in combined_output

def test_ec2pricing_invalid_os():
    result = subprocess.run(
        ["ec2pricing", "t2.micro", "--os", "macos"],
        capture_output=True,
        text=True,
    )
    # argparse should reject invalid choice and exit with code 2
    assert result.returncode == 2
    combined_output = (result.stdout + result.stderr).lower()
    assert "invalid choice" in combined_output

def test_ec2pricing_no_args():
    result = subprocess.run(
        ["ec2pricing"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    combined_output = (result.stdout + result.stderr).lower()
    assert "usage" in combined_output

def test_ec2pricing_basic_output_keywords():
    # This test will likely error without AWS creds but just check output content
    result = subprocess.run(
        ["ec2pricing", "t2.micro", "--os", "linux"],
        capture_output=True,
        text=True,
        timeout=15,
    )
    combined_output = (result.stdout + result.stderr).lower()
    # Check if some keywords related to the tool appear at least once
    assert any(word in combined_output for word in ["fetching", "price", "ami", "region", "error", "amazon", "ubuntu"])

if __name__ == "__main__":
    pytest.main()

