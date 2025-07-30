# AWS EC2 Instance Pricing Tool

A Python CLI tool to fetch and compare **AWS EC2 hourly on-demand pricing** and the latest **AMI IDs** across all available AWS regions.  
Supports Linux distributions (Ubuntu, Amazon Linux, RHEL, SUSE) and Windows instances.

[![PyPI version](https://img.shields.io/pypi/v/aws-ec2-pricing-tool)](https://pypi.org/project/aws-ec2-pricing-tool/)
[![Python version](https://img.shields.io/pypi/pyversions/aws-ec2-pricing-tool)](https://pypi.org/project/aws-ec2-pricing-tool/)
[![License](https://img.shields.io/pypi/l/aws-ec2-pricing-tool)](https://github.com/spithash/AWS-EC2-Instance-Pricing-Tool/blob/main/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/spithash/AWS-EC2-Instance-Pricing-Tool?style=social)](https://github.com/spithash/AWS-EC2-Instance-Pricing-Tool/stargazers)

💡 Ideal for DevOps engineers, cloud architects, and infrastructure teams looking to optimize EC2 costs or automate cloud image selection.

> 🔖 This tool focuses on **on-demand EC2 pricing**, making it perfect for dynamic or short-term workloads where flexibility matters.

![AWS-EC2 Instance Pricing Tool](https://raw.githubusercontent.com/spithash/trunk/refs/heads/master/ec2pricing/AWS-EC2-Instance-Pricing-Tool.png)

## Requirements

- **Python 3.7+**  
  The package is compatible with Python 3.7 and above.

- **AWS Credentials Configured**  
  It uses `boto3` to interact with AWS APIs. Make sure your AWS CLI or environment variables are configured with appropriate credentials and permissions to access EC2 and Pricing APIs.  
  _Note: You don't need to set a default region in your environment._

## Installation

Install from PyPI:

```bash
pip install aws-ec2-pricing-tool
```

Or clone from GitHub and install manually:

```bash
git clone https://github.com/spithash/AWS-EC2-Instance-Pricing-Tool.git
cd AWS-EC2-Instance-Pricing-Tool
pip install .
```

## Usage

Run the tool from the command line by specifying the EC2 instance type, operating system, and optionally the distro:

```bash
ec2pricing <instance_type> --os <linux|windows> [--distro <distro_name>]
```

### Examples

Fetch pricing and AMI info for a Linux Ubuntu t2.micro instance:

```bash
ec2pricing t2.micro --os linux --distro ubuntu
```

Fetch pricing and AMI info for a Windows t3.medium instance (Microsoft publisher):

```bash
ec2pricing t3.medium --os windows --distro microsoft
```

Fetch pricing and AMI info for a Linux instance across all distros (no distro specified):

```bash
ec2pricing t2.micro --os linux
```

## Linux Instances Demo

![EC2 Pricing Linux](https://raw.githubusercontent.com/spithash/trunk/refs/heads/master/ec2pricing/ec2pricing-linux.gif)

## Windows Instances Demo

![EC2 Pricing Windows](https://raw.githubusercontent.com/spithash/trunk/refs/heads/master/ec2pricing/ec2pricing-windows.gif)
