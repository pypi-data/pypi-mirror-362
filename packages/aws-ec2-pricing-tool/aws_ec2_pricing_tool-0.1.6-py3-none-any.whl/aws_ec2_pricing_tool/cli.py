#!/usr/bin/env python3

import argparse
import boto3
import json
import sys
import time
from collections import defaultdict
from botocore.exceptions import BotoCoreError, ClientError
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import track, Progress, SpinnerColumn, BarColumn, TextColumn

console = Console()
DEFAULT_PRICING_REGION = "us-east-1"
LINUX_DISTRO_OWNERS = {
    "amzn": "137112412989",  # Amazon Linux
    "ubuntu": "099720109477",
    "rhel": "309956199498",
    "suse": "013907871322",
}
WINDOWS_DISTRO_OWNERS = {
    "microsoft": "801119661308"
}

LINUX_AMI_PATTERNS = {
    "amzn": "amzn2-ami-hvm-*-x86_64-gp2",
    "ubuntu": "ubuntu/images/hvm-ssd/ubuntu-*-*-amd64-server-*",
    "rhel": "RHEL-*-x86_64-*",
    "suse": "suse-sles-*-x86_64-*"
}

WINDOWS_AMI_PATTERNS = {
    "microsoft": "Windows_Server-*-English-Full-Base-*"
}

def fetch_regions():
    console.print("📡 [bold]Fetching enabled AWS regions...[/bold]")
    ec2 = boto3.client("account")
    try:
        regions = ec2.list_regions(RegionOptStatusContains=["ENABLED_BY_DEFAULT"])["Regions"]
        region_names = [r["RegionName"] for r in regions]
        console.print(f"🌎 Found {len(region_names)} regions.")
        return region_names
    except (BotoCoreError, ClientError) as e:
        console.print(f"[red]Error fetching regions: {e}[/red]")
        sys.exit(1)

def fetch_pricing_data(instance_type, os):
    console.print("💰 [bold]Fetching pricing data...[/bold]")
    pricing = boto3.client("pricing", region_name=DEFAULT_PRICING_REGION)
    filters = [
        {"Type": "TERM_MATCH", "Field": "instanceType", "Value": instance_type},
        {"Type": "TERM_MATCH", "Field": "tenancy", "Value": "Shared"},
        {"Type": "TERM_MATCH", "Field": "preInstalledSw", "Value": "NA"},
        {"Type": "TERM_MATCH", "Field": "capacitystatus", "Value": "Used"},
        {"Type": "TERM_MATCH", "Field": "operatingSystem", "Value": os.capitalize()}
    ]

    results = []
    next_token = None
    pages = 0

    while True:
        try:
            if next_token:
                data = pricing.get_products(
                    ServiceCode="AmazonEC2",
                    Filters=filters,
                    FormatVersion="aws_v1",
                    MaxResults=100,
                    NextToken=next_token
                )
            else:
                data = pricing.get_products(
                    ServiceCode="AmazonEC2",
                    Filters=filters,
                    FormatVersion="aws_v1",
                    MaxResults=100,
                )
            results.extend([json.loads(p) for p in data["PriceList"]])
            next_token = data.get("NextToken")
            pages += 1
            if not next_token:
                break
        except (BotoCoreError, ClientError) as e:
            console.print(f"[red]Error fetching pricing: {e}[/red]")
            sys.exit(1)

    console.print(f"📄 Total pricing pages fetched: {pages}")
    return results

def extract_prices(pricing_data, region_code, os_filter):
    for product in pricing_data:
        attrs = product.get("product", {}).get("attributes", {})
        if attrs.get("regionCode") != region_code:
            continue
        if attrs.get("operatingSystem") != os_filter:
            continue

        ondemand = next(iter(product.get("terms", {}).get("OnDemand", {}).values()), {})
        if ondemand:
            price_dim = next(iter(ondemand.get("priceDimensions", {}).values()), {})
            usd_price = price_dim.get("pricePerUnit", {}).get("USD")
            if usd_price is not None:
                return f"${usd_price}"
    return "-"

