import requests
import csv
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET


url = "https://www.djangoproject.com/rss/weblog/"

response = requests.get(url)
xml_data = response.text

root = ET.fromstring(xml_data)

today = datetime.now()
last_20_days = today - timedelta(days=20)

with open("django_last20days.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Date", "Link"])

    for item in root.findall(".//item"):
        title = item.find("title").text
        link = item.find("link").text
        date_text = item.find("pubDate").text

    
        post_date = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %z").replace(tzinfo=None)

        if post_date >= last_20_days:
            writer.writerow([title, post_date.strftime("%Y-%m-%d"), link])

print(" django_last20days.csv created successfully")
