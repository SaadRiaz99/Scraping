import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_jang_en():
    url = "https://jang.com.pk/en"
    print(f"Scraping Jang English from {url}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch Jang English: {response.status_code}")
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Typically articles are in 'li' or 'div' with specific classes
        # On Jang English, they use 'h2' and 'h3' for titles
        articles = []
        
        # Look for the main article containers
        # Common structure: class="news-list" or similar
        for card in soup.find_all('div', class_='news-card') or soup.find_all('div', class_='list-item'):
            title_tag = card.find('h2') or card.find('h3') or card.find('a')
            if not title_tag: continue
            
            title = title_tag.get_text().strip()
            link = ""
            if title_tag.name == 'a':
                link = title_tag['href']
            elif title_tag.find('a'):
                link = title_tag.find('a')['href']
            
            desc_tag = card.find('p')
            description = desc_tag.get_text().strip() if desc_tag else "No description available."
            
            # If date is not found on homepage, use today's date
            # Jang homepage articles are generally current (last 24-48h)
            date_str = datetime.now().strftime("%Y-%m-%d")
            
            if title and title not in [a['Title'] for a in articles]:
                articles.append({
                    'Title': title,
                    'Date': date_str,
                    'Description': description[:500],
                    'Source': 'Jang English'
                })
        
        # Fallback: Scrape all h2 tags if containers weren't found
        if not articles:
            for h2 in soup.find_all('h2'):
                title = h2.get_text().strip()
                if title and len(title) > 10:
                    articles.append({
                        'Title': title,
                        'Date': datetime.now().strftime("%Y-%m-%d"),
                        'Description': "Latest update from Jang English",
                        'Source': 'Jang English'
                    })

        # Save to CSV
        filename = "jang_news_last20days.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Title', 'Date', 'Description', 'Source'])
            writer.writeheader()
            writer.writerows(articles)
            
        print(f"Successfully saved {len(articles)} articles to {filename}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_jang_en()
