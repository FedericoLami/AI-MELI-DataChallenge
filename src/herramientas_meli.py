import pandas as pd

rut_predicciones = "data/predicciones.csv"
df = pd.read_csv(rut_predicciones)


def productos_en_riesgo(n_dias,top_n=100):
    columnas = [f'dia_{i}' for i in range(1, n_dias + 1)]
    resultado = pd.DataFrame({
        'sku': df['sku'],
        'probabilidad_acumulada': df[columnas].sum(axis=1)
    })
    resultado = resultado.sort_values('probabilidad_acumulada',ascending=False).head(top_n)
    return resultado.to_string()

def top_criticos(top_n):
    columnas = [f'dia_{i}' for i in range(1, 7 + 1)]
    resultado = pd.DataFrame({
        'sku': df['sku'],
        'probabilidad_acumulada': df[columnas].sum(axis=1)
    })
    resultado = resultado.sort_values('probabilidad_acumulada',ascending=False).head(top_n)
    return resultado.to_string()

def analizar_sku(sku):
    row_retorno = df[df['sku'] == sku]
    row_retorno = row_retorno.to_string()
    return(row_retorno)

def resumen_catalogo():
    cols_7 = [f'dia_{i}' for i in range(1, 8)]
    en_7_dias = (df[cols_7].sum(axis=1) > 0.5).sum()
    cols_15 = [f'dia_{i}' for i in range(1, 16)]
    en_15_dias = (df[cols_15].sum(axis=1) > 0.5).sum()
    cols_30 = [f'dia_{i}' for i in range(1, 31)]
    en_30_dias = (df[cols_30].sum(axis=1) > 0.5).sum()
    
    return (f"SKUs en riesgo antes de 7 días: {en_7_dias}\nAntes de 15 días: {en_15_dias}\nAntes de 30 días: {en_30_dias}\nTotal SKUs: {len(df)}")