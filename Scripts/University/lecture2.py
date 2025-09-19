import requests
from bs4 import BeautifulSoup
import os

API_URL = "https://poli.instructure.com/api/v1"
TOKEN = "8994~rABkDzmaDzmJNwuF4Y73Zz82fr9QxrEwFW3JcxE7NeXwGaNN4GXBHmBKxuHZ9KRJ"
headers = {"Authorization": f"Bearer {TOKEN}"}

#id course
course_id = 82683

os.makedirs('lectures', exist_ok=True)

courses = requests.get(f"{API_URL}/courses", headers=headers).json()
pages = requests.get(f"{API_URL}/courses/{course_id}/pages",headers=headers).json()
files = requests.get(f"{API_URL}/courses/{course_id}/files",headers=headers).json()
calendar = requests.get(f"{API_URL}/accounts/search",headers=headers).json()

notifications = requests.get(f"{API_URL}/manageable_accounts",headers=headers).json()
print(notifications)

for page in pages:
    url = page['url']
    title = page['title']

    detail = requests.get(f"{API_URL}/courses/{course_id}/pages/{url}",headers=headers).json()

    body_html = detail['body']
    soup = BeautifulSoup(body_html, 'html.parser')

    links = [a["href"] for a in soup.find_all("a", href=True)]


    iframes = [iframe["src"] for iframe in soup.find_all("iframe", src=True)]

    print(f"\nPágina: {title}")

