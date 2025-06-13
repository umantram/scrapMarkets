from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def buscar_productos_exito(producto):
    url = f"https://www.exito.com/s?q={producto.replace(' ', '+')}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    time.sleep(7)

    productos = []

    # Cada producto individual tiene esta clase
    items = driver.find_elements(By.CLASS_NAME, "productCard_productInfo__yn2lK")

    for item in items:
        try:
            nombre = item.text.split("\n")[0]  # Generalmente el nombre está en la primera línea
            precio = item.text
            link_element = item.find_element(By.XPATH, ".//ancestor::a")
            link = link_element.get_attribute("href") if link_element else "Sin link"
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



# Ejemplo de uso
resultados = []

productos = buscar_productos_exito("ron")
if productos:
    print("🛒 Productos encontrados:")
    for i, prod in enumerate(productos[:5], 1):
        print(f"{i}. {prod['nombre']} - {prod['url']}")
        print(f"   {prod['precio']}")
else:
    print("❌ No se encontraron productos.")