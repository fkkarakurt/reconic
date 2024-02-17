import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests.packages.urllib3


# Güvenlik uyarılarını bastırmak için
requests.packages.urllib3.disable_warnings()

def scan_directory(base_url, directory):
    url = f"{base_url}/{directory}"
    try:
        response = requests.get(url, timeout=10, verify=False)
        if response.status_code == 200:
            return url
    except requests.RequestException:
        pass
    return None

def scan_directories(base_url, wordlist_file, max_threads=50):
    found_directories = []
    with open(wordlist_file, 'r') as file:
        directories = file.read().splitlines()


    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [executor.submit(scan_directory, base_url, directory) for directory in directories]

        for future in as_completed(futures):
            result = future.result()
            if result:
                found_directories.append(result)
    
    return found_directories