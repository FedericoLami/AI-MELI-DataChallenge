# TRABAJO A DESARROLLAR A FUTURO
# Validación del modelo usando los últimos 14 días del parquet como ground truth
# y calculando el Ranked Probability Score (RPS) para evaluar la calidad de las predicciones.

"""import pandas as pd

rut_parquet = "data/meli_train_data.parquet"
df_parquet = pd.read_parquet(rut_parquet)

df_parquet['date'] = pd.to_datetime(df_parquet['date'])

parquet_entrenamiento = df_parquet[df_parquet['date'] <= '2021-03-15']

parquet_validacion = df_parquet[df_parquet['date'] > '2021-03-15']

print(parquet_entrenamiento.shape)
print(parquet_validacion.shape)

def tasa_ventas():
    ventas_sku = parquet_entrenamiento.groupby('sku')['sold_quantity'].mean() 
    return ventas_sku

def total_ventas():
    ventas_sku = parquet_validacion.groupby('sku')['sold_quantity'].sum()
    return ventas_sku"""