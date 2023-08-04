import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def extract_links_with_href(driver, url):
    driver.get(url)
    # Wait for the initial content to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'grid--uniform')))

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    div_collection = soup.find('div', class_='grid--uniform')

    # Extract all the <a> tags with href attributes
    links_with_href = div_collection.find_all('a', href=True)
    return links_with_href

chrome_driver_path = r'C:\Users\abhis\OneDrive\Desktop\pythonselenium\chromedriver-win64\chromedriver.exe'
chrome_service = Service(chrome_driver_path)

driver = webdriver.Chrome(service=chrome_service)

# Storing the links in a list with the base URL
url = 'https://www.facescanada.com/collections/lipstick'
links = extract_links_with_href(driver, url)
base_url = 'https://www.facescanada.com'
formatted_links_set = []

# Storing the extracted links in the formatted_links list
for link in links:
    formatted_links_set.append(base_url + link['href'])  # Append the formatted link to the list

# Convert the set to a list
formatted_links = list(formatted_links_set)

# Close the web driver
driver.quit()

# Step 1: Create a dictionary to store the links
data = {"links": formatted_links}

# Remove duplicates from the list and update the data dictionary
unique_links = list(set(formatted_links))
data["links"] = unique_links

# Step 2: Save the links dictionary to a JSON file
try:
    with open("links.json", "w") as json_file:
        json.dump(data, json_file, indent=4, default=str)  # Use 'default=str' to handle non-serializable data
    print(f"Links have been extracted and saved to links.json.")
except Exception as e:
    print(f"An error occurred while saving to JSON: {e}")