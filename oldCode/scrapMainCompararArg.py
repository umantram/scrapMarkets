from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

def buscar_en_carrefour_ar(producto):
    busqueda = producto.replace(' ', '+')
    url = f"https://www.carrefour.com.ar/{busqueda}?_q={busqueda}&map=ft"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(7)

    productos = []
    # Según inspección, cada producto está en div con data-testid="product-card"
    items = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")

    for item in items:
        try:
            nombre = item.find_element(By.CSS_SELECTOR, "span[data-testid='product-name']").text
            precio = item.find_element(By.CSS_SELECTOR, "span[data-testid='product-price']").text
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

            productos.append({
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "tienda": "Carrefour Argentina"
            })
        except Exception as e:
            print("⚠️ Error extrayendo producto Carrefour:", e)
            continue

    driver.quit()
    print(f"🔎 Carrefour Argentina: encontrados {len(productos)} productos.")
    return productos

if __name__ == "__main__":
    productos = buscar_en_carrefour_ar("arroz")
    for producto in productos:
        print(producto)

def comparar_precios(producto):
    resultados = []
    resultados += buscar_en_carrefour_ar(producto)
    # resultados += buscar_en_otro_supermercado(producto)
    # Agrega más funciones según sea necesario

    # Procesar y mostrar los resultados
    for resultado in resultados:
        print(f"{resultado['tienda']}: {resultado['nombre']} - {resultado['precio']} - {resultado['url']}")
