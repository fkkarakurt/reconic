import dns.resolver
import socket
from rich.table import Table
from rich.console import Console

class DNSRecon:
    def __init__(self, domain):
        self.domain = domain
        self.console = Console()

    def query_a_record(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'A')
            return [rdata.address for rdata in answers]
        except Exception as e:
            return [f"Error: {e}"]

    def query_mx_record(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'MX')
            return [str(rdata.exchange) for rdata in answers]
        except Exception as e:
            return [f"Error: {e}"]

    def query_ns_record(self):
        try:
            answers = dns.resolver.resolve(self.domain, 'NS')
            return [str(rdata.target) for rdata in answers]
        except Exception as e:
            return [f"Error: {e}"]

    def reverse_dns(self, ip_address):
        try:
            result = socket.gethostbyaddr(ip_address)
            return result[0]
        except Exception as e:
            return f"Error: {e}"

    def print_results(self):
        table = Table(show_header=True, header_style="bold green", title="[bold]DNS Recon Results[/bold]")

        table.add_column("Type", justify="center", style="blue", no_wrap=True)
        table.add_column("Value", style="magenta")

        # A Kayıtları
        for a_record in self.query_a_record():
            table.add_row("A", a_record)

        # MX Kayıtları
        for mx_record in self.query_mx_record():
            table.add_row("MX", mx_record)

        # NS Kayıtları
        for ns_record in self.query_ns_record():
            table.add_row("NS", ns_record)

        self.console.print(table)
