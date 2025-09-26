from scraper import scrape_site
from config import SITES
import json

all_promotions = []
for site in SITES:
    print(f"Scraping {site['name']}...")
    
    promotions = scrape_site(site['url'], site['selectors'])
    all_promotions.extend(promotions)
with open('promotions.json', 'w') as f:
    json.dump(all_promotions, f, indent=4)
    
print(f"Scraping completado. {len(all_promotions)} promociones guardadas en 'promotions.json'.")