"""
Port Scanner

This script is part of the Port Scanner project (https://github.com/fkkarakurt/portscanner) by Fatih Küçükkarakurt. 
It is designed to efficiently scan the specified target's ports to identify which ones are open and what services 
they are associated with. The script leverages Python's socket library for port scanning and the Rich library 
to display the results in a user-friendly table format. It employs a thread pool executor to enhance performance 
by scanning multiple ports concurrently.

The PortScan class encapsulates the scanning logic, offering a streamlined process for initializing the scan, 
executing it, and displaying the results. It includes functionality to resolve the target's IP address, 
perform the scan over a predefined list of ports (sourced from a JSON file), and compile 
a summary of open ports along with their respective services.

Features:
- Target IP address resolution and port scanning.
- Concurrent scanning with customizable thread pool size.
- Results displayed in a table format for easy interpretation.

Important:
This tool is intended for educational purposes and ethical use only. 
Users are responsible for obtaining necessary permissions before scanning networks or systems.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Part of the Port Scanner project: https://github.com/fkkarakurt/portscanner
Created: 2022-10-24
Last Updated: 2024-02-18
"""


import socket
import sys
from rich.console import Console
from rich.table import Table
from utils.utils import extractJsonData, threadPoolExecuter

console = Console()

class PortScan:
    PORTS_DATA_FILE = "utils/ports.json"

    def __init__(self, target):
        self.ports_info = {}
        self.open_ports = []
        self.remote_host = self.get_host_ip_addr(target)
        self.get_ports_info()

    def get_ports_info(self):
        # Getting port information from JSON file
        data = extractJsonData(PortScan.PORTS_DATA_FILE)
        self.ports_info = {int(k): v for (k, v) in data.items()}

    def scan_port(self, port):
        # Port scan
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            # If the port is open, add it to the list
            self.open_ports.append(port)  
        sock.close()

    def get_scan_results(self):
        # Return a list containing both port number and service information for open ports
        return [(port, self.ports_info.get(port, "Unknown")) for port in self.open_ports]

    def show_completion_message(self):
        # Print a message to the console when the scan is complete
        print()
        if self.open_ports:
            console.print("Scan Completed. Open Ports: \n", style="green")
            table = Table(show_header=True, header_style="bold green", title="[bold]Port Scanner Results[/bold]")
            table.add_column("Port", style="blue", justify="center")
            table.add_column("Service", style="magenta")
            # The updated get_scan_results method is used here
            for port, service in self.get_scan_results():  
                table.add_row(str(port), service)
            console.print(table)
        else:
            console.print("No Open Ports Found on Target", style="bold magenta")

    @staticmethod
    def get_host_ip_addr(target):
        try:
            return socket.gethostbyname(target)
        except socket.gaierror as e:
            console.print(f"{e}. Exiting.", style="bold red")
            sys.exit()

    def run(self):
        self.get_ports_info()
        threadPoolExecuter(self.scan_port, self.ports_info.keys(), len(self.ports_info.keys()))
        self.show_completion_message()
