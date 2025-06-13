from flask import Flask, request, jsonify

from scrapMainCompararMayoristas import (buscar_en_carrefour_argentina, buscar_en_maxiconsumo)

# Importar la nueva función para consultar a la IA
from ia_product_agent import get_product_info_from_ia

import pandas as pd
import datetime

app = Flask(__name__) # Inicializa app ANTES de usarla en CORS

# CORS ha sido eliminado.

# Función auxiliar para parsear strings de precios a números enteros
def robust_parse_price(price_text: str):
    if not isinstance(price_text, str):
        return None # Cuerpo para el if, soluciona IndentationError
    
    # Placeholder para la lógica completa de robust_parse_price
    # Deberías restaurar aquí tu lógica de parseo de precios completa.
    # Ejemplo mínimo:
    text = price_text.upper().replace("ARS", "").replace("$", "").strip().replace(".", "").replace(",", ".")
    try:
        price_float = float(text)
        return int(price_float)
    except ValueError:
        print(f"⚠️ Error al convertir el precio: '{price_text}' (procesado a: '{text}')")
        return None

@app.route("/comparar", methods=["GET"])
def comparar():
    producto = request.args.get("producto")
    if not producto:
        return jsonify({"error": "Falta el parámetro 'producto'"}), 400

    # 1. Obtener información del producto desde el agente de IA
    all_found_items = []
    try:
        # Llamar a la función que consulta a la IA
        # Esta función ya debería devolver una lista de diccionarios con el formato esperado
        # (nombre, precio_str, tienda, ean, url)
        all_found_items = get_product_info_from_ia(producto)
        print(f"ℹ️ Productos obtenidos de la IA para '{producto}': {len(all_found_items)}")
    except Exception as e:
        print(f"❌ Error al consultar al agente de IA para '{producto}': {e}")
        all_found_items = [] # Asegurar que sea una lista vacía en caso de error

    # 2. Preparar información y generar CSV (opcional, basado en los datos de la IA)
    csv_filename = None
    csv_message = "No se generó archivo CSV porque no se encontraron productos."
    if all_found_items:
        timestamp_str_csv = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_producto_name = "".join(c if c.isalnum() else "_" for c in producto) # Sanitizar nombre para archivo
        csv_filename = f"resultados_ia_{safe_producto_name}_{timestamp_str_csv}.csv"
        try:
            # Los items de la IA ya deberían tener 'nombre', 'precio', 'tienda', 'ean', 'url'
            # Si la IA devuelve el precio como string, la función robust_parse_price lo manejará
            df = pd.DataFrame(all_found_items)
            df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
            csv_message = f"Archivo CSV '{csv_filename}' generado correctamente con {len(all_found_items)} productos (datos de IA)."
            print(f"ℹ️ {csv_message}")
        except Exception as e:
            csv_message = f"Error al generar archivo CSV '{csv_filename}' con datos de IA: {e}"
            print(f"⚠️ {csv_message}")
            csv_filename = None # Resetear si falla el guardado

    # 3. Transformar resultados para la lista de precios comparados
    precios_list = []
    for item in all_found_items: # Usar all_found_items (que vienen de la IA)
        if isinstance(item, dict) and "tienda" in item and "precio" in item:
            price_value = robust_parse_price(item.get("precio")) # 'precio' es el string de la IA
            if price_value is not None:
                precios_list.append({
                    "supermercado": item.get("tienda"),
                    "precio": price_value,
                    "ean": item.get("ean"), # Obtener ean del item de la IA
                    "nombre_producto_ia": item.get("nombre"), # Nombre según la IA
                    "url_producto_ia": item.get("url") # URL según la IA
                })
        else:
            print(f"⚠️ Item de IA ignorado por formato incorrecto: {item}")
            
    # 4. Preparar la respuesta JSON unificada
    current_timestamp_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_data = {
        "producto_buscado": producto,
        "fecha_consulta": current_timestamp_str,
        "fuente_datos": "Agente de Inteligencia Artificial (Simulado)",
        "total_items_encontrados_ia": len(all_found_items),
        "comparativa_precios": precios_list,
        "reporte_csv": {
            "mensaje": csv_message,
            "nombre_archivo": csv_filename
        }
    }

    #return jsonify(response_data)
    return jsonify(response_data)
 
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
