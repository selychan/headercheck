import requests
import argparse
from datetime import datetime
import os
from colorama import Fore, Style, init
import pyfiglet
import logging

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def print_banner():
    """Display fancy ASCII art banner"""
    banner = pyfiglet.figlet_format("Header Scanner", font="slant")
    print(f"{Fore.CYAN}{banner}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Web Security Header Checker Tool - v1.0{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Created by Sely{Style.RESET_ALL}")
    print("=" * 60)

def check_headers(domain):
    """Check security headers for a given domain"""
    if not domain.startswith(("http://", "https://")):
        domain = f"https://{domain}"
    
    try:
        response = requests.get(domain, timeout=5)
        headers = response.headers

        # Security headers to check
        security_headers = {
            'Strict-Transport-Security': 'HSTS',
            'Content-Security-Policy': 'CSP',
            'X-Frame-Options': 'X-Frame-Options',
            'X-Content-Type-Options': 'X-Content-Type-Options',
            'Referrer-Policy': 'Referrer-Policy',
            'Permissions-Policy': 'Permissions-Policy'
        }

        missing_headers = []
        present_headers = []

        for header, description in security_headers.items():
            if header in headers:
                present_headers.append((description, headers[header]))
            else:
                missing_headers.append(description)

        return {
            "domain": domain,
            "status": "success",
            "present_headers": present_headers,
            "missing_headers": missing_headers,
        }

    except requests.exceptions.RequestException as e:
        return {
            "domain": domain,
            "status": "error",
            "error": str(e),
        }

def write_report(result, output_dir):
    """Write report for each domain"""
    domain = result["domain"].replace("https://", "").replace("http://", "")
    filename = os.path.join(output_dir, f"{domain}_report.txt")

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"Security Header Report for {result['domain']}\n")
        f.write("=" * 60 + "\n")
        f.write(f"Scan Time: {datetime.now()}\n\n")

        if result["status"] == "error":
            f.write(f"[ERROR] Could not scan: {result['error']}\n")
            return

        f.write("[+] Present Headers:\n")
        for header, value in result["present_headers"]:
            f.write(f"  ✓ {header}: {value}\n")
        
        f.write("\n[-] Missing Headers:\n")
        for header in result["missing_headers"]:
            f.write(f"  ✗ {header}\n")
    
    logging.info(f"Report saved: {filename}")

def display_result(result):
    """Display result in the terminal with colors"""
    print(f"{Fore.CYAN}Domain: {result['domain']}{Style.RESET_ALL}")

    if result["status"] == "error":
        print(f"{Fore.RED}  Error: {result['error']}{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Present Headers:{Style.RESET_ALL}")
    for header, value in result["present_headers"]:
        print(f"  {Fore.GREEN}✓ {header}: {value}{Style.RESET_ALL}")
    
    print(f"{Fore.YELLOW}[-] Missing Headers:{Style.RESET_ALL}")
    for header in result["missing_headers"]:
        print(f"  {Fore.RED}✗ {header}{Style.RESET_ALL}")

def main():
    
    parser = argparse.ArgumentParser(description="Web Security Header Checker")
    print(f"\n{Fore.YELLOW}[+] Scan starting!{Style.RESET_ALL}")
    parser.add_argument("-l", "--list", required=True, help="File containing list of domains")
    args = parser.parse_args()

    # Print banner
    print_banner()

    # Read domains from file
    if not os.path.exists(args.list):
        print(f"{Fore.RED}[!] Error: File '{args.list}' not found!{Style.RESET_ALL}")
        return

    with open(args.list, "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    if not domains:
        print(f"{Fore.RED}[!] Error: No domains found in '{args.list}'!{Style.RESET_ALL}")
        return

    # Create output directory
    output_dir = f"reports_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(output_dir, exist_ok=True)

    # Process domains
    for domain in domains:
        result = check_headers(domain)
        
        write_report(result, output_dir)

    print(f"\n{Fore.GREEN}[+] Scan completed! Reports saved in: {output_dir}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()

