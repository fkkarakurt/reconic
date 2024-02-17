import requests

def get_http_headers(url):
    try:
        response = requests.get(url)
        headers = response.headers
        return headers
    except requests.exceptions.RequestException as e:
        print(f"HTTP başlıkları alınırken hata oluştu: {e}")
        return {}