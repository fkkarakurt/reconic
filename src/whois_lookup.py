import whois

def whois_lookup(domain):
    try:
        w = whois.whois(domain)
        # Sadece ilginç bazı alanları döndürmek için örnek bir filtreleme
        return {
            "domain_name": w.domain_name,
            "registrar": w.registrar,
            "creation_date": w.creation_date,
            "expiration_date": w.expiration_date,
            "name_servers": w.name_servers
        }
    except Exception as e:
        print(f"Whois sorgulaması sırasında hata: {e}")
        return {}