def fetch_latest_ami(region, patterns, owner):
    ec2 = boto3.client("ec2", region_name=region)
    latest_images = []
    for pattern in patterns:
        images = []
        next_token = ""
        while True:
            try:
                params = {
                    "Owners": [owner],
                    "Filters": [
                        {"Name": "name", "Values": [pattern]},
                        {"Name": "state", "Values": ["available"]},
                    ],
                    "MaxResults": 1000
                }
                if next_token:
                    params["NextToken"] = next_token

                response = ec2.describe_images(**params)
                images.extend(response["Images"])
                next_token = response.get("NextToken")
                if not next_token:
                    break
            except Exception:
                break

        if images:
            latest = sorted(images, key=lambda x: x["CreationDate"])[-1]
            latest_images.append((latest["Name"], latest["ImageId"], latest["CreationDate"]))
    return latest_images

def show_table(title, results):
    table = Table(title=title)
    table.add_column("Region", style="cyan")
    table.add_column("Price", style="green")
    table.add_column("AMI ID", style="white")
    table.add_column("AMI Name", style="dim")
    table.add_column("CreationDate", style="yellow")
    for r in results:
        table.add_row(r["Region"], r["Price"], r["AMI_ID"], r["AMI_Name"], r["CreationDate"])
    console.print(table)

def main():
    parser = argparse.ArgumentParser(
        description="🔍 Compare AWS EC2 on-demand pricing and AMIs by region, OS and distro.",
        epilog="Example: ec2pricing t2.micro --os linux --distro ubuntu",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("instance_type", help="EC2 instance type to compare")
    parser.add_argument("--os", choices=["linux", "windows"], required=True, help="Operating system")
    parser.add_argument("--distro", help="Linux distro or Windows publisher (e.g., ubuntu, amzn, rhel)")

    args = parser.parse_args()
    instance_type = args.instance_type
    selected_os = args.os
    distro = args.distro

    ami_patterns = LINUX_AMI_PATTERNS if selected_os == "linux" else WINDOWS_AMI_PATTERNS
    owners = LINUX_DISTRO_OWNERS if selected_os == "linux" else WINDOWS_DISTRO_OWNERS

    if distro:
        if distro not in ami_patterns:
            console.print(f"[red]❌ Invalid distro '{distro}'. Valid options: {', '.join(ami_patterns)}[/red]")
            sys.exit(1)
        patterns = [ami_patterns[distro]]
        owner = owners[distro]
    else:
        patterns = list(ami_patterns.values())
        console.print(f"[yellow]⚠️  No distro specified. Will search for all possible AMI distributions.[/yellow]")

    regions = fetch_regions()
    pricing_data = fetch_pricing_data(instance_type, selected_os)

    results = []

    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        transient=True,
    ) as progress:
        task = progress.add_task("Fetching AMIs...", total=len(regions))

        for i, region in enumerate(regions, 1):
            progress.update(task, advance=1, description=f"Scanning: {region} ({i}/{len(regions)})")

            use_patterns = patterns if distro else list(ami_patterns.values())
            for key, pattern in ([(distro, patterns[0])] if distro else ami_patterns.items()):
                try:
                    dist_owner = owners[distro] if distro else owners.get(key)
                    if not dist_owner:
                        continue
                    amis = fetch_latest_ami(region, [pattern], dist_owner)
                    price = extract_prices(pricing_data, region, selected_os.capitalize())

                    for name, ami_id, creation_date in amis:
                        results.append({
                            "Region": region,
                            "AMI_Name": name,
                            "AMI_ID": ami_id,
                            "Price": price,
                            "CreationDate": creation_date,
                        })
                except Exception as e:
                    console.print(f"[red]Error in {region}: {e}[/red]")

    if not results:
        console.print("[bold red]❌ No AMIs or pricing data found. Try different filters.[/bold red]")
        sys.exit(1)

    results_sorted = sorted(results, key=lambda x: float(x["Price"].strip("$")) if x["Price"].startswith("$") else 999)
    show_table(f"EC2 Instance Pricing for '{instance_type}' ({selected_os}/{distro or 'all distros'})", results_sorted)

if __name__ == "__main__":
    main()

