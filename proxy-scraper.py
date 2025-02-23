import requests
from bs4 import BeautifulSoup
import re

def get_proxies_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Extracting potential proxies
        proxy_pattern = re.compile(r'\b(\d{1,3}(?:\.\d{1,3}){3}):(\d{2,5})\b')
        matches = proxy_pattern.findall(response.text)
        # Returning formatted proxies
        return [":".join(match) for match in matches]
    except requests.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")
        return []

def load_existing_proxies(filename):
    try:
        with open(filename, 'r') as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        return set()

def save_proxies(proxies, filename):
    existing_proxies = load_existing_proxies(filename)
    new_proxies = set(proxies) - existing_proxies
    
    if new_proxies:
        with open(filename, 'a') as file:
            for proxy in new_proxies:
                file.write(proxy + '\n')
        print(f"Added {len(new_proxies)} new proxies.")
    else:
        print("No new proxies found.")

def main():
    url_file = "urls.txt"
    proxy_file = "proxies.txt"
    
    try:
        with open(url_file, 'r') as file:
            urls = file.read().splitlines()
    except FileNotFoundError:
        print(f"File {url_file} not found!")
        return
    
    all_proxies = []
    for url in urls:
        print(f"Scraping {url}...")
        all_proxies.extend(get_proxies_from_url(url))
    
    if all_proxies:
        save_proxies(all_proxies, proxy_file)
    else:
        print("No proxies found from provided URLs.")

if __name__ == "__main__":
    main()
