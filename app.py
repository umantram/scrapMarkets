from flask import Flask, request, jsonify

from scrapMainCompararMayoristas import (buscar_en_carrefour_argentina, buscar_en_maxiconsumo)


import pandas as pd
import datetime
import re # Importar re para la función de parseo de precios

from flask_cors import CORS # Importa CORS

app = Flask(__name__)
# Configura CORS para permitir solicitudes desde tu origen específico de Cloud Workstation
# o usa "*" para permitir desde cualquier origen (menos seguro para producción)
CORS(app, resources={r"/comparar*": {"origins": "https://6000-firebase-studio-1748623854247.cluster-ux5mmlia3zhhask7riihruxydo.cloudworkstations.dev"}})
# Si quieres permitir cualquier origen (más simple para desarrollo, pero considera la seguridad):
# CORS(app)
# La segunda inicialización de app = Flask(__name__) ha sido eliminada.

app = Flask(__name__)
# Función auxiliar para parsear strings de precios a números enteros
def robust_parse_price(price_text: str):
    if not isinstance(price_text, str):
        return None
    
    text = price_text.upper()
    # Eliminar símbolos de moneda comunes y espacios al inicio/final
    text = text.replace("ARS", "").replace("$", "").strip()
    
    # Eliminar espacios que podrían ser separadores de miles, ej: "1 200,00"
    text = text.replace(" ", "")

    # Estandarizar separadores decimales y de miles
    # Formato común en Argentina: "1.200,00" (punto=miles, coma=decimal)
    if ',' in text and '.' in text: # Formato "1.200,00"
        text = text.replace('.', '') # Eliminar separador de miles
        text = text.replace(',', '.') # Convertir coma decimal a punto
    elif ',' in text: # Formato "1200,00" (solo coma decimal)
        text = text.replace(',', '.') # Convertir coma decimal a punto
    elif '.' in text: # Formato "1.200" (entero) o "1200.00" (punto como decimal)
        # Si la parte después del punto no tiene 2 caracteres, asumir que es un separador de miles para un entero
        # ej: "1.200" -> "1200"
        # ej: "12.00" -> "12.00" (será manejado por float())
        if text.count('.') == 1 and len(text.split('.')[-1]) != 2 :
             text = text.replace('.', '') # ej: "1.200" -> "1200"
        # else: el punto es probablemente un separador decimal, ej: "12.00" - se deja como está
            
    try:
        price_float = float(text)
        return int(price_float) # Convertir a entero según el formato de salida deseado
    except ValueError:
        cleaned_digits = re.sub(r'[^\d]', '', text) # Intento de fallback
        if cleaned_digits:
            try:
                return int(cleaned_digits)
            except ValueError:
                pass
        print(f"⚠️ Error al convertir el precio: '{price_text}' (procesado a: '{text}')")
        return None

@app.route("/comparar", methods=["GET"])
def comparar():
    producto = request.args.get("producto")
    if not producto:
        return jsonify({"error": "Falta el parámetro 'producto'"}), 400

    resultados = []
    
    scraped_results = []
    try:
        resultados += buscar_en_carrefour_argentina(producto)
        scraped_results.extend(buscar_en_carrefour_argentina(producto))
    except Exception as e:
        print("⚠️ Error en Carrefour:", e)
        print(f"⚠️ Error en Carrefour buscando '{producto}': {e}")

    try:
        resultados += buscar_en_maxiconsumo(producto)
        scraped_results.extend(buscar_en_maxiconsumo(producto))
    except Exception as e:
        print("⚠️ Error en Maxiconsumo:", e)
        print(f"⚠️ Error en Maxiconsumo buscando '{producto}': {e}")

    #return jsonify(resultados)

    # Guardar como CSV con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"resultados_{producto}_{timestamp}.csv"
    if resultados: # Solo intentar guardar CSV si hay resultados
        df = pd.DataFrame(resultados)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        mensaje_csv = f"Archivo CSV '{filename}' generado correctamente con {len(resultados)} productos."
    else:
        mensaje_csv = "No se generó archivo CSV porque no se encontraron productos."
        filename = None # No hay archivo si no hay resultados

    
    
    # El siguiente código para el nuevo formato JSON es actualmente inalcanzable
    # debido al 'return' anterior.
    # Si el objetivo es el nuevo formato JSON, se necesitarían más reestructuraciones.
    
    # (Opcional) Guardar como CSV con timestamp (como efecto secundario)
    if scraped_results: # Esta variable se llena pero no se usa para el CSV en la ruta de código actual
        timestamp_csv_nuevo = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        safe_producto_name = "".join(c if c.isalnum() else "_" for c in producto) # Sanitizar nombre para archivo
        filename_nuevo_csv = f"resultados_{safe_producto_name}_{timestamp_csv_nuevo}.csv"
        try:
            df = pd.DataFrame(scraped_results)
            df.to_csv(filename_nuevo_csv, index=False, encoding="utf-8-sig")
            print(f"ℹ️ Archivo CSV (nuevo formato) '{filename_nuevo_csv}' generado con {len(scraped_results)} productos.")
        except Exception as e:
            print(f"⚠️ Error al guardar CSV (nuevo formato) '{filename_nuevo_csv}': {e}")

    # Transformar resultados para la nueva estructura JSON
    precios_list = []
    for item in scraped_results:
        if isinstance(item, dict) and "tienda" in item and "precio" in item:
            price_value = robust_parse_price(item.get("precio"))
            if price_value is not None:
                precios_list.append({
                    "supermercado": item.get("tienda"),
                    "precio": price_value
                })
        else:
            print(f"⚠️ Item de scraping ignorado por formato incorrecto: {item}")
            
    fecha_actual_consulta = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    response_data = {
        "nombre": producto, # El término de búsqueda original
        "precios": precios_list,
        "fecha_consulta": fecha_actual_consulta
    }

    fecha_consulta_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({
        "mensaje": mensaje_csv,
        "archivo": filename,
        "fecha_consulta": fecha_consulta_actual
    }, resultados if resultados else [], response_data) # Asegurarse de pasar una lista vacía si no hay resultados

    #return jsonify(response_data)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)