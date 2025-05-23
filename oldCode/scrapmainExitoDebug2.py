from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def inspeccionar_clases(producto):
    url = f"https://www.exito.com/s?q={producto.replace(' ', '+')}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)

    time.sleep(7)  # Esperar a que cargue JS

    # Buscar elementos que podrían ser productos
    elementos = driver.find_elements(By.CSS_SELECTOR, "div[class*='product'], div[class*='Product'], li[class*='product'], li[class*='Product']")

    print(f"Número de elementos que podrían ser productos: {len(elementos)}")

    # Imprimir algunas clases y textos de ejemplo
    for i, el in enumerate(elementos[:5]):
        clases = el.get_attribute("class")
        texto = el.text[:100].replace("\n", " ")
        print(f"{i+1}. Clase(s): {clases} | Texto: {texto}")

    driver.quit()

# Ejecutar inspección
inspeccionar_clases("ron")
