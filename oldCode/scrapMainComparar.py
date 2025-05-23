from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate

import time

def buscar_en_exito(producto):
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
                "url": link,
                "tienda": "Exito"

            })
        except Exception as e:
            print("Error extrayendo producto:", e)
            continue

    driver.quit()
    return productos

def buscar_en_carulla(producto):
    url = f"https://www.carulla.com/s?q={producto.replace(' ', '+')}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(7)  # Esperar a que se cargue el contenido dinámico

    productos = []
    items = driver.find_elements(By.CLASS_NAME, "productCard_productInfo__yn2lK")  # Ajustar según la estructura actual

    for item in items:
        try:
            nombre = item.text.split("\n")[0]
            precio = item.text
            link_element = item.find_element(By.XPATH, ".//ancestor::a")
            link = link_element.get_attribute("href") if link_element else "Sin link"
            productos.append({
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "tienda": "Carulla"
            })
        except:
            continue

    driver.quit()
    return productos

def buscar_en_jumbo(producto):
    url = f"https://www.jumbocolombia.com/search/?text={producto.replace(' ', '+')}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(7)  # Esperar a que se cargue el contenido dinámico

    productos = []
    items = driver.find_elements(By.CLASS_NAME, "productCard_productInfo__yn2lK")  # Ajustar según la estructura actual

    for item in items:
        try:
            nombre = item.text.split("\n")[0]
            precio = item.text
            link_element = item.find_element(By.XPATH, ".//ancestor::a")
            link = link_element.get_attribute("href") if link_element else "Sin link"
            productos.append({
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "tienda": "Jumbo"
            })
        except:
            continue

    driver.quit()
    return productos

def buscar_en_olimpica(producto):
    url = f"https://www.olimpica.com/s?q={producto.replace(' ', '+')}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    time.sleep(7)  # Esperar a que se cargue el contenido dinámico

    productos = []
    items = driver.find_elements(By.CLASS_NAME, "productCard_productInfo__yn2lK")  # Ajustar según la estructura actual

    for item in items:
        try:
            nombre = item.text.split("\n")[0]
            precio = item.text
            link_element = item.find_element(By.XPATH, ".//ancestor::a")
            link = link_element.get_attribute("href") if link_element else "Sin link"
            productos.append({
                "nombre": nombre,
                "precio": precio,
                "url": link,
                "tienda": "Olímpica"
            })
        except:
            continue

    driver.quit()
    return productos

def comparar_precios(producto):
    print(f"\n🔍 Buscando: {producto}\n")
    resultados = []

    #resultados += buscar_en_exito(producto)
    #resultados += buscar_en_carulla(producto)

    exito_resultados = buscar_en_exito(producto)
    print(f"🛒 Exito: {len(exito_resultados)} productos.")
    resultados += exito_resultados

    carulla_resultados = buscar_en_carulla(producto)
    print(f"🛒 Carulla: {len(carulla_resultados)} productos.")
    resultados += carulla_resultados

    #resultados += buscar_en_jumbo(producto)
    #resultados += buscar_en_olimpica(producto)

    if resultados:
        tabla = [[r['tienda'], r['nombre'], r['precio'], r['url']] for r in resultados]
        print(tabulate(tabla, headers=["Tienda", "Producto", "Precio", "Link"], tablefmt="fancy_grid"))
    else:
        print("❌ No se encontraron productos en ninguna tienda.")

if __name__ == "__main__":
    producto = input("🛍️ ¿Qué producto querés comparar? ")
    comparar_precios(producto)    