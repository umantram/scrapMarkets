# /Users/umantram/Documents/Proyectos/scrapMarkets/ia_product_agent.py
import openai
import json
import os

# (Opcional, para desarrollo local con archivo .env, instala con: pip install python-dotenv)
# from dotenv import load_dotenv
# load_dotenv() # Carga variables desde un archivo .env en el directorio del proyecto

# Carga tu API key de OpenAI desde la variable de entorno.
# Asegúrate de haber configurado la variable de entorno OPENAI_API_KEY en tu sistema.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = None
if not OPENAI_API_KEY:
    print("⚠️ ADVERTENCIA: La variable de entorno OPENAI_API_KEY no está configurada.")
    print("Las llamadas reales a la API de OpenAI fallarán. El script podría depender de la simulación si está activa.")
else:
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        print("ℹ️ Cliente de OpenAI inicializado correctamente con la API Key desde la variable de entorno.")
    except Exception as e:
        print(f"❌ Error al inicializar el cliente de OpenAI: {e}")
        client = None # Asegurarse de que el cliente no esté configurado si hay error

# Lista simulada de supermercados a consultar
SUPERMARKETS_TO_QUERY = ["Maxiconsumo", "Carrefour Argentina", "Diarco"]

def get_product_info_from_ia(product_name: str):
    """
    Consulta a un agente de IA (simulado aquí) para obtener información de productos.
    En un caso real, aquí harías la llamada a la API del LLM.
    """
    if not client:
        print("🚫 Cliente de OpenAI no inicializado (falta API Key o hubo error). No se puede realizar la consulta a la IA.")
        # Podrías retornar una lista vacía o activar un modo de simulación muy básico aquí si lo deseas.
        # Por ahora, retornaremos una lista vacía.
        return []

    # Ejemplo de prompt que podrías enviar a un LLM:
    prompt = f"""
    Basado en tu conocimiento general hasta tu última fecha de corte, proporciona información estimada para el producto "{product_name}" como si se encontrara en los siguientes supermercados de Argentina: {', '.join(SUPERMARKETS_TO_QUERY)}.
    No tienes acceso a internet en tiempo real, así que esta será una estimación basada en tus datos de entrenamiento.

    Para cada supermercado donde estimes que podría estar el producto, proporciona:
    - "nombre": Un nombre descriptivo del producto (ej: "Aceite Girasol Natura Botella 1.5 Lts").
    - "precio": Un precio estimado en formato string (ej: "$1200.50" o "ARS 1200").
    - "tienda": El nombre del supermercado (ej: "Maxiconsumo" o "Carrefour Argentina").
    - "ean": Un código EAN de ejemplo o null si no tienes uno plausible (ej: "7790010001234" o null).
    - "url": Una URL de ejemplo o null (ej: "https://ejemplo.com/producto" o null).

    Responde únicamente con un array JSON de objetos. Cada objeto debe tener las claves: "nombre", "precio", "tienda", "ean", "url".
    Si no puedes hacer una estimación plausible para el producto en un supermercado específico, no incluyas una entrada para él.
    Si no puedes hacer ninguna estimación para el producto en ninguno de los supermercados listados, devuelve un array JSON vacío [].
    Asegúrate de que la respuesta sea solo el array JSON y nada más.
    """
    print(f"DEBUG: Prompt enviado a la IA (simulado):\n{prompt}")

    try:
        # Llamada a la API de OpenAI usando el nuevo formato
        response = client.chat.completions.create(
            model="gpt-4", # Cambiado a gpt-4
            messages=[
                {"role": "system", "content": "Eres un asistente experto en encontrar precios de productos."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2, # Para respuestas más deterministas
            # response_format={ "type": "json_object" } # Solo para modelos que lo soporten (ej. gpt-3.5-turbo-1106, gpt-4-1106-preview)
        )
        raw_response_content = response.choices[0].message.content
        print(f"DEBUG: Respuesta cruda de la IA:\n{raw_response_content}")

        # Intenta parsear la respuesta JSON de la IA
        parsed_products = json.loads(raw_response_content)
        
        # Asegúrate de que la respuesta sea una lista
        if not isinstance(parsed_products, list):
            print("⚠️ La respuesta de la IA no fue una lista JSON como se esperaba.")
            return []
        return parsed_products
    except openai.APIError as e:
        print(f"❌ Error de API de OpenAI: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON de la IA: {e}")
        print(f"Respuesta cruda que causó el error: {raw_response_content if 'raw_response_content' in locals() else 'No se obtuvo respuesta'}")
        return []
    except Exception as e:
        print(f"❌ Error inesperado procesando respuesta de la IA: {e}")
        return []

__all__ = ["get_product_info_from_ia"]
