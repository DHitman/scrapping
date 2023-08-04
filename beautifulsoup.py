import json
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time

# Chrome driver path
chrome_driver_path = r'C:\Users\abhis\OneDrive\Desktop\pythonselenium\chromedriver-win64\chromedriver.exe'
chrome_service = Service(chrome_driver_path)

def scrape_data(url):
    driver = webdriver.Chrome(service=chrome_service)
    driver.get(url)

    try:
        driver.implicitly_wait(10)
        shade_items = driver.find_elements(By.CLASS_NAME, 'variant__button-label')
        product_data_list = []

        for shade_item in shade_items:
            driver.implicitly_wait(10)
            product_data = {}
            product_data['Selected_Shade'] = ''
            product_data['Price'] = ''
            product_data['Product_Name'] = ''
            product_data['Image_URL'] = ''
            product_data['Product_URL'] = ''
            product_data['Color'] = ''

            try:
                shade_item.click()
            except ElementNotInteractableException:
                print("Could not click on the shade item (OUT OF STOCK). Skipping to the next one.")
                continue

            time.sleep(2)
            window_location = driver.execute_script("return window.location.href")
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            try:
                price_match = driver.find_element(By.CSS_SELECTOR, '.product__price')
                price = price_match.text.strip()
                product_data['Price'] = price
            except NoSuchElementException:
                product_data['Price'] = "Price not found"

            try:
                name_match = driver.find_element(By.CSS_SELECTOR, '.product-single__title')
                product_name = name_match.text.strip()
                product_data['Product_Name'] = product_name
            except NoSuchElementException:
                product_data['Product_Name'] = "Product name not found"

            try:
                test = driver.find_element(By.CLASS_NAME, 'selected_color')
                selected_shade_text = test.text.strip()
                product_data['Selected_Shade'] = selected_shade_text
            except NoSuchElementException:
                product_data['Selected_Shade'] = "Shade name not found"

            background_color = shade_item.value_of_css_property("background-image")
            product_data['Color'] = background_color

            try:
                check = driver.find_element(By.CLASS_NAME, 'image-wrap')
                test1 = check.find_element(By.TAG_NAME, 'img')
                data = test1.get_attribute('srcset')
                data = data.replace('//', '')
                full_image_url = data.split()[0] if data else "Image URL not available"
                product_data['Image_URL'] = full_image_url
            except NoSuchElementException:
                product_data['Image_URL'] = "Image URL not available"

            product_data['Product_URL'] = window_location
            product_data_list.append(product_data)

    finally:
        driver.quit()

    return product_data_list

with open('links.json', 'r') as f:
    links_data = json.load(f)

# List of URLs to scrape
links = links_data['links']

# List to store all scraped data
all_data = []

# Scrape data for each URL and store in all_data list
for url in links:
    print(f"Scraping data from: {url}")
    data_list = scrape_data(url)
    all_data.extend(data_list)
    print("-" * 50)

# Write all_data to a JSON file
output_file = 'scraped_data.json'
with open(output_file, 'w') as f:
    json.dump(all_data, f, indent=2)

print(f"Scraped data written to {output_file}")
