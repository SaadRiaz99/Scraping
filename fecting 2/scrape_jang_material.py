import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

def scrape_jang_material():
    url = "https://jang.com.pk/en/news"
    print(f"Scraping Jang English News from {url}...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # Based on inspection, articles are in 'div' with class 'post-item'
        post_items = soup.find_all('div', class_='post-item')
        
        print(f"Found {len(post_items)} potential articles.")
        
        for item in post_items[:15]: # Limit to 15 to be respectful and fast
            title_tag = item.find(class_='post-title') or item.find('h3') or item.find('h2')
            if not title_tag: continue
            
            title = title_tag.get_text().strip()
            link_tag = title_tag.find('a')
            link = link_tag.get('href') if link_tag else None
            
            if not link: continue
            
            # Category and Date often in 'rt-post-meta' or similar
            category = "News"
            cat_tag = item.find(class_='rt-cat-name')
            if cat_tag:
                category = cat_tag.get_text().strip()
            
            # Fetch "Material" (Full Content) from the article link
            print(f"   Fetching material for: {title[:30]}...")
            full_content = "Could not fetch content."
            try:
                # Small delay to avoid hammering the server
                time.sleep(1)
                art_res = requests.get(link, headers=headers, timeout=10)
                art_soup = BeautifulSoup(art_res.text, 'html.parser')
                
                # Content is usually in a div with class 'main-details-area' or similar
                content_div = art_soup.find(class_='main-details-area') or art_soup.find(class_='post-content') or art_soup.find('article')
                if content_div:
                    # Remove unwanted elements from content
                    for social in content_div.find_all(class_=re.compile('social|share|sidebar')):
                        social.decompose()
                    full_content = content_div.get_text(separator=' ').strip()
                
                # Try to get actual date from article page
                date_tag = art_soup.find(class_='rt-meta') or art_soup.find('time')
                date_str = date_tag.get_text().strip() if date_tag else datetime.now().strftime("%Y-%m-%d")
                
            except Exception as e:
                print(f"      Error fetching details: {e}")
                date_str = datetime.now().strftime("%Y-%m-%d")

            articles.append({
                'Title': title,
                'Category': category,
                'Date': date_str,
                'Link': link,
                'Material': full_content[:2000], # Limit content for CSV
                'Source': 'Jang English'
            })
            
        # Save to CSV
        filename = "jang_news_with_material.csv"
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['Title', 'Category', 'Date', 'Link', 'Material', 'Source'])
            writer.writeheader()
            writer.writerows(articles)
            
        print(f"Successfully saved {len(articles)} articles with material to {filename}")

    except Exception as e:
        print(f"Global Error: {e}")

if __name__ == "__main__":
    import re
    scrape_jang_material()
