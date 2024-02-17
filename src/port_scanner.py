import socket
import sys
from rich.console import Console
from rich.table import Table
from utils.utils import extractJsonData, threadPoolExecuter

console = Console()

class PortScan:
    PORTS_DATA_FILE = "utils/fake_port.json"

    def __init__(self, target):
        self.ports_info = {}
        self.open_ports = []
        self.remote_host = self.get_host_ip_addr(target)

    def get_ports_info(self):
        data = extractJsonData(PortScan.PORTS_DATA_FILE)
        self.ports_info = {int(k): v for (k, v) in data.items()}

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        conn_status = sock.connect_ex((self.remote_host, port))
        if conn_status == 0:
            self.open_ports.append(port)
        sock.close()

    def show_completion_message(self):
        print()
        if self.open_ports:
            console.print("Scan Completed. Open Ports: \n", style="green")
            table = Table(show_header=True, header_style="bold green", title="[bold]Port Scanner Results[/bold]")
            table.add_column("Ports", style="blue", justify="center")
            table.add_column("States", style="blue", justify="center")
            table.add_column("Services", style="magenta")
            for port in self.open_ports:
                table.add_row(str(port), "OPEN", self.ports_info.get(port, "Unknown"))
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
