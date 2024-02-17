import dns.resolver

def perform_subdomain_scan(domain):
    subdomains = []
    found_subdomains = {}
    
    # subdomains.txt dosyasını oku
    with open("wordlists/subdomains.txt", "r") as file:
        subdomains = [line.strip() for line in file]
    
    for subdomain in subdomains:
        try:
            full_domain = f"{subdomain}.{domain}"
            answers = dns.resolver.resolve(full_domain, 'A')
            found_subdomains[full_domain] = [answer.to_text() for answer in answers]
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            continue
        except Exception as e:
            print(f"Subdomain taraması sırasında hata: {e}")
    return found_subdomains
