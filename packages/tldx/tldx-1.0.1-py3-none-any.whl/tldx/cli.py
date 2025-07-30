import argparse
import sys
from .core import fetch_tlds, load_keywords, generate_combinations

def main():
    parser = argparse.ArgumentParser(description='TLDX - TLD Expansion Tool for Bug Bounty')
    parser.add_argument('-k', '--keyword', help='Single keyword to combine with TLDs')
    parser.add_argument('-kf', '--keyword-file', help='File containing keywords (one per line)')
    parser.add_argument('-o', '--output', help='Output file to save results')
    parser.add_argument('-t', '--tld-file', help='Custom TLD file (default: fetch from IANA)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()

    if not args.keyword and not args.keyword_file:
        sys.exit("Error: Must specify either -k or -kf")

    # Load keywords
    keywords = load_keywords(args.keyword, args.keyword_file)

    # Fetch TLDs
    tlds = fetch_tlds(args.tld_file)
    if args.verbose:
        print(f"[*] Loaded {len(tlds)} TLDs", file=sys.stderr)
        print(f"[*] Using {len(keywords)} keywords", file=sys.stderr)

    # Output results
    output = sys.stdout
    if args.output:
        try:
            output = open(args.output, 'w')
        except IOError:
            sys.exit(f"Error: Couldn't write to {args.output}")

    # Generate and output combinations
    count = 0
    for domain in generate_combinations(keywords, tlds):
        print(domain, file=output)
        count += 1

    if args.verbose:
        print(f"[*] Generated {count} combinations", file=sys.stderr)
        
    if args.output:
        output.close()
        if args.verbose:
            print(f"[+] Results saved to {args.output}", file=sys.stderr)

if __name__ == "__main__":
    main()