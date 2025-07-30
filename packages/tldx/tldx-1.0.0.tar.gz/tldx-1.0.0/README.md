# TLDX - TLD Expansion Tool for Bug Bounty

Expand keywords across all TLDs to discover hidden assets during reconnaissance.

## Features
- Generate domain permutations (keyword + TLD)
- Supports single keywords or keyword files
- Uses official IANA TLD list
- Custom TLD lists support
- Output to console or file

## Installation
```bash
pip install tldx
```
### Usage
```yaml
# Single keyword
tldx -k google

# Keyword file
tldx -kf keywords.txt

# Save output
tldx -k admin -o targets.txt

# Custom TLD list
tldx -k test -t custom_tlds.txt

# Verbose mode
tldx -k dev -v
```
### Example

```yaml
# Generate government domains
tldx -k gov | head -5
gov.aaa
gov.aarp
gov.abb
gov.abbott
gov.abbvie

# Pipe to DNS resolver
tldx -k api | dnsx -silent

# Full recon workflow
tldx -kf keywords.txt | httpx -silent | nuclei -t vulnerabilities/
```

```yaml
tldx/
├── setup.py
├── requirements.txt
├── README.md
├── tldx/
│   ├── __init__.py
│   ├── cli.py
│   └── core.py
└── tests/
    └── test_tldx.py
```