"""
Whois Lookup Tool

This class, `WhoisScanner`, provides a straightforward way to perform a WHOIS lookup for a given domain name. 
It retrieves and displays key information about the domain, such as the domain name, registrar, 
creation and expiration dates, and name servers. This information is essential for domain registration details verification, 
cybersecurity analysis, and IT research.

Attributes:
- domain (str): The domain name to perform the WHOIS lookup on.

Methods:
- __init__(self, domain): Initializes the `WhoisScanner` instance with the specified domain name.
- perform_whois_lookup(self): Performs the WHOIS lookup and returns a dictionary containing the domain's registration details.
- display_results(self, whois_data): Accepts a dictionary of WHOIS data and displays it in a formatted table in the console.

Example:
```python
# Initialize the scanner with a domain
scanner = WhoisScanner("example.com")

# Perform the WHOIS lookup
whois_data = scanner.perform_whois_lookup()

# Display the lookup results
scanner.display_results(whois_data)

Note:
This tool relies on external services for the WHOIS data, and its availability or accuracy may vary depending on 
the queried domain's registrar and WHOIS server.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-05
Last Updated: 2024-02-18
"""

import whois
from src.textwrap import wrap_text
from rich.console import Console
from rich.table import Table
from rich.text import Text

class WhoisScanner:

    def __init__(self, domain):
        self.domain = domain
        self.console = Console()

    def perform_whois_lookup(self):
        try:
            w = whois.whois(self.domain)
            return {
                "Domain Name": w.domain_name,
                "Registrar": w.registrar,
                "Creation Date": w.creation_date,
                "Expiration Date": w.expiration_date,
                "Name servers": w.name_servers
            }
        except Exception as e:
            self.console.print(f"[red]Error during Whois query: {e}[/red]")
            return {}

    def display_results(self, whois_data):
        table = Table(title="Whois Lookup Results")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="magenta")

        for key, value in whois_data.items():
            wrapped_value = Text.from_markup(wrap_text(str(value), 40))
            table.add_row(key.replace("_", " ").title(), wrapped_value)
        
        self.console.print(table)
