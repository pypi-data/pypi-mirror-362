import sys
import requests

def fetch_tlds(tld_file=None):
    """Fetch TLDs from IANA or custom file"""
    if tld_file:
        try:
            with open(tld_file, 'r') as f:
                return [line.strip().lower() for line in f 
                        if line.strip() and not line.startswith('#')]
        except FileNotFoundError:
            sys.exit(f"Error: TLD file {tld_file} not found")
    else:
        url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return [
                line.strip().lower() 
                for line in response.text.splitlines() 
                if line.strip() and not line.startswith('#')
            ]
        except requests.exceptions.RequestException as e:
            sys.exit(f"Failed to fetch TLD data: {str(e)}")

def load_keywords(keyword=None, keyword_file=None):
    """Load keywords from input sources"""
    keywords = []
    if keyword:
        keywords.append(keyword.strip().lower())
    if keyword_file:
        try:
            with open(keyword_file, 'r') as f:
                keywords.extend([line.strip().lower() for line in f if line.strip()])
        except FileNotFoundError:
            sys.exit(f"Error: Keyword file {keyword_file} not found")
    return keywords

def generate_combinations(keywords, tlds):
    """Generate keyword-tld combinations"""
    for keyword in keywords:
        for tld in tlds:
            yield f"{keyword}.{tld}"