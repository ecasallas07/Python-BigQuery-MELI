import requests
from bs4 import BeautifulSoup

def scrape_site(url,selectors):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    promotions = []
    
    promo_boxes = soup.select(selectors['container'])
    
    for box in promo_boxes:
        try:
            promotion = {
                'title':box.select_one(selectors['title']).text.strip(),
                'price':box.select_one(selectors['price']).text.strip(),
                'image_url':box.select_one(selectors['image'])['src'],
                'link':box.select_one(selectors['link'])['href']   
            }
            
            if promotion['title'] and promotion['price']:
                promotions.append(promotion)
                
        except AttributeError:
            continue    
        
        
    return promotions