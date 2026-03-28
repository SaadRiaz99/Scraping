import requests
import csv
import feedparser
from datetime import datetime, timedelta
import time
from bs4 import BeautifulSoup

def scrape_django_to_csv():
    url = "https://www.djangoproject.com/rss/weblog/"
    print(f"Fetching Django RSS from {url}...")
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    feed = feedparser.parse(response.content)
    
    # Calculate the threshold (start of the day 21 days ago)
    threshold = (datetime.now() - timedelta(days=21)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    data = []
    for entry in feed.entries:
        # Get publication date
        date_struct = entry.get('published_parsed') or entry.get('updated_parsed')
        if not date_struct:
            continue
            
        entry_date = datetime.fromtimestamp(time.mktime(date_struct))
        
        if entry_date >= threshold:
            title = entry.get('title', 'No Title')
            description = entry.get('summary') or entry.get('description') or ""
            # Clean HTML from description
            soup = BeautifulSoup(description, "html.parser")
            description_text = soup.get_text().strip().replace('\n', ' ')
            
            data.append({
                'Title': title,
                'Date': entry_date.strftime('%Y-%m-%d'),
                'Description': description_text[:500], # Keep description concise for CSV
                'Source': 'Django Project'
            })

    # Write to CSV
    filename = "django_last20days.csv"
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Title', 'Date', 'Description', 'Source'])
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Successfully saved {len(data)} records to {filename}")

if __name__ == "__main__":
    scrape_django_to_csv()
