import argparse
import pyfiglet
import time

from src.whois_lookup import whois_lookup
from src.subdomain_scan import perform_subdomain_scan
from src.http_headers import get_http_headers
from src.textwrap import wrap_text
from src.port_scanner import PortScan
from src.directory_scan import scan_directories
from src.dns_scan import DNSRecon
from src.js_scan import find_javascript_files

from rich.console import Console
from rich.table import Table
from rich.text import Text


console = Console()

@staticmethod
def show_ascii():
    ascii_art = pyfiglet.figlet_format("RECONIC", font="ogre")
    console.print(f"[blue]{ascii_art}[/blue]")
    console.print("#" * 41  , style = "blue")
    console.print(
        "#" * 14, "[link=https://github.com/fkkarakurt]@fkkarakurt[/link]", "#" * 14, style = "white"
    )
    console.print("#" * 41, style = "blue")
    print()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Reconic Help Menu")
    parser.add_argument("-u", "--url", help="Target URL", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--https", action="store_true", help="Use HTTPS for web technology detection")
    group.add_argument("--http", action="store_true", help="Use HTTP for web technology detection")
    args = parser.parse_args()
    return args


### WHOIS
def whois(full_url):
    whois_table = Table(show_header=True, header_style="bold green", title="[bold]WHOIS Results[/bold]")
    whois_table.add_column("Info", style="blue")
    whois_table.add_column("Value", style="magenta")
    
    whois_data = whois_lookup(full_url) 
    for key, value in whois_data.items():
        whois_table.add_row(key, wrap_text(value, 40))
    console.print(whois_table)

### DNS RESOLVER
def dns_scanner(domain):
    dns_recon = DNSRecon(domain)
    dns_recon.print_results()

### HTTP HEADERS
def http_header(full_url):
    headers = get_http_headers(full_url)
    headers_table = Table(show_header=True, header_style="bold green", title="[bold]HTTP Headers Results[/bold]")
    headers_table.add_column("Header", style="blue")
    headers_table.add_column("Value", style="magenta")
    for key, value in headers.items():
        headers_table.add_row(key, wrap_text(value, 40))
    console.print(headers_table)


### PORT SCANNING
def port_scanning(domain):
    port_scanner = PortScan(domain)
    port_scanner.run()


### SUBDOMAIN SCANNING
def subdomain_scanning(domain):
    subdomains = perform_subdomain_scan(domain)
    subdomains_table = Table(show_header=True, header_style="bold green", title="[bold]Subdomain Scanner Results[/bold]")
    subdomains_table.add_column("Subdomain", style="blue")
    subdomains_table.add_column("IP", style="magenta")
    for subdomain, ips in subdomains.items():
        subdomains_table.add_row(wrap_text(subdomain, 40), ".".join(ips))
    console.print(subdomains_table)

### DIRECTORY SCANNING
def directory_scanning(full_url):
    wordlist_file = "wordlists/directories.txt"
    max_threads = 50 # iş parçacığı sayısını ayarlayabilirsiniz.
    found_directories = scan_directories(full_url, wordlist_file, max_threads)

    directories_table = Table(show_header=True, header_style="bold green", title="[bold]Directory Scanner Results[/bold]")
    directories_table.add_column("Directory", style="blue")
    directories_table.add_column("Status", style="magenta", justify="center")
    for directory in found_directories:
        directories_table.add_row(directory, "200")
    console.print(directories_table)
    
### JS FILE SCANNING
def find_js_files(full_url):
    js_files = find_javascript_files(full_url)
    find_js_files_table = Table(show_header=True, header_style="bold green", title="[bold]JavaScript Files Scanner Results[/bold]")
    find_js_files_table.add_column("JavaScript Files", style="blue", no_wrap=False)
    find_js_files_table.add_column("Status", style="magenta", justify="center")

    for js_file, status_code in js_files:
        js_file_text = Text(js_file, no_wrap=True, overflow="fold")
        find_js_files_table.add_row(wrap_text(js_file_text), str(status_code))
    
    console.print(find_js_files_table)


def main():
    args = parse_arguments()
    domain = args.url

    protocol = "https://" if args.https else "http://"
    full_url = f"{protocol}{domain}"

    show_ascii()
    print("\n")

    console.print(f"Starting recon for the target: ", end="")
    console.print(f"{domain}", style='red', end="\n")
    console.print("\n")
    time.sleep(1)
    
    print("\n")
    console.print(f"Whois Lookup is being done...", end="\n\n")
    whois(domain)
    time.sleep(1)

    print("\n")
    console.print(f"DNS Scanning is in progress...", end="\n\n")
    dns_scanner(domain)
    time.sleep(1)

    print("\n")
    console.print(f"Retrieving HTTP Headers...", end="\n\n")
    http_header(full_url)
    time.sleep(1)

    print("\n")
    console.print(f"Port scanning is in progress...", end="\n\n")
    port_scanning(domain)
    time.sleep(1)

    print("\n")
    console.print(f"Subdomain scanning is in progress...", end="\n\n")
    subdomain_scanning(domain)
    time.sleep(1)

    print("\n")
    console.print(f"Directory scanning in progress...", end="\n\n")
    directory_scanning(full_url)
    time.sleep(1)

    print("\n")
    console.print(f"JavaScript files scanning in progress...", end="\n\n")
    find_js_files(full_url)
    time.sleep(1)

if __name__ == "__main__":
    main()
    