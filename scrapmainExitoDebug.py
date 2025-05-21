from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def buscar_productos_exito_debug(producto):
    url = f"https://www.exito.com/s?q={producto.replace(' ', '+')}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    print("Título de la página:", driver.title)
    time.sleep(7)  # Esperamos un poco más para que cargue JS

    html = driver.page_source
    print("Primeros 1000 caracteres del HTML:")
    print(html[:1000])

    productos = []
    items = driver.find_elements(By.CLASS_NAME, "vtex-product-summary-2-x-container")
    print(f"Número de items encontrados: {len(items)}")

    for item in items:
        try:
            nombre = item.find_element(By.CLASS_NAME, "vtex-product-summary-2-x-productName").text
            precio = item.find_element(By.CLASS_NAME, "vtex-product-price-1-x-sellingPriceValue").text
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")
            productos.append({
                "nombre": nombre,
                "precio": precio,
                "url": link
            })
        except Exception as e:
            print("Error extrayendo producto:", e)
            continue

    driver.quit()
    return productos

# Ejecutar debug
productos = buscar_productos_exito_debug("ron")
print(f"Productos encontrados: {len(productos)}")
