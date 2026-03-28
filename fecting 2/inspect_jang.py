import requests
from bs4 import BeautifulSoup

def inspect_page():
    url = "https://jang.com.pk/en/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    # Let's find common headers
    print("Titles found:")
    for h in soup.find_all(['h2', 'h3', 'h4'])[:10]:
        print(f"[{h.name}] {h.text.strip()[:100]}")
        # Look for links
        link = h.find('a')
        if link:
            print(f"   Link: {link.get('href')}")
            
    # Look for article blocks
    print("\nPotential Article Blocks:")
    # Trying to find common containers
    for div in soup.find_all('div')[:100]:
        cls = div.get('class')
        if cls and any(c in str(cls) for c in ['news', 'article', 'item', 'post']):
            text = div.get_text().strip()
            if len(text) > 50:
                print(f"Class: {cls}, Text snippet: {text[:50]}...")

if __name__ == "__main__":
    inspect_page()
