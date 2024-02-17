import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def find_javascript_files(url):
    js_files = []
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        script_tags = soup.find_all('script')

        for script in script_tags:
            if script.get('src'):
                js_url = urljoin(url, script.get('src'))
                try:
                    js_response = requests.head(js_url)  # Sadece HTTP headers için HEAD isteği
                    js_files.append((js_url, js_response.status_code))
                except requests.RequestException:
                    js_files.append((js_url, 'Error'))  # Erişim hatası varsa
    except requests.RequestException as e:
        print(f"Error: {e}")

    return js_files
