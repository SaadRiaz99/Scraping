import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
import pyodbc
import time
import re

def get_last_21_days_threshold():
    return datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=20)

def connect_db():
    conn_str = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=D:\python\project\fecting 2\webscraping.accdb;'
    return pyodbc.connect(conn_str)

def insert_data(table, data):
    if not data:
        print(f"No records to insert into {table}")
        return
    conn = connect_db()
    cursor = conn.cursor()
    for item in data:
        cursor.execute(f"INSERT INTO [{table}] (Title, [Date], Description, Source) VALUES (?, ?, ?, ?)",
                       (item['title'][:255], item['date'], item['description'], item['source'][:100]))
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Inserted {len(data)} records into {table}")

def fetch_rss(url, table, source_name):
    print(f"Fetching RSS from {url}...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # Some RSS feeds need headers, so we fetch with requests and parse
        response = requests.get(url, headers=headers)
        feed = feedparser.parse(response.content)
        threshold = get_last_21_days_threshold()
        data = []
        for entry in feed.entries:
            date_struct = entry.get('published_parsed') or entry.get('updated_parsed') or entry.get('created_parsed')
            if not date_struct:
                continue
            
            entry_date = datetime.fromtimestamp(time.mktime(date_struct))
            if entry_date >= threshold:
                title = entry.get('title', 'No Title')
                description = entry.get('summary') or entry.get('description') or ""
                soup = BeautifulSoup(description, "html.parser")
                description_text = soup.get_text()[:30000] 

                data.append({
                    'title': title,
                    'date': entry_date,
                    'description': description_text,
                    'source': source_name
                })
        insert_data(table, data)
    except Exception as e:
        print(f"Error fetching {source_name}: {e}")

def fetch_python_org():
    print("Fetching Python.org Blogs...")
    url = "https://www.python.org/blogs/"
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        posts = soup.select(".list-recent-posts li")
        threshold = get_last_21_days_threshold()
        data = []
        for post in posts:
            title_tag = post.find("a")
            date_tag = post.find("time")
            if not title_tag or not date_tag: continue
            
            title = title_tag.text.strip()
            date_text = date_tag.text.strip().replace(".", "")
            
            try:
                post_date = datetime.strptime(date_text, "%b %d, %Y")
            except:
                try:
                    post_date = datetime.strptime(date_text, "%B %d, %Y")
                except:
                    continue

            if post_date >= threshold:
                data.append({
                    'title': title,
                    'date': post_date,
                    'description': f"Python.org Blog post: {title}",
                    'source': "Python.org"
                })
        insert_data("PythonOrg", data)
    except Exception as e:
        print(f"Error fetching Python.org: {e}")

if __name__ == "__main__":
    # 1. Hacker News
    fetch_rss("https://news.ycombinator.com/rss", "HackerNews", "Hacker News")
    
    # 2. Django Project
    fetch_rss("https://www.djangoproject.com/rss/weblog/", "DjangoSite", "Django Project")
    
    # 3. Smashing Magazine
    fetch_rss("https://www.smashingmagazine.com/feed/", "SmashingMag", "Smashing Magazine")
    
    # 4. Slashdot
    fetch_rss("https://rss.slashdot.org/Slashdot/slashdotMain", "Slashdot", "Slashdot")
    
    # 5. Python.org
    fetch_python_org()
    
    print("Data integration complete.")
