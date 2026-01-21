import time
import pandas as pd
import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

TARGET_PRODUCTS = [
    "https://www.snapdeal.com/product/asian-mexico11-beige-mens-sneakers/5188147402095882363",
    "https://www.snapdeal.com/product/asian-everest24-black-mens-trekking/8070451150763703721", 
    "https://www.snapdeal.com/product/campus-oxyfit-n-blue-running/4899917063895353934",
    "https://www.snapdeal.com/product/asian-desire-lifestyle-white-casual/629748687908",
    "https://www.snapdeal.com/product/asian-white-mesh-textile-sport/662912850947",
    "https://www.snapdeal.com/product/asian-blue-running-shoes/6917529689503073923",
    "https://www.snapdeal.com/product/asian-blue-running-shoes/647066066887",
    "https://www.snapdeal.com/product/asian-blue-sport-shoes-for/646041775158",
    "https://www.snapdeal.com/product/asian-superfit-blue-running-shoes/673170361588",
    "https://www.snapdeal.com/product/asian-cosco-navy-mens-sports/7493990423950623709",
    "https://www.snapdeal.com/product/asian-white-mesh-textile-sport/6917529690553932803"
]

PAGES_PER_PRODUCT = 10  # Scrape deep (10 pages per product = 100 reviews each)
CSV_FILE = "reviews.csv"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def setup_driver():
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    # Speed optimizations
    options.page_load_strategy = 'eager' 
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_page_load_timeout(60)
    return driver

def scrape_manual_list():
    driver = setup_driver()
    
    try:
        logging.info(f"🚀 Starting Scraper for {len(TARGET_PRODUCTS)} Manual Products...")

        for i, link in enumerate(TARGET_PRODUCTS):
            clean_link = link.split('#')[0]
            logging.info(f"\n👟 Product {i+1}/{len(TARGET_PRODUCTS)}")
            
            product_reviews = []
            review_url_base = f"{clean_link}/reviews?page={{}}"
            
            try:
                product_name = clean_link.split('/')[-2].replace('-', ' ').title()
            except:
                product_name = "Unknown Shoe"

            for page in range(1, PAGES_PER_PRODUCT + 1):
                try:
                    driver.get(review_url_base.format(page))
                    time.sleep(1.5) 

                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    review_blocks = soup.find_all('div', class_='user-review')
                    
                    if not review_blocks:
                        break 

                    for block in review_blocks:
                        try:
                            stars = len(block.find_all('i', class_='sd-icon-star-active'))
                            
                            for junk in block.find_all('div', class_='review-helpful'): junk.decompose()
                            raw_text = block.get_text(separator=". ", strip=True)
                            clean_text = raw_text.replace("\n", " ").replace("Verified Buyer", "")
                            
                            if len(clean_text) > 10:
                                product_reviews.append({
                                    "Product Name": product_name,
                                    "Review Text": clean_text,
                                    "Review Rating": stars,
                                    "Review Date": "2025-01-20",
                                    "Reviewer Verified": "Yes"
                                })
                        except:
                            continue
                except Exception as e:
                    logging.warning(f"⚠️ Page {page} skipped.")
                    continue

            # Save immediately after each product
            if product_reviews:
                df = pd.DataFrame(product_reviews)
                file_exists = os.path.exists(CSV_FILE)
                df.to_csv(CSV_FILE, mode='a', header=not file_exists, index=False)
                logging.info(f"   ✅ Saved {len(product_reviews)} reviews.")
            else:
                logging.info("   No reviews found.")

    except Exception as e:
        logging.error(f"Critical Error: {e}")
    finally:
        driver.quit()
        logging.info("🏁 Scraper Finished.")

if __name__ == "__main__":
    scrape_manual_list()