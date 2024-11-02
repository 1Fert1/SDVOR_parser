from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time

URL_SDVOR = "https://www.sdvor.com/moscow/category/krovlja-i-fasad-9050"
PRODUCT_TAG_SDVOR = {"tag": "div", "class_name": "product"}
PRODUCT_NAME_TAG_SDVOR = {"tag": "a", "class_name": "product-name"}
PRODUCT_PRICE_TAG_SDVOR = {"tag": "span", "class_name": "main"}

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=chrome_options)

def get_products(url):
    driver.get(url)
    all_products = []
    page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_pause_time = 2

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_page_height = driver.execute_script("return document.body.scrollHeight")
        if new_page_height == page_height:
            break
        page_height = new_page_height

    soup = BeautifulSoup(driver.page_source, "html.parser")
    products = soup.find_all(PRODUCT_TAG_SDVOR["tag"], class_=PRODUCT_TAG_SDVOR["class_name"])

    for product in products:
        name_elem = product.find(PRODUCT_NAME_TAG_SDVOR['tag'], class_=PRODUCT_NAME_TAG_SDVOR['class_name'])
        price_elem = product.find(PRODUCT_PRICE_TAG_SDVOR['tag'], class_=PRODUCT_PRICE_TAG_SDVOR['class_name'])

        name = name_elem.text.strip() if name_elem else 'Нет названия'
        price = price_elem.text.strip() if price_elem else 'Нет цены'

        all_products.append({"name": name, "price": price})

    return all_products

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    products = get_products(URL_SDVOR)
    filename = "SDVOR_products.json"
    save_to_json(products, filename)
    print(f"Всего собрано товаров: {len(products)}")
    print(f"Данные сохранены в файл {filename}")

driver.quit()
