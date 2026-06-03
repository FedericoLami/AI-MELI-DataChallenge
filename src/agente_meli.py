import anthropic
from dotenv import load_dotenv
from src.herramientas_meli import productos_en_riesgo, top_criticos, analizar_sku, resumen_catalogo

load_dotenv()
client = anthropic.Anthropic()

tools = [
    {
        "name" : "productos_en_riesgo",
        "description" : "Calcula y ordena SKUs por riesgo acumulado hasta n_dias",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "n_dias" : {
                    "type" : "integer",
                    "description" : "Número de días para calcular el riesgo acumulado. Ejemplo: 7, 15, 30"
                }
            },
            "required" : ["n_dias"]
        }
    },
    {
        "name" : "top_criticos",
        "description" : "Devuelve los SKUs más críticos según riesgo en 7 días",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "top_n" : {
                    "type" : "integer",
                    "description" : "Cantidad de SKUs críticos a devolver. Ejemplo: 5, 10, 20"
                }
            },
            "required" : ["top_n"]
        }
    },
    {
        "name" : "analizar_sku",
        "description" : "Muestra la información completa de un SKU específico",
        "input_schema" : {
            "type" : "object",
            "properties" : {
                "sku" : {
                    "type" : "integer",
                    "description" : "ID numérico del SKU a analizar. Ejemplo: 464801"
                }
            },
            "required" : ["sku"]
        }
    },
    {
        "name" : "resumen_catalogo",
        "description" : "Resume cuántos SKUs están en riesgo a 7, 15 y 30 días",
        "input_schema" : {
            "type" : "object",
            "properties" : {
            },
            "required" : []
        }
    }   
]

def ejecutar_agente(pregunta):
    mensajes = [{"role": "user", "content": pregunta}]
    fin = False
    herramientas_map = {
        "productos_en_riesgo": productos_en_riesgo,
        "analizar_sku": analizar_sku,
        "top_criticos": top_criticos,
        "resumen_catalogo": resumen_catalogo
    }
    while not fin:
        answer = client.messages.create(
                    model = "claude-haiku-4-5",
                    max_tokens = 1024,
                    system = """
                            Sos un agente de análisis de inventario de MercadoLibre. Tenés acceso a herramientas para analizar predicciones de agotamiento
                            de stock de 551,472 productos.
                            Usá las herramientas disponibles para responder preguntas sobre riesgo de quiebre de stock, productos críticos y distribución de inventario.
                            El dataset contiene predicciones de agotamiento de stock para 551,472 SKUs de MercadoLibre. 
                            Cada SKU tiene 30 probabilidades — una por día — que indican la chance de agotarse ese día específico.
                            IMPORTANTE: Nunca hagas preguntas de seguimiento al final de tus respuestas. Nunca sugieras análisis adicionales. 
                            Respondé únicamente lo que se te preguntó y terminá ahí.
                            """,
                    messages = mensajes,
                    tools = tools
                )
        
        if answer.stop_reason == "end_turn":
            fin = True
            return answer.content[0].text
        elif answer.stop_reason == "tool_use":
            mensajes.append({"role" : "assistant","content" : answer.content})
            
            for bloque in answer.content:
                if bloque.type == "tool_use":
                    nombre = bloque.name    
                    argumentos = bloque.input
                    id_herramienta = bloque.id
                    resultado = herramientas_map[nombre](**argumentos)
                    mensajes.append({
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": id_herramienta,
                            "content": resultado
                        }]
                    })