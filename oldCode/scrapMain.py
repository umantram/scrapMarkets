import requests
from bs4 import BeautifulSoup
import geocoder

def obtener_ubicacion():
    g = geocoder.ip('me')
    ciudad = g.city
    pais = g.country
    print(f"🌍 Ubicación detectada: {ciudad}, {pais}")
    return pais

def pais_a_dominio(pais):
    dominios = {
        "Argentina": "com.ar",
        "México": "com.mx",
        "Colombia": "com.co",
        "Chile": "cl",
        "Uruguay": "com.uy",
        "Perú": "com.pe",
        "Venezuela": "com.ve",
    }
    return dominios.get(pais, "com")

import geocoder

def obtener_ubicacion_nombre(pais_codigo):

    # Diccionario de códigos ISO a nombres de país
    paises = {
        "AR": "Argentina",
        "MX": "México",
        "CO": "Colombia",
        "CL": "Chile",
        "UY": "Uruguay",
        "PE": "Perú",
        "VE": "Venezuela",
        "US": "Estados Unidos",
        "BR": "Brasil",
        "ES": "España",
    }

    pais_nombre = paises.get(pais_codigo, "Desconocido")

    return pais_nombre

def buscar_producto_mercadolibre(producto, dominio):
    query = producto.replace(" ", "-")
    url = f"https://listado.mercadolibre.{dominio}/{query}"
    print(f"🔎 Buscando en: {url}")

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/113.0.0.0 Safari/537.36"
    }

    try:
        resp = requests.get(url, headers=headers)
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return []

    if resp.status_code != 200:
        print("❌ No se pudo acceder a MercadoLibre.")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    resultados = []

    # Selector actualizado más flexible
    items = soup.select("li.ui-search-layout__item")

    for item in items:
        titulo_el = item.select_one("h2.ui-search-item__title")
        precio_entero = item.select_one("span.price-tag-fraction")
        precio_decimal = item.select_one("span.price-tag-cents")
        link_el = item.select_one("a.ui-search-link")

        if titulo_el and precio_entero and link_el:
            precio = precio_entero.text
            if precio_decimal:
                precio += "," + precio_decimal.text

            resultados.append({
                "titulo": titulo_el.text.strip(),
                "precio": precio.strip(),
                "url": link_el["href"]
            })

    return resultados

import requests
from bs4 import BeautifulSoup

def buscar_en_exito(producto):
    query = producto.replace(" ", "+")
    url = f"https://www.exito.com/s?q={query}"
    print(f"🔎 Buscando en: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/113.0.0.0 Safari/537.36"
    }

    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")

    resultados = []

    for item in soup.select("div.vtex-product-summary-2-x-container"):
        titulo = item.select_one("span.vtex-product-summary-2-x-productBrand")
        nombre = item.select_one("span.vtex-product-summary-2-x-productName")
        precio = item.select_one("span.vtex-product-price-1-x-sellingPriceValue")
        link = item.select_one("a.vtex-product-summary-2-x-clearLink")

        if titulo and nombre and precio and link:
            resultados.append({
                "producto": f"{titulo.text.strip()} {nombre.text.strip()}",
                "precio": precio.text.strip(),
                "url": "https://www.exito.com" + link["href"]
            })

    return resultados

def main():
    pais = obtener_ubicacion()
    pais_nombre = obtener_ubicacion_nombre(pais)
    dominio = pais_a_dominio(pais_nombre)

    producto = input("📦 ¿Qué producto quieres buscar?: ")
    """ resultados = buscar_producto_mercadolibre(producto, dominio)

    if not resultados:
        print("❌ No se encontraron resultados.")
        return

    print("\n🛍️ Resultados:")
    for i, r in enumerate(resultados[:5], 1):
        print(f"{i}. {r['titulo']}")
        print(f"   Precio: ${r['precio']}")
        print(f"   Link: {r['url']}\n")
 """
    # Prueba
    resultados = buscar_en_exito(producto)

    if resultados:
        print("\n🛒 Resultados:")
        for i, r in enumerate(resultados[:5], 1):
            print(f"{i}. {r['producto']}")
            print(f"   Precio: {r['precio']}")
            print(f"   Link: {r['url']}\n")
    else:
        print("❌ No se encontraron productos.")


if __name__ == "__main__":
    main()
