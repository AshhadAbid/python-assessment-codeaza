import json
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os

import requests
import time
from bs4 import BeautifulSoup
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.amazon.com/',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}
class Product:
    def __init__(self, title=None, reviews=None, price=None, image_url=None, creation_time=None, update_time=None, scrape_date=None, **kwargs):
        self.title = title
        self.total_reviews = reviews
        self.price = price
        self.image_url = image_url
        self.creation_time = creation_time if creation_time else datetime.utcnow().isoformat()
        self.update_time = update_time if update_time else datetime.utcnow().isoformat()
        self.scrape_date = scrape_date if scrape_date else datetime.now().strftime("%Y-%m-%d")
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_dict(self):
        return self.__dict__

def read_queries(file_path="user_queries.json"):
    try:
        with open(file_path, 'r') as f:
            queries = json.load(f)
        return queries
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return []

def scrape_amazon(query, num_pages=2): # Limiting to 2 pages for debugging
    products = []
    base_url = "https://www.amazon.com/s"
    headers = {
         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
         'Accept-Language': 'en-US,en;q=0.5',
         'Referer': 'https://www.amazon.com/',
         'DNT': '1',
         'Connection': 'keep-alive',
         'Upgrade-Insecure-Requests': '1',
         'Sec-Fetch-Dest': 'document',
         'Sec-Fetch-Mode': 'navigate',
         'Sec-Fetch-Site': 'same-origin',
         'Sec-Fetch-User': '?1',
         'Pragma': 'no-cache',
         'Cache-Control': 'no-cache',
    }

    for page in range(1, num_pages + 1):
        params = {'k': query, 'page': page}
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            print(f"Status code for page {page}: {response.status_code}")
            # print(f"Content for page {page}: {response.content[:500]}...") # Uncomment for debugging content
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'lxml')
            product_cards = soup.select('div[data-component-type="s-search-result"]') # Adjust selector if needed

            for card in product_cards:
                try:
                    
                    title_element = card.select_one('h2.a-size-medium.a-spacing-none.a-color-base.a-text-normal span') # Adjust selector
                    title = title_element.text.strip() if title_element else None

                    review_element = card.select_one('span.a-size-base.s-underline-text') # Adjust selector
                    reviews = review_element.text.strip().replace(',', '') if review_element else None

                    price_whole = card.select_one('span.a-price-whole') # Adjust selector
                    price_whole_element = card.select_one('span.a-price-whole')
                    price_fraction_element = card.select_one('span.a-price-fraction')

                    if price_whole:
                       price = f"{price_whole.text}" 
                    else:
                        price = price_fraction_element
                        

                    image_element = card.select_one('img.s-image') # Adjust selector
                    image_url = image_element['src'] if image_element and 'src' in image_element.attrs else None

                    product = Product(title=title, reviews=reviews, price=price, image_url=image_url)
                    products.append(product.to_dict())

                except Exception as e:
                    print(f"Error parsing product card: {e}")

            time.sleep(random.uniform(1, 3))

        except requests.exceptions.RequestException as e:
            print(f"Request error for page {page} of '{query}': {e}")
            break
        except Exception as e:
            print(f"An unexpected error occurred while scraping page {page} of '{query}': {e}")
            break

    return products

def save_to_json(data, filename):
    # Replace '/path/to/your/frontend/public/data' with the actual absolute path
    output_dir = '/workspaces/python-assessment-codeaza/frontend/public/data'
    file_path = os.path.join(output_dir, filename)
    try:
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Data saved to {file_path}")
    except IOError as e:
        print(f"Error saving to {file_path}: {e}")

def main():
    queries = read_queries()
    if queries:
        for query in queries:
            print(f"Scraping products for '{query}'...")
            scraped_data = scrape_amazon(query)
            output_filename = f"{query.replace(' ', '_')}.json"
            save_to_json(scraped_data, output_filename)
            print(f"Finished scraping '{query}'.")

if __name__ == "__main__":
    main()