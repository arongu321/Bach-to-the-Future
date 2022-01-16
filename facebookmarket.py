import requests
from bs4 import BeautifulSoup
URL = "https://www.facebook.com/marketplace/item/323207356201091/?ref=search&referral_code=marketplace_search&referral_story_type=post"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")
for title in soup.find_all('title'):
    print(title.get_text())