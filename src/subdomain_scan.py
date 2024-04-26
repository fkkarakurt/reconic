"""
Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>

This Python script provides functionality to scan subdomains of a given domain using crt.sh database and check their availability by sending HTTP requests. It utilizes the requests library to fetch data from crt.sh and check the availability of subdomains.

The SubdomainScanner class contains static methods to fetch subdomains, check their availability, and display the results in a tabular format using the rich library for better visualization.

To use this script, simply create an instance of SubdomainScanner and call the get_subdomains method with the desired domain. The display_results method can then be used to print the available subdomains in a formatted table.

Important:
This tool is intended for educational purposes and ethical use only. 
Users are responsible for obtaining necessary permissions before scanning networks or systems.
"""


import requests
from rich.console import Console
from rich.table import Table

class SubdomainScanner:
    def __init__(self):
        pass

    @staticmethod
    def get_subdomains(domain):
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        try:
            response = requests.get(url)
            data = response.json()
            subdomain_set = set()
            subdomains = []
            for entry in data:
                name_value = entry['name_value'].strip()
                if name_value.endswith(f".{domain}") and name_value not in subdomain_set:
                    subdomain_set.add(name_value)
                    subdomains.append({'subdomain': name_value})
            return subdomains
        except Exception as e:
            print(f"Error fetching subdomains: {e}")
            return []

    @staticmethod
    def check_subdomain(subdomain):
        try:
            response = requests.get(f"http://{subdomain}")
            if response.status_code != 404:
                return True
            else:
                return False
        except requests.exceptions.RequestException:
            return False
        

    @staticmethod
    def display_results(found_subdomains):
        console = Console()

        table = Table(show_header=True, header_style="bold green")
        table.add_column("Subdomain", style="blue")

        subdomain_set = set()

        for subdomain in found_subdomains:
            if subdomain['subdomain'] not in subdomain_set and SubdomainScanner.check_subdomain(subdomain['subdomain']):
                table.add_row(
                    subdomain['subdomain']
                )
                subdomain_set.add(subdomain['subdomain'])

        console.print(table)