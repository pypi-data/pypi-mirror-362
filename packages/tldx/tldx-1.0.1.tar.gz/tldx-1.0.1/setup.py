from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="tldx",
    version="1.0.1",
    author="Loca Martin",
    author_email="locaboyff@gmail.com",
    description="TLD Expansion Tool for Bug Bounty Reconnaissance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LocaMartin/tldx",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "argparse>=1.4.0"
    ],
    entry_points={
        "console_scripts": [
            "tldx = tldx.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Intended Audience :: Information Technology"
    ],
    python_requires='>=3.6',
    keywords='bugbounty recon tld security'
)