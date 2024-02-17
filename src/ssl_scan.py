import ssl
import socket
from datetime import datetime

def get_ssl_certificate_info(hostname, port = 443):
    ssl_info = {}
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            certificate = ssock.getpeercert()

    # Sertifika bilgilerini çıkar
    ssl_info['issuer'] = dict(x[0] for x in certificate['issuer'])
    ssl_info['subject'] = dict(x[0] for x in certificate['subject'])
    ssl_info['valid_from'] = datetime.strptime(certificate['notBefore'], '%b %d %H:%M:%S %Y %Z')
    ssl_info['valid_to'] = datetime.strptime(certificate['notAfter'], '%b %d %H:%M:%S %Y %Z')
    ssl_info['version'] = certificate['version']
    ssl_info['serial_number'] = certificate['serialNumber']

    return ssl_info