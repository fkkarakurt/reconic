"""
Reconic: Comprehensive Network Reconnaissance Tool

Description:
Reconic is a powerful and versatile network reconnaissance tool designed to automate 
the process of gathering information about a given target. It integrates various scanning 
functionalities including WHOIS lookups, DNS resolution, SSL/TLS certificate inspections, 
HTTP header analysis, port scanning, subdomain discovery, directory traversal, and 
JavaScript file enumeration. The tool aims to provide a holistic overview of 
the target's security posture, facilitating early detection of potential vulnerabilities 
and misconfigurations.

Features:
- WHOIS Lookup: Retrieves domain registration details to identify the domain owner.
- DNS Scan: Resolves DNS records to uncover associated domains and subdomains.
- SSL/TLS Certificate Inspection: Examines SSL/TLS certificates for validity and configuration.
- HTTP Header Analysis: Captures and analyzes HTTP headers for security headers and configurations.
- Port Scanning: Scans for open ports to discover exposed services and potential entry points.
- Subdomain Discovery: Enumerates subdomains to map the target's online presence.
- Directory Traversal: Searches for accessible directories that may contain sensitive information.
- JavaScript File Enumeration: Identifies JavaScript files for further analysis of client-side code.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Repository: https://github.com/reconic
"""



import argparse
import pyfiglet

from src.whois_lookup import WhoisScanner
from src.subdomain_scan import SubdomainScanner
from src.http_headers import HTTPHeadersScanner
from src.port_scanner import PortScan
from src.directory_scan import DirectoryScanner
from src.dns_scan import DNSRecon
from src.js_scan import JSScanner
from src.ssl_scan import SSLCertScanner
from src.report_generator import ReportGenerator

from rich.console import Console

console = Console(record=True)

report_data = {}

### ASCII ART
@staticmethod
def show_ascii():
    ascii_art = pyfiglet.figlet_format("RECONIC", font="ogre")
    console.print(f"[blue]{ascii_art}[/blue]")
    console.print("#" * 41  , style = "blue")
    console.print(
        "#" * 14, "@fkkarakurt", "#" * 14, style = "white"
    )
    console.print("#" * 41, style = "blue")
    print()

### PARSER
def parse_arguments():    
    parser = argparse.ArgumentParser(
        description="Reconic Help Menu",
        epilog="Example usage: python3 reconic.py -u example.com --https"
    )
    parser.add_argument("-u", "--url", help="Target URL", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--https", action="store_true", help="Use HTTPS for web technology detection")
    group.add_argument("--http", action="store_true", help="Use HTTP for web technology detection")
    args = parser.parse_args()
    return args

### WHOIS
def whois(full_url):
    whois_scanner = WhoisScanner(full_url)
    whois_data = whois_scanner.perform_whois_lookup()
    whois_scanner.display_results(whois_data)
    report_data["Whois"] = whois_data

### DNS RESOLVER
def dns_scanner(domain):
    dns_recon = DNSRecon(domain)
    dns_recon.print_results()
    dns_data = dns_recon.perform_dns_recon()
    report_data["DNS"] = dns_data

### SSL/TLS CERTIFICATES
def display_ssl_certificate_info(domain):
    ssl_scanner = SSLCertScanner(domain)
    ssl_info = ssl_scanner.get_ssl_certificate_info()
    ssl_scanner.display_results(ssl_info) 
    report_data["SSL"] = ssl_info
    
### HTTP HEADERS
def http_header(full_url):
    headers_scanner = HTTPHeadersScanner(full_url)
    headers = headers_scanner.get_http_headers()
    headers_scanner.display_results(headers)
    report_data["HTTP Headers"] = headers

### PORT SCANNING
def port_scanning(domain):
    port_scanner = PortScan(domain)
    port_scanner.run()
    port_scan_results = port_scanner.get_scan_results()
    report_data["Port Scanner"] = port_scan_results

### SUBDOMAIN SCANNING
def subdomain_scanning(domain):
    scanner = SubdomainScanner()
    subdomains = scanner.get_subdomains(domain)
    checked_subdomains = [subdomain for subdomain in subdomains if scanner.check_subdomain(subdomain['subdomain'])]
    scanner.display_results(checked_subdomains)
    report_data["Subdomain"] = checked_subdomains

### DIRECTORY SCANNING    
def directory_scanning(base_url, wordlist_file):
    directory_scanner = DirectoryScanner(base_url, wordlist_file)
    found_directories = directory_scanner.scan_directories()
    directory_scanner.display_results(found_directories)
    report_data["Directories"] = found_directories

### JS FILE SCANNING
def js_file_scanning(url):
    js_scanner = JSScanner(url)
    js_files = js_scanner.find_javascript_files()
    js_scanner.display_results(js_files)
    report_data["JavaScriptFiles"] = js_files


def main():
    args = parse_arguments()
    domain = args.url

    protocol = "https://" if args.https else "http://"
    full_url = f"{protocol}{domain}"

    show_ascii()
    console.print("\n")
    
    console.print(f"Starting recon for the target: ", end="")
    console.print(f"{domain}", style='red', end="\n")
    console.print("\n")
    
    print("\n")
    console.print(f"Whois Lookup is being done...", end="\n\n")
    whois(full_url)    

    print("\n")
    console.print(f"DNS Scanning is in progress...", end="\n\n")
    dns_scanner(domain)

    print("\n")
    console.print(f"SSL/TLS scanning is in progress...", end="\n\n")
    display_ssl_certificate_info(domain)

    print("\n")
    console.print(f"Retrieving HTTP Headers...", end="\n\n")
    http_header(full_url)

    print("\n")
    console.print(f"Port scanning is in progress...", end="\n\n")
    port_scanning(domain)

    print("\n")
    console.print(f"Subdomain scanning is in progress...", end="\n\n")
    subdomain_scanning(domain)

    print("\n")
    console.print(f"Directory scanning in progress...", end="\n\n")
    directory_scanning(full_url, "wordlists/directories.txt")

    print("\n")
    console.print(f"JavaScript files scanning in progress...", end="\n\n")
    js_file_scanning(full_url)

    report_generator = ReportGenerator(report_data)
    report_generator.generate_html_report(f"{domain}.html")

if __name__ == "__main__":
    main()
    