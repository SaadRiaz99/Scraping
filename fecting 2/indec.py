import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta

def scrape_last_20d():
    url = "https://www.python.org/blogs/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    posts = soup.select(".list-recent-posts li")

    today = datetime.now()
    last_20_days = today - timedelta(days=20)

    with open("python_last20days.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "Date"])

        for post in posts:
            title = post.find("a").text.strip()
            date_text = post.find("time").text.strip()

            
            date_text = date_text.replace(".", "")

           
            post_date = datetime.strptime(date_text, "%b %d, %Y")

            if post_date >= last_20_days:
                writer.writerow([title, date_text])

    print(" python_last20days.csv created successfully")

scrape_last_20d()
