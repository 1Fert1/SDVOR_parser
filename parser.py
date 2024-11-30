from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
from database import SessionLocal, Product

# Настройка Selenium для headless режима
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

URL = "https://www.sdvor.com/moscow/category/krovlja-i-fasad-9050"


def get_products():
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(URL)

    # Скроллинг страницы
    page_height = driver.execute_script("return document.body.scrollHeight")
    scroll_pause_time = 2

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

        new_page_height = driver.execute_script("return document.body.scrollHeight")
        if new_page_height == page_height:
            break
        page_height = new_page_height

    # Парсинг контента страницы с BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    products = soup.find_all("div", class_="product")
    db = SessionLocal()

    for product in products:
        name_elem = product.find("a", class_="product-name")
        price_elem = product.find("span", class_="main")

        name = name_elem.text.strip() if name_elem else "Нет названия"
        price = price_elem.text.strip() if price_elem else "Нет цены"

        # Проверка на дубликаты перед добавлением
        existing_product = db.query(Product).filter_by(name=name).first()
        if not existing_product:
            db_product = Product(name=name, price=price)
            db.add(db_product)

    db.commit()
    db.close()
