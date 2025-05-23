from flask import Flask, request, jsonify
#from scraping_carrefour import buscar_en_carrefour
#from scraping_maxiconsumo import buscar_en_maxiconsumo

from scrapMainCompararMayoristas import (buscar_en_carrefour_argentina, buscar_en_maxiconsumo)

import pandas as pd
import datetime

app = Flask(__name__)

@app.route("/comparar", methods=["GET"])
def comparar():
    producto = request.args.get("producto")
    if not producto:
        return jsonify({"error": "Falta el parámetro 'producto'"}), 400

    resultados = []
    try:
        resultados += buscar_en_carrefour_argentina(producto)
    except Exception as e:
        print("⚠️ Error en Carrefour:", e)

    try:
        resultados += buscar_en_maxiconsumo(producto)
    except Exception as e:
        print("⚠️ Error en Maxiconsumo:", e)

    #return jsonify(resultados)

    # Guardar como CSV con timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"resultados_{producto}_{timestamp}.csv"
    df = pd.DataFrame(resultados)
    df.to_csv(filename, index=False, encoding="utf-8-sig")

    return jsonify({
        "mensaje": f"Archivo CSV generado correctamente.",
        "archivo": filename,
        "total_productos": len(resultados)
    },
        resultados
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
