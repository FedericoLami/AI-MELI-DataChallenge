# AI MeLi DataChallenge — Agente de Análisis de Inventario

Sistema completo de predicción de agotamiento de stock para el [MeLi Data Challenge 2021](https://www.kaggle.com/datasets/hubot01/meli-data-challenge-2021) de Kaggle. Dado el historial de ventas de 551,472 SKUs de MercadoLibre, el sistema predice la distribución de probabilidades de agotamiento de stock para cada producto en un horizonte de 30 días, usando simulaciones de Monte Carlo.

El sistema incluye un agente de análisis con inteligencia artificial que permite consultar los resultados en lenguaje natural — respondiendo preguntas como "¿qué productos se van a quedar sin stock esta semana?" o "dame los 10 SKUs más críticos" sin necesidad de escribir código.

---

## Demo

![Demo del sistema](demo.gif)

---

## Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Modelo predictivo | Monte Carlo (NumPy) |
| Procesamiento de datos | Pandas |
| Agente de análisis | Claude Haiku (Anthropic API) + Tool Use |
| Backend / API REST | FastAPI + Uvicorn |
| Frontend | HTML · CSS · JavaScript vanilla |
| Formato de datos | Parquet · CSV · JSON Lines |
| Configuración | python-dotenv |
| Entorno | Python 3.11 + venv |

---

## Arquitectura del proyecto

```
AI-MELI-Analytics/
├── src/
│   ├── modelo.py              # Simulación Monte Carlo y generación de predicciones
│   ├── herramientas_meli.py   # Funciones de análisis sobre las predicciones
│   ├── agente_meli.py         # Agente con tool use para consultas en lenguaje natural
│   ├── main_meli.py           # Loop de consola (modo desarrollo)
│   ├── main_api.py            # API REST con FastAPI
│   └── validacion.py          # Trabajo futuro: validación con RPS
├── notebooks/
│   └── exploracion.ipynb      # Análisis exploratorio del dataset
├── data/                      # Dataset (no se sube a GitHub)
│   ├── meli_train_data.parquet
│   ├── meli_test_data.csv
│   ├── items_static_metadata.jl
│   └── predicciones.csv
├── index.html                 # Interfaz web
├── .env                       # Variables de entorno (no se sube a GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ¿Cómo funciona el modelo?

El modelo usa **simulación de Monte Carlo** para generar una distribución de probabilidades de agotamiento para cada SKU:

1. Calcula la tasa de ventas diaria promedio de cada SKU usando el historial del parquet
2. Para cada SKU, simula 1000 veces cuántos días tarda en vender el `target_stock`
3. En cada simulación, genera ventas diarias aleatorias usando una distribución de Poisson
4. Convierte los resultados en probabilidades para cada día del 1 al 30

El resultado es una distribución probabilística — no un número fijo sino 30 probabilidades que responden "¿cuántas chances hay de que este producto se agote exactamente en N días?".

---

## Dataset

El dataset proviene del [MeLi Data Challenge 2021](https://www.kaggle.com/datasets/hubot01/meli-data-challenge-2021) de Kaggle.

| Archivo | Descripción |
|---------|------------|
| `meli_train_data.parquet` | Historial de ventas diarias por SKU (37M filas, Feb-Mar 2021) |
| `meli_test_data.csv` | SKUs a predecir con su target stock (551,472 productos) |
| `items_static_metadata.jl` | Metadata de productos: nombre, dominio, país |

---

## Herramientas del agente

El agente de IA tiene acceso a cuatro herramientas para analizar las predicciones:

| Herramienta | Descripción |
|------------|------------|
| `productos_en_riesgo(n_dias)` | SKUs ordenados por probabilidad acumulada hasta N días |
| `top_criticos(top_n)` | Top N productos con mayor riesgo de agotarse en 7 días |
| `analizar_sku(sku)` | Distribución completa de probabilidades de un SKU específico |
| `resumen_catalogo()` | Métricas globales: cuántos SKUs en riesgo a 7, 15 y 30 días |

---

## Endpoints de la API

### `POST /analizar`

Recibe una pregunta en lenguaje natural y devuelve el análisis del agente.

**Request:**
```json
{
  "mensaje": "¿Cuáles son los 10 productos más críticos?"
}
```

**Response:**
```
"Los 10 productos con mayor riesgo de agotamiento en los próximos 7 días son..."
```

---

## Instalación y uso

### Requisitos previos

- Python 3.11
- API Key de Anthropic ([console.anthropic.com](https://console.anthropic.com))
- Dataset del [MeLi Data Challenge 2021](https://www.kaggle.com/datasets/hubot01/meli-data-challenge-2021)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/FedericoLami/AI-MELI-DataChallenge.git
cd AI-MELI-DataChallenge

# 2. Crear y activar entorno virtual
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env en la raíz del proyecto:
ANTHROPIC_API_KEY=tu-api-key-aquí

# 5. Agregar el dataset en la carpeta data/

# 6. Generar predicciones (tarda aproximadamente 60 minutos)
python src/modelo.py

# 7. Iniciar el servidor
uvicorn src.main_api:app --reload
```

### Interfaz web

Con el servidor corriendo, abrí `index.html` directamente en el navegador.

### Modo consola

```bash
python src/main_meli.py
```

### Documentación interactiva de la API

```
http://127.0.0.1:8000/docs
```

---

## Análisis exploratorio

El notebook `notebooks/exploracion.ipynb` documenta el análisis inicial del dataset:

- El dataset cubre 59 días (febrero y marzo 2021)
- 660,916 SKUs únicos con un promedio de 57 días de historial cada uno
- Más del 50% de los días no registran ventas — distribución de cola larga típica de e-commerce
- El 75% de los registros tienen entre 0 y 1 venta por día
- Stock mediano de 6 unidades por SKU

---

## Trabajo futuro

- Implementar validación del modelo usando los últimos 14 días del historial como ground truth
- Calcular el Ranked Probability Score (RPS) para medir la calidad de las predicciones
- Optimizar el tiempo de generación de predicciones usando operaciones vectorizadas de NumPy
- Segmentar el análisis por país (MLB Brasil, MLM México, MLA Argentina)

---

## Autor

**Federico Lami**
[LinkedIn](https://www.linkedin.com/in/federicolami/) · [GitHub](https://github.com/FedericoLami/AI-MELI-DataChallenge)