from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from tabulate import tabulate

import pandas as pd

# Función para buscar en Maxiconsumo
def buscar_en_maxiconsumo(producto):
    url = f"https://maxiconsumo.com/sucursal_capital/catalogsearch/result/?q={producto.replace(' ', '+')}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(5)

    productos = []
    items = driver.find_elements(By.CSS_SELECTOR, ".item.product.product-item")

    for item in items:
        try:
            nombre_el = item.find_element(By.CSS_SELECTOR, ".product-item-link")
            nombre = nombre_el.text.strip()
            precio = item.find_element(By.CLASS_NAME, "price").text
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            productos.append({
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "tienda": "Maxiconsumo"
            })
        except Exception as e:
            print("❌ Error extrayendo producto Maxiconsumo:", e)
            continue

    driver.quit()
    return productos

# Función para buscar en Carrefour
def buscar_en_carrefour_argentina(producto):
    url = f"https://www.carrefour.com.ar/{producto.replace(' ', '-')}" + f"?_q={producto.replace(' ', '+')}&map=ft"
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(6)

    productos = []

    try:
       
        cards = driver.find_elements(
            By.CSS_SELECTOR,
            ".valtech-carrefourar-search-result-3-x-galleryItem.valtech-carrefourar-search-result-3-x-galleryItem--normal.pa4"
        )

        for card in cards:
            try:
                nombre = card.find_element(By.CLASS_NAME, "vtex-product-summary-2-x-productBrand").text

                moneda = card.find_element(By.CSS_SELECTOR, ".valtech-carrefourar-product-price-0-x-currencyCode").text
                
                entero = card.find_elements(By.CSS_SELECTOR, ".valtech-carrefourar-product-price-0-x-currencyInteger")
                entero0 = entero[0].text
                                
                entero = card.find_elements(By.CSS_SELECTOR, ".valtech-carrefourar-product-price-0-x-currencyInteger")
                entero1 = entero[1].text

                centavos = card.find_element(By.CSS_SELECTOR, ".valtech-carrefourar-product-price-0-x-currencyFraction").text
                precio = f"{moneda} {entero0} {entero1},{centavos}"

                link = card.find_element(By.TAG_NAME, "a").get_attribute("href")

                productos.append({
                    "nombre": nombre,
                    "precio": precio,
                    "url": link,
                    "tienda": "Carrefour"
                })
            except Exception as e:
                print("⚠️ Error extrayendo producto:", e)
                continue

    except Exception as e:
        print("❌ Error general:", e)

    driver.quit()
    return productos

__all__ = ["buscar_en_carrefour_argentina", "buscar_en_maxiconsumo", "buscar_en_yaguar"]
