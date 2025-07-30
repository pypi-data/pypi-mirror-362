from setuptools import setup, find_packages

setup(
    name="aws-ec2-pricing-tool",
    version="0.1.6",
    author="Stathis Xantinidis",
    author_email="spithash@tuta.io",
    description="CLI tool to compare AWS EC2 on-demand pricing and AMIs across regions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/spithash/AWS-EC2-Instance-Pricing-Tool",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "rich"
    ],
    entry_points={
        "console_scripts": [
            "ec2pricing=aws_ec2_pricing_tool.cli:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
